from unctl.lib.check.models import Check, Check_Report_K8S
from croniter import croniter


class k8s_cronjobs_suspended_or_invalid_schedule(Check):
    def is_valid_cron_expression(self, cron_expression):
        return croniter.is_valid(cron_expression)

    def _execute(self, cron, report) -> bool:
        if self.is_valid_cron_expression(cron.spec.schedule) is False:
            report.status_extended = (
                f"Cron {cron.metadata.name} "
                f"in namespace {cron.metadata.namespace} "
                f"has invalid schedule {cron.spec.schedule}"
            )
            return False

        if cron.spec.suspend is not None and cron.spec.suspend is True:
            report.status_extended = (
                f"Cron {cron.metadata.name} in namespace "
                f"{cron.metadata.namespace} is suspended"
            )
            return False

        return True

    def execute(self, data) -> list[Check_Report_K8S]:
        findings = []

        for cron in data.get_cronjobs():
            report = Check_Report_K8S(self.metadata())
            report.resource_id = cron.metadata.uid
            report.resource_name = cron.metadata.name
            report.resource_namespace = cron.metadata.namespace
            report.status = "PASS"

            if not self._execute(cron, report):
                report.status = "FAIL"

            findings.append(report)

        return findings
