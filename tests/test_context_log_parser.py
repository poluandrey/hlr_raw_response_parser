import pytest

from hlr.parser.context_log_parser import (extruct_raw_response,
                                           get_nested_context_log,
                                           serialize_context_log)
from hlr.parser.errors import (ContextLogNotFoundError, InvalidContextLogError,
                               RawResponseNotFoundError)


def test__serialize_context_log__raise_error_when_empty_context_log_provided():
    with pytest.raises(ContextLogNotFoundError):
        serialize_context_log('')


def test__serialize_context_log__raise_error_when_not_json_context_log_provided(context_log_not_serializable_context_log):
    with pytest.raises(InvalidContextLogError):
        serialize_context_log(context_log_not_serializable_context_log)


def test__get_nested_context_log__return_nested_context_log(context_log_valid):
    context_log = serialize_context_log(context_log_valid)

    assert get_nested_context_log(context_log)


def test__get_nested_context_log__raise_error_if_context_log_not_presented(context_log_without_nested_context_log):
    context_log = serialize_context_log(context_log_without_nested_context_log)

    with pytest.raises(InvalidContextLogError):
        get_nested_context_log(context_log)


def test__extruct_raw_response__raise_error_when_raw_response_not_found(context_log_without_raw_response):
    context_log = serialize_context_log(context_log_without_raw_response)
    nested_context_log = get_nested_context_log(context_log)

    with pytest.raises(RawResponseNotFoundError):
        extruct_raw_response(nested_context_log)


def test__extruct_raw_response__return_raw_response(context_log_valid):
    context_log = serialize_context_log(context_log_valid)
    nested_context_log = get_nested_context_log(context_log)
    assert extruct_raw_response(nested_context_log)


def test__get_raw_response__raise_error_if_raw_response_is_not_serializable(context_log_not_serializable_raw_response):
    context_log = serialize_context_log(context_log_not_serializable_raw_response)
    nested_context_log = get_nested_context_log(context_log)
    with pytest.raises(RawResponseNotFoundError):
        extruct_raw_response(nested_context_log)
