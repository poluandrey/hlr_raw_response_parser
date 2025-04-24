from enum import Enum, auto
from typing import Any, Protocol, Optional

from pydantic import BaseModel, Field
from typing_extensions import NoReturn, assert_never

from hlr.parser.hlr_responses import (InfobipHlrResponse, TmtHlrResponse, TMTMnpResponse, NetnumberHlrResponse,
                                      XconnectHlrResponse, XconnectMnpResponse, MittoHlrResponse, TyntecHlrResponse,
                                      TyntecMnpResponse, DatafoneMnpResponse, AlarisResponse,
                                      GTelecomHlrResponse, MittoMnpResponse, NetnumberMnpResponse, MediafonMnpResponse)


class MsisdnInfo(BaseModel):
    msisdn: Optional[str] = None # не все возвращают в ответе исходный тел
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


class TmtMnpHlrParser:

    def get_msisdn_info(self, raw_response: dict[str, Any]) -> MsisdnInfo:
        parts = raw_response.strip("!").split(";")
        parsed = {}
        for part in parts:
            if "=" in part:
                key, value = part.split("=", 1)
                parsed[key] = value

        # Создаем модель
        hlr_response = TMTMnpResponse(**parsed)
        if len(f'{hlr_response.mcc}0{hlr_response.mnc}') == 6:
            mccmnc = f'{hlr_response.mcc}0{hlr_response.mnc}'
        else:
            mccmnc = f'{hlr_response.mcc}{hlr_response.mnc}'

        return MsisdnInfo(
            mccmnc=mccmnc,
            ported=True if hlr_response.np == 'yes' else False,
            roaming=None,
        )


class InfobipHlrHlrParser:

    def get_msisdn_info(self, raw_response: dict[str, Any]) -> MsisdnInfo:
        hlr_response = InfobipHlrResponse(**raw_response)
        result = hlr_response.results[0]
        msisdn = result.msisdn
        mcc = result.mccMnc[:3]
        mnc = result.mccMnc[3:]
        ported = result.ported
        present = self.convert_present_to_local_format(result.status.groupName)

        if len(f'{mcc}{mnc}') == 5:
            mccmnc = f'{mcc}0{mnc}'
        else:
            mccmnc = f'{mcc}{mnc}'

        return MsisdnInfo(
            msisdn=msisdn,
            mccmnc=mccmnc,
            ported=ported,
            presents=present,
            roaming=result.roaming,
        )

    def convert_present_to_local_format(self, present) -> Optional[bool]:
        if present == 'DELIVERED':
            return True
        if present == 'UNDELIVERABLE':
            return False
        return None


class XconnectHlrParser:

    def get_msisdn_info(self, raw_response: dict[str, Any]) -> MsisdnInfo:
        hlr_response = XconnectHlrResponse(**raw_response)
        presents = self.parse_presents(hlr_response)
        if len(f'{hlr_response.mcc}{hlr_response.mnc}') == 5:
            mccmnc = f'{hlr_response.mcc}0{hlr_response.mnc}'
        else:
            mccmnc = f'{hlr_response.mcc}{hlr_response.mnc}'

        return MsisdnInfo(
            msisdn=hlr_response.msisdn,
            mccmnc=mccmnc,
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

        if len(f'{xconnect_response.mcc}{xconnect_response.mnc}') == 5:
            mccmnc = f'{xconnect_response.mcc}0{xconnect_response.mnc}'
        else:
            mccmnc = f'{xconnect_response.mcc}{xconnect_response.mnc}'
        return MsisdnInfo(
            msisdn=xconnect_response.msisdn,
            mccmnc=mccmnc,
            ported=xconnect_response.ported,
            presents=None,
            roaming=None,
        )


class MittoHlrParser:

    def get_msisdn_info(self, raw_response: dict[str: Any]) -> MsisdnInfo:
        hlr_response = MittoHlrResponse(**raw_response[0])
        if len(f'{hlr_response.mcc}{hlr_response.mnc}') == 5:
            mccmnc = f'{hlr_response.mcc}0{hlr_response.mnc}'
        else:
            mccmnc = f'{hlr_response.mcc}{hlr_response.mnc}'
        return MsisdnInfo(
            msisdn=hlr_response.msisdn,
            mccmnc=mccmnc,
            ported=hlr_response.ported,
            presents=hlr_response.present,
            roaming=hlr_response.roaming,
        )


class MittoMnpParser:

    def get_msisdn_info(self, raw_response: dict[str: Any]) -> MsisdnInfo:
        mnp_response = MittoMnpResponse(**raw_response[0])

        if len(f'{mnp_response.mcc}{mnp_response.mnc}') == 5:
            mccmnc = f'{mnp_response.mcc}0{mnp_response.mnc}'
        else:
            mccmnc = f'{mnp_response.nrhMCC}{mnp_response.nrhMNC}'

        return MsisdnInfo(
            msisdn=mnp_response.msisdn,
            mccmnc=mccmnc,
            ported=mnp_response.ported,
        )


class TyntecHlrParser:

    def get_msisdn_info(self, raw_response: dict[str: Any]) -> MsisdnInfo:
        hlr_response = TyntecHlrResponse(**raw_response)

        if len(f'{hlr_response.nrhMCC}{hlr_response.nrhMNC}') == 5:
            mccmnc = f'{hlr_response.nrhMCC}0{hlr_response.nrhMNC}'
        else:
            mccmnc = f'{hlr_response.nrhMCC}{hlr_response.nrhMNC}'

        return MsisdnInfo(
            msisdn=hlr_response.msisdn,
            mccmnc=mccmnc,
            ported=hlr_response.ported,
            presents=hlr_response.present,
            roaming=hlr_response.roaming,
        )


class TyntecMnpParser:

    def get_msisdn_info(self, raw_response: dict[str: Any]) -> MsisdnInfo:
        hlr_response = TyntecMnpResponse(**raw_response)
        if len(f'{hlr_response.mcc}{hlr_response.mnc}') == 5:
            mccmnc = f'{hlr_response.mcc}0{hlr_response.mnc}'
        else:
            mccmnc = f'{hlr_response.mcc}{hlr_response.mnc}'
        return MsisdnInfo(
            msisdn=hlr_response.msisdn,
            mccmnc=mccmnc,
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
        if len(f'{hlr_response.mnis.mccmnc[0:3]}{hlr_response.mnis.mccmnc[3:]}') == 5:
            mccmnc = f'{hlr_response.mnis.mccmnc[0:3]}0{hlr_response.mnis.mccmnc[3:]}'
        else:
            mccmnc = f'{hlr_response.mnis.mccmnc[0:3]}{hlr_response.mnis.mccmnc[3:]}'

        return MsisdnInfo(
            msisdn=hlr_response.mnis.msisdn[1:],
            mccmnc=mccmnc,
            presents=presents,
        )


class NetnumberMnpParser:

    def get_msisdn_info(self, raw_response: dict[str: Any]) -> MsisdnInfo:
        hlr_response = NetnumberMnpResponse(**raw_response)
        info = hlr_response.cid

        if len(info.hni) == 5:
            mccmnc = f'{info.hni[0:3]}0{info.hni[3:]}'
        else:
            mccmnc = info.hni

        return MsisdnInfo(
            msisdn=info.tel[1:],
            mccmnc=mccmnc,
            ported=bool(info.pi),
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


class MediafonMnpParser:

    def get_msisdn_info(self, raw_response) -> MsisdnInfo:
        response = MediafonMnpResponse(**raw_response)
        info = response.results[0]

        mnc = str(info.mnc)
        while len(mnc) < 3:
            mnc = f'0{info.mnc}'

        mccmnc = f'{info.mcc}{mnc}'
        return MsisdnInfo(
            msisdn=info.msisdn,
            mccmnc=mccmnc,
            ported=info.isPorted,

        )

class HlrParserType(Enum):
    TMT_HLR = auto()
    TMT_MNP = auto()
    INFOBIP_HLR = auto()
    XCONNECT_HLR = auto()
    XCONNECT_MNP = auto()
    MITTO_HLR = auto()
    MITTO_MNP = auto()
    TYNTEC_HLR = auto()
    TYNTEC_MNP = auto()
    NETNUMBER_HLR = auto()
    NETNUMBER_MNP = auto()
    DATAFON_MNP = auto()
    SINCH_MNP = auto()
    G_TELECOM_HLR = auto()
    MEDIAFON_MNP = auto()


def create_parser(provider_type: HlrParserType) -> HlrParser:
    match provider_type:
        case provider_type.TMT_HLR:
            return TmtHlrHlrParser()
        case provider_type.TMT_MNP:
            return TmtMnpHlrParser()
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
        case provider_type.NETNUMBER_MNP:
            return NetnumberMnpParser()
        case provider_type.DATAFON_MNP:
            return DatafoneMnpParser()
        case provider_type.SINCH_MNP:
            return SinchMnpParser()
        case provider_type.G_TELECOM_HLR:
            return GTelecomHlrParser()
        case provider_type.MITTO_MNP:
            return MittoMnpParser()
        case provider_type.MEDIAFON_MNP:
            return MediafonMnpParser()
        case _:
            raise assert_never(NoReturn)
