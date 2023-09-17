import pytest
from parser.context_log_parser import serialize_context_log, get_nested_context_log, get_raw_response, get_record_with_raw_response
from parser.errors import InvalidContextLogError, RawResponseNotFoundError, InvalidRawResponseError

CONTEXT_LOG = '{"startTime":"2023-09-14 09:54:11","contextLog":["s:2023-09-14 09:54:11 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i: \\u003d79226503431. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i: \\u003d79226503431 prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i:Processing: 79226503431 HLR vendor: tmtlive cacheTtl: 14400","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i:Process request, source: tmtlive, dnis: 79226503431, cachedRawResponse: null","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i:request link1: https://api.tmtvelocity.com/live/json///[dnis]","s:2023-09-14 09:54:11 d:PT0.047S t:AsyncHttpClient-71-49 i:first raw response: {\\n  \\"79226503431\\": {\\n    \\"cic\\": \\"7643\\",\\n    \\"error\\": 191,\\n    \\"imsi\\": \\"25002XXXXXXXXXX\\",\\n    \\"mcc\\": \\"250\\",\\n    \\"mnc\\": \\"02\\",\\n    \\"network\\": \\"MegaFon pjsc\\",\\n    \\"number\\": 79226503431,\\n    \\"ported\\": false,\\n    \\"present\\": \\"na\\",\\n    \\"status\\": 0,\\n    \\"status_message\\": \\"Success\\",\\n    \\"type\\": \\"mobile\\",\\n    \\"trxid\\": \\"tp02NAX\\"\\n  }\\n}","s:2023-09-14 09:54:11 d:PT0.047S t:AsyncHttpClient-71-49 i:Caching raw response with cacheTtl: 14405","s:2023-09-14 09:54:11 d:PT0.047S t:AsyncHttpClient-71-49 i:Result is Ok, setCompleted","s:2023-09-14 09:54:11 d:PT0.048S t:AsyncHttpClient-71-49 i:Finishing"]}'
CONTEXT_LOG_NOT_SERIALIZABLE = '"startTime":"2023-09-12 20:52:24","contextLog":["s:2023-09-12 20:52:24 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i: \\u003d79216503431. prefix\\u003dnull process time sec.\\u003dPT-0.001S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i: \\u003d79216503431 prefix\\u003d79216503431 process time sec.\\u003dPT0S mccmnc\\u003d250001 fullMatched\\u003dtrue ownerID\\u003dmMTS providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Processing: 79216503431 HLR vendor: tmtlive cacheTtl: 14400","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Process request, source: tmtlive, dnis: 79216503431, cachedRawResponse: {\\n  \\"79216503431\\": {\\n    \\"cic\\": \\"7629\\",\\n    \\"error\\": 191,\\n    \\"imsi\\": \\"25001XXXXXXXXXX\\",\\n    \\"mcc\\": \\"250\\",\\n    \\"mnc\\": \\"01\\",\\n    \\"network\\": \\"Mobilnyye TeleSistemy pjsc (MTS)\\",\\n    \\"number\\": 79216503431,\\n    \\"ported\\": true,\\n    \\"present\\": \\"na\\",\\n    \\"status\\": 0,\\n    \\"status_message\\": \\"Success\\",\\n    \\"type\\": \\"mobile\\",\\n    \\"trxid\\": \\"dPgTp1Y\\"\\n  }\\n}","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Result is Ok, setCompleted","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Finishing"]}'
CONTEXT_WITH_INVALID_RAW_RESP_LOG = '{"startTime":"2023-09-12 20:52:24","contextLog":["s:2023-09-12 20:52:24 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i: \\u003d79216503431. prefix\\u003dnull process time sec.\\u003dPT-0.001S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i: \\u003d79216503431 prefix\\u003d79216503431 process time sec.\\u003dPT0S mccmnc\\u003d250001 fullMatched\\u003dtrue ownerID\\u003dmMTS providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Processing: 79216503431 HLR vendor: tmtlive cacheTtl: 14400","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Process request, source: tmtlive, dnis: 79216503431, cachedRawResponse: \\n  \\"79216503431\\": {\\n    \\"cic\\": \\"7629\\",\\n    \\"error\\": 191,\\n    \\"imsi\\": \\"25001XXXXXXXXXX\\",\\n    \\"mcc\\": \\"250\\",\\n    \\"mnc\\": \\"01\\",\\n    \\"network\\": \\"Mobilnyye TeleSistemy pjsc (MTS)\\",\\n    \\"number\\": 79216503431,\\n    \\"ported\\": true,\\n    \\"present\\": \\"na\\",\\n    \\"status\\": 0,\\n    \\"status_message\\": \\"Success\\",\\n    \\"type\\": \\"mobile\\",\\n    \\"trxid\\": \\"dPgTp1Y\\"\\n  }\\n}","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Result is Ok, setCompleted","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Finishing"]}'
CONTEXT_LOG_WITHOUT_RAW_RESPONSE_PATTERNS = '{"startTime":"2023-09-12 19:13:56","contextLog":["s:2023-09-12 19:13:56 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i: \\u003d79216503431. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i: \\u003d79216503431 prefix\\u003d79216503431 process time sec.\\u003dPT0S mccmnc\\u003d250001 fullMatched\\u003dtrue ownerID\\u003dmMTS providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i:Processing: 79216503431 HLR vendor: tmtlive cacheTtl: 14400","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i:Process request, source: tmtlive, dnis: 79216503431, cached: null","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i:request link1: https://api.tmtvelocity.com/live/json/ZspUQp2a4xYX7/Z7K4xEX5YwGD7v7/[dnis]","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:: {\\n  \\"79216503431\\": {\\n    \\"cic\\": \\"7629\\",\\n    \\"error\\": 191,\\n    \\"imsi\\": \\"25001XXXXXXXXXX\\",\\n    \\"mcc\\": \\"250\\",\\n    \\"mnc\\": \\"01\\",\\n    \\"network\\": \\"Mobilnyye TeleSistemy pjsc (MTS)\\",\\n    \\"number\\": 79216503431,\\n    \\"ported\\": true,\\n    \\"present\\": \\"na\\",\\n    \\"status\\": 0,\\n    \\"status_message\\": \\"Success\\",\\n    \\"type\\": \\"mobile\\",\\n    \\"trxid\\": \\"dPgTp1Y\\"\\n  }\\n}","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:Caching raw response with cacheTtl: 14405","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:Result is Ok, setCompleted","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:Finishing"]}'
CONTEXT_LOG_WITHOUT_NESTED_CONTEXT_LOG = '{"startTime":"2023-09-12 19:13:56","sameOtherKey":["s:2023-09-12 19:13:56 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i: \\u003d79216503431. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i: \\u003d79216503431 prefix\\u003d79216503431 process time sec.\\u003dPT0S mccmnc\\u003d250001 fullMatched\\u003dtrue ownerID\\u003dmMTS providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i:Processing: 79216503431 HLR vendor: tmtlive cacheTtl: 14400","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i:Process request, source: tmtlive, dnis: 79216503431, cachedRawResponse: null","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i:request link1: https://api.tmtvelocity.com/live/json/ZspUQp2a4xYX7/Z7K4xEX5YwGD7v7/[dnis]","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:first raw response: {\\n  \\"79216503431\\": {\\n    \\"cic\\": \\"7629\\",\\n    \\"error\\": 191,\\n    \\"imsi\\": \\"25001XXXXXXXXXX\\",\\n    \\"mcc\\": \\"250\\",\\n    \\"mnc\\": \\"01\\",\\n    \\"network\\": \\"Mobilnyye TeleSistemy pjsc (MTS)\\",\\n    \\"number\\": 79216503431,\\n    \\"ported\\": true,\\n    \\"present\\": \\"na\\",\\n    \\"status\\": 0,\\n    \\"status_message\\": \\"Success\\",\\n    \\"type\\": \\"mobile\\",\\n    \\"trxid\\": \\"dPgTp1Y\\"\\n  }\\n}","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:Caching raw response with cacheTtl: 14405","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:Result is Ok, setCompleted","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:Finishing"]}'


def test__serialize_context_log__raise_error_when_empty_context_log_provided():
    with pytest.raises(InvalidContextLogError):
        serialize_context_log('')


def test__serialize_context_log__raise_error_when_not_json_context_log_provided():
    with pytest.raises(InvalidContextLogError):
        serialize_context_log(CONTEXT_LOG_NOT_SERIALIZABLE)


def test__get_nested_context_log__return_nested_context_log():
    context_log = serialize_context_log(CONTEXT_LOG)

    assert get_nested_context_log(context_log)


def test__get_nested_context_log__raise_error_if_context_log_not_presented():
    context_log = serialize_context_log(CONTEXT_LOG_WITHOUT_NESTED_CONTEXT_LOG)

    with pytest.raises(InvalidContextLogError):
        get_nested_context_log(context_log)


def test__get_record_with_raw_response__raise_error_when_raw_response_not_found():
    context_log = serialize_context_log(CONTEXT_LOG_WITHOUT_RAW_RESPONSE_PATTERNS)
    nested_context_log = get_nested_context_log(context_log)

    with pytest.raises(RawResponseNotFoundError):
        get_record_with_raw_response(nested_context_log)


def test__get_record_with_raw_response__return_raw_response():
    context_log = serialize_context_log(CONTEXT_LOG)
    nested_context_log = get_nested_context_log(context_log)

    assert get_record_with_raw_response(nested_context_log)


def test__get_raw_response__return_raw_response():
    context_log = serialize_context_log(CONTEXT_LOG)
    nested_context_log = get_nested_context_log(context_log)
    raw_response_record = get_record_with_raw_response(nested_context_log)

    assert get_raw_response(raw_response_record)


def test__get_raw_response__raise_error_if_raw_response_is_not_serializable():
    context_log = serialize_context_log(CONTEXT_WITH_INVALID_RAW_RESP_LOG)
    nested_context_log = get_nested_context_log(context_log)
    raw_response_record = get_record_with_raw_response(nested_context_log)

    with pytest.raises(InvalidRawResponseError):
        get_raw_response(raw_response_record)

