import json
import re
from parser.errors import (ContextLogNotFoundError, InvalidContextLogError,
                           InvalidRawResponseError, RawResponseNotFoundError)
from typing import Any


RAW_RESPONSE_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r'.*first raw response: (\{.*\})', re.S),
    re.compile(r'.*cachedRawResponse: (\{.*\})', re.S),
]


def serialize_context_log(context_log: str) -> dict[str, Any]:
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


def is_raw_response(line: str) -> re.Match[str] | None:
    match = None
    for pattern in RAW_RESPONSE_PATTERNS:
        match = re.match(pattern, line)
        if match:
            break

    return match


def get_raw_response(nested_context_log: list[str]) -> str:
    for log_rec in nested_context_log:
        if match := is_raw_response(log_rec):
            return match.group(1)

    raise RawResponseNotFoundError


def parse_context_log(context_log: str) -> dict[str, Any]:
    serialized_context_log = serialize_context_log(context_log)
    nested_context_log = get_nested_context_log(serialized_context_log)
    raw_response = get_raw_response(nested_context_log)
    try:
        return json.loads(raw_response)
    except json.JSONDecodeError as error:
        raise InvalidRawResponseError from error
