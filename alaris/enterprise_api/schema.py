from pydantic import BaseModel, ConfigDict


class RequestCarrierFilterArgs(BaseModel):
    model_config = ConfigDict(extra='forbid')
    car_id: int | None = None
    have_client_prods: int | None = None
    have_vendor_prods: int | None = None
    car_inbound_allowed: int | None = None
    car_outbound_allowed: int | None = None


class RequestParam(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str
    auth: str
    args: RequestCarrierFilterArgs | None = None


class RequestBody(BaseModel):
    model_config = ConfigDict(extra='forbid')
    jsonrpc: str
    id: int
    method: str
    params: RequestParam


class ResponseBase(BaseModel):
    model_config = ConfigDict(extra='forbid')
    jsonrpc: str
    id: int


class ResponseErrorBase(ResponseBase):
    code: int
    message: str
    data: None = None


class ResponseCarrier(BaseModel):
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


class ResponseResult(BaseModel):
    data: list[ResponseCarrier]


class ResponseCarrierListBase(ResponseBase):
    result: ResponseResult
