from dataclasses import dataclass
from itertools import product

from hlr.client import HlrClient, HlrFailedResponse, HlrResponse
from hlr.client_errors import (HlrClientError, HlrClientHTTPError,
                               HlrProxyError, HlrVendorNotFoundError)


@dataclass(kw_only=True, frozen=True, slots=True)
class Task:
    providers: list[str]
    msisdns: list[str]


@dataclasses.dataclass(kw_only=True, slots=True, frozen=True)
class HlrFailedResponse:
    msisdn: str = Field(alias='dnis')
    result: int
    message_id: str | None = None
    message: str | None
    provider: str
    http_error: int | None = None


def convert_from_hlr_error(
        error: HlrVendorNotFoundError | HlrProxyError,
        msisdn: str,
        provider: str,
) -> HlrFailedResponse:
    return HlrFailedResponse(
        msisdn=msisdn,
        provider=provider,
        message_id=error.message_id,
        result=error.result,
        message=error.message,
    )


def convert_from_hlr_http_error(
        error: HlrClientHTTPError,
        msisdn: str,
        provider: str,
) -> HlrFailedResponse:
    return HlrFailedResponse(
        msisdn=msisdn,
        provider=provider,
        result=-8,
        message='Internal HTTP error',
        http_error=error.error_code,
    )


def convert_from_hlr_failed_response(
        error: HlrClientError,
        msisdn: str,
        provider: str,
) -> HlrFailedResponse:
    return HlrFailedResponse(
        msisdn=msisdn,
        provider=provider,
        result=-9,
        message=str(error),
    )


def handle_task(
        task: Task,
        hlr_client: HlrClient,
) -> tuple[list[HlrResponse], list[HlrFailedResponse]]:
    details, errors = [], []
    try:
        msisdn_info = hlr_client.get_mccmnc_info(msisdn=task.msisdn, provider=task.provider)
        details.append(msisdn_info)
    except HlrClientError as error:
        failed_response = handle_client_error(error, msisdn=task.msisdn, provider=task.provider)
        errors.append(failed_response)

    return details, errors
