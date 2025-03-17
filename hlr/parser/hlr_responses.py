from pydantic import BaseModel, Field


class InfobipMsisdnStatus(BaseModel):
    groupName: str


class InfobipResult(BaseModel):
    msisdn: str = Field(alias='to')
    mccMnc: str
    imsi: str
    ported: bool
    roaming: bool
    status: InfobipMsisdnStatus


class InfobipHlrResponse(BaseModel):
    results: list[InfobipResult]


class TmtHlrResponse(BaseModel):
    msisdn: int = Field(alias='number')
    mcc: str
    mnc: str
    network: str
    ported: bool
    present: str
    type: str


class DatafoneMnpResponse(BaseModel):
    msisdn: str = Field(alias='dnis')
    mccmnc: str
    ported:  int
    result: int


class SinchMnpResponse(BaseModel):
    imsi: str


class AlarisResponse(BaseModel):
    msisdn: str
    mccmnc: str
    ported: int
    result: int


class XconnectHlrResponse(BaseModel):
    msisdn: str = Field(alias='tn')
    mcc: str
    mnc: str
    present: str = Field(alias='ns')
    ported: bool = Field(alias='npi')


class XconnectMnpResponse(BaseModel):
    msisdn: str = Field(alias='tn')
    mcc: str
    mnc: str
    ported: bool = Field(alias='npi')


class MittoHlrResponse(BaseModel):
    mcc: str
    mnc: str
    msisdn: str
    present: bool = Field(alias='response')
    roaming: bool
    ported: bool


class TyntecHlrResponse(BaseModel):
    nrhMCC: str
    nrhMNC: str
    ported: str
    msisdn: str
    present: str = Field(alias='presence')
    roaming: str


class TyntecMnpResponse(BaseModel):
    mcc: str
    mnc: str
    ported: bool
    msisdn: str


class NetumberMnis(BaseModel):
    mccmnc: str = Field(alias='hni')
    name: str
    msisdn: str = Field(alias='tel')
    present: str = Field(alias='status')
    cic: str


class NetnumberHlrResponse(BaseModel):
    response_code: int
    message: str
    mnis: NetumberMnis


class GTelecomOriginalNetDetail(BaseModel):
    name: str
    mccmnc: str



class GTelecomHlrDetail(BaseModel):
    is_ported: str
    detected_telephone_number: str
    live_status: str
    original_network_details: GTelecomOriginalNetDetail


class GTelecomHlrResponse(BaseModel):
    results: list[GTelecomHlrDetail]



