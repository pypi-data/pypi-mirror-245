import logging
import time
import boto3

from cast_ai.se.models.cloud_confs import AwsConfig
from cast_ai.se.models.execution_status import ExecutionStatus
from cast_ai.se.contollers.cloud_controller_svc import CloudController


class EKSController(CloudController):
    def __init__(self, aws_conf: AwsConfig):
        try:
            self._asg = aws_conf.default_node_group
            self._logger = logging.getLogger(__name__)
            self._client = boto3.client(
                'autoscaling',
                region_name=aws_conf.region,
                aws_access_key_id=aws_conf.access_key,
                aws_secret_access_key=aws_conf.access_secret_key
            )
        except Exception as e:
            self._logger.critical(f"An error occurred during EKSController initialization: {str(e)}")
            raise RuntimeError(f"An error occurred during EKSController initialization: {str(e)}")

    def scale_default_ng(self, node_count: int) -> ExecutionStatus:
        self._logger.info(f"{'-' * 70}[ Scaling EKS Auto Scaling Group to {node_count} ]")

        try:
            for _ in range(5):
                response = self._client.update_auto_scaling_group(
                    AutoScalingGroupName=self._asg,
                    MinSize=node_count,
                    MaxSize=node_count + 1,  # You can adjust the max size as needed
                    DesiredCapacity=node_count,
                )
                if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                    if not self._is_ng_scaled(node_count):
                        self._logger.warning(f"Default ng=({self._asg}) has still not changed going to retry")
                        time.sleep(1)
                        continue
                    else:
                        self._logger.debug(f"Successfully updated AWS Auto Scaling Group [{self._asg}] : [{str()}]")
                        self._logger.info('Successfully updated AWS Auto Scaling Group')
                        return ExecutionStatus()
                else:
                    self._logger.error(f"Scaling default ng result = [{response}]")
                    return ExecutionStatus(f'HTTP {response["ResponseMetadata"]["HTTPStatusCode"]}')
        except Exception as e:
            self._logger.exception(f"Error trying to set Demo Nodes capacity: {str(e)}")
            raise RuntimeError(f"Error trying to set Demo Nodes capacity: {str(e)}")

    def _is_ng_scaled(self, node_count: int) -> bool:
        validate_ng_response = self._client.describe_auto_scaling_groups(AutoScalingGroupNames=[self._asg])
        self._logger.debug(f"Validating ASG={validate_ng_response['AutoScalingGroups'][0]}")
        return (validate_ng_response["AutoScalingGroups"][0]["DesiredCapacity"] == node_count and
                validate_ng_response["AutoScalingGroups"][0]["MinSize"] == node_count)
