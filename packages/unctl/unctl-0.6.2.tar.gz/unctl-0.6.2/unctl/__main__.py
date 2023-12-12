import json
from argparse import ArgumentParser
import sys
import asyncio

from pydantic import ValidationError

from unctl.lib.checks.loader import ChecksLoader
from unctl.lib.checks.check_report import CheckReport

from unctl.lib.llm.base import LanguageModel
from unctl.lib.llm.assistant import OpenAIAssistant
from unctl.lib.display import Display

from unctl.lib.llm.instructions import GROUP, INSTRUCTIONS
from unctl.lib.llm.session import LLMSessionKeeper
from unctl.lib.models.recommendations import LLMRecommendation

from unctl.scanrkube import JobDefinition, ResourceChecker, KubernetesDataCollector
from unctl.version import check, current
from unctl.list import load_checks, get_categories, get_services
from unctl.interactive.__main__ import InteractiveTable

LLM_ANALYSIS_THRESHOLD = 10


def unctl_process_args():
    parser = ArgumentParser(prog="unctl")

    description = ""
    description = description + str("\n")
    description = description + str("\t  Welcome to unSkript CLI Interface \n")
    parser.description = description

    parser.add_argument(
        "-s",
        "--scan",
        help="Run a k8s scan",
        action="store_true",
    )
    parser.add_argument(
        "-f",
        "--failing-only",
        help="Show only failing checks",
        action="store_true",
    )
    parser.add_argument(
        "-d",
        "--diagnose",
        help="Run fixed diagnosis",
        action="store_true",
    )
    parser.add_argument(
        "-e",
        "--explain",
        help="Explain failures using AI",
        action="store_true",
    )
    parser.add_argument(
        "-r",
        "--remediate",
        help="Create remediation plan",
        action="store_true",
    )
    parser.add_argument(
        "--no-interactive",
        default=False,
        help="Interactive mode is not allowed. Prompts will be skipped",
    )
    parser.add_argument(
        "--sort-by",
        choices=["object", "check"],
        default="object",
        help="Sort results by 'object' (default) or 'check'",
    ),
    parser.add_argument(
        "-c",
        "--checks",
        help="Filter checks by IDs",
        nargs="+",
    )
    parser.add_argument(
        "--categories",
        help="Filter checks by category",
        nargs="+",
        default=None,
    ),
    parser.add_argument(
        "--services",
        help="Filter checks by services",
        nargs="+",
        default=None,
    )
    parser.add_argument(
        "-l",
        "--list-checks",
        help="List available checks",
        action="store_true",
    )
    parser.add_argument(
        "--list-categories",
        help="List available categories",
        action="store_true",
    )
    parser.add_argument(
        "--list-services",
        help="List available services",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=current(),
    )

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    return args


# analyze results
# Find create a dictionary of objects that failed checks


def annotate_failing_objects(results: dict[str, list[CheckReport]]):
    # FIXME: can be improved
    failed_objects_dict: dict[str, list[CheckReport]] = {}
    failure_record_list: list[CheckReport] = []

    for _, reports in results.items():
        for r in reports:
            if r.passed:
                continue

            failure_record_list.append(r)
            if r.object_name not in failed_objects_dict:
                failed_objects_dict[r.object_name] = []
            # else:
            #     failed_objects[r.object_name].append(r)

    return failed_objects_dict, failure_record_list


# Set up and invoke the LLM analysis
async def analyze_result(
    report: CheckReport,
    failed_objects: dict[str, list[CheckReport]],
    llm_helper: LanguageModel,
):
    # start an assisted troubleshooting session
    await report.init_llm(llm_helper)
    await report.get_next_steps()

    # TODO: this should be revised as it is part of initial implementation
    await report.postprocess(failed_objects)

    return report


async def analyze_results(
    results: dict[str, list[CheckReport]],
    llm_helper: LanguageModel,
    failed_objects,
    failure_record_list,
):
    batch_size = 10
    total_tasks = len(failure_record_list)
    for batch_start in range(0, total_tasks, batch_size):
        batch_end = min(batch_start + batch_size, total_tasks)
        tasks = [
            analyze_result(
                report=failed_item, failed_objects=failed_objects, llm_helper=llm_helper
            )
            for failed_item in failure_record_list[batch_start:batch_end]
        ]
        await asyncio.gather(*tasks)


def get_failure_id(r: CheckReport):
    return r.object_name, r.check_metadata.CheckID


# Convert the dict of objects with their failures
# to a dict of failures with a list of objects
def analyze_failure_relationships(failed_objects):
    triage = {}
    for obj, failures in failed_objects.items():
        for f in failures:
            if triage.get(get_failure_id(f)) is None:
                triage[get_failure_id(f)] = [obj]
            else:
                triage[get_failure_id(f)].append(obj)

    # return only the items where multiple failure are related
    return {k: v for k, v in triage.items() if len(v) > 1}


async def analyze_related_objects(
    failing_object_names,
    objs,
    failed_objects: dict[str, list[CheckReport]],
    provider,
    llm_helper: LanguageModel,
):
    related_failures = {}
    count = 0

    session = LLMSessionKeeper(llm=llm_helper)
    await session.init_session()

    for obj in objs:
        for r in failed_objects[obj]:
            check_name = r.check_metadata.CheckTitle
            fail_sig = (
                f"{r.resource_id} failed check for {check_name} because "
                f"({r.status_extended})"
            )
            if fail_sig in related_failures:
                # skipping duplicate failures
                continue

            count += 1
            print(f"\t❌ Failed {check_name}: {r.object_name} ({r.status_extended})")
            related_failures[fail_sig] = True

            # FIXME: manual de-duplication
            if check_name.find("CrashLoopBackOff") >= 0:
                continue

            for cmd in r.cmd_output_messages:
                await session.push_info(message=cmd)

    instructions = f"""{INSTRUCTIONS[provider][GROUP]}
    Here is the pool of objects: {failing_object_names}
    """
    recommendation = await session.request_llm_recommendation(instructions=instructions)

    parsed = None
    try:
        parsed = LLMRecommendation().model_validate_json(recommendation)
    except ValidationError:
        parsed = LLMRecommendation(summary="Failed to parse llm response")

    return count, session, parsed


def unctl():
    # check version and notify if new version released
    check()

    options = unctl_process_args()
    llm_helper: LanguageModel = None
    if options.explain is True:
        try:
            llm_helper = OpenAIAssistant()
        except Exception as e:
            sys.exit("Failed to initialize LLM: " + str(e))

    Display.init(options)

    if options.list_checks:
        checks_metadata = load_checks(
            provider="k8s",
            categories=options.categories,
            services=options.services,
            checks=options.checks,
        )
        Display.display_list_checks_table(checks_metadata)
        sys.exit()

    if options.list_categories:
        categories = get_categories(provider="k8s")
        Display.display_grouped_data("Category", categories)
        sys.exit()

    if options.list_services:
        services = get_services(provider="k8s")
        Display.display_grouped_data("Service", services)
        sys.exit()

    # Load the checks to be run
    loader = ChecksLoader()
    check_modules = loader.load_all(
        provider="k8s",
        categories=options.categories,
        services=options.services,
        checks=options.checks,
    )

    # Create a job definition
    job_definer = JobDefinition(check_modules)
    jobs = job_definer.generate_jobs()
    print("✅ Created jobs")

    # collect inventory
    collector = KubernetesDataCollector()
    print("✅ Collected Kubernetes data")

    # Run the checks
    run_diags = options.diagnose or options.explain
    app = ResourceChecker(collector, jobs)
    results = asyncio.run(app.execute(run_diags=run_diags))

    if options.explain is False:
        # explanations not needed: print and exit
        Display.display_results_table(results, sort_by=options.sort_by)

        if not options.no_interactive:
            choice = input("Do You want enter interactive mode to continue? (Y/n)\n> ")
            if choice != "n":
                InteractiveTable(checker=app, results=results).run()

        return

    # create list of failures on which to call LLM
    failed_objects, failure_record_list = annotate_failing_objects(results)

    if len(failed_objects) > LLM_ANALYSIS_THRESHOLD:
        choice = input(
            f"unctl found {len(failed_objects)} failed items in your system. "
            "It will start sessions at LLM service for each of the item. "
            "Do You still want to use LLM to explain all the failures? (Y/n)\n> "
        )
        if choice == "n":
            Display.display_results_table(results, sort_by=options.sort_by)
            if not options.no_interactive:
                choice = input(
                    "Do You want enter interactive mode to continue? (Y/n)\n> "
                )
                if choice != "n":
                    InteractiveTable(checker=app, results=results).run()

            return

    # for each failure, print out the summary
    # and the recommendations
    print("\n\n🤔 Analyzing results...\n")
    asyncio.run(
        analyze_results(results, llm_helper, failed_objects, failure_record_list)
    )
    failing_object_names = ", ".join(list(failed_objects.keys()))
    Display.display_results_table(results, llm_summary=True, sort_by=options.sort_by)

    if options.remediate is False:
        if not options.no_interactive:
            choice = input("Do You want enter interactive mode to continue? (Y/n)\n> ")
            if choice != "n":
                InteractiveTable(checker=app, results=results, use_llm=True).run()

        return

    # TODO: everything done below should be behind remediation abstraction

    print("\n")
    print("🤔 Trying to find failures with related root cause...\n")

    # Convert the list of objects with failures
    # to a list of failures with objects
    triage = analyze_failure_relationships(failed_objects)
    triage_summary = []
    for failure_id, objs in triage.items():
        name, check_id = failure_id

        print(
            f"\n💡 Failures on {objs} are correlated by check {check_id}. "
            f"Initiating common analysis\n"
        )

        # print(f"✅ Analyzing the following failures together:")
        count, session, llm_recommendation = asyncio.run(
            analyze_related_objects(
                failing_object_names, objs, failed_objects, "k8s", llm_helper
            )
        )

        summary = llm_recommendation.summary
        # if summary is not None:
        #     print(f"\n✅ Diagnosis: {summary}✅")
        # else:
        #     print(f"\n✅ Diagnosis: {diagnosis}✅")

        # print(f"Next steps: {llm_next_steps_record.get('objects')}")

        # FIXME: create proper class type
        triage_record = {
            "summary": summary,
            "objects": objs,
            "check_id": check_id,
            "next_steps": llm_recommendation,
            "session": session,
            "count": count,
        }
        triage_summary.append(triage_record)

    print("\n")
    print("💡 Issues to be triaged in order of suggested priority:\n")

    # done with failure clustering
    # received set of next steps for each cluster
    # ask user to select the cluster and start executing next steps

    triage_summary = sorted(triage_summary, key=lambda k: k.get("count"), reverse=True)

    for i, t in enumerate(triage_summary):
        objs = t.get("objects")
        summary = t.get("summary")
        count = t.get("count")

        print(f"🧠 Issue {i+1}:\n")
        print(
            f"💬 Summary: {count} failures across objects {objs} "
            f"are found to be related. {summary}\n"
        )

    if len(triage_summary) < 1:
        print("No relations found between failed items.")
        return

    selection = "1"
    if len(triage_summary) > 1:
        selection = input(
            f"🔢 Select the issue to analyze (1-{len(triage_summary) })"
            " and press enter to continue\n> "
        )
        if selection == "":
            return

    t = triage_summary[int(selection) - 1]

    recommendation = asyncio.run(
        t.get("session").request_llm_recommendation(
            message="""
            Based on summary and objects list provided by you give me
            the list of objects sorted by priority of investigation.
            To sort the objects by priority of investigation,
            focus on the root cause of the issue and then look at
            the objects that are directly affected by it.
            Provide the answer as a unformatted json object with the following keys:
            p1: Highest priority - Root Cause
            p2: Medium priority - Directly Affected Objects
            p3: Low priority - Indirectly Affected/Dependent Objects
            justification: justification for the priority order"""
        )
    )

    plan = json.loads(recommendation)

    print(f"🔬 Next steps: {plan.get('justification')}")
    print(f"1. Root Cause Objects : {plan.get('p1')}")
    print(f"2. Directly Affected Objects {plan.get('p2')}")
    print(f"3. Indirectly Affected Objects {plan.get('p3')}")

    selection = input(
        "🔢 Select the group (1, 2, or 3) that you want to investigate further "
        "and press enter to continue\n> "
    )
    print("Select object:")
    for i, obj in enumerate(plan.get("p" + selection)):
        print(f"{i+1}. {obj}")

    obj_idx = ""
    while obj_idx == "":
        obj_idx = input("Enter the object number to execute the plan\n> ")
    obj = plan.get("p" + selection)[int(obj_idx) - 1]

    # print(failed_objects[obj])

    print(f"Executing plan {selection} for {obj}")
    for r in failed_objects[obj]:
        if r.object_name != obj:
            continue
        print(f"🧠 Summary: {r.llm_summary}")
        d = "> " + "\n> ".join(r.diagnosis_options)
        print(f"Recommended Diagnostics:\n{d}")
        choice = input("Execute diagnostics? (Y/n)\n> ")

        if choice == "n":
            print("Skipping")
            continue

        print(f"Executing diagnostics for {r.object_name}")
        asyncio.run(r.execute_diagnostics())

        # print(f"Diagnostics output:\n{reco_output}")

        recommendation = asyncio.run(
            r.get_next_steps(
                "What would be your recommendation "
                "for next steps towards fixing this problem?"
            )
        )

        print(recommendation.summary)

        # print(f"Details: {r.llm_analysis_record}")

    return
    # failed_objects is a dictionary of objects that failed checks
    # the keys are the object names, and the values are a list of
    # Check_Report_K8S objects

    # for any given failure, find all associated objects and then
    # try to analyze all the failures together

    # above is simply the failure explanations from LLM. These are basic
    # as a next step, we can start trying to relate the failures
    # strategies
    # 1. collect objects in a single namespace
    # 2. collect items in a single investigation
    # 3. collect items in

    # asyncio.run(o.get_global_recommendations())

    # second pass
    # should skip objects with depends_on set to non-empty
    # print("\n\n---Executing second pass---\n\n")

    # for object_name, results in failed_objects.items():
    #     for r in results:
    #         if len(r.depends_on) > 0:
    #             print(
    #                 f"Skipping {r.resource_id} because it depends on "
    #                 f"downstream failures {r.depends_on}"
    #             )
    #             continue

    #         check_name = r.check_metadata.CheckTitle

    #         print(f"❌ Failed {check_name}: {r.resource_id} " f"({r.status_extended})")
    #         fail_sig = (
    #             f"{r.resource_id} failed check for {check_name} "
    #             f"because ({r.status_extended})"
    #         )

    #         for check_cli in r.check_cli_output:
    #             check_cli_output = r.check_cli_output[check_cli]

    #         # execute the recommended diagnostics for the failed objects
    #         execute_recommendations(r)

    #         for cli in r.diagnostics_cli_output:
    #             output = r.diagnostics_cli_output[cli]
    #             print(f"Diagnostics:\n{cli}")

    #         for cli in r.recommendations_output:
    #             reco_output = r.recommendations_output[cli]
    #             print(f"Diagnostics:\n{cli}")

    #         output = "\n".join(output.splitlines())
    #         check_cli_output = "\n".join(check_cli_output.splitlines())
    #         reco_output = "\n".join(reco_output.splitlines())

    #         d_output = "\n" + cli + "\n" + output + "\n" + reco_output + "\n"
    #         d_check_cli_output = "\n" + check_cli + "\n" + check_cli_output + "\n"

    #         llm_analysis_record = asyncio.run(
    #             llm_helper.get_recommendations(
    #                 fail_sig, check_cli, d_check_cli_output, cli, d_output
    #             )
    #         )

    #         # LLM gives a list of possible downstream failures
    #         # and we run it through the list of known failures
    #         # this means that LLM list of failures is a superset
    #         related_objects = []
    #         for obj in llm_analysis_record.get("objects"):
    #             # FIXME: this needs to be improved,
    #             # and is assuming that names are unique across types
    #             object_name = obj.split("/")[-1]
    #             if object_name == r.resource_id:
    #                 # self referntial failure means this is a leaf node
    #                 continue
    #             if object_name in failed_objects and object_name != r.resource_id:
    #                 related_objects.append(object_name)

    #         # note that depends_on stores the object_id
    #         r.depends_on = related_objects
    #         if len(r.depends_on) > 0:
    #             print(f"Related objects: {json_dumps(related_objects, indent=2)}")

    #         # print(f"Diagnostics\n: {d_output}")


if __name__ == "__main__":
    sys.exit(unctl())
