from parser.hlr_parser import TmtHlrParser

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
TMT_CONTEXT_LOG = '{"startTime":"2023-09-12 20:52:24","contextLog":["s:2023-09-12 20:52:24 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i: \\u003d79216503431. prefix\\u003dnull process time sec.\\u003dPT-0.001S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i: \\u003d79216503431 prefix\\u003d79216503431 process time sec.\\u003dPT0S mccmnc\\u003d250001 fullMatched\\u003dtrue ownerID\\u003dmMTS providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Processing: 79216503431 HLR vendor: tmtlive cacheTtl: 14400","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Process request, source: tmtlive, dnis: 79216503431, cachedRawResponse: {\\n  \\"79216503431\\": {\\n    \\"cic\\": \\"7629\\",\\n    \\"error\\": 191,\\n    \\"imsi\\": \\"25001XXXXXXXXXX\\",\\n    \\"mcc\\": \\"250\\",\\n    \\"mnc\\": \\"01\\",\\n    \\"network\\": \\"Mobilnyye TeleSistemy pjsc (MTS)\\",\\n    \\"number\\": 79216503431,\\n    \\"ported\\": true,\\n    \\"present\\": \\"na\\",\\n    \\"status\\": 0,\\n    \\"status_message\\": \\"Success\\",\\n    \\"type\\": \\"mobile\\",\\n    \\"trxid\\": \\"dPgTp1Y\\"\\n  }\\n}","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Result is Ok, setCompleted","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Finishing"]}'
TMT_CONTEXT_LOG_CACHED = '{"startTime":"2023-09-13 19:27:39","contextLog":["s:2023-09-13 19:27:39 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-13 19:27:39 d:PT0S t:HlrExecutor-pool-6-thread-53 i: \\u003d79216503621. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-13 19:27:39 d:PT0.001S t:HlrExecutor-pool-6-thread-53 i: \\u003d79216503621 prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-13 19:27:39 d:PT0.001S t:HlrExecutor-pool-6-thread-53 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-13 19:27:39 d:PT0.001S t:HlrExecutor-pool-6-thread-53 i:Processing: 79216503621 HLR vendor: tmtlive cacheTtl: 14400","s:2023-09-13 19:27:39 d:PT0.001S t:HlrExecutor-pool-6-thread-53 i:Process request, source: tmtlive, dnis: 79216503621, cachedRawResponse: {\\n  \\"79216503621\\": {\\n    \\"cic\\": \\"7643\\",\\n    \\"error\\": 191,\\n    \\"imsi\\": \\"25002XXXXXXXXXX\\",\\n    \\"mcc\\": \\"250\\",\\n    \\"mnc\\": \\"02\\",\\n    \\"network\\": \\"MegaFon pjsc\\",\\n    \\"number\\": 79216503621,\\n    \\"ported\\": false,\\n    \\"present\\": \\"na\\",\\n    \\"status\\": 0,\\n    \\"status_message\\": \\"Success\\",\\n    \\"type\\": \\"mobile\\",\\n    \\"trxid\\": \\"pxg1Ef7\\"\\n  }\\n}","s:2023-09-13 19:27:39 d:PT0.001S t:HlrExecutor-pool-6-thread-53 i:Result is Ok, setCompleted","s:2023-09-13 19:27:39 d:PT0.001S t:HlrExecutor-pool-6-thread-53 i:Finishing"]}'


def test_TmtHlrParser__return_all_fields():
    parser = TmtHlrParser(TMT_CONTEXT_LOG, None)

    assert TMT_HLR_ALL_RAW_FIELDS == list(parser.get_raw_fields().keys())


def test_TmtHlrParser__return_specified_fields():
    fields = ['present', 'status']

    parser = TmtHlrParser(TMT_CONTEXT_LOG, fields)

    assert list(parser.get_raw_fields().keys()) == fields