"""на вход передается context_log на выходе RawResponse или cachedRawResponse"""
import json

from parser.errors import InvalidContextLogError, RawResponseNotFoundError, InvalidRawResponseError


RAW_RESPONSE_PATTERNS: list[str] = [
    'first raw response', 'cachedRawResponse',
]


def serialize_context_log(context_log: str):
    if not context_log:
        raise InvalidContextLogError
    try:
        return json.loads(context_log)
    except json.JSONDecodeError as error:
        raise InvalidContextLogError(error) from None


def get_nested_context_log(context_log: dict) -> list[str]:
    try:
        return context_log['contextLog']
    except KeyError as error:
        raise InvalidContextLogError(error) from None


def get_record_with_raw_response(nested_context_log: list[str]) -> str:
    for patterns in RAW_RESPONSE_PATTERNS:
        for log_string in nested_context_log:
            if patterns in log_string:
                return log_string
    raise RawResponseNotFoundError


def get_raw_response(raw_response_record: str) -> str:
    first_brace_index = raw_response_record.find('{')
    last_brace_index = raw_response_record.rfind('}')
    raw_response = raw_response_record[first_brace_index:last_brace_index + 1]
    try:
        return json.loads(raw_response)
    except json.JSONDecodeError as error:
        raise InvalidRawResponseError(error) from None


# class ContextLogParser:
#     """принимает на вход строку с ответом от HLR и достает из нее  ответ провайдера"""
#
#     def __init__(self, context_log: str) -> None:
#         if not context_log:
#             raise ValueError('empty context_log')
#         try:
#             self.context_log = json.loads(context_log)
#         except json.JSONDecodeError as error:
#             raise InvalidContextLogError(error) from None
#
#         try:
#             self.raw_response = json.loads(self.get_raw_response())
#         except json.JSONDecodeError as error:
#             raise InvalidRawResponseError(error) from None
#
#     def get_nested_context_log(self) -> list[str]:
#         try:
#             return self.context_log['contextLog']
#         except KeyError:
#             raise KeyError('context log did not contain nested context log')
#
#     def get_string_with_raw_response(self, nested_context_log: list[str]) -> str:
#         for patterns in RAW_RESPONSE_PATTERNS:
#             for log_string in nested_context_log:
#                 if patterns in log_string:
#                     return log_string
#         raise RawResponseNotFoundError
#
#     def get_raw_response(self) -> str:
#         nested_context_log = self.get_nested_context_log()
#         raw_string_response = self.get_string_with_raw_response(nested_context_log)
#         first_brace_index = raw_string_response.find('{')
#         last_brace_index = raw_string_response.rfind('}')
#         raw_resp = raw_string_response[first_brace_index:last_brace_index + 1]
#         return raw_resp
