from parser.hlr_parser import TmtHlrParser, InfobipHlrParser, XconnectParser

TMT_HLR_ALL_RAW_FIELDS = ['cic',
                          'error',
                          'imsi',
                          'mcc',
                          'mnc',
                          'network',
                          'number',
                          'ported',
                          'present',
                          'status',
                          'status_message',
                          'type',
                          'trxid',
                          ]
TMT_CONTEXT_LOG = '{"startTime":"2023-09-14 09:54:11","contextLog":["s:2023-09-14 09:54:11 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i: \\u003d79226503431. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i: \\u003d79226503431 prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i:Processing: 79226503431 HLR vendor: tmtlive cacheTtl: 14400","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i:Process request, source: tmtlive, dnis: 79226503431, cachedRawResponse: null","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i:request link1: https://api.tmtvelocity.com/live/json///[dnis]","s:2023-09-14 09:54:11 d:PT0.047S t:AsyncHttpClient-71-49 i:first raw response: {\\n  \\"79226503431\\": {\\n    \\"cic\\": \\"7643\\",\\n    \\"error\\": 191,\\n    \\"imsi\\": \\"25002XXXXXXXXXX\\",\\n    \\"mcc\\": \\"250\\",\\n    \\"mnc\\": \\"02\\",\\n    \\"network\\": \\"MegaFon pjsc\\",\\n    \\"number\\": 79226503431,\\n    \\"ported\\": false,\\n    \\"present\\": \\"na\\",\\n    \\"status\\": 0,\\n    \\"status_message\\": \\"Success\\",\\n    \\"type\\": \\"mobile\\",\\n    \\"trxid\\": \\"tp02NAX\\"\\n  }\\n}","s:2023-09-14 09:54:11 d:PT0.047S t:AsyncHttpClient-71-49 i:Caching raw response with cacheTtl: 14405","s:2023-09-14 09:54:11 d:PT0.047S t:AsyncHttpClient-71-49 i:Result is Ok, setCompleted","s:2023-09-14 09:54:11 d:PT0.048S t:AsyncHttpClient-71-49 i:Finishing"]}'
TMT_CONTEXT_LOG_CACHED = '{"startTime":"2023-09-14 09:45:35","contextLog":["s:2023-09-14 09:45:35 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-14 09:45:35 d:PT0S t:HlrExecutor-pool-6-thread-55 i: \\u003d79216503431. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-14 09:45:35 d:PT0S t:HlrExecutor-pool-6-thread-55 i: \\u003d79216503431 prefix\\u003d79216503431 process time sec.\\u003dPT0S mccmnc\\u003d250001 fullMatched\\u003dtrue ownerID\\u003dmMTS providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-14 09:45:35 d:PT0S t:HlrExecutor-pool-6-thread-55 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-14 09:45:35 d:PT0S t:HlrExecutor-pool-6-thread-55 i:Processing: 79216503431 HLR vendor: tmtlive cacheTtl: 14400","s:2023-09-14 09:45:35 d:PT0S t:HlrExecutor-pool-6-thread-55 i:Process request, source: tmtlive, dnis: 79216503431, cachedRawResponse: {\\n  \\"79216503431\\": {\\n    \\"cic\\": \\"7629\\",\\n    \\"error\\": 191,\\n    \\"imsi\\": \\"25001XXXXXXXXXX\\",\\n    \\"mcc\\": \\"250\\",\\n    \\"mnc\\": \\"01\\",\\n    \\"network\\": \\"Mobilnyye TeleSistemy pjsc (MTS)\\",\\n    \\"number\\": 79216503431,\\n    \\"ported\\": true,\\n    \\"present\\": \\"na\\",\\n    \\"status\\": 0,\\n    \\"status_message\\": \\"Success\\",\\n    \\"type\\": \\"mobile\\",\\n    \\"trxid\\": \\"WIM9pHC\\"\\n  }\\n}","s:2023-09-14 09:45:35 d:PT0S t:HlrExecutor-pool-6-thread-55 i:Result is Ok, setCompleted","s:2023-09-14 09:45:35 d:PT0S t:HlrExecutor-pool-6-thread-55 i:Finishing"]}'

INFOBIP_HLR_ALL_RAW_FIELDS = [
    'to',
    'originalNetwork',
    'roaming',
    'status',
    'error',
]
INFOBIP_CONTEXT_LOG = '{"startTime":"2023-09-14 11:58:10","contextLog":["s:2023-09-14 11:58:10 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-14 11:58:10 d:PT0S t:HlrExecutor-pool-6-thread-112 i: \\u003d792165034312. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-14 11:58:10 d:PT0S t:HlrExecutor-pool-6-thread-112 i: \\u003d792165034312 prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-14 11:58:10 d:PT0S t:HlrExecutor-pool-6-thread-112 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-14 11:58:10 d:PT0S t:HlrExecutor-pool-6-thread-112 i:Processing: 792165034312 HLR vendor: infobip cacheTtl: 14400","s:2023-09-14 11:58:10 d:PT0S t:HlrExecutor-pool-6-thread-112 i:Process request, source: infobip, dnis: 792165034312, cachedRawResponse: null","s:2023-09-14 11:58:10 d:PT0S t:HlrExecutor-pool-6-thread-112 i:request link1: https://api.infobip.com/number/1/query","s:2023-09-14 11:58:10 d:PT0.055S t:AsyncHttpClient-75-21 i:first raw response: {\\"results\\":[{\\"to\\":\\"792165034312\\",\\"originalNetwork\\":{},\\"roaming\\":false,\\"status\\":{\\"groupId\\":5,\\"groupName\\":\\"REJECTED\\",\\"id\\":52,\\"name\\":\\"REJECTED_DESTINATION\\",\\"description\\":\\"Invalid destination address.\\",\\"action\\":\\"Check to parameter.\\"},\\"error\\":{\\"groupId\\":0,\\"groupName\\":\\"OK\\",\\"id\\":0,\\"name\\":\\"NO_ERROR\\",\\"description\\":\\"No Error\\",\\"permanent\\":false}}]}","s:2023-09-14 11:58:10 d:PT0.056S t:AsyncHttpClient-75-21 i:Caching raw response with cacheTtl: 10","s:2023-09-14 11:58:10 d:PT0.056S t:AsyncHttpClient-75-21 i:Result is not Ok, try to request other vendors","s:2023-09-14 11:58:10 d:PT0.056S t:AsyncHttpClient-75-21 i:Finishing"]}'
INFOBIP_CONTEXT_LOG_CACHED = '{"startTime":"2023-09-15 12:08:25","contextLog":["s:2023-09-15 12:08:25 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-15 12:08:25 d:PT0S t:HlrExecutor-pool-6-thread-69 i: \\u003d792165034312. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-15 12:08:25 d:PT0S t:HlrExecutor-pool-6-thread-69 i: \\u003d792165034312 prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-15 12:08:25 d:PT0S t:HlrExecutor-pool-6-thread-69 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-15 12:08:25 d:PT0S t:HlrExecutor-pool-6-thread-69 i:Processing: 792165034312 HLR vendor: infobip cacheTtl: 14400","s:2023-09-15 12:08:25 d:PT0S t:HlrExecutor-pool-6-thread-69 i:Process request, source: infobip, dnis: 792165034312, cachedRawResponse: {\\"results\\":[{\\"to\\":\\"792165034312\\",\\"originalNetwork\\":{},\\"roaming\\":false,\\"status\\":{\\"groupId\\":5,\\"groupName\\":\\"REJECTED\\",\\"id\\":52,\\"name\\":\\"REJECTED_DESTINATION\\",\\"description\\":\\"Invalid destination address.\\",\\"action\\":\\"Check to parameter.\\"},\\"error\\":{\\"groupId\\":0,\\"groupName\\":\\"OK\\",\\"id\\":0,\\"name\\":\\"NO_ERROR\\",\\"description\\":\\"No Error\\",\\"permanent\\":false}}]}","s:2023-09-15 12:08:25 d:PT0S t:HlrExecutor-pool-6-thread-69 i:Result is not Ok, try to request other vendors","s:2023-09-15 12:08:25 d:PT0S t:HlrExecutor-pool-6-thread-69 i:Finishing"]}'


XCONNECT_HLR_ALL_RAW_FIELDS = ['tn', 'cc', 'mcc', 'mnc', 'npdi', 'npi', 'nt', 'nv', 'ns', 'rc']
XCONNECT_CONTEXT_LOG = '{"startTime":"2023-09-15 09:51:01","contextLog":["s:2023-09-15 09:51:01 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-15 09:51:01 d:PT0S t:HlrExecutor-pool-6-thread-29 i: \\u003d79216503431. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-15 09:51:01 d:PT0S t:HlrExecutor-pool-6-thread-29 i: \\u003d79216503431 prefix\\u003d79216503431 process time sec.\\u003dPT0S mccmnc\\u003d250001 fullMatched\\u003dtrue ownerID\\u003dmMTS providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-15 09:51:01 d:PT0S t:HlrExecutor-pool-6-thread-29 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-15 09:51:01 d:PT0S t:HlrExecutor-pool-6-thread-29 i:Processing: 79216503431 HLR vendor: xconnect cacheTtl: 3600","s:2023-09-15 09:51:01 d:PT0.001S t:HlrExecutor-pool-6-thread-29 i:Process request, source: xconnect, dnis: 79216503431, cachedRawResponse: null","s:2023-09-15 09:51:02 d:PT0.985S t:HlrExecutor-pool-6-thread-29 i:first raw response: {\\"tn\\": \\"79216503431\\", \\"cc\\": \\"RU\\", \\"mcc\\": \\"250\\", \\"mnc\\": \\"01\\", \\"npdi\\": true, \\"npi\\": true, \\"nt\\": \\"wireless\\", \\"nv\\": \\"000\\", \\"ns\\": \\"000\\", \\"rc\\": \\"000\\"}","s:2023-09-15 09:51:02 d:PT0.985S t:HlrExecutor-pool-6-thread-29 i:Caching raw response with cacheTtl: 3605","s:2023-09-15 09:51:02 d:PT0.985S t:HlrExecutor-pool-6-thread-29 i:Result is Ok, setCompleted","s:2023-09-15 09:51:02 d:PT0.986S t:HlrExecutor-pool-6-thread-29 i:Finishing"]}'
XCONNECT_CONTEXT_LOG_CACHED = '{"startTime":"2023-09-15 09:40:17","contextLog":["s:2023-09-15 09:40:17 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-15 09:40:17 d:PT0S t:HlrExecutor-pool-6-thread-4 i: \\u003d306980165782. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-15 09:40:17 d:PT0.001S t:HlrExecutor-pool-6-thread-4 i: \\u003d306980165782 prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-15 09:40:17 d:PT0.001S t:HlrExecutor-pool-6-thread-4 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-15 09:40:17 d:PT0.001S t:HlrExecutor-pool-6-thread-4 i:Processing: 306980165782 HLR vendor: xconnect cacheTtl: 3600","s:2023-09-15 09:40:17 d:PT0.001S t:HlrExecutor-pool-6-thread-4 i:Process request, source: xconnect, dnis: 306980165782, cachedRawResponse: {\\"tn\\": \\"306980165782\\", \\"cc\\": \\"GR\\", \\"mcc\\": \\"202\\", \\"mnc\\": \\"01\\", \\"npdi\\": true, \\"npi\\": false, \\"nt\\": \\"wireless\\", \\"nv\\": \\"000\\", \\"ns\\": \\"000\\", \\"rc\\": \\"000\\"}","s:2023-09-15 09:40:17 d:PT0.001S t:HlrExecutor-pool-6-thread-4 i:Result is Ok, setCompleted","s:2023-09-15 09:40:17 d:PT0.001S t:HlrExecutor-pool-6-thread-4 i:Finishing"]}'


def test__TmtHlrParser__return_all_fields():
    parser = TmtHlrParser(TMT_CONTEXT_LOG)

    assert TMT_HLR_ALL_RAW_FIELDS == list(parser.get_raw_fields().keys())


def test__TmtHlrParser__return_all_fields_for_cached_response():
    parser = TmtHlrParser(TMT_CONTEXT_LOG_CACHED)

    assert TMT_HLR_ALL_RAW_FIELDS == list(parser.get_raw_fields().keys())


def test__TmtHlrParser__return_specified_fields():
    filters = ['present', 'status']

    parser = TmtHlrParser(TMT_CONTEXT_LOG)

    assert list(parser.get_raw_fields(filters).keys()) == filters


def test__TmtHlrParser__return_specified_fields_for_cached_response():
    filters = ['present', 'status']

    parser = TmtHlrParser(TMT_CONTEXT_LOG_CACHED)

    assert list(parser.get_raw_fields(filters).keys()) == filters


def test__InfobipHlrParser__return_all_fields():
    parser = InfobipHlrParser(INFOBIP_CONTEXT_LOG)

    assert list(parser.get_raw_fields().keys()) == INFOBIP_HLR_ALL_RAW_FIELDS


def test__InfobipHlrParser__return_all_fields_for_cached_response():
    parser = InfobipHlrParser(INFOBIP_CONTEXT_LOG_CACHED)

    assert list(parser.get_raw_fields().keys()) == INFOBIP_HLR_ALL_RAW_FIELDS


def test__InfobipHlrParser__return_specified_fields_filtered_by_flat_filter():
    filters = ['to', 'roaming']

    parser = InfobipHlrParser(INFOBIP_CONTEXT_LOG)

    assert list(parser.get_raw_fields(filters).keys()) == filters


def test__InfobipHlrParser__return_specified_fields_filtered_by_flat_filter_for_cached_response():
    filters = ['to', 'roaming']

    parser = InfobipHlrParser(INFOBIP_CONTEXT_LOG_CACHED)

    assert list(parser.get_raw_fields(filters).keys()) == filters


def test__InfobipHlrParser__return_specified_fields_filtered_by_nested_filter():
    expected_fields = ['groupId', 'groupName']

    filters = [{'status': ['groupId', 'groupName']}]
    parser = InfobipHlrParser(INFOBIP_CONTEXT_LOG)

    assert list(parser.get_raw_fields(filters)['status']) == expected_fields


def test__InfobipHlrParser__return_specified_fields_filtered_by_nested_filter_for_cached_response():
    expected_fields = ['groupId', 'groupName']

    filters = [{'status': ['groupId', 'groupName']}]
    parser = InfobipHlrParser(INFOBIP_CONTEXT_LOG_CACHED)

    assert list(parser.get_raw_fields(filters)['status']) == expected_fields


def test__XconnectHlrParser__return_all_fields():
    parser = XconnectParser(XCONNECT_CONTEXT_LOG)

    assert list(parser.get_raw_fields().keys()) == XCONNECT_HLR_ALL_RAW_FIELDS


def test__XconnectHlrParser__return_all_fields_for_cached_response():
    parser = XconnectParser(XCONNECT_CONTEXT_LOG_CACHED)

    assert list(parser.get_raw_fields().keys()) == XCONNECT_HLR_ALL_RAW_FIELDS


def test__XconnectHlrParser__return_specified_fields():
    filters = ['tn', 'cc']
    parser = XconnectParser(XCONNECT_CONTEXT_LOG)

    assert list(parser.get_raw_fields(filters).keys()) == filters


def test__XconnectHlrParser__return_specified_fields_for_cached_response():
    filters = ['tn', 'cc']

    parser = XconnectParser(XCONNECT_CONTEXT_LOG_CACHED)

    assert list(parser.get_raw_fields(filters).keys()) == filters

