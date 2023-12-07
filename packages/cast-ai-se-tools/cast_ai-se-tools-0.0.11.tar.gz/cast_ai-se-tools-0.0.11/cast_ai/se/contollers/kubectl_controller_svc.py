import logging
import shutil
import subprocess
import time
from typing import Optional

from cast_ai.se.constants import CAST_NS, EVERY_MINUTE_SCHEDULE
from cast_ai.se.misc_utils import get_get_deployments_command, validate_required_tools_exist
from cast_ai.se.services.logging_svc import setup_logging
from cast_ai.se.models.execution_status import ExecutionStatus


class KubectlController:
    def __init__(self, log_level: str = logging.INFO):
        self._logger = setup_logging(__name__, log_level)
        self._log_level = log_level
        validate_required_tools_exist(log_level)
        if not shutil.which("kubectl") or ():
            self._logger.exception("Kubectl not in path")
            raise RuntimeError("Kubectl not in path")

    def modify_cronjob_schedule_sequence(self, cronjob_name: str, namespace: str = CAST_NS) -> ExecutionStatus:
        self._logger.info(f"{'-' * 70} Triggering {cronjob_name} cronjob")
        try:
            # Step 1: Get the original schedule
            origin_schedule = self.get_original_schedule(cronjob_name)
            # Step 2: Modify CronJob schedule (so it runs every minute...so it starts right away (NOW))
            self.patch_cronjob(cronjob_name, EVERY_MINUTE_SCHEDULE)
            # Step 3: Wait for execution
            for i in range(60):
                if self.is_cronjob_active(cronjob_name, namespace):
                    self._logger.debug(f"Cronjob {cronjob_name} found ACTIVE")
                    break
                else:
                    time.sleep(1)  # Wait for a second

            # Step 4: Restore original schedule
            self.patch_cronjob(cronjob_name, origin_schedule)
            return ExecutionStatus()
        except subprocess.CalledProcessError as e:
            self._logger.exception(f"Error executing kubectl: {str(e)}")
            raise RuntimeError(f"Error executing kubectl: {str(e)}")
        except Exception as e:
            self._logger.exception(f"An error occurred: {str(e)}")
            raise RuntimeError(f"An error occurred: {str(e)}")

    def patch_cronjob(self, cronjob_name: str, schedule: str) -> None:
        self._logger.info(f"Modifying schedule for CronJob '{cronjob_name}' in namespace '{CAST_NS}' to {schedule}")
        kubectl_cmd = ["kubectl", "patch", "cronjob", cronjob_name, "-n", CAST_NS, "--type=json",
                       "-p", f'[{{"op": "replace", "path": "/spec/schedule", "value": "{schedule}"}}]']
        result = subprocess.check_output(kubectl_cmd, text=True, shell=True)
        self._logger.debug(f"Command=[{' '.join(kubectl_cmd)} | Output=[{result.rstrip()}]")

    def get_original_schedule(self, cronjob_name) -> str:
        json_path = "jsonpath='{.spec.schedule}'"
        get_schedule_cmd = f"kubectl get cronjob {cronjob_name} -n {CAST_NS} -o {json_path}"
        origin_schedule = subprocess.check_output(get_schedule_cmd, text=True, shell=True).strip("'")
        self._logger.info(f"Original schedule of {cronjob_name} = {origin_schedule}")
        return origin_schedule

    def scale_deployments(self, replica_count: int) -> ExecutionStatus:
        self._logger.info(f"{'-' * 70}[ Scaling Deployments to {replica_count} ]")
        try:
            # Get the list of deployments across all namespaces with namespace and name
            get_deployments_command = get_get_deployments_command(bool(not replica_count), self._log_level)
            result = subprocess.check_output(get_deployments_command, text=True, shell=True)
            deployments = result.split()
            self._logger.debug(f'Command=[{str(get_deployments_command)}] | Output=[{" ".join(deployments)}]')

            # Iterate over pairs of namespace and deployment name
            for i in range(0, len(deployments), 1):
                deployment_name = deployments[i]

                kubectl_cmd = ["kubectl", "scale", f"--replicas={replica_count}", f"deployment/{deployment_name}",
                               "--namespace=default"]
                result = subprocess.check_output(kubectl_cmd, text=True, shell=True)
                self._logger.debug(f'Command=[{" ".join(kubectl_cmd)}] | Output=[{result.rstrip()}]')
                self._logger.info(f"Deployment {deployment_name}[default] scaled to {replica_count} replicas.")
            return ExecutionStatus()
        except subprocess.CalledProcessError as e:
            self._logger.exception(f"Error executing kubectl command related to deployments scaling: {str(e)}")
            raise RuntimeError(f"Error executing kubectl command related to deployments scaling: {str(e)}")

    def is_cronjob_active(self, cronjob_name: str, namespace: str) -> Optional[bool]:
        command = f'kubectl get cronjobs.batch -n {namespace} {cronjob_name}'
        try:
            result = subprocess.check_output(command, shell=True, text=True)
            # Split the output by lines
            lines = result.split("\n")

            result = result.rstrip().replace("\n", " -<!n>- ")
            result = ' '.join(result.split())
            self._logger.debug(f"Command=[{command}] | Output=[{result}]")

            if lines[1].split()[-3] == "1":
                return True
            return False

        except subprocess.CalledProcessError as e:
            self._logger.exception(f"Error executing/parsing kubectl command:{command} -=> {e}")
            print(f"Error executing kubectl command: {e}")
            return None
