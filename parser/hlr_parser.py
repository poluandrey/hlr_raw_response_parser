from typing import Any

from parser.context_log_parser import parse_context_log


def filter_by_flat_field(
        msisdn_info: dict,
        flat_fields: list[str]
) -> dict[str, Any]:
    return {key: msisdn_info[key] for key in msisdn_info if key in flat_fields}


def filter_by_nested_field(
        msisdn_info: dict,
        nested_fields: dict[str, list[str]]
) -> dict[str, Any]:
    filtered_msisdn_info: dict[str, dict] = {}
    for key, values in nested_fields.items():
        if key in msisdn_info.keys():
            for f in values:
                if key not in filtered_msisdn_info.keys():
                    filtered_msisdn_info[key] = {f: msisdn_info[key][f]}
                else:
                    filtered_msisdn_info[key][f] = msisdn_info[key][f]
    return filtered_msisdn_info


class TmtHlrParser:
    """
    raw response example
    {
    "79216503431": {
        "cic": "7629",
        "error": 191,
        "imsi": "25001XXXXXXXXXX",
        "mcc": "250",
        "mnc": "01",
        "network": "Mobilnyye TeleSistemy pjsc (MTS)",
        "number": 79216503431,
        "ported": true,
        "present": "na",
        "status": 0,
        "status_message": "Success",
        "type": "mobile",
        "trxid": "wRgugxm"
    }
    }
    """

    def __init__(self, context_log: str) -> None:
        self.raw_response = parse_context_log(context_log)

    def get_msisdn_from_raw_response(self) -> str:
        return list(self.raw_response.keys())[0]

    def get_raw_fields(
            self,
            fields_to_return: list[str] | None = None
    ) -> dict[str, str | int]:
        msisdn = self.get_msisdn_from_raw_response()
        msisdn_info = self.raw_response[msisdn]
        if not fields_to_return:
            return msisdn_info
        filtered_raw_resp = {key: msisdn_info[key] for key in msisdn_info
                             if key in fields_to_return
                             }
        return filtered_raw_resp


class InfobipHlrParser:
    """
    raw response example
    {"results": [
     {
       "to":"306980165782",
       "mccMnc":"20201",
       "imsi":"202010000000000",
       "originalNetwork":{
          "networkName":"Cosmote (Mobile Telecommunications S.A.)",
          "networkPrefix":"6980165",
          "countryName":"Greece",
          "countryPrefix":"30",
          "networkId":1560
       },
       "ported":false,
       "roaming":false,
       "status":{
          "groupId":3,
          "groupName":"DELIVERED",
          "id":5,
          "name":"DELIVERED_TO_HANDSET",
          "description":"Message delivered to handset"
       },
       "error":{
          "groupId":0,
          "groupName":"OK",
          "id":0,
          "name":"NO_ERROR",
          "description":"No Error",
          "permanent":false
       }
     }]}
    """

    def __init__(self, context_log: str) -> None:
        self.raw_response = parse_context_log(context_log)

    def retrieve_result(self) -> dict:
        return self.raw_response['results'][0]

    def get_raw_fields(
            self,
            fields_to_return: list[str | dict[str, list[str]]] | None = None
    ) -> dict[str, str | int]:
        msisdn_info = self.retrieve_result()
        if not fields_to_return:
            return msisdn_info

        filtered_fields = {}
        flat_fields = [field for field in fields_to_return
                       if isinstance(field, str)
                       ]
        if flat_fields:
            msisdn_info_filter_by_flat_fields = filter_by_flat_field(
                msisdn_info,
                flat_fields)
            filtered_fields.update(msisdn_info_filter_by_flat_fields)

        nested_fields = [field for field in fields_to_return
                         if isinstance(field, dict)
                         ]
        if nested_fields:
            msisdn_info_filter_by_nested_fields = filter_by_nested_field(
                msisdn_info,
                nested_fields[0]
            )
            filtered_fields.update(msisdn_info_filter_by_nested_fields)

        return filtered_fields


class XconnectParser:

    def __init__(self, context_log: str) -> None:
        self.raw_response = parse_context_log(context_log)

    def get_raw_fields(
            self,
            fields_to_return: list[str] | None = None
    ) -> dict:
        if not fields_to_return:
            return self.raw_response

        return {
            field: self.raw_response[field] for field in fields_to_return
            if field in list(self.raw_response.keys())
        }
