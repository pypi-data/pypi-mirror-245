from typing import cast

from textual.app import App

from unctl.interactive.screens.table import TableScreen
from unctl.interactive.screens.quit_confirm import QuitConfirm
from unctl.interactive.screens.resolving import ResolvingScreen

from unctl.lib.checks.check_report import CheckReport
from unctl.scanrkube import ResourceChecker

from unctl.lib.llm.assistant import OpenAIAssistant


class InteractiveTable(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        ("q", "request_quit", "Quit"),
    ]

    def __init__(
        self,
        use_llm=False,
        checker: ResourceChecker | None = None,
        results: dict[str, list[CheckReport]] = None,
    ):
        super().__init__()

        self.use_llm = use_llm

        if results is None:
            results = {}

        self.headers = ["Namespace", "Object", "Check", "Severity", "Status", "Summary"]

        self.items: list[CheckReport] = []
        for check_list in results.values():
            self.items.extend(item for item in check_list if item.status == "FAIL")

        self.checker = checker

    def on_mount(self):
        self.install_screen(
            TableScreen(columns=self.headers, items=self.items), name="table"
        )
        self.push_screen("table")

    def on_data_table_row_selected(self, row_selected):
        item: CheckReport = self.items[row_selected.cursor_row]
        if not self.is_screen_installed(item.object_id):
            self.install_screen(ResolvingScreen(item=item), item.object_id)
        self.push_screen(item.object_id)

    def action_request_quit(self):
        self.push_screen(QuitConfirm())

    async def re_run_checks(self):
        results = await self.checker.execute()
        flat_results = [item for sublist in results.values() for item in sublist]

        # Update existing items
        for item in self.items:
            found = False
            for res in flat_results:
                if item.object_id == res.object_id:
                    item.status = item.status
                    found = True

            # if item not in the list anymore then mark it as resolved
            if not found:
                item.status = "PASS"

        # append new failed items
        for res in flat_results:
            if not res.passed and not any(
                res.object_id == item.object_id for item in self.items
            ):
                if self.use_llm:
                    await res.execute_diagnostics()
                    await res.init_llm(OpenAIAssistant())
                    await res.get_next_steps()

                self.items.append(res)

        # table is persistent screen so need update it with new list
        table = cast(TableScreen, self.get_screen("table"))
        table.update(items=self.items)

        return self.items


if __name__ == "__main__":
    app = InteractiveTable()
    app.run()
