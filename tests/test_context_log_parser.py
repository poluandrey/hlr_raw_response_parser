import pytest

from hlr.parser.context_log_parser import (extruct_raw_response,
                                           get_nested_context_log,
                                           serialize_context_log, parse_context_log)
from hlr.parser.errors import (ContextLogNotFoundError, InvalidContextLogError,
                               RawResponseNotFoundError, InvalidRawResponseError)


def test__serialize_context_log__raise_error_when_empty_context_log_provided():
    with pytest.raises(ContextLogNotFoundError):
        serialize_context_log('')


def test__serialize_context_log__raise_error_when_not_json_context_log_provided(make_context_log):
    with pytest.raises(InvalidContextLogError):
        serialize_context_log(make_context_log(not_serializable_context_log=True))


def test__get_nested_context_log__return_nested_context_log():
    assert get_nested_context_log({'contextLog': 'test'}) == 'test'


def test__get_nested_context_log__raise_error_when_key_not_found(faker):
    with pytest.raises(InvalidContextLogError):
        get_nested_context_log({faker.pystr(): faker.pystr()})


def test__get_nested_context_log__raise_error_if_context_log_not_presented(make_context_log):
    with pytest.raises(InvalidContextLogError):
        get_nested_context_log(make_context_log(without_nested_context_log=True))


def test__extruct_raw_response__raise_error_when_raw_response_not_found(make_context_log):
    with pytest.raises(RawResponseNotFoundError):
        extruct_raw_response(make_context_log(without_nested_context_log=True))


def test__parse_context_log__raise_error_if_raw_response_is_not_serializable(make_context_log):
    with pytest.raises(InvalidRawResponseError):
        parse_context_log(make_context_log(invalid_raw_response=True))
