import logging
from typing import List, Generator

import pandas as pd
import requests
from pandas.tseries.offsets import MonthEnd
from spaceone.core.connector import BaseConnector
from spaceone.core.error import ERROR_REQUIRED_PARAMETER

__all__ = ["MimirConnector"]

_LOGGER = logging.getLogger(__name__)

_PAGE_SIZE = 1000


class MimirConnector(BaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mimir_endpoint = None
        self.mimir_headers = {
            "Content-Type": "application/json",
            "X-Scope-OrgID": "",
        }

        self.field_mapper = None
        self.default_vars = None

    def create_session(
        self, domain_id: str, options: dict, secret_data: dict, schema: str
    ) -> None:
        self._check_required_params(secret_data)
        self.mimir_endpoint = secret_data["mimir_endpoint"]
        self.mimir_headers["X-Scope-OrgID"] = secret_data["X-Scope-OrgID"]

        self.field_mapper = options.get("field_mapper")
        self.default_vars = options.get("default_vars")

    @staticmethod
    def _check_required_params(secret_data: dict) -> None:
        required_parameters = ["mimir_endpoint", "X-Scope-OrgID"]
        for param in required_parameters:
            if param not in secret_data:
                raise ERROR_REQUIRED_PARAMETER(key=f"secret_data.{param}")

    def get_promql_response(self, promql_query_range: str, start: str) -> List[dict]:
        start_unix_timestamp, end_unix_timestamp = self._get_unix_timestamp(start)

        response = requests.get(
            promql_query_range,
            headers=self.mimir_headers,
            params={
                "query": self._construct_promql_query(start),
                "start": start_unix_timestamp,
                "end": end_unix_timestamp,
                "step": "1d",
            },
        )

        try:
            response.raise_for_status()
            return response.json().get("data", {}).get("result")
        except requests.HTTPError as http_err:
            _LOGGER.error(f"[get_promql_response] HTTP error occurred: {http_err}")
            _LOGGER.error(response.text)
            return None

    @staticmethod
    def _construct_promql_query(start: str) -> str:
        days = int((pd.Timestamp(start) + MonthEnd(0)).strftime("%d"))

        return f"""
            sum by (cluster, node, namespace, pod) (
                sum_over_time (
                    (
                        label_replace (
                            (
                                avg by (container, cluster, node, namespace, pod) (container_cpu_allocation)
                                * on (node) group_left ()
                                avg by (node) (node_cpu_hourly_cost)
                            ),
                            "type",
                            "CPU",
                            "",
                            ""
                        )
                        or
                        label_replace (
                            (
                                (
                                    avg by (container, cluster, node, namespace, pod) (container_memory_allocation_bytes)
                                    * on (node) group_left ()
                                    avg by (node) (node_ram_hourly_cost)
                                )
                                /
                                (1024 * 1024 * 1024)
                            ),
                            "type",
                            "RAM",
                            "",
                            ""
                        )
                        or
                        label_replace (
                            (
                                (
                                    avg by (persistentvolume, cluster, node, namespace, pod) (pod_pvc_allocation)
                                    * on (persistentvolume) group_left ()
                                    avg by (persistentvolume) (pv_hourly_cost)
                                )
                                /
                                (1024 * 1024 * 1024)
                            ),
                            "type",
                            "PV",
                            "",
                            ""
                        )
                    )[{days}d:10m]  
                )
                /
                scalar(count_over_time(vector(1)[{days}d:10m]))  
                * 24 * {days} 
            )
        """

    @staticmethod
    def _get_unix_timestamp(start: str) -> (str, str):
        start = pd.Timestamp(start)
        end = (pd.Timestamp(start) + MonthEnd(0)).replace(hour=23, minute=59, second=59)

        return str(start.timestamp()), str(end.timestamp())

    @staticmethod
    def get_cost_data(promql_response: List[dict]) -> Generator[List[dict], None, None]:
        _LOGGER.debug(f"[get_cost_data] promql_response: {promql_response}")
        # Paginate
        page_count = int(len(promql_response) / _PAGE_SIZE) + 1

        for page_num in range(page_count):
            offset = _PAGE_SIZE * page_num
            yield promql_response[offset : offset + _PAGE_SIZE]
