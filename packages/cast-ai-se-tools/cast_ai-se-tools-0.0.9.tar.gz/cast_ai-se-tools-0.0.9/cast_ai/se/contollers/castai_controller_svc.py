from typing import Dict, Any

from cast_ai.se.constants import API_SERVER, EXTERNAL_CLUSTER_PREFIX, NODES_POSTFIX, CLUSTERS_PREFIX, POLICIES_POSTFIX
from cast_ai.se.models.execution_status import ExecutionStatus
from cast_ai.se.services.api_requests_svc import cast_api_get, cast_api_put, cast_api_delete
from cast_ai.se.misc_utils import setup_logging


class CastController:
    def __init__(self, cast_api_key: str, default_cluster_id: str, log_level: str = "INFO"):
        self._logger = setup_logging(__name__, log_level)
        self._api_key = cast_api_key

        self._cluster_id = default_cluster_id
        self.cluster = None
        self.get_cluster_info()

    def get_cluster_info(self):
        get_cluster_info_url = f"{API_SERVER}{EXTERNAL_CLUSTER_PREFIX}{self._cluster_id}"
        self.cluster = cast_api_get(get_cluster_info_url, self._api_key)

    def get_nodes(self):
        get_nodes_url = f"{API_SERVER}{EXTERNAL_CLUSTER_PREFIX}{self._cluster_id}{NODES_POSTFIX}"
        return cast_api_get(get_nodes_url, self._api_key)

    def delete_nodes(self, nodes) -> ExecutionStatus:
        self._logger.info(f"{'-' * 70}[ Deleting Nodes via CAST API ]")
        # TODO: add failure logic (return)
        for node in nodes["items"]:
            delete_node_url = f"{API_SERVER}{EXTERNAL_CLUSTER_PREFIX}{self._cluster_id}{NODES_POSTFIX}/{node['id']}"
            cast_api_delete(delete_node_url, self._api_key)
        return ExecutionStatus()

    def enable_existing_policies(self) -> ExecutionStatus:
        self._logger.info(f"{'-' * 70}[ Enabling CAST policies ]")
        current_policies = self._get_policies()
        if current_policies['enabled']:
            self._logger.warning("Current policies were already enabled")
            return ExecutionStatus()
        current_policies['enabled'] = True
        return self._set_policies(current_policies)

    def _set_policies(self, policies: Dict[str, Any]) -> ExecutionStatus:
        set_policies_url = f"{API_SERVER}{CLUSTERS_PREFIX}{self._cluster_id}{POLICIES_POSTFIX}"
        result = cast_api_put(set_policies_url, self._api_key, policies)
        # TODO: Add logic for failed execution
        return ExecutionStatus()

    def _get_policies(self) -> Dict[str, Any]:
        get_policies_url = f"{API_SERVER}{CLUSTERS_PREFIX}{self._cluster_id}{POLICIES_POSTFIX}"
        return cast_api_get(get_policies_url, self._api_key)
