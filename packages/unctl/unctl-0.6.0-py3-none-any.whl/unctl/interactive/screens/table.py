from textual import work
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header

from unctl.lib.checks.check_report import CheckReport


class TableScreen(Screen):
    TITLE = "Interactive remediation"

    BINDINGS = [
        ("r", "re_run_check", "Re-run checks"),
    ]

    def __init__(self, columns: list[str], items: list[CheckReport]):
        super().__init__()
        self.columns = columns
        self.items = items

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield DataTable(zebra_stripes=True, cursor_type="row", id="table")

    def on_mount(self):
        data_table = self.query_one(DataTable)
        data_table.add_columns(*self.columns)
        # data_table.expand = True

        rows = list(map(lambda item: item.display_row, self.items))
        data_table.add_rows(rows)

    def action_re_run_check(self):
        table = self.query_one(DataTable)
        table.loading = True

        self.re_run_checks()

    def update(self, items: list[CheckReport]):
        table = self.query_one(DataTable)
        rows = list(map(lambda item: item.display_row, self.items))
        table.rows = {}
        table.add_rows(rows)

    @work()
    async def re_run_checks(self):
        await self.app.re_run_checks()
        table = self.query_one(DataTable)
        table.loading = False
