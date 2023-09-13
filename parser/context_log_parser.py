"""на вход передается context_log на выходе RawResponse или cachedRawResponse"""
import json

RAW_RESPONSE_PATTERNS: list[str] = ['cachedRawResponse', 'first raw response']


class InvalidContextLog(Exception):
    pass


class LogStringWithRawRespNotExists(Exception):
    pass


class InvalidRawResponse(Exception):
    pass


class ContextLogParser:
    """принимает на вход строку с ответом от HLR и достает из нее  ответ провайдера"""

    def __init__(self, context_log: str) -> None:
        if not len(context_log):
            raise ValueError('empty context_log')
        try:
            self.context_log = json.loads(context_log)
        except json.JSONDecodeError:
            raise InvalidContextLog

        try:
            self.raw_response = json.loads(self.get_raw_response())
        except json.JSONDecodeError:
            raise InvalidRawResponse

    def get_nested_context_log(self) -> list[str]:
        try:
            return self.context_log['contextLog']
        except KeyError:
            raise KeyError('context log did not contain nested context log')

    def get_string_with_raw_response(self, nested_context_log: list[str]) -> str:
        for log_string in nested_context_log:
            for pattern in RAW_RESPONSE_PATTERNS:
                if pattern in log_string:
                    return log_string
        raise LogStringWithRawRespNotExists

    def get_raw_response(self) -> str:
        nested_context_log = self.get_nested_context_log()
        raw_string_response = self.get_string_with_raw_response(nested_context_log)
        first_brace_index = raw_string_response.find('{')
        last_brace_index = raw_string_response.rfind('}')
        raw_resp = raw_string_response[first_brace_index:last_brace_index + 1]
        return raw_resp
