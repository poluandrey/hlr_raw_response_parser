import dataclasses
import uuid
from dataclasses import dataclass
from itertools import product
from typing import Generator

from django.conf import settings

from celery import shared_task
from pydantic import Field

from alaris.models import Product
from hlr.models import TaskDetail, Task as DbTask
from hlr.parser.context_log_parser import parse_context_log
from hlr.parser.hlr_parser import create_parser, HlrParserType, MsisdnInfo
from hlr.client.errors import (HlrClientError, HlrClientHTTPError,
                               HlrProxyError, HlrVendorNotFoundError)
from hlr.client.client import HlrClient


@dataclass(kw_only=True, frozen=True, slots=True)
class Task:
    provider_name: str
    provider_type: str
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
        message='Internal HTTP failed_response',
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
) -> tuple[MsisdnInfo | None, HlrFailedResponse | None]:
    msisdn_info, hlr_error = None, None
    try:
        hlr_response = hlr_client.get_mccmnc_info(msisdn=task.msisdn, provider=task.provider_name)
        parser = create_parser(HlrParserType[task.provider_type])
        context_log = parse_context_log(hlr_response.context_log)
        msisdn_info = parser.get_msisdn_info(context_log)
        msisdn_info.request_id = hlr_response.message_id if (
            hlr_response.message_id
        ) else str(uuid.uuid4())
    except HlrVendorNotFoundError as error:
        hlr_error = convert_from_hlr_error(error, msisdn=task.msisdn, provider=task.provider_name)
    except HlrProxyError as error:
        hlr_error = convert_from_hlr_error(error, msisdn=task.msisdn, provider=task.provider_name)
    except HlrClientHTTPError as error:
        hlr_error = convert_from_hlr_http_error(error,
                                                msisdn=task.msisdn,
                                                provider=task.provider_name,
                                                )

    return msisdn_info, hlr_error


@shared_task()
def celery_task_handler(task: DbTask,
                        msisdns: list[str],
                        hlr_products_external_id: list[str],
                        ) -> None:
    hlr_client = HlrClient(login=settings.HLR_LOGIN,
                           password=settings.HLR_PASSWORD,
                           base_url=settings.HLR_BASE_URL,
                           )
    hlr_products = Product.objects.select_related('hlr').filter(
        external_product_id__in=hlr_products_external_id,
    )
    hlr_task_data = product(msisdns, hlr_products)
    created_data = create_task_detail_and_hlr_task(hlr_task_data=hlr_task_data, task=task)
    for task_detail, hlr_task in created_data:
        msisdn_info, error = handle_task(hlr_task, hlr_client)
        if msisdn_info:
            insert_successful_check(msisdn_info, task_detail)

        if error:
            insert_failed_check(error, task_detail)

    return


def insert_failed_check(failed_response: HlrFailedResponse, task_detail: TaskDetail) -> None:
    task_detail.result = failed_response.result
    task_detail.message = failed_response.message
    task_detail.request_id = failed_response.message_id
    task_detail.http_error_code = failed_response.http_error
    task_detail.save()


def insert_successful_check(msisdn_info: MsisdnInfo, task_detail: TaskDetail) -> None:
    task_detail.result = 0
    task_detail.request_id = msisdn_info.request_id
    task_detail.mccmnc = msisdn_info.mccmnc
    task_detail.ported = msisdn_info.ported
    task_detail.roaming = msisdn_info.roaming
    task_detail.presents = msisdn_info.presents
    task_detail.save()


def create_task_detail_and_hlr_task(
        hlr_task_data: product, task: DbTask
) -> Generator[tuple[TaskDetail, Task], None, None]:
    for msisdn, hlr_product in hlr_task_data:
        task_detail = TaskDetail.objects.create(
            task=task,
            external_product_id=hlr_product,
            msisdn=msisdn,
        )
        hlr_task = Task(msisdn=msisdn,
                        provider_name=hlr_product.description,
                        provider_type=hlr_product.hlr.type,
                        )
        yield task_detail, hlr_task
