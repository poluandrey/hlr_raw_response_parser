from dataclasses import dataclass
from enum import Enum, auto
from parser.errors import InvalidRawResponseError
from parser.types import Json
from typing import Protocol


@dataclass(frozen=True, kw_only=True)
class MsisdnInfo:
    msisdn: str
    mcc: str
    mnc: str
    ported: str
    present: str | None


class HlrParser(Protocol):
    def get_msisdn_info(self, raw_response: Json) -> MsisdnInfo:
        pass


class TmtHlrHlrParser(HlrParser):
    """
    raw response example
    {
    "79216503431": {
        "cic": "7629",
        "error": 191,
        "imsi": "25001XXXXXXXXXX",
        "mcc": "250",
        "mnc": "01",
        "network": "Mobilnyye TeleSistemy pjsc (MTS)",
        "number": 79216503431,
        "ported": true,
        "present": "na",
        "status": 0,
        "status_message": "Success",
        "type": "mobile",
        "trxid": "wRgugxm"
    }
    }
    """
    def get_msisdn_from_raw_response(self, raw_response) -> str:
        if not isinstance(raw_response, dict):
            raise InvalidRawResponseError('msisdn not found in raw response')
        return list(raw_response.keys())[0]

    def get_msisdn_info(self, raw_response):
        msisdn = self.get_msisdn_from_raw_response(raw_response)
        raw_info = raw_response[msisdn]
        mcc = raw_info.get('mnc')
        mnc = raw_info.get('mnc')
        ported = raw_info.get('ported')
        present = raw_info.get('present')
        return MsisdnInfo(
            msisdn=msisdn,
            mcc=mcc,
            mnc=mnc,
            ported=ported,
            present=present,
        )


class InfobipHlrHlrParser(HlrParser):
    """
    raw response example
    {"results": [
     {
       "to":"306980165782",
       "mccMnc":"20201",
       "imsi":"202010000000000",
       "originalNetwork":{
          "networkName":"Cosmote (Mobile Telecommunications S.A.)",
          "networkPrefix":"6980165",
          "countryName":"Greece",
          "countryPrefix":"30",
          "networkId":1560
       },
       "ported":false,
       "roaming":false,
       "status":{
          "groupId":3,
          "groupName":"DELIVERED",
          "id":5,
          "name":"DELIVERED_TO_HANDSET",
          "description":"Message delivered to handset"
       },
       "error":{
          "groupId":0,
          "groupName":"OK",
          "id":0,
          "name":"NO_ERROR",
          "description":"No Error",
          "permanent":false
       }
     }]}
    """

    def get_result(self, raw_response) -> Json:
        if not isinstance(raw_response, dict):
            raise InvalidRawResponseError('Unexpected raw response format')
        if 'results' not in list(raw_response.keys()):
            raise InvalidRawResponseError('Results not found in raw response')
        if not isinstance(raw_response['results'], list):
            raise InvalidRawResponseError(
                'Msisdn details not found in raw response'
            )
        return raw_response['results'][0]

    def get_msisdn_info(self, raw_response):
        result = self.get_result(raw_response)
        msisdn = result.get('to')
        mcc = result.get('mccMnc')[:2]
        mnc = result.get('mccMnc')[2:]
        ported = result.get('ported')
        present = None
        return MsisdnInfo(
            msisdn=msisdn,
            mcc=mcc,
            mnc=mnc,
            ported=ported,
            present=present,
        )


class XconnectHlrParser(HlrParser):
    """
    {
    'tn': '306980165782',
    'cc': 'GR',
    'mcc': '202',
    'mnc': '01',
    'npdi': True,
    'npi': False,
    'nt': 'wireless',
    'nv': '000',
    'ns': '000',
    'rc': '000'
    }
    """
    def get_msisdn_info(self, raw_response):
        msisdn = raw_response.get('tn')
        mcc = raw_response.get('mcc')
        mnc = raw_response.get('mnc')
        ported = raw_response.get('npi')
        present = None
        return MsisdnInfo(
            msisdn=msisdn,
            mcc=mcc,
            mnc=mnc,
            ported=ported,
            present=present,
        )


class XconnectMnpParser(HlrParser):
    """
    {'tn': '306980165782',
    'npdi': True,
    'npi': False,
    'mcc': '202',
    'mnc': '01',
    'cic': '83000009',
    'cn': 'COSMOTE A.E.',
    'cc': 'GR',
    'nt': 'wireless'}
    """

    def get_msisdn_info(self, raw_response):
        msisdn = raw_response.get('tn')
        mcc = raw_response.get('mcc')
        mnc = raw_response.get('mnc')
        ported = raw_response.get('npi')
        present = None
        return MsisdnInfo(
            msisdn=msisdn,
            mcc=mcc,
            mnc=mnc,
            ported=ported,
            present=present,
        )


class HlrParserType(Enum):
    TMT_HLR = auto()
    INFOBIP_HLR = auto()
    XCONNECT_HLR = auto()
    XCONNECT_MNP = auto()


def create_parser(provider_type: HlrParserType) -> HlrParser:
    if provider_type == HlrParserType.TMT_HLR:
        return TmtHlrHlrParser()
    if provider_type == HlrParserType.INFOBIP_HLR:
        return InfobipHlrHlrParser()
    if provider_type == HlrParserType.XCONNECT_HLR:
        return XconnectHlrParser()
    if provider_type == HlrParserType.XCONNECT_MNP:
        return XconnectMnpParser()
    else:
        raise ValueError('Invalid provider type')
