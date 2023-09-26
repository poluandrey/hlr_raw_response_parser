from pydantic import BaseModel


class Result(BaseModel):
    to: str
    mccMnc: str
    imsi: str
    ported: bool
    roaming: bool


class InfobipHlrResponse(BaseModel):
    results: list[Result]


class TmtHlrResponse(BaseModel):
    number: int
    mcc: str
    mnc: str
    network: str
    ported: bool
    present: str
    type: str


class XconnectHlrResponse(BaseModel):
    tn: str
    mcc: str
    mnc: str
    ns: str
    npi: bool


class XconnectMnpResponse(BaseModel):
    tn: str
    mcc: str
    mnc: str
    npi: bool
