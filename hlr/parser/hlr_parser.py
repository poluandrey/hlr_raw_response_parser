from enum import Enum, auto
from hlr.parser.hlr_responses import (InfobipHlrResponse, TmtHlrResponse,
                                      XconnectHlrResponse, XconnectMnpResponse)
from typing import Any, Protocol
from typing_extensions import assert_never, NoReturn

from pydantic import BaseModel


class MsisdnInfo(BaseModel):
    msisdn: str
    mcc: str
    mnc: str
    ported: int
    present: bool | None


class HlrParser(Protocol):
    def get_msisdn_info(self, raw_response: dict[str, Any]) -> MsisdnInfo:
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

    def get_msisdn_info(self, raw_response: dict[str, Any]) -> MsisdnInfo:
        msisdn = list(raw_response.keys())[0]
        hlr_response = TmtHlrResponse(**raw_response[msisdn])
        # msisdn_info = raw_response[msisdn]
        # msisdn = str(msisdn_info['number'])
        # mcc = msisdn_info['mcc']
        # mnc = msisdn_info['mnc']
        # ported = msisdn_info['ported']
        # TODO after providing documentation parse the value correctly
        # present = bool(msisdn_info['present'])
        return MsisdnInfo(
            msisdn=str(hlr_response.msisdn),
            mcc=hlr_response.mcc,
            mnc=hlr_response.mnc,
            ported=hlr_response.ported,
            present=bool(hlr_response.present),
        )


class InfobipHlrHlrParser:
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

    def get_msisdn_info(self, raw_response: dict[str, Any]) -> MsisdnInfo:
        hlr_response = InfobipHlrResponse(**raw_response)
        result = hlr_response.results[0]
        msisdn = result.msisdn
        mcc = result.mccMnc[:2]
        mnc = result.mccMnc[2:]
        ported = result.ported
        present = None
        return MsisdnInfo(
            msisdn=msisdn,
            mcc=mcc,
            mnc=mnc,
            ported=ported,
            present=present,
        )


class XconnectHlrParser:
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

    def get_msisdn_info(self, raw_response: dict[str, Any]) -> MsisdnInfo:
        hlr_response = XconnectHlrResponse(**raw_response)
        return MsisdnInfo(
            msisdn=hlr_response.msisdn,
            mcc=hlr_response.mcc,
            mnc=hlr_response.mnc,
            ported=hlr_response.ported,
            present=bool(hlr_response.present),
        )


class XconnectMnpParser:
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

    def get_msisdn_info(self, raw_response: dict[str, Any]) -> MsisdnInfo:
        xconnect_response = XconnectMnpResponse(**raw_response)
        return MsisdnInfo(
            msisdn=xconnect_response.msisdn,
            mcc=xconnect_response.mcc,
            mnc=xconnect_response.mnc,
            ported=xconnect_response.ported,
            present=bool(xconnect_response.ported),
        )


class HlrParserType(Enum):
    TMT_HLR = auto()
    INFOBIP_HLR = auto()
    XCONNECT_HLR = auto()
    XCONNECT_MNP = auto()


def create_parser(provider_type: HlrParserType) -> HlrParser:
    match provider_type:
        case provider_type.TMT_HLR:
            return TmtHlrHlrParser()
        case provider_type.INFOBIP_HLR:
            return InfobipHlrHlrParser()
        case provider_type.XCONNECT_MNP:
            return XconnectMnpParser()
        case provider_type.XCONNECT_HLR:
            return XconnectHlrParser()
        case _:
            raise assert_never(NoReturn)