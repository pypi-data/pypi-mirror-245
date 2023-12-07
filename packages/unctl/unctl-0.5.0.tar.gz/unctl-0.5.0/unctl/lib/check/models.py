import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, InitVar
from typing import Optional

from pydantic import BaseModel
from json import dumps as json_dumps
from re import findall as find_substrings
from unctl.checks.k8s.service import execute_k8s_cli, execute_k8s_clis
from unctl.lib.llm.openai import LLM
from collections import OrderedDict


class Code(BaseModel):
    """
    Check's remediation information using IaC like CloudFormation, Terraform,
    or the native CLI"""

    NativeIaC: str
    Terraform: str
    CLI: str
    Other: str


class Recommendation(BaseModel):
    """Check's recommendation information"""

    Text: str
    Url: str


class Remediation(BaseModel):
    """Check's remediation: Code and Recommendation"""

    Code: Code
    Recommendation: Recommendation


class Check_Metadata_Model(BaseModel):
    """Check Metadata Model"""

    Enabled: bool = field(default=True)

    # target system - k8s, aws etc
    Provider: str
    CheckID: str

    # Name of the check
    CheckTitle: str
    CheckType: list[str]
    ServiceName: str
    SubServiceName: str
    ResourceIdTemplate: str
    Severity: str
    ResourceType: str
    Description: str
    Risk: str
    RelatedUrl: str
    Remediation: Remediation
    Categories: list[str]
    DependsOn: list[str]
    RelatedTo: list[str]
    Notes: str

    # Cli to be typed to get the same check implemented
    Cli: str

    # Healthy Pattern: presence of this pattern indicates healthy items
    PositiveMatch: str

    # Unhealthy Pattern: presence of this pattern indicates unhealthy items
    NegativeMatch: str

    # For unhealthy items, what further outputs can be collected
    DiagnosticClis: list[str]

    # When did it start failing MM-DD-YYYY-HH-MM-SS
    # LastPassTimestamp: str
    # LastFailTimestamp: str


class ViewCheck:
    def __init__(
        self,
        check_title,
        check_id,
        description,
        service_name,
        provider,
        severity,
        categories,
        module,
    ):
        self.check_title = check_title
        self.check_id = check_id
        self.description = description
        self.service_name = service_name
        self.provider = provider
        self.severity = severity
        self.categories = categories
        self.module = module

    def __str__(self):
        return (
            f"CheckTitle: {self.check_title}, "
            f"Description: {self.description}, "
            f"ServiceName: {self.service_name}, "
            f"SubServiceName: {self.SubServiceName}, "
            f"Provider: {self.provider}, "
            f"Severity: {self.severity}, "
            f"Categories: {self.categories}"
        )


class Check(ABC, Check_Metadata_Model):
    def __init__(self, **data):
        """Check's init function. Calls the CheckMetadataModel init."""
        # Parse the Check's metadata file
        metadata_file = (
            os.path.abspath(sys.modules[self.__module__].__file__)[:-3] + ".json"
        )

        # Store it to validate them with Pydantic
        data = Check_Metadata_Model.parse_file(metadata_file).dict()

        # Calls parents init function
        super().__init__(**data)
        # print(f"loading check {self.CheckID}")

        self._metadata_file = metadata_file

    def metadata(self) -> str:
        """Return the JSON representation of the check's metadata"""
        return self.model_dump_json()

    @abstractmethod
    def execute(self, data):
        """Execute the check's logic"""

    def _find_substrings(self, input_str) -> list[str]:
        # Regular expression pattern for matching
        # substrings within double curly braces
        pattern = r"\{\{([^}]+)\}\}"
        matches = find_substrings(pattern, input_str)
        return matches if len(matches) > 0 else []

    def _create_diag_cli(self, cli, params):
        """Create the diagnostic CLI"""

        for p in self._find_substrings(cli):
            if getattr(params, p) is None or len(getattr(params, p)) == 0:
                print(f"Error: {p} is None for {params.resource_id}")
                break
            cli = cli.replace("{{" + p + "}}", params.__dict__[p])

        if len(self._find_substrings(cli)) != 0:
            print(
                f"Error: {cli} has unresolved parameters for " f"{params.resource_id}"
            )
            return None

        return cli

    def build_cli(self, result, *, template=None):
        return self._create_diag_cli(template or self.Cli, result)

    def get_diagnostics_cli(self, result):
        diags_list = []
        for cli in self.DiagnosticClis:
            diagnostics = self.build_cli(result, template=cli)
            if diagnostics is None:
                # todo should we continue or break?
                continue
            diags_list.append(diagnostics)
        return diags_list

    async def execute_diagnostics(self, result):
        """Execute the check's diagnostics logic"""

        check_cli = self.build_cli(result)
        if check_cli is None:
            return

        result.check_cli_output[check_cli] = await execute_k8s_cli(check_cli)

        diags_list = self.get_diagnostics_cli(result)

        if len(diags_list) > 1:
            result.diagnostics_cli_output = await execute_k8s_clis(diags_list)
        else:
            diagnostics = diags_list[0]
            exec_output = await execute_k8s_cli(diagnostics)
            result.diagnostics_cli_output[diagnostics] = (
                diagnostics + "\n" + exec_output
            )

        return


@dataclass
class Check_Report:
    """Contains the Check's finding information."""

    metadata: InitVar[str]
    status: str = ""
    status_extended: str = ""
    check_metadata: Check_Metadata_Model = field(init=False)

    resource_id: str = ""
    resource_name: str = ""
    resource_details: str = ""
    resource_tags: list = field(default_factory=list)
    resource_configmap: str = ""

    # TBD: convert to string
    check_cli_output: dict = field(default_factory=dict)
    diagnostics_cli_output: dict = field(default_factory=dict)
    recommendations_output: dict = field(default_factory=dict)
    llm_failure_summary: Optional[str] = None
    llm_failure_diagnostics: list = field(default_factory=list)
    llm_analysis_record: dict = field(default_factory=dict)

    depends_on: list = field(default_factory=list)
    recommendations: list = field(default_factory=list)

    def __post_init__(self, metadata):
        self.check_metadata = Check_Metadata_Model.parse_raw(metadata)

    @property
    def fix_options(self) -> list[str]:
        if self.llm_analysis_record is None:
            return []

        return self.llm_analysis_record.get("fix") or []

    @property
    def diagnosis_options(self) -> list[str]:
        if self.llm_analysis_record is None:
            return []

        return self.llm_analysis_record.get("diagnostics") or []

    @property
    def llm_summary(self) -> str:
        if self.llm_analysis_record is None:
            return ""

        return self.llm_analysis_record.get("summary") or ""

    @property
    def passed(self):
        return self.status == "PASS"

    @abstractmethod
    def get_next_steps(self, message: str | None = None, is_async=False):
        """Get set of commands to diagnose and fix problems"""

    @abstractmethod
    async def execute_commands(self, commands: list[str]):
        """Execute commands"""

    @abstractmethod
    def start_troubleshooting_session(self, llm):
        """Start llm session"""

    @property
    @abstractmethod
    def display_object(self) -> str:
        """Returns object to display"""

    @property
    @abstractmethod
    def display_row(self) -> list[str]:
        """Returns row to display"""


# TBD lookup the inventory and make sure this matches up
def get_object_id(object_name):
    return object_name.split("/")[-1]


@dataclass
class Check_Report_K8S(Check_Report):
    """Contains the AWS Check's finding information."""

    resource_namespace: str = ""
    resource_pod: str = ""
    resource_node: str = ""
    resource_cluster: str = ""
    resource_service: str = ""
    resource_pvc: str = ""
    resource_container: str = ""
    resource_selector: str = ""
    resource_dep_type: str = ""
    resource_dep_name: str = ""
    resource_configmap: str = ""

    def __init__(self, metadata):
        super().__init__(metadata)

        self.check_cli_output = {}
        self.diagnostics_cli_output = {}
        self.recommendations_output = {}

    def analyze_result_postprocess(self, failed_objects):
        resource_id = self.resource_id
        status = self.status_extended
        check_name = self.check_metadata.CheckTitle

        print(f"\n❌ Failed {check_name}: {resource_id} ({status})")
        if self.llm_analysis_record is None:
            print(f"🤯 LLM failed to analyze {resource_id} check {check_name}")
            return

        diags = "> " + "\n> ".join(self.llm_failure_diagnostics)
        print(f"💬  Summary:\n{self.llm_failure_summary.rstrip()}")
        print(f"🛠️  Diagnostics: \n{diags}")

        fix_steps = self.llm_analysis_record.get("fix")
        fix = "> " + "\n> ".join(fix_steps)
        print(f"🛠️  Remediation: \n{fix}")

        # LLM gives a list of possible downstream failures
        # and we run it through the list of known failures
        # this means that LLM list of failures is a superset
        related_objects = []
        for obj in self.llm_analysis_record.get("objects"):
            # FIXME: this needs to be improved,
            # and is assuming that names are unique across types
            object_name = get_object_id(obj)
            if object_name in failed_objects and object_name != resource_id:
                related_objects.append(object_name)
                failed_objects[object_name].append(self)

        # note that depends_on stores the object_id
        self.depends_on = related_objects
        if len(self.depends_on) > 0:
            print(f"⚙️  Related objects: {json_dumps(related_objects, indent=2)}")
        failed_objects[resource_id].append(self)

        # print(f"Diagnostics\n: {d_output}")
        return self

    def start_troubleshooting_session(self, llm):
        self.session = LLM_Diags_Tracker(llm, self)

    async def get_next_steps(self, message: str | None = None, is_async=False):
        self.llm_analysis_record = await self.session.get_next_steps(
            message=message, is_async=is_async
        )
        return self.llm_analysis_record

    def get_diagnostics(self):
        return self.llm_failure_diagnostics

    async def execute_diagnosis(self) -> OrderedDict[str, str]:
        # if self.resource_id != "workflows-84596775c8-5vtgl":
        #     return None

        return await self.session.execute_diagnosis()

    async def execute_commands(self, commands: list[str]):
        return await execute_k8s_clis(cmds=commands)

    @property
    def display_object(self) -> str:
        fmt_view = ""
        fmt_view += f'\n  "Status":  "{self.status}"'
        fmt_view += f'\n  "Check":  "{self.check_metadata.CheckTitle}"'
        fmt_view += f'\n  "Namespace":  "{self.resource_namespace}"'
        fmt_view += f'\n  "Object":  "{self.resource_name}"'
        fmt_view += f'\n  "Severity":  "{self.check_metadata.Severity}"'
        fmt_view += f'\n  "Summary":  "{self.status_extended}"'
        return fmt_view

    @property
    def display_row(self):
        return [
            self.resource_namespace,
            self.resource_name,
            self.check_metadata.CheckTitle,
            self.check_metadata.Severity,
            self.status,
            self.status_extended,
        ]


class LLM_Diags_Tracker:

    """
    This class tracks the diagnostics and remediations
    using an ordered dictionary where the keys are the
    CLI and the values are the outputs of that CLI
    """

    def __init__(self, llm: LLM, r: Check_Report):
        check_name = r.check_metadata.CheckTitle
        self.check_name = check_name
        self.check_cli = OrderedDict()
        self.diagnostics = OrderedDict()
        self.llm = llm
        self.fail_sig = (
            f"{r.resource_id} failed check for {check_name} because "
            f"({r.status_extended})"
        )
        for cli in r.check_cli_output:
            self.check_cli[cli] = r.check_cli_output[cli]

        for cli in r.diagnostics_cli_output:
            self.diagnostics[cli] = r.diagnostics_cli_output[cli]

    # This is the starting point for the LLM analysis
    # and it is called by the check's execute function
    async def get_next_steps(self, message: str | None = None, is_async=False):
        check_cli = "\n".join(self.check_cli.keys())
        check_cli_output = "\n".join(self.check_cli.values())
        check_output = "\n" + check_cli + "\n" + check_cli_output + "\n"

        diags_output = "\n".join(self.diagnostics.values())

        llm_analysis_record = await self.llm.get_recommendations(
            self.fail_sig,
            check_cli,
            check_output,
            diags_output,
            message=message,
            is_async=is_async,
        )

        self.diagnosis_steps = llm_analysis_record.get("diagnostics")

        return llm_analysis_record

    async def execute_diagnosis(self) -> OrderedDict[str, str]:
        if self.diagnosis_steps is None:
            return

        print(f"🛠️  Executing next steps for {self.check_name}")
        for cli in self.diagnosis_steps:
            print(f"🛠️  Executing: {cli}")

        outputs = await execute_k8s_clis(self.diagnosis_steps)
        for cli in outputs:
            self.diagnostics[cli] = outputs[cli]
            print(f"🛠️  Executed: {cli}")
            print(f"🛠️  Output: {outputs[cli]}")

        return outputs
