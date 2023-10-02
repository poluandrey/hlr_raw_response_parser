from pytest import fixture

from hlr.client import HlrClient


@fixture()
def context_log():
    def get_context_log(is_valid: bool = False,
                        without_raw_response: bool = False,
                        without_nested_context_log: bool = False,
                        not_serializable_context_log: bool = False,
                        not_serializable_raw_response: bool = False
                        ):
        if is_valid:
            return '{"startTime":"2023-09-14 09:54:11","contextLog":["s:2023-09-14 09:54:11 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i: \\u003d79226503431. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i: \\u003d79226503431 prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i:Processing: 79226503431 HLR vendor: tmtlive cacheTtl: 14400","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i:Process request, source: tmtlive, dnis: 79226503431, cachedRawResponse: null","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i:request link1: https://api.tmtvelocity.com/live/json///[dnis]","s:2023-09-14 09:54:11 d:PT0.047S t:AsyncHttpClient-71-49 i:first raw response: {\\n  \\"79226503431\\": {\\n    \\"cic\\": \\"7643\\",\\n    \\"error\\": 191,\\n    \\"imsi\\": \\"25002XXXXXXXXXX\\",\\n    \\"mcc\\": \\"250\\",\\n    \\"mnc\\": \\"02\\",\\n    \\"network\\": \\"MegaFon pjsc\\",\\n    \\"number\\": 79226503431,\\n    \\"ported\\": false,\\n    \\"present\\": \\"na\\",\\n    \\"status\\": 0,\\n    \\"status_message\\": \\"Success\\",\\n    \\"type\\": \\"mobile\\",\\n    \\"trxid\\": \\"tp02NAX\\"\\n  }\\n}","s:2023-09-14 09:54:11 d:PT0.047S t:AsyncHttpClient-71-49 i:Caching raw response with cacheTtl: 14405","s:2023-09-14 09:54:11 d:PT0.047S t:AsyncHttpClient-71-49 i:Result is Ok, setCompleted","s:2023-09-14 09:54:11 d:PT0.048S t:AsyncHttpClient-71-49 i:Finishing"]}'
        if without_raw_response:
            return '{"startTime":"2023-09-12 19:13:56","contextLog":["s:2023-09-12 19:13:56 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i: \\u003d79216503431. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i: \\u003d79216503431 prefix\\u003d79216503431 process time sec.\\u003dPT0S mccmnc\\u003d250001 fullMatched\\u003dtrue ownerID\\u003dmMTS providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i:Processing: 79216503431 HLR vendor: tmtlive cacheTtl: 14400","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i:Process request, source: tmtlive, dnis: 79216503431, cached: null","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i:request link1: https://api.tmtvelocity.com/live/json///[dnis]","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:: {\\n  \\"79216503431\\": {\\n    \\"cic\\": \\"7629\\",\\n    \\"error\\": 191,\\n    \\"imsi\\": \\"25001XXXXXXXXXX\\",\\n    \\"mcc\\": \\"250\\",\\n    \\"mnc\\": \\"01\\",\\n    \\"network\\": \\"Mobilnyye TeleSistemy pjsc (MTS)\\",\\n    \\"number\\": 79216503431,\\n    \\"ported\\": true,\\n    \\"present\\": \\"na\\",\\n    \\"status\\": 0,\\n    \\"status_message\\": \\"Success\\",\\n    \\"type\\": \\"mobile\\",\\n    \\"trxid\\": \\"dPgTp1Y\\"\\n  }\\n}","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:Caching raw response with cacheTtl: 14405","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:Result is Ok, setCompleted","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:Finishing"]}'
        if without_nested_context_log:
            return '{"startTime":"2023-09-12 19:13:56","sameOtherKey":["s:2023-09-12 19:13:56 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i: \\u003d79216503431. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i: \\u003d79216503431 prefix\\u003d79216503431 process time sec.\\u003dPT0S mccmnc\\u003d250001 fullMatched\\u003dtrue ownerID\\u003dmMTS providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i:Processing: 79216503431 HLR vendor: tmtlive cacheTtl: 14400","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i:Process request, source: tmtlive, dnis: 79216503431, cachedRawResponse: null","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i:request link1: https://api.tmtvelocity.com/live/json///[dnis]","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:first raw response: {\\n  \\"79216503431\\": {\\n    \\"cic\\": \\"7629\\",\\n    \\"error\\": 191,\\n    \\"imsi\\": \\"25001XXXXXXXXXX\\",\\n    \\"mcc\\": \\"250\\",\\n    \\"mnc\\": \\"01\\",\\n    \\"network\\": \\"Mobilnyye TeleSistemy pjsc (MTS)\\",\\n    \\"number\\": 79216503431,\\n    \\"ported\\": true,\\n    \\"present\\": \\"na\\",\\n    \\"status\\": 0,\\n    \\"status_message\\": \\"Success\\",\\n    \\"type\\": \\"mobile\\",\\n    \\"trxid\\": \\"dPgTp1Y\\"\\n  }\\n}","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:Caching raw response with cacheTtl: 14405","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:Result is Ok, setCompleted","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:Finishing"]}'
        if not_serializable_context_log:
            return '"startTime":"2023-09-12 20:52:24","contextLog":["s:2023-09-12 20:52:24 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i: \\u003d79216503431. prefix\\u003dnull process time sec.\\u003dPT-0.001S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i: \\u003d79216503431 prefix\\u003d79216503431 process time sec.\\u003dPT0S mccmnc\\u003d250001 fullMatched\\u003dtrue ownerID\\u003dmMTS providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Processing: 79216503431 HLR vendor: tmtlive cacheTtl: 14400","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Process request, source: tmtlive, dnis: 79216503431, cachedRawResponse: {\\n  \\"79216503431\\": {\\n    \\"cic\\": \\"7629\\",\\n    \\"error\\": 191,\\n    \\"imsi\\": \\"25001XXXXXXXXXX\\",\\n    \\"mcc\\": \\"250\\",\\n    \\"mnc\\": \\"01\\",\\n    \\"network\\": \\"Mobilnyye TeleSistemy pjsc (MTS)\\",\\n    \\"number\\": 79216503431,\\n    \\"ported\\": true,\\n    \\"present\\": \\"na\\",\\n    \\"status\\": 0,\\n    \\"status_message\\": \\"Success\\",\\n    \\"type\\": \\"mobile\\",\\n    \\"trxid\\": \\"dPgTp1Y\\"\\n  }\\n}","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Result is Ok, setCompleted","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Finishing"]}'
        if not_serializable_raw_response:
            return '{"startTime":"2023-09-12 20:52:24","contextLog":["s:2023-09-12 20:52:24 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i: \\u003d79216503431. prefix\\u003dnull process time sec.\\u003dPT-0.001S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i: \\u003d79216503431 prefix\\u003d79216503431 process time sec.\\u003dPT0S mccmnc\\u003d250001 fullMatched\\u003dtrue ownerID\\u003dmMTS providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Processing: 79216503431 HLR vendor: tmtlive cacheTtl: 14400","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Process request, source: tmtlive, dnis: 79216503431, cachedRawResponse: \\n  \\"79216503431\\": {\\n    \\"cic\\": \\"7629\\",\\n    \\"error\\": 191,\\n    \\"imsi\\": \\"25001XXXXXXXXXX\\",\\n    \\"mcc\\": \\"250\\",\\n    \\"mnc\\": \\"01\\",\\n    \\"network\\": \\"Mobilnyye TeleSistemy pjsc (MTS)\\",\\n    \\"number\\": 79216503431,\\n    \\"ported\\": true,\\n    \\"present\\": \\"na\\",\\n    \\"status\\": 0,\\n    \\"status_message\\": \\"Success\\",\\n    \\"type\\": \\"mobile\\",\\n    \\"trxid\\": \\"dPgTp1Y\\"\\n  }\\n}","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Result is Ok, setCompleted","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Finishing"]}'
    return get_context_log


@fixture()
def tmt_context_log():
    return '{"startTime":"2023-09-14 09:54:11","contextLog":["s:2023-09-14 09:54:11 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i: \\u003d79226503431. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i: \\u003d79226503431 prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i:Processing: 79226503431 HLR vendor: tmtlive cacheTtl: 14400","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i:Process request, source: tmtlive, dnis: 79226503431, cachedRawResponse: null","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i:request link1: https://api.tmtvelocity.com/live/json///[dnis]","s:2023-09-14 09:54:11 d:PT0.047S t:AsyncHttpClient-71-49 i:first raw response: {\\n  \\"79226503431\\": {\\n    \\"cic\\": \\"7643\\",\\n    \\"error\\": 191,\\n    \\"imsi\\": \\"25002XXXXXXXXXX\\",\\n    \\"mcc\\": \\"250\\",\\n    \\"mnc\\": \\"02\\",\\n    \\"network\\": \\"MegaFon pjsc\\",\\n    \\"number\\": 79226503431,\\n    \\"ported\\": false,\\n    \\"present\\": \\"na\\",\\n    \\"status\\": 0,\\n    \\"status_message\\": \\"Success\\",\\n    \\"type\\": \\"mobile\\",\\n    \\"trxid\\": \\"tp02NAX\\"\\n  }\\n}","s:2023-09-14 09:54:11 d:PT0.047S t:AsyncHttpClient-71-49 i:Caching raw response with cacheTtl: 14405","s:2023-09-14 09:54:11 d:PT0.047S t:AsyncHttpClient-71-49 i:Result is Ok, setCompleted","s:2023-09-14 09:54:11 d:PT0.048S t:AsyncHttpClient-71-49 i:Finishing"]}'


@fixture()
def infobip_context_log():
    return '{"startTime":"2023-09-19 11:40:25","contextLog":["s:2023-09-19 11:40:25 d:PT0S t:epollEventLoopGroup-6-20 i:Starting","s:2023-09-19 11:40:25 d:PT0.001S t:HlrExecutor-pool-6-thread-102 i: \\u003d306980165782. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-19 11:40:25 d:PT0.001S t:HlrExecutor-pool-6-thread-102 i: \\u003d306980165782 prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-19 11:40:25 d:PT0.001S t:HlrExecutor-pool-6-thread-102 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-19 11:40:25 d:PT0.001S t:HlrExecutor-pool-6-thread-102 i:Processing: 306980165782 HLR vendor: infobip cacheTtl: 14400","s:2023-09-19 11:40:25 d:PT0.001S t:HlrExecutor-pool-6-thread-102 i:Process request, source: infobip, dnis: 306980165782, cachedRawResponse: {\\"results\\":[{\\"to\\":\\"306980165782\\",\\"mccMnc\\":\\"20201\\",\\"imsi\\":\\"202010000000000\\",\\"originalNetwork\\":{\\"networkName\\":\\"Cosmote (Mobile Telecommunications S.A.)\\",\\"networkPrefix\\":\\"6980165\\",\\"countryName\\":\\"Greece\\",\\"countryPrefix\\":\\"30\\",\\"networkId\\":1560},\\"ported\\":false,\\"roaming\\":false,\\"status\\":{\\"groupId\\":3,\\"groupName\\":\\"DELIVERED\\",\\"id\\":5,\\"name\\":\\"DELIVERED_TO_HANDSET\\",\\"description\\":\\"Message delivered to handset\\"},\\"error\\":{\\"groupId\\":0,\\"groupName\\":\\"OK\\",\\"id\\":0,\\"name\\":\\"NO_ERROR\\",\\"description\\":\\"No Error\\",\\"permanent\\":false}}]}","s:2023-09-19 11:40:25 d:PT0.002S t:HlrExecutor-pool-6-thread-102 i:Result is Ok, setCompleted","s:2023-09-19 11:40:25 d:PT0.002S t:HlrExecutor-pool-6-thread-102 i:Finishing"]}'


@fixture()
def xconnect_hlr_context_log():
    return '{"startTime":"2023-09-15 09:51:01","contextLog":["s:2023-09-15 09:51:01 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-15 09:51:01 d:PT0S t:HlrExecutor-pool-6-thread-29 i: \\u003d79216503431. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-15 09:51:01 d:PT0S t:HlrExecutor-pool-6-thread-29 i: \\u003d79216503431 prefix\\u003d79216503431 process time sec.\\u003dPT0S mccmnc\\u003d250001 fullMatched\\u003dtrue ownerID\\u003dmMTS providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-15 09:51:01 d:PT0S t:HlrExecutor-pool-6-thread-29 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-15 09:51:01 d:PT0S t:HlrExecutor-pool-6-thread-29 i:Processing: 79216503431 HLR vendor: xconnect cacheTtl: 3600","s:2023-09-15 09:51:01 d:PT0.001S t:HlrExecutor-pool-6-thread-29 i:Process request, source: xconnect, dnis: 79216503431, cachedRawResponse: null","s:2023-09-15 09:51:02 d:PT0.985S t:HlrExecutor-pool-6-thread-29 i:first raw response: {\\"tn\\": \\"79216503431\\", \\"cc\\": \\"RU\\", \\"mcc\\": \\"250\\", \\"mnc\\": \\"01\\", \\"npdi\\": true, \\"npi\\": true, \\"nt\\": \\"wireless\\", \\"nv\\": \\"000\\", \\"ns\\": \\"000\\", \\"rc\\": \\"000\\"}","s:2023-09-15 09:51:02 d:PT0.985S t:HlrExecutor-pool-6-thread-29 i:Caching raw response with cacheTtl: 3605","s:2023-09-15 09:51:02 d:PT0.985S t:HlrExecutor-pool-6-thread-29 i:Result is Ok, setCompleted","s:2023-09-15 09:51:02 d:PT0.986S t:HlrExecutor-pool-6-thread-29 i:Finishing"]}'


@fixture()
def xconnect_mnp_context_log():
    return '{"startTime":"2023-09-19 11:09:42","contextLog":["s:2023-09-19 11:09:42 d:PT0S t:epollEventLoopGroup-6-20 i:Starting","s:2023-09-19 11:09:42 d:PT0.001S t:HlrExecutor-pool-6-thread-80 i: \\u003d306980165782. prefix\\u003dnull process time sec.\\u003dPT-0.001S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-19 11:09:42 d:PT0.001S t:HlrExecutor-pool-6-thread-80 i: \\u003d306980165782 prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-19 11:09:42 d:PT0.001S t:HlrExecutor-pool-6-thread-80 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-19 11:09:42 d:PT0.001S t:HlrExecutor-pool-6-thread-80 i:Processing: 306980165782 HLR vendor: xconnect cacheTtl: 86400","s:2023-09-19 11:09:42 d:PT0.001S t:HlrExecutor-pool-6-thread-80 i:Process request, source: xconnect, dnis: 306980165782, cachedRawResponse: {\\"tn\\": \\"306980165782\\", \\"npdi\\": true, \\"npi\\": false, \\"mcc\\": \\"202\\", \\"mnc\\": \\"01\\", \\"cic\\": \\"83000009\\", \\"cn\\": \\"COSMOTE A.E.\\", \\"cc\\": \\"GR\\", \\"nt\\": \\"wireless\\"}","s:2023-09-19 11:09:42 d:PT0.001S t:HlrExecutor-pool-6-thread-80 i:Result is Ok, setCompleted","s:2023-09-19 11:09:42 d:PT0.001S t:HlrExecutor-pool-6-thread-80 i:Finishing"]}'


@fixture()
def hlr_client():
    login = "your_login"
    password = "your_password"
    base_url = "https://example.com/api/"
    hlr_client = HlrClient(login, password, base_url)
    return hlr_client


@fixture()
def hlr_response_vendor_not_found():
    mock_response_data = {
        "message_id": "befa5ba6-f50b-42ab-9e35-c83557731fd8",
        "result": -2,
        "ported": 0,
        "message": "Vendor not found",
        "dnis": "7911036721995",
        "cached": 0,
        "login": "alaris",
        "context_log": "..."
    }
    return mock_response_data


@fixture()
def hlr_response_successful_for_tmt_hlr():
    mock_response_data = {
        "message_id": "b13439c5-3811-40b4-a001-531892df114c",
        "mccmnc": "250001",
        "result": 0,
        "ported": 1,
        "source": "HLR",
        "message": "message",
        "source_name": "tmt_hlr",
        "source_type": "tmtlive",
        "dnis": "79216503431",
        "cached": 0,
        "error": "na",
        "login": "alaris",
        "context_log": "{\"startTime\":\"2023-10-02 10:33:37\",\"contextLog\":[\"s:2023-10-02 10:33:37 d:PT0S t:epollEventLoopGroup-6-20 i:Starting\",\"s:2023-10-02 10:33:37 d:PT0S t:HlrExecutor-pool-6-thread-84 i: \=79216503431. prefix\=null process time sec.\=PT0S mccmnc\=null fullMatched\=false ownerID\=null providerResponseCode\=null mode\=EXACTLY\",\"s:2023-10-02 10:33:37 d:PT0.001S t:HlrExecutor-pool-6-thread-84 i: \=79216503431 prefix\=null process time sec.\=PT-0.001S mccmnc\=null fullMatched\=false ownerID\=null providerResponseCode\=null mode\=EXACTLY\",\"s:2023-10-02 10:33:37 d:PT0.001S t:HlrExecutor-pool-6-thread-84 i: \=. prefix\=null process time sec.\=PT0S mccmnc\=null fullMatched\=false ownerID\=null providerResponseCode\=null mode\=EXACTLY\",\"s:2023-10-02 10:33:37 d:PT0.001S t:HlrExecutor-pool-6-thread-84 i:Processing: 79216503431 HLR vendor: tmtlive cacheTtl: 14400\",\"s:2023-10-02 10:33:37 d:PT0.001S t:HlrExecutor-pool-6-thread-84 i:Process request, source: tmtlive, dnis: 79216503431, cachedRawResponse: null\",\"s:2023-10-02 10:33:37 d:PT0.001S t:HlrExecutor-pool-6-thread-84 i:request link1: https://api.tmtvelocity.com/live/json/ZspUQp2a4xYX7/Z7K4xEX5YwGD7v7/[dnis]\",\"s:2023-10-02 10:33:37 d:PT0.018S t:AsyncHttpClient-43-9 i:first raw response: {\\n  \\\"79216503431\\\": {\\n    \\\"cic\\\": \\\"7629\\\",\\n    \\\"error\\\": 191,\\n    \\\"imsi\\\": \\\"25001XXXXXXXXXX\\\",\\n    \\\"mcc\\\": \\\"250\\\",\\n    \\\"mnc\\\": \\\"01\\\",\\n    \\\"network\\\": \\\"Mobilnyye TeleSistemy pjsc (MTS)\\\",\\n    \\\"number\\\": 79216503431,\\n    \\\"ported\\\": true,\\n    \\\"present\\\": \\\"na\\\",\\n    \\\"status\\\": 0,\\n    \\\"status_message\\\": \\\"Success\\\",\\n    \\\"type\\\": \\\"mobile\\\",\\n    \\\"trxid\\\": \\\"EfwonAB\\\"\\n  }\\n}\",\"s:2023-10-02 10:33:37 d:PT0.018S t:AsyncHttpClient-43-9 i:Caching raw response with cacheTtl: 14405\",\"s:2023-10-02 10:33:37 d:PT0.018S t:AsyncHttpClient-43-9 i:Result is Ok, setCompleted\",\"s:2023-10-02 10:33:37 d:PT0.018S t:AsyncHttpClient-43-9 i:Finishing\"]}",
        "provider_ttl": 14400,
        "providerResponseCode": "na"
    }
    return mock_response_data


@fixture()
def hlr_response_hlr_proxy_internal_error_contain_message():
    mock_response_data = {
        "message_id": "fd161140-0ed5-44c5-a125-140a2d281e06",
        "result": -1,
        "ported": 0,
        "source": "HLR",
        "message": "Invalid Number",
        "source_name": "tmt_hlr",
        "source_type": "tmtlive",
        "dnis": "792165034311",
        "cached": 0,
        "login": "alaris",
        "context_log": "{\"startTime\":\"2023-10-02 12:53:24\",\"contextLog\":[\"s:2023-10-02 12:53:24 d:PT0S t:epollEventLoopGroup-6-20 i:Starting\",\"s:2023-10-02 12:53:24 d:PT0S t:HlrExecutor-pool-6-thread-32 i: \=792165034311. prefix\=null process time sec.\=PT0S mccmnc\=null fullMatched\=false ownerID\=null providerResponseCode\=null mode\=EXACTLY\",\"s:2023-10-02 12:53:24 d:PT0S t:HlrExecutor-pool-6-thread-32 i: \=792165034311 prefix\=null process time sec.\=PT0S mccmnc\=null fullMatched\=false ownerID\=null providerResponseCode\=null mode\=EXACTLY\",\"s:2023-10-02 12:53:24 d:PT0S t:HlrExecutor-pool-6-thread-32 i: \=. prefix\=null process time sec.\=PT0S mccmnc\=null fullMatched\=false ownerID\=null providerResponseCode\=null mode\=EXACTLY\",\"s:2023-10-02 12:53:24 d:PT0S t:HlrExecutor-pool-6-thread-32 i:Processing: 792165034311 HLR vendor: tmtlive cacheTtl: 14400\",\"s:2023-10-02 12:53:24 d:PT0S t:HlrExecutor-pool-6-thread-32 i:Process request, source: tmtlive, dnis: 792165034311, cachedRawResponse: null\",\"s:2023-10-02 12:53:24 d:PT0S t:HlrExecutor-pool-6-thread-32 i:request link1: https://api.tmtvelocity.com/live/json/ZspUQp2a4xYX7/Z7K4xEX5YwGD7v7/[dnis]\",\"s:2023-10-02 12:53:24 d:PT0.017S t:AsyncHttpClient-43-37 i:first raw response: {\\n  \\\"792165034311\\\": {\\n    \\\"number\\\": 792165034311,\\n    \\\"status\\\": 1,\\n    \\\"status_message\\\": \\\"Invalid Number\\\",\\n    \\\"error\\\": 0\\n  }\\n}\",\"s:2023-10-02 12:53:24 d:PT0.017S t:AsyncHttpClient-43-37 i:Caching raw response with cacheTtl: 10\",\"s:2023-10-02 12:53:24 d:PT0.017S t:AsyncHttpClient-43-37 i:Result is not Ok, try to request other vendors\",\"s:2023-10-02 12:53:24 d:PT0.018S t:AsyncHttpClient-43-37 i:Finishing\"]}",
        "provider_ttl": 14400
    }
    return mock_response_data


@fixture()
def hlr_response_hlr_proxy_internal_error_contain_error():
    mock_response_data = {
        "message_id": "8b582f81-6238-4f2d-bacf-8b50bcf6e09d",
        "result": -3,
        "ported": 0,
        "source": "HLR",
        "source_name": "tmt_mnp",
        "source_type": "tmtenum",
        "dnis": "792165034311",
        "cached": 0,
        "error": "Empty vendor response: null",
        "login": "alaris",
        "context_log": "{\"startTime\":\"2023-10-02 12:40:02\",\"contextLog\":[\"s:2023-10-02 12:40:02 d:PT0S t:epollEventLoopGroup-6-20 i:Starting\",\"s:2023-10-02 12:40:02 d:PT0S t:HlrExecutor-pool-6-thread-20 i: \=792165034311. prefix\=null process time sec.\=PT0S mccmnc\=null fullMatched\=false ownerID\=null providerResponseCode\=null mode\=EXACTLY\",\"s:2023-10-02 12:40:02 d:PT0S t:HlrExecutor-pool-6-thread-20 i: \=792165034311 prefix\=null process time sec.\=PT0S mccmnc\=null fullMatched\=false ownerID\=null providerResponseCode\=null mode\=EXACTLY\",\"s:2023-10-02 12:40:02 d:PT0S t:HlrExecutor-pool-6-thread-20 i: \=. prefix\=null process time sec.\=PT0S mccmnc\=null fullMatched\=false ownerID\=null providerResponseCode\=null mode\=EXACTLY\",\"s:2023-10-02 12:40:02 d:PT0S t:HlrExecutor-pool-6-thread-20 i:Processing: 792165034311 HLR vendor: tmtenum cacheTtl: 86400\",\"s:2023-10-02 12:40:02 d:PT0S t:HlrExecutor-pool-6-thread-20 i:Process request, source: tmtenum, dnis: 792165034311, cachedRawResponse: null\",\"s:2023-10-02 12:40:02 d:PT0.016S t:HlrExecutor-pool-6-thread-20 i:Result is not Ok, try to request other vendors\",\"s:2023-10-02 12:40:02 d:PT0.016S t:HlrExecutor-pool-6-thread-20 i:Finishing\"]}",
        "provider_ttl": 86400
    }
    return mock_response_data
