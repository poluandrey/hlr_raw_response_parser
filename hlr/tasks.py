import dataclasses
import uuid
from dataclasses import dataclass
from itertools import product
from typing import Generator
import asyncio

from django.conf import settings

from celery import shared_task
from pydantic import Field

from alaris.models import Product
from hlr.client.schemas import HlrResponse
from hlr.models import TaskDetail, Task as DbTask
from hlr.parser.context_log_parser import parse_context_log
from hlr.parser.errors import ContextLogParserError
from hlr.parser.hlr_parser import create_parser, HlrParserType, MsisdnInfo
from hlr.client.errors import (HlrClientError, HlrClientHTTPError,
                               HlrProxyError, HlrVendorNotFoundError, HlrProxyInternalError)
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


async def handle_task(
        tasks: list[Task],
        hlr_client: HlrClient,
) -> list[tuple[tuple[MsisdnInfo | None, HlrParserType | None], HlrFailedResponse | None]]:
    response = []
    results = await asyncio.gather(
        *(hlr_client.get_mccmnc_info(msisdn=task.msisdn, provider=task.provider_name) for task in tasks),
        return_exceptions=True,
    )
    print(results)
    for result in results:
        print(result)
        msisdn_info, hlr_error = None, None
        if isinstance(result, HlrResponse):
            try:
                parser = create_parser(HlrParserType[result.source_name.upper()])
                context_log = parse_context_log(result.context_log)
                msisdn_info = parser.get_msisdn_info(context_log)
                msisdn_info.request_id = result.message_id if (
                    result.message_id
                ) else str(uuid.uuid4())
            except HlrVendorNotFoundError as error:
                pass
                hlr_error = convert_from_hlr_error(error, msisdn=result.msisdn, provider=result.provider_name)
            except HlrProxyError as error:
                hlr_error = convert_from_hlr_error(error, msisdn=result.msisdn, provider=result.provider_name)
            except HlrClientHTTPError as error:
                hlr_error = convert_from_hlr_http_error(error,
                                                        msisdn=result.msisdn,
                                                        provider=result.provider_name,
                                                        )
            response.append(((msisdn_info, HlrParserType[result.source_name.upper()]), hlr_error))
        elif isinstance(result, HlrProxyInternalError):
            hlr_error = HlrFailedResponse(
                msisdn=result.msisdn,
                result=result.result,
                message_id=result.message_id,
                http_error=result.result,
                message=result.message,
                provider=result.provider,
            )
            response.append(((msisdn_info, None), hlr_error))

    return response


@shared_task()
def celery_task_handler(task_id: int,
                        msisdns: list[str],
                        hlr_products_external_id: list[int],
                        ) -> None:
    hlr_client = HlrClient(login=settings.HLR_LOGIN,
                           password=settings.HLR_PASSWORD,
                           base_url=settings.HLR_BASE_URL,
                           )
    main_task = DbTask.objects.get(pk=task_id)
    main_task.in_progress()
    main_task.save()

    hlr_sources = Product.objects.filter(pk__in=hlr_products_external_id)
    task_details = product(msisdns, hlr_sources)
    loop = asyncio.get_event_loop()
    hlr_tasks = []
    hlr_task_details = []
    for msisdn, hlr_source in task_details:
        task = TaskDetail.objects.create(
            task=main_task,
            product=hlr_source,
            msisdn=msisdn,
        )
        hlr_task = Task(msisdn=msisdn,
                        provider_name=hlr_source.description,
                        provider_type=hlr_source.hlr.type,
                        )
        hlr_tasks.append(hlr_task)

        task.in_progress()
        task.save()
        hlr_task_details.append(task)

    handled_tasks = loop.run_until_complete(handle_task(hlr_tasks, hlr_client))
    print(handled_tasks)
    for result in handled_tasks:
        print(result)
        try:
            msisdn_info, error = result
        except ContextLogParserError:
            # need to add logging
            main_task.ready()
            main_task.save()
            return
        if error:
            print(error)
            detail = [
                task for task in hlr_task_details if
                task.msisdn == error.msisdn and task.product.description == error.provider
            ][0]
            insert_failed_check(error, detail)
            detail.failed()
            detail.save()
            continue


        detail = [
            task for task in hlr_task_details if
            task.msisdn == msisdn_info[0].msisdn and task.product.description == msisdn_info[1].name.lower()
        ][0]
        insert_successful_check(msisdn_info[0], detail)
        detail.ready()
        detail.save()

    main_task.ready()
    main_task.save()


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
        hlr_task_data: product,
        task: DbTask,
) -> Generator[tuple[TaskDetail, Task], None, None]:
    for msisdn, hlr_product in hlr_task_data:
        task_detail = TaskDetail.objects.create(
            task=task,
            external_product_id=hlr_product.product,
            msisdn=msisdn,
        )
        hlr_task = Task(msisdn=msisdn,
                        provider_name=hlr_product.product.description,
                        provider_type=hlr_product.product.type,
                        )
        yield task_detail, hlr_task
