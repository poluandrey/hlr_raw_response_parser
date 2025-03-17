from enum import Enum, auto
from typing import Any, Protocol, Optional

from pydantic import BaseModel, Field
from typing_extensions import NoReturn, assert_never

from hlr.parser.hlr_responses import (InfobipHlrResponse, TmtHlrResponse, NetnumberHlrResponse,
                                      XconnectHlrResponse, XconnectMnpResponse, MittoHlrResponse, TyntecHlrResponse,
                                      TyntecMnpResponse, DatafoneMnpResponse, SinchMnpResponse, AlarisResponse,
                                      GTelecomHlrResponse, GTelecomHlrDetail)


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


class DatafoneMnpParser:

    def get_msisdn_info(self, raw_response: dict[str, Any]) -> MsisdnInfo:
        hlr_response = DatafoneMnpResponse(**raw_response)
        return MsisdnInfo(
            msisdn=hlr_response.msisdn,
            mccmnc=hlr_response.mccmnc,
            ported=hlr_response.ported,
            presents=None,
            roaming=None,
        )

class SinchMnpParser:

    def get_msisdn_info(self, raw_response:dict[str, Any]) -> MsisdnInfo:
        print(raw_response)
        print(type(raw_response))
        hlr_response = AlarisResponse(**raw_response)
        return MsisdnInfo(
            msisdn=hlr_response.msisdn,
            mccmnc=hlr_response.mccmnc,
            ported=hlr_response.ported,
            presents=None,
            roaming=None,
        )


class TmtHlrHlrParser:

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
        print(result)
        msisdn = result.msisdn
        mcc = result.mccMnc[:2]
        mnc = result.mccMnc[2:]
        ported = result.ported
        present = result.status.groupName

        return MsisdnInfo(
            msisdn=msisdn,
            mccmnc=f'{mcc}0{mnc}',
            ported=ported,
            presents=present,
            roaming=result.roaming,
        )

    def convert_present_to_local_format(self, present) -> Optional[bool]:
        if present == 'DELIVERD':
            return True
        if present == 'UNDELIVERED':
            return False
        return None


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
        # print(raw_response)
        hlr_response = MittoHlrResponse(**raw_response[0])
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
            mccmnc=f'{hlr_response.nrhMCC}0{hlr_response.nrhMNC}',
            ported=hlr_response.ported,
            presents=hlr_response.present,
            roaming=hlr_response.roaming,
        )


class TyntecMnpParser:

    def get_msisdn_info(self, raw_response: dict[str: Any]) -> MsisdnInfo:
        hlr_response = TyntecMnpResponse(**raw_response)
        return MsisdnInfo(
            msisdn=hlr_response.msisdn,
            mccmnc=f'{hlr_response.mcc}0{hlr_response.mnc}',
            ported=hlr_response.ported,
            presents=None,
            roaming=None,
        )


class NetnumberHlrParser:

    def get_msisdn_info(self, raw_response: dict[str: Any]) -> MsisdnInfo:
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


class GTelecomHlrParser:
    def get_msisdn_info(self, raw_response: dict[str: Any]) -> MsisdnInfo:
        responses: GTelecomHlrResponse = GTelecomHlrResponse(**raw_response)
        hlr_response = responses.results[0]
        match hlr_response.live_status:
            case 'LIVE':
                presents = True
            case 'DEAD':
                presents = False
            case 'ABSENT_SUBSCRIBER ':
                presents = False
            case _:
                presents = None
        match hlr_response.is_ported:
            case 'YES':
                ported = True
            case 'NO':
                ported = False
            case _:
                ported = None
        return MsisdnInfo(
            msisdn=hlr_response.detected_telephone_number,
            mccmnc=f'{hlr_response.original_network_details.mccmnc[0:3]}0{hlr_response.original_network_details.mccmnc[3:]}',
            presents=presents,
            ported=ported,
        )


class HlrParserType(Enum):
    TMT_HLR = auto()
    INFOBIP_HLR = auto()
    XCONNECT_HLR = auto()
    XCONNECT_MNP = auto()
    MITTO_HLR = auto()
    TYNTEC_HLR = auto()
    TYNTEC_MNP = auto()
    NETNUMBER_HLR = auto()
    DATAFON_MNP = auto()
    SINCH_MNP = auto()
    G_TELECOM_HLR = auto()


def create_parser(provider_type: HlrParserType) -> HlrParser:
    match provider_type:
        case provider_type.TMT_HLR:
            return TmtHlrHlrParser()
        case provider_type.TYNTEC_MNP:
            return TyntecMnpParser()
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
        case provider_type.DATAFON_MNP:
            return DatafoneMnpParser()
        case provider_type.SINCH_MNP:
            return SinchMnpParser()
        case provider_type.G_TELECOM_HLR:
            return GTelecomHlrParser()
        case _:
            raise assert_never(NoReturn)
