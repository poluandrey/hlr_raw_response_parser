"""на вход передается context_log на выходе RawResponse или cachedRawResponse"""
import re
import json

RAW_RESPONSE_PATTERNS: list[str] = ['cachedRawResponse', 'first raw response']


class LogStringWithRawRespNotExists(Exception):
    pass


class RawResponseNotFound(Exception):
    pass


class ContextLogParser:
    regular_exp = r'\{([^}]*)\}'

    def __init__(self, context_log: str) -> None:
        if not len(context_log):
            raise ValueError('empty context_log')
        self.context_log = json.loads(context_log)
        self.nested_context_log = self.get_nested_context_log()
        self.raw_response_string = self.get_string_with_raw_response()
        self.raw_response = self.get_raw_response()

    def get_nested_context_log(self) -> list[str]:
        try:
            return self.context_log['contextLog']
        except KeyError:
            raise KeyError('context log did not contain nested context log')

    def get_string_with_raw_response(self) -> str | None:
        for log_string in self.nested_context_log:
            for pattern in RAW_RESPONSE_PATTERNS:
                if pattern in log_string:
                    return log_string
        raise LogStringWithRawRespNotExists

    def get_raw_response(self):
        print(self.raw_response_string)
        matches = re.findall(self.regular_exp, self.raw_response_string)
        if matches:
            return '{' + matches[0] + '}'
        raise RawResponseNotFound
