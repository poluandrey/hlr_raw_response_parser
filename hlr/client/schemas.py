from pydantic import BaseModel, Field


class HlrResponse(BaseModel):
    message_id: str
    msisdn: str = Field(alias='dnis')
    source_name: str
    mccmnc: str
    result: int
    ported: int
    cached: int
    context_log: str
    message: str
