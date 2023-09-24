import json
import re
from parser.errors import (ContextLogNotFoundError, InvalidContextLogError,
                           InvalidRawResponseError, RawResponseNotFoundError)
from parser.types import Json
from typing import Any

RAW_RESPONSE_PATTERNS: list[str] = [
    r'.*first raw response: (\{.*\})', r'.*cachedRawResponse: (\{.*\})',
]


def serialize_context_log(context_log: str):
    if not context_log:
        raise ContextLogNotFoundError

    try:
        return json.loads(context_log)
    except json.JSONDecodeError as error:
        raise InvalidContextLogError from error


def get_nested_context_log(context_log: dict[str, Any]) -> list[str]:
    nested_context_log = context_log.get('contextLog')

    if not nested_context_log:
        raise InvalidContextLogError('Nested context log not found')

    return nested_context_log


def contain_raw_response(line: str) -> bool:
    for pattern in RAW_RESPONSE_PATTERNS:

        if re.match(pattern, line.replace('\n', '')):
            return True

    return False


def get_record_with_raw_response(nested_context_log: list[str]) -> str:
    raw_response_lines = list(filter(contain_raw_response, nested_context_log))
    if not raw_response_lines:
        raise RawResponseNotFoundError

    return raw_response_lines[0]


def get_raw_response(raw_response_record: str) -> dict[str, Any]:
    first_brace_index = raw_response_record.find('{')
    last_brace_index = raw_response_record.rfind('}')
    raw_response = raw_response_record[first_brace_index:last_brace_index + 1]

    try:
        return json.loads(raw_response)
    except json.JSONDecodeError as error:
        raise InvalidRawResponseError(error) from error


def parse_context_log(context_log: str) -> dict[str, Any]:
    serialized_context_log = serialize_context_log(context_log)
    nested_context_log = get_nested_context_log(serialized_context_log)
    record_with_raw_response = get_record_with_raw_response(nested_context_log)
    return get_raw_response(record_with_raw_response)
