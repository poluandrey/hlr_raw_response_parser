import json
import re
from itertools import product
from typing import Any

from hlr.parser.errors import (ContextLogNotFoundError, InvalidContextLogError,
                               InvalidRawResponseError,
                               RawResponseNotFoundError)

RAW_RESPONSE_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r'.*first raw response: (\{.*\})', re.S),
    re.compile(r'.*cachedRawResponse: (\{.*\})', re.S),
    re.compile(r'.*cachedRawResponse: (\[\{.*\}\])', re.S),
    re.compile(r'.*cachedRawResponse: (\[\{.*\}\])', re.S),
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


def extruct_raw_response(nested_context_log: list[str]) -> str:
    for pattern, line in product(RAW_RESPONSE_PATTERNS, nested_context_log):
        match = re.match(pattern, line)
        if match:
            return match.group(1)

    raise RawResponseNotFoundError


def parse_context_log(context_log: str) -> dict[str, Any]:
    serialized_context_log = serialize_context_log(context_log)
    nested_context_log = get_nested_context_log(serialized_context_log)
    print(f'nested context log: {nested_context_log}')
    raw_response = extruct_raw_response(nested_context_log)
    print(raw_response)
    try:
        return json.loads(raw_response)
    except json.JSONDecodeError as error:
        raise InvalidRawResponseError from error
