from typing import Any

from pydantic import BaseModel, ConfigDict


class JsonRpcError(BaseModel):
    code: int
    message: str
    data: None = None


class ResultData(BaseModel):
    data: list[dict[str, Any]] | None = None


class JsonRpcResponse(BaseModel):
    model_config = ConfigDict(extra='forbid')
    jsonrpc: str
    id: str
    result: ResultData | None = None
    error: JsonRpcError | None = None


class Carrier(BaseModel):
    car_id: int
    car_cc_id: int
    car_address: str | None
    car_comments: str | None
    car_inbound_allowed: int
    car_outbound_allowed: int
    car_is_active: int
    car_name: str
    car_region_id: int | None
    car_test: int
    car_trusted_customer: int
    country_name: str | None
    have_client_prods: int | None
    have_vendor_prods: int | None
