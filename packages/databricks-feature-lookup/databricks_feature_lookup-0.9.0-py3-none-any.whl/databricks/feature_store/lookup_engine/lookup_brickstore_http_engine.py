import json
import threading
import time
from collections import defaultdict
from typing import Any, Dict, List, Tuple, Union

import pandas as pd
import requests

from databricks.feature_store.lookup_engine.lookup_engine import LookupEngine
from databricks.feature_store.utils.brickstore_http_type_utils import (
    BRICKSTORE_HTTP_DATA_TYPE_CONVERTER_FACTORY,
)
from databricks.feature_store.utils.brickstore_http_utils import (
    BRICKSTORE_OAUTH_TOKEN_FILE_PATH,
)
from databricks.feature_store.utils.metrics_utils import LookupClientMetrics
from databricks.ml_features_common.entities.online_feature_table import (
    OnlineFeatureTable,
)

LookupKeyType = Tuple[str, ...]

# Token should be updated every 30 mins by serving scheduler.
# Implement more frequent refresh for safety.
_TOKEN_REFRESH_DURATION_SECONDS = 5 * 60


class LookupBrickstoreHttpEngine(LookupEngine):
    """
    Read online features from Brickstore by making requests aginst the HTTP gateway.
    """

    def _refresh_oauth_token(self, is_retry=False):
        """
        Periodically refresh from mounted secret file. Upstream validation ensures this path
        should exist.
        """
        should_retry = False
        with open(BRICKSTORE_OAUTH_TOKEN_FILE_PATH, "r") as f:
            json_data = f.read()
            try:
                oauth_dict = json.loads(json_data)
                ret_val = oauth_dict["OAUTH_TOKEN"][0]["oauthTokenValue"]
                self._oauth_token = ret_val
            except Exception:
                # Remediation for potential race condition in which the read occurs
                # simultaneously with the secret mount update, resulting in a malformed
                # token
                if is_retry:
                    raise Exception("Invalid online store credential configuration.")
                else:
                    should_retry = True
        if should_retry:
            self._refresh_oauth_token(is_retry=True)

    def _refresh_oauth_token_loop(self):
        """
        Periodically refresh from mounted secret file. Upstream validation ensures this path
        should exist.
        """
        while self._run_token_refresh_thread:
            time.sleep(_TOKEN_REFRESH_DURATION_SECONDS)
            self._refresh_oauth_token()

    def _get_oauth_token(self):
        if self._oauth_token == "":
            self._refresh_oauth_token()
        return self._oauth_token

    def __init__(
        self,
        online_feature_tables: Union[OnlineFeatureTable, List[OnlineFeatureTable]],
    ):
        # Table serving URL will be the same for all tables, so we can read the first.
        # Consistency is enforced by the control plane.
        if isinstance(online_feature_tables, OnlineFeatureTable):
            online_feature_tables = [online_feature_tables]

        self._table_serving_url = online_feature_tables[
            0
        ].online_store.extra_configs.table_serving_url

        self._refresh_oauth_token()
        self._run_token_refresh_thread = True

        background_thread = threading.Thread(target=self._refresh_oauth_token_loop)
        background_thread.daemon = True
        background_thread.start()

        self._columns_to_type_converter_map = {
            oft.online_feature_table_name: {
                col.name: BRICKSTORE_HTTP_DATA_TYPE_CONVERTER_FACTORY.get_converter(col)
                for col in oft.primary_keys + oft.features
            }
            for oft in online_feature_tables
        }

    def _pandas_to_json_input_df(
        self, feature_table_name: str, row: pd.core.series.Series
    ) -> List[Any]:
        """
        Converts the input Pandas row to JSON inputs
        """
        dic = {
            col_name: self._columns_to_type_converter_map[feature_table_name][
                col_name
            ].to_online_store(col_value)
            for col_name, col_value in row.items()
        }
        return pd.Series(dic)

    def _raw_response_df_to_typed_df(
        self, feature_table_name: str, row: pd.core.series.Series
    ) -> List[Any]:
        """
        Converts the input results list with dynamodb-compatible python values to pandas types based on
        the input features_names and features converter.
        :return:List[Any]
        """
        dic = {
            feature_name: self._columns_to_type_converter_map[feature_table_name][
                feature_name
            ].to_pandas(feature_value)
            for feature_name, feature_value in row.items()
        }
        return pd.Series(dic)

    def _lookup_df_dict_to_request_json(
        self,
        lookup_df_dict: Dict[str, Dict[LookupKeyType, pd.DataFrame]],
        feature_names_dict: Dict[str, Dict[LookupKeyType, List[str]]],
    ):
        tables_dict = {}

        for oft_name, lookup_to_pk_values_dict in lookup_df_dict.items():
            selected_features_for_table = set()
            pk_input_values_for_table = []

            def convert_fn(row):
                return self._pandas_to_json_input_df(oft_name, row)

            for lookup_key, pk_df in lookup_to_pk_values_dict.items():
                features_for_this_lookup_key = feature_names_dict[oft_name][lookup_key]
                # Always want to look up PKs.
                selected_features_for_table.update(list(pk_df.columns))
                selected_features_for_table.update(features_for_this_lookup_key)

                converted_df = pk_df.apply(convert_fn, axis=1, result_type="expand")

                lookup_dict = converted_df.to_dict(orient="records")
                pk_input_values_for_table += lookup_dict

            table_dict = {
                "keys": pk_input_values_for_table,
                "select": list(selected_features_for_table),
            }

            tables_dict[oft_name] = table_dict
        return tables_dict

    def _response_to_looked_up_df_dict(
        self,
        lookup_df_dict: Dict[str, Dict[LookupKeyType, pd.DataFrame]],
        feature_names_dict: Dict[str, Dict[LookupKeyType, List[str]]],
        results: Dict,
    ):
        result_dict = defaultdict(lambda: defaultdict(list))

        for oft_name, table_results_dict in results.items():
            if "rows" not in table_results_dict:
                table_results_dict["rows"] = []
            looked_up_data = enumerate(table_results_dict["rows"])
            col_infos = table_results_dict["schema"]["columns"]

            def convert_fn(row):
                return self._raw_response_df_to_typed_df(oft_name, row)

            # Turn the result set into a dataframe to make it easier to query.
            looked_up_data_df = pd.DataFrame.from_dict(
                data={i: data_row for i, data_row in looked_up_data},
                orient="index",
                columns=[col_info["name"] for col_info in col_infos],
            )
            converted_looked_up_df = looked_up_data_df.apply(
                convert_fn, axis=1, result_type="expand"
            )

            looup_key_to_input_pk_df_dict = lookup_df_dict[oft_name]
            for lookup_key, input_pks_df in looup_key_to_input_pk_df_dict.items():
                # Input pks df is raw input from user, so we need to convert it to same types
                # as converted looked up df for merge to work.
                converted_input_df = input_pks_df.apply(
                    convert_fn, axis=1, result_type="expand"
                )
                feat_names_to_look_up = feature_names_dict[oft_name][lookup_key]
                pk_cols = list(converted_input_df.columns)
                filtered_df = pd.merge(
                    converted_looked_up_df, converted_input_df, how="right", on=pk_cols
                )[feat_names_to_look_up]
                result_dict[oft_name][lookup_key] = filtered_df

        return {k: dict(v) for k, v in result_dict.items()}

    def _lookup_and_aggregate_features(self, requested_table_info_dict):
        """
        Send lookup request. If the response contains a page token,
        send requests until there is no page token and aggregate responses.
        """

        def _send_req(page_token=None, is_retry=False):
            headers = {"Authorization": f"Bearer {self._get_oauth_token()}".strip()}
            req_json = {
                "tables": requested_table_info_dict,
            }
            if page_token is not None:
                req_json["page_token"] = page_token
            response = requests.post(
                self._table_serving_url, json=req_json, headers=headers
            )
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                if is_retry:
                    raise Exception(f"Expired token: {response.text}")
                else:
                    self._refresh_oauth_token()
                    return _send_req(page_token, is_retry=True)
            else:
                raise Exception(response.text)

        resp = _send_req()
        if "results" in resp:
            aggregated_table_info = resp["results"]
        else:
            raise Exception(
                "No online feature information found. Ensure all feature tables are synchronized to an online store."
            )
        while "next_page_token" in resp:
            resp = _send_req(resp["next_page_token"])
            for table, table_info in resp["results"].items():
                if table not in aggregated_table_info:
                    aggregated_table_info[table] = resp["results"][table]
                else:
                    aggregated_table_info[table]["rows"] += table_info["rows"]

        return aggregated_table_info

    def batch_lookup_features(
        self,
        lookup_df_dict: Dict[str, Dict[LookupKeyType, pd.DataFrame]],
        feature_names_dict: Dict[str, Dict[LookupKeyType, List[str]]],
        *,
        metrics: LookupClientMetrics = None,
    ) -> Dict[str, Dict[LookupKeyType, pd.DataFrame]]:
        """
        Assume the following lookup_df_dict:
        { table_a: {
          ("my_name",): pd.DataFrame("name_pk": ["x1", "x2"]),
          ("friend_name",): pd.DataFrame("name_pk": ["y1", "y2"])
        }}

        We need to turn into this request JSON:
        {
            "tables": {
                "catalog.schema.table_a": {
                    "keys": [
                        {"name_pk": "x1"},
                        {"name_pk": "y1"},
                        {"name_pk": "x2"},
                        {"name_pk": "y2"}
                    ],
                    "select": ["phone_number", "address"]
                }
            }
        }

        Assuming this provides the response:
        {
            "results": {
                "catalog.schema.table_a": {
                    "schema": {
                        "columns": [
                            {"name": "name", "type_name": "STRING", "nullable": false},
                            {"name": "phone_number", "type_name": "STRING", "nullable": false},
                            {"name": "address", "type_name": "STRING", "nullable": true}
                        ]
                    },
                    "rows": [
                        ["x1", "123", "abc"],
                        ["y1", "456", "def"],
                        ["x2", "789", "ghi"],
                        ["y2", "000", "jkl"],
                    ]
                },
            },
            "next_page_token": "Y2F0YWxvZy5zY2hlbWEudGFibGUyOjE="
        }

        We then need to turn into this map:
        {
            "table_a": {
                ("my_name",): pd.DataFrame({"phone_number": [123, 789]),
                ("your_name",): pd.DataFrame({"address": [def, jkl})
            }
        }

        """
        tables_info = self._lookup_df_dict_to_request_json(
            lookup_df_dict, feature_names_dict
        )
        looked_up_features = self._lookup_and_aggregate_features(tables_info)
        return self._response_to_looked_up_df_dict(
            lookup_df_dict, feature_names_dict, looked_up_features
        )

    def lookup_features(
        self,
        lookup_df: pd.DataFrame,
        feature_names: List[str],
        *,
        metrics: LookupClientMetrics = None,
    ) -> pd.DataFrame:
        raise NotImplementedError

    def shutdown(self) -> None:
        self._run_token_refresh_thread = False
