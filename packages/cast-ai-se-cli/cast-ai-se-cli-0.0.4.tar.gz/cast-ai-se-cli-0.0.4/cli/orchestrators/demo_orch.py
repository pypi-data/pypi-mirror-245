import logging
import time

from cli.models.config import ConfigObject
from cli.orchestrators.base_orch import BaseOrchestrator
from cli.services.validators import validate_kubectl_context

from cast_ai.se.contollers.castai_controller_svc import CastController
from cast_ai.se.contollers.eks_controller_svc import EKSController
from cast_ai.se.contollers.kubectl_controller_svc import KubectlController
from cast_ai.se.models.execution_status import ExecutionStatus
from cast_ai.se.models.cloud_confs import AwsConfig


class DemoOrchestrator(BaseOrchestrator):
    def __init__(self, cfg: ConfigObject):
        super().__init__(cfg)
        self._logger = logging.getLogger(__name__)

        cid = cfg.custom_cid if cfg.custom_cid else cfg.app_config["CAST"]["DEFAULT_CLUSTER_ID"]

        self._cast_ctrl = CastController(cfg.app_config["CAST"]["CAST_API_KEY"], cid)
        self._kubectl_ctrl = KubectlController()

        self._initial_nodes = self._cast_ctrl.get_nodes()

        self._cloud_ctrl = None
        self._set_cloud_controller()
        self.demo_subcommand_mapping = {
            "on": self.demo_on_sequence,
            "off": self.demo_off_sequence,
            "refresh": self.demo_refresh_sequence,
        }
        validate_kubectl_context(self._kubectl_ctrl, self._cast_ctrl.cluster['providerType'])

    def execute(self) -> None:
        subcommand = self._cfg.app_inputs["demo_subcommand"]
        if subcommand in self.demo_subcommand_mapping:
            self.demo_subcommand_mapping[subcommand]()
        else:
            raise ValueError(f'Invalid option: {subcommand}')

    def demo_refresh_sequence(self):
        if self._cast_ctrl.are_policies_disabled():
            self._logger.critical("Policies are off - Cluster hibernating")
            raise RuntimeError("Policies are off - Cluster hibernating (Consider [on] subcommand)")

        self._logger.info(f"{'=' * 80}< Starting demo-REFRESH sequence >{'=' * 80} ")
        start_time = time.time()
        demo_node_count = self._cfg.app_config["GENERAL"]["DEMO_NODE_COUNT"]
        demo_replica_count = self._cfg.app_config["GENERAL"]["DEMO_REPLICAS"]

        initial_nodes = self._cast_ctrl.get_nodes()
        demo_node_count = demo_node_count + len(initial_nodes["items"])

        if not self._cast_ctrl.is_downscaler_disabled():
            self.spinner_run("Disabling downscaler policy", lambda: self._cast_ctrl.disable_downscaler_policy())

        self.spinner_run(f'Scaling cloud default ng to {demo_node_count}',
                         lambda: self._cloud_ctrl.scale_default_ng(demo_node_count))

        all_demo_nodes_up = self.spinner_run("Waiting for new nodes to be ready",
                                             lambda: self._wait_for_new_nodes(len(initial_nodes["items"]),
                                                                              demo_node_count))

        if all_demo_nodes_up.success:
            self.spinner_run(f'Deleting nodes prior to refresh ({len(initial_nodes["items"])})',
                             lambda: self._cast_ctrl.delete_nodes(initial_nodes))
        else:
            print("❗❕ You may want to delete the nodes that existed prior to refresh")

        print(f"It took {int(time.time() - start_time)} seconds to refresh demo")

    def demo_off_sequence(self):
        if self._cast_ctrl.are_policies_disabled():
            self._logger.critical("Policies are off - Cluster hibernating")
            raise RuntimeError("Policies are off - Cluster hibernating")
        demo_off_cronjob = self._cfg.app_config["KUBECTL"]["DEMO_OFF_CRONJOB"]
        self._logger.info(f"{'=' * 80}< Starting demo-OFF sequence >{'=' * 80} ")

        msg = "Scaling all deployments in default namespace to 0"
        self.spinner_run(msg, lambda: self._kubectl_ctrl.scale_deployments(0))

        self.spinner_run("Disabling CAST Unscheduled pods policy",
                         lambda: self._cast_ctrl.disable_unscheduled_pods_policy())

        msg = f"Manually triggering {demo_off_cronjob}"
        cronjob_triggered = (
            self.spinner_run(msg, lambda: self._kubectl_ctrl.trigger_cronjob(demo_off_cronjob, exec_wait=True)))

        if cronjob_triggered.success:
            self.spinner_run("Turning off autoscaling on default ng", lambda: self._cloud_ctrl.scale_default_ng(0))
        else:
            print("❗❕ You may want to turn off autoscaling manually...")

    def demo_on_sequence(self):
        if not self._cast_ctrl.are_policies_disabled():
            self._logger.critical("Policies are on - Cluster not properly Hibernated")
            raise RuntimeError("Policies are on - Cluster not properly Hibernated (Consider [refresh] subcommand)")

        self._logger.info(f"{'=' * 80}< Starting demo-ON sequence >{'=' * 80}")
        start_time = time.time()
        demo_node_count = self._cfg.app_config["GENERAL"]["DEMO_NODE_COUNT"]
        demo_replicas = self._cfg.app_config["GENERAL"]["DEMO_REPLICAS"]
        initial_nodes = self._cast_ctrl.get_nodes()

        self.spinner_run(f"Scaling cloud default ng to {demo_node_count}",
                         lambda: self._cloud_ctrl.scale_default_ng(demo_node_count))
        all_demo_nodes_up = (self.spinner_run("Waiting for new nodes to be ready",
                             lambda: self._wait_for_new_nodes(len(initial_nodes["items"]), demo_node_count)))
        self.spinner_run("Disabling CAST Binpacking policies",
                         lambda: self._cast_ctrl.disable_downscaler_policy())
        self.spinner_run("Enabling CAST policies",
                         lambda: self._cast_ctrl.enable_existing_policies())
        self.spinner_run(f"Scaling all deployments to {demo_replicas} replicas",
                         lambda: self._kubectl_ctrl.scale_deployments(demo_replicas))
        if all_demo_nodes_up.success:
            self.spinner_run(f'Deleting initial {len(initial_nodes["items"])} fallback nodes ',
                             lambda: self._cast_ctrl.delete_nodes(initial_nodes))
        else:
            print("❗❕ You may want to delete the Fallback nodes...")

        print(f"It took {int(time.time() - start_time)} seconds to prep demo")

    def _wait_for_new_nodes(self, initial_node_count: int, new_demo_count: int) -> ExecutionStatus:
        try:
            self._logger.info(f"{'-' * 70}[ Waiting for new nodes to be ready ]")
            # demo_node_count = self._cfg.app_config["GENERAL"]["DEMO_NODE_COUNT"]
            ng_scaling_timeout = self._cfg.app_config["GENERAL"]["NG_SCALING_TIMEOUT"]
            start_time = time.time()
            while True:
                nodes = self._cast_ctrl.get_nodes()
                self._logger.debug(f"Current:{len(nodes['items'])} "
                                   f"Initial:{initial_node_count} "
                                   f"Requested:{new_demo_count}")
                if len(nodes["items"]) == initial_node_count + new_demo_count:
                    all_nodes_ready = all(node["state"]["phase"] == "ready" for node in nodes["items"])
                    if all_nodes_ready:
                        self._logger.info(f"Waited {time.time() - start_time} for all new nodes to be ready...")
                        return ExecutionStatus()
                    else:
                        node_states = [node["state"]["phase"] for node in nodes["items"]]
                        node_states_str = ", ".join(node_states)
                        self._logger.debug(f"Node states: ({node_states_str})")
                if time.time() - start_time > ng_scaling_timeout:
                    self._logger.warning(f"Timeout ({ng_scaling_timeout}sec) reached while waiting for new nodes")
                    return ExecutionStatus(f"Timeout ({ng_scaling_timeout}sec)")
                time.sleep(1)
        except Exception as e:
            self._logger.error(f"Something went wrong:[{str(e)}]")
            return ExecutionStatus(f"Something went wrong:[{str(e)}]")

    def _set_cloud_controller(self):
        provider_type = self._cast_ctrl.cluster['providerType']
        #match (self._cast_ctrl.cluster['providerType']):
        if provider_type == "eks":
            self._cloud_ctrl = EKSController(AwsConfig(self._cfg.app_config["AWS"]))
            self._logger.info("Orchestrator is using EKS as Cloud Controller")
        else:
            self._logger.error(f"Unsupported cloud {self._cast_ctrl.cluster['providerType']}")
            raise ValueError(f"{self._cast_ctrl.cluster['providerType']}")
