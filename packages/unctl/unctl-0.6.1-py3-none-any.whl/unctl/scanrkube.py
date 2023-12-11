from kubernetes_asyncio import client, config

from kubernetes_asyncio.client import (
    AppsV1Api,
    AutoscalingV1Api,
    NetworkingV1Api,
    BatchV1Api,
    StorageV1Api,
)

from kubernetes_asyncio.client.rest import ApiException
from kubernetes_asyncio.client.api_client import ApiClient

from unctl.lib.checks.check_report import CheckReport
from unctl.lib.checks.check import Check
from unctl.lib.display import Display


# Data Collection Module


class DataCollector:
    async def fetch_data(self):
        raise NotImplementedError


class KubernetesData:
    # keep parameters sorted alphabetically to avoid merge conflicts
    def __init__(
        self,
        configmaps,
        cronjobs,
        daemonsets,
        deployments,
        endpoints,
        hpas,
        ingress_classes,
        ingresses,
        nodes,
        pods,
        pvcs,
        replicationControllers,
        replicaSets,
        secrets,
        services,
        statefulsets,
        storageClasses,
    ):
        self._configmaps = configmaps
        self._cronjobs = cronjobs
        self._daemonsets = daemonsets
        self._deployments = deployments
        self._endpoints = endpoints
        self._hpas = hpas
        self._ingress_classes = ingress_classes
        self._ingresses = ingresses
        self._nodes = nodes
        self._pods = pods
        self._pvcs = pvcs
        self._replicationControllers = replicationControllers
        self._replicaSets = replicaSets
        self._secrets = secrets
        self._services = services
        self._statefulsets = statefulsets
        self._storageClasses = storageClasses

    def get_configmaps(self):
        return self._configmaps

    def get_cronjobs(self):
        return self._cronjobs

    def get_daemonsets(self):
        return self._daemonsets

    def get_deployments(self):
        return self._deployments

    def get_endpoints(self):
        return self._endpoints

    def get_hpas(self):
        return self._hpas

    def get_ingress_classes(self):
        return self._ingress_classes

    def get_ingresses(self):
        return self._ingresses

    def get_nodes(self):
        return self._nodes

    def get_pods(self):
        return self._pods

    def get_pvcs(self):
        return self._pvcs

    def get_replication_controllers(self):
        return self._replicationControllers

    def get_replica_sets(self):
        return self._replicaSets

    def get_secrets(self):
        return self._secrets

    def get_services(self):
        return self._services

    def get_statefulsets(self):
        return self._statefulsets

    def get_storage_classes(self):
        return self._storageClasses


class KubernetesDataCollector(DataCollector):
    async def fetch_data(self):
        # Load kube config
        await config.load_kube_config()

        try:
            async with ApiClient() as api:
                # Get an instance of the API class
                v1 = client.CoreV1Api(api)
                v1apps = AppsV1Api(api)
                v1autoscaling = AutoscalingV1Api(api)
                v1networking = NetworkingV1Api(api)
                v1storage = StorageV1Api(api)
                v1batch = BatchV1Api(api)

                # Fetch the list of nodes and pods

                configmaps = (await v1.list_config_map_for_all_namespaces()).items
                cronjobs = (await v1batch.list_cron_job_for_all_namespaces()).items
                daemonsets = (await v1apps.list_daemon_set_for_all_namespaces()).items
                deployments = (await v1apps.list_deployment_for_all_namespaces()).items
                endpoints = (await v1.list_endpoints_for_all_namespaces()).items
                autoscaling = await (
                    v1autoscaling.list_horizontal_pod_autoscaler_for_all_namespaces()
                )
                hpas = (autoscaling).items
                ingress_classes = (await v1networking.list_ingress_class()).items
                ingresses = (await v1networking.list_ingress_for_all_namespaces()).items
                nodes = (await v1.list_node(watch=False)).items
                pods = (await v1.list_pod_for_all_namespaces()).items
                pvcs = (
                    await v1.list_persistent_volume_claim_for_all_namespaces()
                ).items
                replicationControllers = (
                    await v1.list_replication_controller_for_all_namespaces()
                ).items
                replicaSets = (await v1apps.list_replica_set_for_all_namespaces()).items
                secrets = (await v1.list_secret_for_all_namespaces()).items
                services = (await v1.list_service_for_all_namespaces()).items
                statefulsets = (
                    await v1apps.list_stateful_set_for_all_namespaces()
                ).items
                storageClasses = (await v1storage.list_storage_class()).items

                return KubernetesData(
                    configmaps,
                    cronjobs,
                    daemonsets,
                    deployments,
                    endpoints,
                    hpas,
                    ingress_classes,
                    ingresses,
                    nodes,
                    pods,
                    pvcs,
                    replicationControllers,
                    replicaSets,
                    secrets,
                    services,
                    statefulsets,
                    storageClasses,
                )

        except ApiException as api_exception:
            # Handle exceptions raised by Kubernetes API interactions
            print(f"An error occurred with the Kubernetes API: {api_exception.reason}")
            # print(api_exception.body)
            return None

        except Exception as general_exception:
            # A generic handler for all other exceptions
            print(f"An unexpected error occurred: {general_exception}")
            return None


# Main Application


class ResourceChecker:
    def __init__(self, collector: DataCollector, checks: list[Check]):
        self.collector = collector
        self.checks = checks

    async def execute(self, run_diags=False):
        data = await self.collector.fetch_data()
        if data is None:
            print("Failed to collect inventory")
            exit(1)

        results: dict[str, list[CheckReport]] = {}
        total_checks = len(self.checks)
        completed_checks = 0

        # Display the progress bar header
        Display.display_progress_bar_header()

        for check in self.checks:
            if check.Enabled is False:
                continue

            results[check.__class__.__name__] = result = check.execute(data)
            completed_checks += 1
            Display.display_progress_bar(
                completed_checks / total_checks, check.CheckTitle
            )

            print()  # New line after the progress bar completion

            if run_diags is True:
                # For all items in the result, we expect the JSON keys
                # to be present to run the diagnostics
                for result in results[check.__class__.__name__]:
                    if result.passed:
                        continue

                    await result.execute_diagnostics()

        return results


class JobDefinition:
    def __init__(self, check_modules):
        self.check_modules = check_modules

    def generate_jobs(self, suite_name=None):
        # TBD: this list should be generated based on the JSON file
        # Loads checks related to the suite specified
        # suite_path = os.path.join(self.checks_dir, suite_name)
        check_modules = self.check_modules

        jobs: list[Check] = []
        for module in check_modules:
            # Load only the checks
            if len(module.__package__.split(".")) < 4:
                continue

            # Extract class name from the module's file name
            class_name = module.__package__.split(".")[-1]

            # Instantiate the class named after the module
            check_class = getattr(module, class_name)

            # load the class
            check_instance = check_class()

            # Ensure that the execute method exists in the check class
            if hasattr(check_instance, "execute"):
                jobs.append(check_instance)

        return jobs
