from textual.app import App

from unctl.interactive.screens.table import TableScreen
from unctl.interactive.screens.quit_confirm import QuitConfirm
from unctl.interactive.screens.resolving import ResolvingScreen

from unctl.lib.check.models import Check_Report
from unctl.scanrkube import ResourceChecker

from unctl.lib.llm.openai import LLM


class InteractiveTable(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        ("q", "request_quit", "Quit"),
    ]

    def __init__(
        self,
        checker: ResourceChecker | None = None,
        results: dict[str, list[Check_Report]] = None,
    ):
        super().__init__()

        if results is None:
            results = {}

        self.headers = ["Namespace", "Object", "Check", "Severity", "Status", "Summary"]

        self.items: list[Check_Report] = []
        for check_list in results.values():
            self.items.extend(item for item in check_list if item.status == "FAIL")

        self.checker = checker

    def on_mount(self):
        self.install_screen(
            TableScreen(columns=self.headers, items=self.items), name="table"
        )
        self.push_screen("table")

    def on_data_table_row_selected(self, row_selected):
        item: Check_Report = self.items[row_selected.cursor_row]
        if not self.is_screen_installed(item.resource_id):
            self.install_screen(ResolvingScreen(item=item), item.resource_id)
        self.push_screen(ResolvingScreen(item=item), item.resource_id)

    def action_request_quit(self):
        self.push_screen(QuitConfirm())

    async def re_run_checks(self):
        results = await self.checker.execute(run_diags=True)
        flat_results = [item for sublist in results.values() for item in sublist]

        # Update existing items
        for item in self.items:
            found = False
            for res in flat_results:
                if item.resource_id == res.resource_id:
                    item.status = item.status
                    found = True

            # if item not in the list anymore then mark it as resolved
            if not found:
                item.status = "PASS"

        # append new failed items
        for res in flat_results:
            if not res.passed and not any(
                res.resource_id == item.resource_id for item in self.items
            ):
                res.start_troubleshooting_session(LLM())
                await res.get_next_steps(is_async=True)
                self.items.append(res)

        # table is persistant screen so need update it with new list
        table = self.get_screen("table")
        table.update(items=self.items)

        return self.items


if __name__ == "__main__":
    app = InteractiveTable()
    app.run()
