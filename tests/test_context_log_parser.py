import pytest
from parser.context_log_parser import serialize_context_log, get_nested_context_log, get_raw_response
from parser.errors import InvalidContextLogError, RawResponseNotFoundError, \
    ContextLogNotFoundError


def test__serialize_context_log__raise_error_when_empty_context_log_provided():
    with pytest.raises(ContextLogNotFoundError):
        serialize_context_log('')


def test__serialize_context_log__raise_error_when_not_json_context_log_provided(not_serializable_context_log):
    with pytest.raises(InvalidContextLogError):
        serialize_context_log(not_serializable_context_log)


def test__get_nested_context_log__return_nested_context_log(valid_context_log):
    context_log = serialize_context_log(valid_context_log)

    assert get_nested_context_log(context_log)


def test__get_nested_context_log__raise_error_if_context_log_not_presented(context_log_without_nested_context_log):
    context_log = serialize_context_log(context_log_without_nested_context_log)

    with pytest.raises(InvalidContextLogError):
        get_nested_context_log(context_log)


def test__get_raw_response__raise_error_when_raw_response_not_found(context_log_without_raw_response):
    context_log = serialize_context_log(context_log_without_raw_response)
    nested_context_log = get_nested_context_log(context_log)

    with pytest.raises(RawResponseNotFoundError):
        get_raw_response(nested_context_log)


def test__get_record_with_raw_response__return_raw_response(valid_context_log):
    context_log = serialize_context_log(valid_context_log)
    nested_context_log = get_nested_context_log(context_log)
    assert get_raw_response(nested_context_log)


def test__get_raw_response__raise_error_if_raw_response_is_not_serializable(not_serializable_raw_response):
    context_log = serialize_context_log(not_serializable_raw_response)
    nested_context_log = get_nested_context_log(context_log)

    with pytest.raises(RawResponseNotFoundError):
        get_raw_response(nested_context_log)
