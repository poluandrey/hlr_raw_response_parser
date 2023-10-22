import dataclasses
from dataclasses import dataclass

from celery import shared_task
from pydantic import Field

from hlr.client.client import HlrResponse
from hlr.client.errors import (HlrClientError, HlrClientHTTPError,
                               HlrProxyError, HlrVendorNotFoundError)
from hlr.client.client import HlrClient


@dataclass(kw_only=True, frozen=True, slots=True)
class Task:
    provider: str
    msisdn: str


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
    except HlrVendorNotFoundError as error:
        errors.append(convert_from_hlr_error(error, msisdn=task.msisdn, provider=task.provider))
    except HlrProxyError as error:
        errors.append(convert_from_hlr_error(error, msisdn=task.msisdn, provider=task.provider))
    except HlrClientHTTPError as error:
        errors.append(convert_from_hlr_http_error(error, msisdn=task.msisdn, provider=task.provider))

    return details, errors

@shared_task()
def celery_task_handler(task: Task):
    hlr_client = HlrClient(login='alaris', password='alaris', base_url='https://hlr.lancktele.com/hlr')
    detail, error = handle_task(task, hlr_client)
    print(detail, error)
    return handle_task(task, hlr_client)
