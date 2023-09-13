from parser.context_log_parser import ContextLogParser


class TmtHlrParser(ContextLogParser):

    def __init__(self, context_log: str, fields_to_return: list[str] | None) -> None:
        self.fields_to_return = fields_to_return
        super().__init__(context_log)

    def get_msisdn_from_raw_response(self) -> str:
        return list(self.raw_response.keys())[0]

    def get_raw_fields(self) -> dict[str, str | int]:
        msisdn = self.get_msisdn_from_raw_response()
        msisdn_info = self.raw_response[msisdn]
        if not self.fields_to_return:
            return msisdn_info
        filtered_raw_resp = {key: msisdn_info[key] for key in msisdn_info if key in self.fields_to_return}
        return filtered_raw_resp
