import asyncio
import json
import subprocess
from abc import abstractmethod
from collections import OrderedDict
from tempfile import NamedTemporaryFile
from typing import Literal

from dataclasses import dataclass, field
from re import findall as find_substrings

from pydantic import ValidationError

from unctl.lib.llm.base import LanguageModel, LLMAPIError
from unctl.lib.llm.session import LLMSessionKeeper
from unctl.lib.models.checks import CheckMetadataModel
from unctl.lib.models.recommendations import LLMRecommendation


async def _execute_command(cmd: str):
    if cmd == "":
        return

    script = NamedTemporaryFile(mode="w+t", delete=False)
    script.write("#!/bin/bash\n")
    script.write(cmd)
    script.close()

    bash_script = ["bash", script.name]
    proc = await asyncio.create_subprocess_exec(
        *bash_script, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    stdout, stderr = await proc.communicate()

    if stderr:
        print(f"Error(executing command({cmd}) stderr: {stderr.decode('utf-8')}")
        return f"stderr: {stderr.decode('utf-8')}"

    return stdout.decode("utf-8")


@dataclass
class CheckReport:
    """Contains the Check's finding information."""

    check_metadata: CheckMetadataModel

    _recommendation: LLMRecommendation | None = None
    _session_keeper: LLMSessionKeeper | None = None

    status: Literal["PASS", "FAIL"] | None = None
    status_extended: str = ""
    module: str = ""

    _executed_cmd: OrderedDict[str, str] = field(default_factory=OrderedDict)
    _depends_on: list[str] = field(default_factory=list)

    def __init__(self, metadata):
        self.check_metadata = CheckMetadataModel.model_validate_json(metadata)
        self._executed_cmd = OrderedDict()
        self._depends_on = []

    def _find_substrings(self, input_str) -> list[str]:
        # Regular expression pattern for matching substrings within double curly braces
        pattern = r"\{\{([^}]+)\}\}"
        matches = find_substrings(pattern, input_str)
        return matches if len(matches) > 0 else []

    def _fill_tmpl_cmd(self, cmd: str):
        # TODO: switch to proper template tool
        for p in self._find_substrings(cmd):
            if getattr(self, p) is None or len(getattr(self, p)) == 0:
                print(f"Error: {p} is None for {self.object_id}")
                break
            cmd = cmd.replace("{{" + p + "}}", self.__dict__[p])

        if len(self._find_substrings(cmd)) != 0:
            print(f"Error: {cmd} has unresolved parameters for {self.object_id}")
            return None

        return cmd

    async def init_llm(self, llm: LanguageModel):
        """Initializes AI LLM component"""
        self._session_keeper = LLMSessionKeeper(llm=llm)
        await self._session_keeper.init_session(data=self.cmd_output_messages)

    async def execute_commands(self, cmds: list[str]):
        """Execute commands"""
        result = OrderedDict()
        error = dict()

        for cmd in cmds:
            cli_output = await _execute_command(cmd=cmd)
            self._executed_cmd[cmd] = cli_output
            result[cmd] = cli_output

            if not self.is_llm_disabled:
                # sending data to LLM may fail
                # but we still want to return output and error
                try:
                    await self._session_keeper.push_info(
                        f"""After command {cmd} got output:
                            {cli_output}"""
                    )
                except LLMAPIError as e:
                    error[cmd] = e.message

        return result, error

    async def execute_diagnostics(self):
        """Execute check and builtin diagnostics commands"""
        check_cmd = self._fill_tmpl_cmd(self.check_metadata.Cli)
        if check_cmd is not None:
            self._executed_cmd[check_cmd] = await _execute_command(check_cmd)

        for cmd in self.check_metadata.DiagnosticClis:
            diagnostic_cmd = self._fill_tmpl_cmd(cmd)
            if diagnostic_cmd is not None:
                self._executed_cmd[diagnostic_cmd] = await _execute_command(
                    diagnostic_cmd
                )

    async def postprocess(self, failed_objects: dict[str, list]):
        name = self.object_name
        status = self.status_extended
        check_name = self.check_metadata.CheckTitle

        print(f"\n❌ Failed {check_name}: {name} ({status})")
        if self._recommendation is None:
            print(f"🤯 LLM failed to analyze {name} check {check_name}")
            return

        diags = "> " + "\n> ".join(self.diagnosis_options)
        print(f"💬  Summary:\n{self.llm_summary.rstrip()}")
        print(f"🛠️  Diagnostics: \n{diags}")

        fix_steps = self.fix_options
        fix = "> " + "\n> ".join(fix_steps)
        print(f"🛠️  Remediation: \n{fix}")

        # LLM gives a list of possible downstream failures
        # and we run it through the list of known failures
        # this means that LLM list of failures is a superset
        related_objects = []
        for object_name in self.failed_objects:
            if object_name in failed_objects and object_name != name:
                related_objects.append(object_name)
                failed_objects[object_name].append(self)

        # note that depends_on stores the object_id
        self._depends_on = related_objects
        if len(self._depends_on) > 0:
            print(f"⚙️  Related objects: {json.dumps(related_objects, indent=2)}")
        failed_objects[name].append(self)

        return self

    async def get_next_steps(self, message: str | None = None):
        """Get set of commands to diagnose and fix problems"""
        if self._session_keeper is None:
            return self._recommendation

        try:
            recommendation = await self._session_keeper.request_llm_recommendation(
                message=message
            )

            try:
                self._recommendation = LLMRecommendation.model_validate_json(
                    recommendation
                )
            except ValidationError:
                return LLMRecommendation(
                    summary=f"Failed to parse openai response. {recommendation}"
                )

            return self._recommendation
        except LLMAPIError as e:
            return LLMRecommendation(summary=e.message)

    @property
    def cmd_output_messages(self):
        messages: list[str] = []
        for cmd, output in self._executed_cmd.items():
            messages.append(
                f"""After running command "{cmd}" got output:
                    {output}"""
            )

        return messages

    @property
    def fix_options(self) -> list[str]:
        if self._recommendation is None:
            return []

        return self._recommendation.fixes or []

    @property
    def failed_objects(self) -> list[str]:
        if self._recommendation is None:
            return []

        return self._recommendation.objects or []

    @property
    def diagnosis_options(self) -> list[str]:
        if self._recommendation is None:
            return []

        return self._recommendation.diagnostics or []

    @property
    def llm_summary(self) -> str:
        if self._recommendation is None:
            return "LLM is disabled."

        return self._recommendation.summary or "Analysis empty or hasn't been made"

    @property
    def passed(self):
        return self.status == "PASS"

    @property
    def is_llm_disabled(self):
        return self._recommendation is None

    @property
    @abstractmethod
    def display_object(self) -> str:
        """Returns object to display"""

    @property
    @abstractmethod
    def display_row(self) -> list[str]:
        """Returns row to display"""

    @property
    @abstractmethod
    def object_id(self) -> str:
        """Returns identifier of failed object"""

    @property
    @abstractmethod
    def object_name(self) -> str:
        """Returns name of failed object"""
