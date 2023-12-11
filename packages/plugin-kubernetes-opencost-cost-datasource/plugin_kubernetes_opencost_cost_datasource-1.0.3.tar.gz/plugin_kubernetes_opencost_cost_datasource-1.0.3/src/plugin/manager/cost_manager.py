import logging
from typing import Generator, List

import pandas as pd
from spaceone.core.manager import BaseManager
from spaceone.cost_analysis.error import ERROR_REQUIRED_PARAMETER

from ..connector.mimir_connector import MimirConnector

_LOGGER = logging.getLogger(__name__)

_REQUIRED_FIELDS = [
    "cost",
]


class CostManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mimir_connector = MimirConnector()

    def get_data(
            self,
            domain_id: str,
            options: dict,
            secret_data: dict,
            schema: str,
            task_options: dict,
    ) -> Generator[dict, None, None]:
        self._validate_secret_data(secret_data)

        self.mimir_connector.create_session(domain_id, options, secret_data, schema)

        promql_query_range = (
            f"{secret_data['mimir_endpoint']}/prometheus/api/v1/query_range"
        )

        promql_response = self.mimir_connector.get_promql_response(
            promql_query_range, task_options["start"]
        )

        response_stream = self.mimir_connector.get_cost_data(promql_response)
        for results in response_stream:
            yield self._make_cost_data(results)

        yield {"results": []}

    @staticmethod
    def _validate_secret_data(secret_data: dict):
        required_parameters = ["mimir_endpoint", "X-Scope-OrgID"]
        for param in required_parameters:
            if param not in secret_data:
                raise ERROR_REQUIRED_PARAMETER(key=f"secret_data.{param}")

    def _make_cost_data(self, results: List[dict]) -> dict:
        costs_data = []
        for result in results:
            result = self._strip_dict_keys(result)
            result = self._strip_dict_values(result)

            if self.mimir_connector.default_vars:
                self._set_default_vars(result)

            # self._convert_cost_and_billed_date(result)

            for i in range(len(result["values"])):
                result["cost"] = float(result["values"][i][1])
                result["billed_date"] = pd.to_datetime(
                    result["values"][i][0], unit="s"
                ).strftime("%Y-%m-%d")

                self._check_required_fields(result)

                additional_info = self._make_additional_info(result)
                data = self._make_data(result)

                try:
                    data = {
                        "cost": result["cost"],
                        "usage_quantity": result.get("usage_quantity", 0),
                        "usage_type": result.get("usage_type"),
                        "usage_unit": result.get("usage_unit"),
                        "provider": "OpenCost",
                        "region_code": result.get("region_code"),
                        "product": result.get("product"),
                        "resource": result.get("resource", ""),
                        "billed_date": result["billed_date"],
                        "data": data,
                        "additional_info": additional_info,
                        "tags": result.get("tags", {}),
                    }
                except Exception as e:
                    _LOGGER.error(
                        f"[_make_cost_data] make data error: {e}", exc_info=True
                    )
                    raise e
                costs_data.append(data)

        return {"results": costs_data}

    @staticmethod
    def _strip_dict_keys(result: dict) -> dict:
        return {
            key: value.strip() if isinstance(value, str) else value
            for key, value in result.items()
        }

    @staticmethod
    def _strip_dict_values(result: dict) -> dict:
        return {
            key: value.strip() if isinstance(value, str) else value
            for key, value in result.items()
        }

    def _set_default_vars(self, result: dict):
        for key, value in self.mimir_connector.default_vars.items():
            result[key] = value

    @staticmethod
    def _check_required_fields(result: dict):
        for field in _REQUIRED_FIELDS:
            if field not in result:
                raise ERROR_REQUIRED_PARAMETER(key=field)

    @staticmethod
    def _make_additional_info(result: dict) -> dict:
        additional_info = {"Cluster": result["metric"]["cluster"]}

        try:
            # if result["metric"]["node"]:
            additional_info["Node"] = result["metric"]["node"]
        except KeyError:
            additional_info["Node"] = ""

        additional_info["Namespace"] = result["metric"]["namespace"]

        additional_info["Pod"] = result["metric"]["pod"]

        # additional_info["Type"] = result["metric"]["type"]

        return additional_info

    @staticmethod
    def _make_data(result: dict) -> dict:
        data = {"Change Percent": float(result.get("Change Percent", 0.0))}

        return data
