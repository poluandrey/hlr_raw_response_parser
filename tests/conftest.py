import random
from itertools import product
from unittest import mock

from pytest import fixture

from alaris.models import ProductType, Product, Carrier
from hlr.client.client import HlrClient
from hlr.client.schemas import HlrResponse
from hlr.models import User, Task as ApiTask, HlrProduct, TaskDetail
from hlr.parser.hlr_parser import HlrParserType, MsisdnInfo, create_parser
from hlr.tasks import Task, HlrFailedResponse


@fixture()
def tmt_hlr_parser():
    return create_parser(HlrParserType.TMT_HLR)


@fixture()
def xconnect_mnp_parser():
    return create_parser(HlrParserType.XCONNECT_MNP)


@fixture()
def xconnect_hlr_parser():
    return create_parser(HlrParserType.XCONNECT_HLR)


@fixture()
def infobip_hrl_parser():
    return create_parser(HlrParserType.INFOBIP_HLR)


@fixture()
def context_log_valid():
    return '{"startTime":"2023-09-14 09:54:11","contextLog":["s:2023-09-14 09:54:11 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i: \\u003d79226503431. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i: \\u003d79226503431 prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i:Processing: 79226503431 HLR vendor: tmtlive cacheTtl: 14400","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i:Process request, source: tmtlive, dnis: 79226503431, cachedRawResponse: null","s:2023-09-14 09:54:11 d:PT0S t:HlrExecutor-pool-6-thread-40 i:request link1: https://api.tmtvelocity.com/live/json///[dnis]","s:2023-09-14 09:54:11 d:PT0.047S t:AsyncHttpClient-71-49 i:first raw response: {\\n  \\"79226503431\\": {\\n    \\"cic\\": \\"7643\\",\\n    \\"failed_response\\": 191,\\n    \\"imsi\\": \\"25002XXXXXXXXXX\\",\\n    \\"mcc\\": \\"250\\",\\n    \\"mnc\\": \\"02\\",\\n    \\"network\\": \\"MegaFon pjsc\\",\\n    \\"number\\": 79226503431,\\n    \\"ported\\": false,\\n    \\"presents\\": \\"na\\",\\n    \\"status\\": 0,\\n    \\"status_message\\": \\"Success\\",\\n    \\"type\\": \\"mobile\\",\\n    \\"trxid\\": \\"tp02NAX\\"\\n  }\\n}","s:2023-09-14 09:54:11 d:PT0.047S t:AsyncHttpClient-71-49 i:Caching raw response with cacheTtl: 14405","s:2023-09-14 09:54:11 d:PT0.047S t:AsyncHttpClient-71-49 i:Result is Ok, setCompleted","s:2023-09-14 09:54:11 d:PT0.048S t:AsyncHttpClient-71-49 i:Finishing"]}'


@fixture()
def context_log_without_raw_response():
    return '{"startTime":"2023-09-12 19:13:56","contextLog":["s:2023-09-12 19:13:56 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i: \\u003d79216503431. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i: \\u003d79216503431 prefix\\u003d79216503431 process time sec.\\u003dPT0S mccmnc\\u003d250001 fullMatched\\u003dtrue ownerID\\u003dmMTS providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i:Processing: 79216503431 HLR vendor: tmtlive cacheTtl: 14400","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i:Process request, source: tmtlive, dnis: 79216503431, cached: null","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i:request link1: https://api.tmtvelocity.com/live/json///[dnis]","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:: {\\n  \\"79216503431\\": {\\n    \\"cic\\": \\"7629\\",\\n    \\"failed_response\\": 191,\\n    \\"imsi\\": \\"25001XXXXXXXXXX\\",\\n    \\"mcc\\": \\"250\\",\\n    \\"mnc\\": \\"01\\",\\n    \\"network\\": \\"Mobilnyye TeleSistemy pjsc (MTS)\\",\\n    \\"number\\": 79216503431,\\n    \\"ported\\": true,\\n    \\"presents\\": \\"na\\",\\n    \\"status\\": 0,\\n    \\"status_message\\": \\"Success\\",\\n    \\"type\\": \\"mobile\\",\\n    \\"trxid\\": \\"dPgTp1Y\\"\\n  }\\n}","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:Caching raw response with cacheTtl: 14405","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:Result is Ok, setCompleted","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:Finishing"]}'


@fixture()
def context_log_without_nested_context_log():
    return '{"startTime":"2023-09-12 19:13:56","sameOtherKey":["s:2023-09-12 19:13:56 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i: \\u003d79216503431. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i: \\u003d79216503431 prefix\\u003d79216503431 process time sec.\\u003dPT0S mccmnc\\u003d250001 fullMatched\\u003dtrue ownerID\\u003dmMTS providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i:Processing: 79216503431 HLR vendor: tmtlive cacheTtl: 14400","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i:Process request, source: tmtlive, dnis: 79216503431, cachedRawResponse: null","s:2023-09-12 19:13:56 d:PT0S t:HlrExecutor-pool-6-thread-47 i:request link1: https://api.tmtvelocity.com/live/json///[dnis]","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:first raw response: {\\n  \\"79216503431\\": {\\n    \\"cic\\": \\"7629\\",\\n    \\"failed_response\\": 191,\\n    \\"imsi\\": \\"25001XXXXXXXXXX\\",\\n    \\"mcc\\": \\"250\\",\\n    \\"mnc\\": \\"01\\",\\n    \\"network\\": \\"Mobilnyye TeleSistemy pjsc (MTS)\\",\\n    \\"number\\": 79216503431,\\n    \\"ported\\": true,\\n    \\"presents\\": \\"na\\",\\n    \\"status\\": 0,\\n    \\"status_message\\": \\"Success\\",\\n    \\"type\\": \\"mobile\\",\\n    \\"trxid\\": \\"dPgTp1Y\\"\\n  }\\n}","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:Caching raw response with cacheTtl: 14405","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:Result is Ok, setCompleted","s:2023-09-12 19:13:56 d:PT0.017S t:AsyncHttpClient-67-4 i:Finishing"]}'


@fixture()
def context_log_not_serializable_context_log():
    return '"startTime":"2023-09-12 20:52:24","contextLog":["s:2023-09-12 20:52:24 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i: \\u003d79216503431. prefix\\u003dnull process time sec.\\u003dPT-0.001S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i: \\u003d79216503431 prefix\\u003d79216503431 process time sec.\\u003dPT0S mccmnc\\u003d250001 fullMatched\\u003dtrue ownerID\\u003dmMTS providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Processing: 79216503431 HLR vendor: tmtlive cacheTtl: 14400","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Process request, source: tmtlive, dnis: 79216503431, cachedRawResponse: {\\n  \\"79216503431\\": {\\n    \\"cic\\": \\"7629\\",\\n    \\"failed_response\\": 191,\\n    \\"imsi\\": \\"25001XXXXXXXXXX\\",\\n    \\"mcc\\": \\"250\\",\\n    \\"mnc\\": \\"01\\",\\n    \\"network\\": \\"Mobilnyye TeleSistemy pjsc (MTS)\\",\\n    \\"number\\": 79216503431,\\n    \\"ported\\": true,\\n    \\"presents\\": \\"na\\",\\n    \\"status\\": 0,\\n    \\"status_message\\": \\"Success\\",\\n    \\"type\\": \\"mobile\\",\\n    \\"trxid\\": \\"dPgTp1Y\\"\\n  }\\n}","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Result is Ok, setCompleted","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Finishing"]}'


@fixture()
def context_log_not_serializable_raw_response():
    return '{"startTime":"2023-09-12 20:52:24","contextLog":["s:2023-09-12 20:52:24 d:PT0S t:epollEventLoopGroup-6-11 i:Starting","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i: \\u003d79216503431. prefix\\u003dnull process time sec.\\u003dPT-0.001S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i: \\u003d79216503431 prefix\\u003d79216503431 process time sec.\\u003dPT0S mccmnc\\u003d250001 fullMatched\\u003dtrue ownerID\\u003dmMTS providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i: \\u003d. prefix\\u003dnull process time sec.\\u003dPT0S mccmnc\\u003dnull fullMatched\\u003dfalse ownerID\\u003dnull providerResponseCode\\u003dnull mode\\u003dEXACTLY","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Processing: 79216503431 HLR vendor: tmtlive cacheTtl: 14400","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Process request, source: tmtlive, dnis: 79216503431, cachedRawResponse: \\n  \\"79216503431\\": {\\n    \\"cic\\": \\"7629\\",\\n    \\"failed_response\\": 191,\\n    \\"imsi\\": \\"25001XXXXXXXXXX\\",\\n    \\"mcc\\": \\"250\\",\\n    \\"mnc\\": \\"01\\",\\n    \\"network\\": \\"Mobilnyye TeleSistemy pjsc (MTS)\\",\\n    \\"number\\": 79216503431,\\n    \\"ported\\": true,\\n    \\"presents\\": \\"na\\",\\n    \\"status\\": 0,\\n    \\"status_message\\": \\"Success\\",\\n    \\"type\\": \\"mobile\\",\\n    \\"trxid\\": \\"dPgTp1Y\\"\\n  }\\n}","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Result is Ok, setCompleted","s:2023-09-12 20:52:24 d:PT0.001S t:HlrExecutor-pool-6-thread-61 i:Finishing"]}'


@fixture()
def make_tmt_hlr_response(faker):
    def inner(msisdn: int | None = None,
              mcc: str | None = None,
              mnc: str | None = None,
              presents: str | None = None,
              ported: str | None = None,
              ):
        if not msisdn:
            msisdn = faker.random_number(digits=13)

        if not mcc:
            mcc = str(faker.random_number(digits=3))

        if not mnc:
            mnc = str(faker.random_number(digits=2))

        if not presents:
            presents = random.choice(['yes', 'no', 'na'])

        if not ported:
            ported = random.choice([True, False])

        return {
            msisdn:
                {
                    'cic': faker.pystr(),
                    'failed_response': faker.random_number(digits=3),
                    'imsi': str(faker.random_number(digits=5)) + '0' * 8,
                    'mcc': mcc,
                    'mnc': mnc,
                    'network': faker.pystr(),
                    'number': msisdn,
                    'ported': ported,
                    'presents': presents,
                    'status': faker.random_number(digits=1),
                    'status_message': faker.pystr(),
                    'type': faker.pystr(),
                    'trxid': faker.pystr(),
                },
        }

    return inner


@fixture()
def make_infobip_hlr_response(faker):
    def inner(
            ported: bool | None = None,
            roaming: bool | None = None,
            present: str | None = None,
            msisdn: str | None = None,
            mccmnc: str | None = None,
    ):
        if not msisdn:
            msisdn = str(faker.random_number(digits=13))

        if not mccmnc:
            mccmnc = str(faker.random_number(digits=5))

        if not present:
            present = random.choice(['DELIVERED', 'UNDELIVERABLE', 'REJECTED'])

        if not roaming:
            roaming = random.choice([True, False])

        if not ported:
            ported = random.choice([True, False])

        return {
            'results':
                [
                    {
                        'to': msisdn,
                        'mccMnc': mccmnc,
                        'imsi': str(faker.random_number(digits=15)),
                        'originalNetwork': {
                            'networkName': faker.pystr(),
                            'networkPrefix': str(faker.random_number(digits=5)),
                            'countryName': faker.pystr(),
                            'countryPrefix': str(faker.random_number(digits=3)),
                            'networkId': faker.random_number(digits=5),
                        },
                        'ported': ported,
                        'roaming': roaming,
                        'status': {
                            'groupId': faker.random_number(digits=1),
                            'groupName': present,
                            'id': faker.random_number(digits=1),
                            'name': faker.pystr(),
                            'description': faker.pystr(),
                        },
                        'failed_response': {
                            'groupId': faker.random_number(digits=1),
                            'groupName': faker.pystr(),
                            'id': faker.random_number(digits=1),
                            'name': faker.pystr(),
                            'description': faker.pystr(),
                        },
                        'permanent': faker.pystr(),
                    },
                ],
        }

    return inner


@fixture()
def make_xconnect_mnp_response(faker):
    def inner(
            msisdn: str | None = None,
            ported: str | None = None,
            mcc: str | None = None,
            mnc: str | None = None,
    ):
        if not msisdn:
            msisdn = str(faker.random_number(digits=12))

        if not ported:
            ported = random.choice([True, False])

        if not mcc:
            mcc = str(faker.random_number(digits=3))

        if not mnc:
            mnc = str(faker.random_number(digits=2))

        return {
            'tn': msisdn,
            'npdi': faker.pystr(),
            'npi': ported,
            'mcc': mcc,
            'mnc': mnc,
            'cic': str(faker.random_number(digits=8)),
            'cn': faker.pystr(),
            'cc': faker.pystr(),
            'nt': faker.pystr(),
        }

    return inner


@fixture()
def make_xconnect_hlr_response(faker):
    def inner(
            msisdn: str | None = None,
            mcc: str | None = None,
            mnc: str | None = None,
            ported: str | None = None,
            presents: str | None = None,

    ):
        if not msisdn:
            msisdn = str(faker.random_number(digits=12))

        if not mcc:
            mcc = str(faker.random_number(digits=3))

        if not mnc:
            mnc = str(faker.random_number(digits=2))

        if not ported:
            ported = random.choice(['true', 'false'])

        if not presents:
            presents = random.choice(['000', '001', '002', '003', '004'])

        return {
            'tn': msisdn,
            'cc': 'RU',
            'mcc': mcc,
            'mnc': mnc,
            'npdi': faker.pystr(),
            'npi': ported,
            'nt': faker.pystr(),
            'nv': str(faker.random_number(digits=3)),
            'ns': presents,
            'rc': str(faker.random_number(digits=3)),
        }

    return inner


@fixture()
def hlr_client():
    login = 'your_login'
    password = 'your_password'
    base_url = 'https://example.com/api/'
    return HlrClient(login, password, base_url)


@fixture()
def hlr_response_vendor_not_found():
    return {
        'message_id': 'befa5ba6-f50b-42ab-9e35-c83557731fd8',
        'result': -2,
        'ported': 0,
        'message': 'Vendor not found',
        'dnis': '7911036721995',
        'cached': 0,
        'login': 'alaris',
        'context_log': '...',
    }


@fixture()
def hlr_response_successful_for_tmt_hlr(context_log_valid):
    return {
        'message_id': 'b13439c5-3811-40b4-a001-531892df114c',
        'mccmnc': '250001',
        'result': 0,
        'ported': 1,
        'source': 'HLR',
        'message': 'message',
        'source_name': 'tmt_hlr',
        'source_type': 'tmtlive',
        'dnis': '79216503431',
        'cached': 0,
        'failed_response': 'na',
        'login': 'alaris',
        'context_log': context_log_valid,
        'provider_ttl': 14400,
        'providerResponseCode': 'na',
    }


@fixture()
def hlr_response_hlr_proxy_internal_error_contain_message():
    return {
        'message_id': 'fd161140-0ed5-44c5-a125-140a2d281e06',
        'result': -1,
        'ported': 0,
        'source': 'HLR',
        'message': 'Invalid Number',
        'source_name': 'tmt_hlr',
        'source_type': 'tmtlive',
        'dnis': '792165034311',
        'cached': 0,
        'login': 'alaris',
        'context_log': '{\"startTime\":\"2023-10-02 12:53:24\",\"contextLog\":[\"s:2023-10-02 12:53:24 d:PT0S t:epollEventLoopGroup-6-20 i:Starting\",\"s:2023-10-02 12:53:24 d:PT0S t:HlrExecutor-pool-6-thread-32 i: \=792165034311. prefix\=null process time sec.\=PT0S mccmnc\=null fullMatched\=false ownerID\=null providerResponseCode\=null mode\=EXACTLY\",\"s:2023-10-02 12:53:24 d:PT0S t:HlrExecutor-pool-6-thread-32 i: \=792165034311 prefix\=null process time sec.\=PT0S mccmnc\=null fullMatched\=false ownerID\=null providerResponseCode\=null mode\=EXACTLY\",\"s:2023-10-02 12:53:24 d:PT0S t:HlrExecutor-pool-6-thread-32 i: \=. prefix\=null process time sec.\=PT0S mccmnc\=null fullMatched\=false ownerID\=null providerResponseCode\=null mode\=EXACTLY\",\"s:2023-10-02 12:53:24 d:PT0S t:HlrExecutor-pool-6-thread-32 i:Processing: 792165034311 HLR vendor: tmtlive cacheTtl: 14400\",\"s:2023-10-02 12:53:24 d:PT0S t:HlrExecutor-pool-6-thread-32 i:Process request, source: tmtlive, dnis: 792165034311, cachedRawResponse: null\",\"s:2023-10-02 12:53:24 d:PT0S t:HlrExecutor-pool-6-thread-32 i:request link1: https://api.tmtvelocity.com/live/json/ZspUQp2a4xYX7/Z7K4xEX5YwGD7v7/[dnis]\",\"s:2023-10-02 12:53:24 d:PT0.017S t:AsyncHttpClient-43-37 i:first raw response: {\\n  \\\"792165034311\\\": {\\n    \\\"number\\\": 792165034311,\\n    \\\"status\\\": 1,\\n    \\\"status_message\\\": \\\"Invalid Number\\\",\\n    \\\"failed_response\\\": 0\\n  }\\n}\",\"s:2023-10-02 12:53:24 d:PT0.017S t:AsyncHttpClient-43-37 i:Caching raw response with cacheTtl: 10\",\"s:2023-10-02 12:53:24 d:PT0.017S t:AsyncHttpClient-43-37 i:Result is not Ok, try to request other vendors\",\"s:2023-10-02 12:53:24 d:PT0.018S t:AsyncHttpClient-43-37 i:Finishing\"]}',
        'provider_ttl': 14400,
    }


@fixture()
def hlr_response_hlr_proxy_internal_error_contain_error():
    return {
        'message_id': '8b582f81-6238-4f2d-bacf-8b50bcf6e09d',
        'result': -3,
        'ported': 0,
        'source': 'HLR',
        'source_name': 'tmt_mnp',
        'source_type': 'tmtenum',
        'dnis': '792165034311',
        'cached': 0,
        'failed_response': 'Empty vendor response: null',
        'login': 'alaris',
        'context_log': '{\"startTime\":\"2023-10-02 12:40:02\",\"contextLog\":[\"s:2023-10-02 12:40:02 d:PT0S t:epollEventLoopGroup-6-20 i:Starting\",\"s:2023-10-02 12:40:02 d:PT0S t:HlrExecutor-pool-6-thread-20 i: \=792165034311. prefix\=null process time sec.\=PT0S mccmnc\=null fullMatched\=false ownerID\=null providerResponseCode\=null mode\=EXACTLY\",\"s:2023-10-02 12:40:02 d:PT0S t:HlrExecutor-pool-6-thread-20 i: \=792165034311 prefix\=null process time sec.\=PT0S mccmnc\=null fullMatched\=false ownerID\=null providerResponseCode\=null mode\=EXACTLY\",\"s:2023-10-02 12:40:02 d:PT0S t:HlrExecutor-pool-6-thread-20 i: \=. prefix\=null process time sec.\=PT0S mccmnc\=null fullMatched\=false ownerID\=null providerResponseCode\=null mode\=EXACTLY\",\"s:2023-10-02 12:40:02 d:PT0S t:HlrExecutor-pool-6-thread-20 i:Processing: 792165034311 HLR vendor: tmtenum cacheTtl: 86400\",\"s:2023-10-02 12:40:02 d:PT0S t:HlrExecutor-pool-6-thread-20 i:Process request, source: tmtenum, dnis: 792165034311, cachedRawResponse: null\",\"s:2023-10-02 12:40:02 d:PT0.016S t:HlrExecutor-pool-6-thread-20 i:Result is not Ok, try to request other vendors\",\"s:2023-10-02 12:40:02 d:PT0.016S t:HlrExecutor-pool-6-thread-20 i:Finishing\"]}',
        'provider_ttl': 86400,
    }


@fixture()
def hlr_task():
    return Task(provider_name='any_provider',
                msisdn='79999999999',
                provider_type=HlrParserType.TMT_HLR.name)


@fixture()
def successfully_handled_response(faker):
    return MsisdnInfo(
        msisdn=str(faker.random_number(digits=12)),
        mccmnc=str(faker.random_number(digits=6)),
        ported=random.choice([True, False, None]),
        presents=random.choice([True, False, None]),
        roaming=random.choice([True, False, None]),
        request_id=faker.pystr(),
    )

@fixture()
def failed_handled_response(faker):
    return HlrFailedResponse(
        msisdn=str(faker.random_number(digits=12)),
        result=faker.random_number(digits=1),
        message_id=faker.pystr(),
        message=faker.pystr(),
        provider=faker.pystr(),
        http_error=faker.random_number(digits=3)
    )


@fixture()
def hlr_response_successful(hlr_response_successful_for_tmt_hlr):
    return HlrResponse(**hlr_response_successful_for_tmt_hlr)


@fixture()
def hlr_client_mock():
    with mock.patch('hlr.client.client.HlrClient') as get_mccmnc_info_mock:
        yield get_mccmnc_info_mock


@fixture()
def user(db) -> User:
    return User.objects.create_user('TestUser')


@fixture()
def task_create_payload(user):
    return {
        'author': user.id,
        'msisdn': ['79216503431', '79216503432'],
        'external_product_id': [123, 124],
    }


@fixture()
def task(db, user):
    return ApiTask.objects.create(author=user)

@fixture()
def task_detail(db, task, hlr_product):
    return TaskDetail.objects.create(
        task=task,
        external_product_id=hlr_product,
        msisdn='79216503431'
    )


@fixture
def hlr_product(db, faker):
    product_type = ProductType.objects.create(
        external_product_type_id=7,
        name='HLR',
    )
    carrier = Carrier.objects.create(
        external_carrier_id=faker.random_number(),
        name=faker.pystr(),
        is_active=True,

    )
    hlr_product = Product.objects.create(
        external_product_id=1,
        account_currency_code='USD',
        external_account_id=faker.random_number(),
        carrier=carrier,
        is_active=True,
        caption=faker.pystr(),
        description=faker.pystr(),
        direction=1,
        notes=faker.pystr(),
        type=product_type,
    )
    HlrProduct.objects.create(
        product=hlr_product,
        type=HlrParserType.TMT_HLR,
    )
    return hlr_product


@fixture()
def make_hlr_task_data(db, faker, hlr_product):
    def inner(msisdn_count: int = 1):
        hlr_products = Product.objects.all()
        msisdns = []
        for _ in range(msisdn_count):
            msisdns.append(str(faker.random_number(digits=13)))

        return product(msisdns, hlr_products)

    return inner
