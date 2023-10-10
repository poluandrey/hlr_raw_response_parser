from pydantic import BaseModel, Field


class Result(BaseModel):
    msisdn: str = Field(alias='to')
    mccMnc: str
    imsi: str
    ported: bool
    roaming: bool


class InfobipHlrResponse(BaseModel):
    results: list[Result]


class TmtHlrResponse(BaseModel):
    msisdn: int = Field(alias='number')
    mcc: str
    mnc: str
    network: str
    ported: bool
    present: str
    type: str


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
