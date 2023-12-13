from enum import Enum, auto
from typing import Any, Protocol

from pydantic import BaseModel, Field
from typing_extensions import NoReturn, assert_never

from hlr.parser.hlr_responses import (InfobipHlrResponse, TmtHlrResponse, NetnumberHlrResponse,
                                      XconnectHlrResponse, XconnectMnpResponse, MittoHlrResponse, TyntecHlrResponse)


class MsisdnInfo(BaseModel):
    msisdn: str
    mccmnc: str
    ported: bool | None = Field(default=None)
    presents: bool | None = Field(default=None)
    roaming: bool | None = Field(default=None)
    request_id: str | None = Field(default=None)


class HlrParser(Protocol):
    def get_msisdn_info(self, raw_response: dict[str, Any]) -> MsisdnInfo:
        pass


class TmtHlrHlrParser(HlrParser):

    def get_msisdn_info(self, raw_response: dict[str, Any]) -> MsisdnInfo:
        msisdn = list(raw_response.keys())[0]
        hlr_response = TmtHlrResponse(**raw_response[msisdn])
        return MsisdnInfo(
            msisdn=str(hlr_response.msisdn),
            mccmnc=f'{hlr_response.mcc}0{hlr_response.mnc}',
            ported=hlr_response.ported,
            presents=self.parse_presents(hlr_response.present),
            roaming=None,
        )

    def parse_presents(self, presents: str) -> bool | None:
        match presents:
            case 'na':
                return None
            case 'yes':
                return True
            case _:
                return False


class InfobipHlrHlrParser:

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
            mccmnc=f'{mcc}0{mnc}',
            ported=ported,
            presents=present,
            roaming=result.roaming,
        )


class XconnectHlrParser:

    def get_msisdn_info(self, raw_response: dict[str, Any]) -> MsisdnInfo:
        hlr_response = XconnectHlrResponse(**raw_response)
        presents = self.parse_presents(hlr_response)
        return MsisdnInfo(
            msisdn=hlr_response.msisdn,
            mccmnc=f'{hlr_response.mcc}0{hlr_response.mnc}',
            ported=hlr_response.ported,
            presents=presents,
            roaming=None,
        )

    def parse_presents(self, hlr_response: XconnectHlrResponse) -> bool | None:
        if hlr_response.present == '000':
            return True

        if hlr_response.present == '004':
            return None

        return False


class XconnectMnpParser:

    def get_msisdn_info(self, raw_response: dict[str, Any]) -> MsisdnInfo:
        xconnect_response = XconnectMnpResponse(**raw_response)
        return MsisdnInfo(
            msisdn=xconnect_response.msisdn,
            mccmnc=f'{xconnect_response.mcc}0{xconnect_response.mnc}',
            ported=xconnect_response.ported,
            presents=None,
            roaming=None,
        )


class MittoHlrParser:

    def get_msisdn_info(self, raw_response: dict[str: Any]) -> MsisdnInfo:
        hlr_response = MittoHlrResponse(**raw_response)
        return MsisdnInfo(
            msisdn=hlr_response.msisdn,
            mccmnc=f'{hlr_response.mcc}0{hlr_response.mnc}',
            ported=hlr_response.ported,
            presents=hlr_response.present,
            roaming=hlr_response.roaming,
        )


class TyntecHlrParser:

    def get_msisdn_info(self, raw_response: dict[str: Any]) -> MsisdnInfo:
        hlr_response = TyntecHlrResponse(**raw_response)
        return MsisdnInfo(
            msisdn=hlr_response.msisdn,
            mccmnc=f'{hlr_response.hlrMCC}0{hlr_response.hlrMNC}',
            ported=hlr_response.ported,
            presents=hlr_response.present,
            roaming=hlr_response.roaming,
        )


class NetnumberHlrParser:

    def get_msisdn_info(self, raw_response: dict[str: Any]) -> MsisdnInfo:
        print(raw_response)
        hlr_response = NetnumberHlrResponse(**raw_response)
        match hlr_response.mnis.present:
            case 'active':
                presents = True
            case 'not_active':
                presents = False
            case _:
                presents = None

        return MsisdnInfo(
            msisdn=hlr_response.mnis.msisdn[1:],
            mccmnc=f'{hlr_response.mnis.mccmnc[0:3]}0{hlr_response.mnis.mccmnc[3:]}',
            presents=presents,
        )


class HlrParserType(Enum):
    TMT_HLR = auto()
    INFOBIP_HLR = auto()
    XCONNECT_HLR = auto()
    XCONNECT_MNP = auto()
    MITTO_HLR = auto()
    TYNTEC_HLR = auto()
    NETNUMBER_HLR = auto()


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
        case provider_type.MITTO_HLR:
            return MittoHlrParser()
        case provider_type.TYNTEC_HLR:
            return TyntecHlrParser()
        case provider_type.NETNUMBER_HLR:
            return NetnumberHlrParser()
        case _:
            raise assert_never(NoReturn)
