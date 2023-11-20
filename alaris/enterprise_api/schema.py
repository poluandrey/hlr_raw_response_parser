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


class Product(BaseModel):
    acc_car_manager_id: int | None
    acc_currency_code: str
    acc_id: int
    agr_timezone_name: str | None
    billing_mode: int
    car_cc_id: int
    car_id: int
    car_region_id: int | None
    check_ani_tags: int
    check_lata: int
    cnt: int | None
    decrease_period: int | None
    def_indeterminate_price: None
    have_sms_poi: int
    have_voice_poi: int
    im_channel_id: int | None
    increase_period: int | None
    is_active: int
    parent_product_id: int | None
    product_caption: str
    product_descr: str
    product_direction: int
    product_id: int
    product_notes: str | None
    product_type: int
    rate_inheritance_mode: None
    rate_set_code: None
    rates_based_on: None
    rcs_billing_scheme_id: int | None
    style: int
    systemid_list: str | None
    use_sender_mccmnc_rates: int

