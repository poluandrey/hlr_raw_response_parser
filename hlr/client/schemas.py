from typing import Optional

from pydantic import BaseModel, Field


class HlrResponse(BaseModel):
    task_detail_id: Optional[int] = None
    message_id: str
    msisdn: str = Field(alias='dnis')
    source_name: str
    mccmnc: Optional[str] = None
    result: Optional[int] = None
    ported: Optional[int] = None
    cached: Optional[int] = None
    context_log: Optional[str] = None
    message: str | None = Field(default=None)
    raw_response: Optional[str] = None

