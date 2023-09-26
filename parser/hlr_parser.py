from pydantic import BaseModel
from enum import Enum, auto
from typing import Any, Protocol

from parser.hlr_responses import (InfobipHlrResponse,
                                  TmtHlrResponse,
                                  XconnectHlrResponse,
                                  XconnectMnpResponse)
from parser.types import HlrResponse


class MsisdnInfo(BaseModel):
    msisdn: str | int
    mcc: str
    mnc: str
    ported: int
    present: str | None | bool


class HlrParser(Protocol):
    def get_msisdn_info(self, raw_response: dict[str, Any]) -> MsisdnInfo:
        pass

    def convert_raw_response_to_obj(
            self,
            raw_response: dict[str, Any],
    ) -> HlrResponse:
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
        hlr_response = self.convert_raw_response_to_obj(raw_response)
        msisdn = hlr_response.number
        mcc = hlr_response.mcc
        mnc = hlr_response.mnc
        ported = hlr_response.ported
        present = hlr_response.present
        return MsisdnInfo(
            msisdn=msisdn,
            mcc=mcc,
            mnc=mnc,
            ported=ported,
            present=present,
        )

    def convert_raw_response_to_obj(
            self,
            raw_response: dict[str, Any],
    ) -> HlrResponse:
        for _, value in raw_response.items():
            return TmtHlrResponse(**value)


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

    # def get_result(self, raw_response: dict[str, Any]) -> dict[str, Any]:
    #     if 'results' not in list(raw_response.keys()):
    #         raise InvalidRawResponseError(
    #             'Results in raw response is not a list instance',
    #         )
    #
    #     if not isinstance(raw_response['results'], list):
    #         raise InvalidRawResponseError(
    #             'Msisdn details not found in raw response',
    #         )
    #
    #     return raw_response['results'][0]

    def get_msisdn_info(self, raw_response: dict[str, Any]) -> MsisdnInfo:
        hlr_response = self.convert_raw_response_to_obj(raw_response)
        result = hlr_response.results[0]
        msisdn = result.to
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

    def convert_raw_response_to_obj(
            self,
            raw_response: dict[str, Any],
    ) -> HlrResponse:
        return InfobipHlrResponse(**raw_response)


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
        hlr_response = self.convert_raw_response_to_obj(raw_response)
        return MsisdnInfo(
            msisdn=hlr_response.tn,
            mcc=hlr_response.mcc,
            mnc=hlr_response.mnc,
            ported=hlr_response.npi,
            present=hlr_response.npi,
        )

    def convert_raw_response_to_obj(
            self,
            raw_response: dict[str, Any],
    ) -> HlrResponse:
        return XconnectHlrResponse(**raw_response)


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
        msisdn = raw_response['tn']
        mcc = raw_response['mcc']
        mnc = raw_response['mnc']
        ported = raw_response['npi']
        present = None
        return MsisdnInfo(
            msisdn=msisdn,
            mcc=mcc,
            mnc=mnc,
            ported=ported,
            present=present,
        )

    def convert_raw_response_to_obj(
            self,
            raw_response: dict[str, Any],
    ) -> HlrResponse:
        return XconnectMnpResponse(**raw_response)


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
            raise ValueError('Unexpected provider type')
