import dataclasses
from dataclasses import dataclass
from itertools import product

from pydantic import Field

from hlr.client.client import HlrClient
from hlr.client.errors import (HlrClientError, HlrClientHTTPError,
                               HlrProxyError, HlrVendorNotFoundError)
from hlr.client.schemas import HlrResponse


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
    for msisdn, provider in product(task.msisdns, task.providers):
        try:
            msisdn_info = hlr_client.get_mccmnc_info(msisdn=msisdn, provider=provider)
            details.append(msisdn_info)
        except HlrVendorNotFoundError as error:
            errors.append(convert_from_hlr_error(error, msisdn=msisdn, provider=provider))
        except HlrProxyError as error:
            errors.append(convert_from_hlr_error(error, msisdn=msisdn, provider=provider))
        except HlrClientHTTPError as error:
            errors.append(convert_from_hlr_http_error(error, msisdn=msisdn, provider=provider))

    return details, errors
