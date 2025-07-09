import dataclasses
import json
import uuid
from dataclasses import dataclass
from itertools import product
from typing import Generator, Optional
import asyncio

import django_fsm
from django.conf import settings

from celery import shared_task
from pydantic import Field, BaseModel, ConfigDict

from alaris.models import Product
from hlr.client.schemas import HlrResponse
from hlr.models import TaskDetail, Task as DbTask
from hlr.parser.errors import ContextLogParserError
from hlr.parser.hlr_parser import create_parser, HlrParserType, MsisdnInfo
from hlr.client.errors import (HlrClientError, HlrClientHTTPError,
                               HlrProxyError, HlrVendorNotFoundError, HlrProxyInternalError)
from hlr.client.client import HlrClient


@dataclass(kw_only=True, frozen=True, slots=True)
class Task:
    # cхема для отправки запроса на проверку в аларис
    provider_name: str
    provider_type: str
    msisdn: str
    task_detail_id: Optional[int] = None


@dataclasses.dataclass(kw_only=True, slots=True, frozen=True)
class HlrFailedResponse:
    msisdn: str = Field(alias='dnis')
    result: int
    message_id: str | None = None
    message: str | None
    provider: str
    http_error: int | None = None


class DetailTaskResult(BaseModel):
    # cхема для хранения детального таска
    # model_config = ConfigDict(extra='ignore')

    task_id: int
    result: Optional[int] = None
    msisdn: str
    mccmnc: Optional[str] = None
    ported: Optional[bool] = None
    roaming: Optional[bool] = None
    presents: Optional[bool] = None
    message: Optional[str] = None
    request_id: Optional[str] = None





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
) -> list[DetailTaskResult]:
    response = []
    results: list[HlrResponse] = await asyncio.gather(
        *(hlr_client.get_mccmnc_info(task_detail_id=task.task_detail_id, msisdn=task.msisdn, provider=task.provider_name) for task in tasks),
        return_exceptions=True,
    )
    # проходим по результатам проверки через аларис
    for result in results:
        print(result)
        try:
            if result.result == 0:
                source = result.source_name.upper()

                if source == '3GTELECOM_HLR':
                    source = 'G_TELECOM_HLR'

                parser = create_parser(HlrParserType[source])

                try:
                    raw_response = json.loads(result.raw_response)
                except json.decoder.JSONDecodeError:
                    # в случае подключения по ENUM ответ может быть не сериализуем
                    raw_response = result.raw_response


                msisdn_info = parser.get_msisdn_info(raw_response)
                if not msisdn_info.msisdn:
                    msisdn_info.msisdn = result.msisdn

                msisdn_info.request_id = result.message_id if (
                    result.message_id
                ) else str(uuid.uuid4())
                detail_result = DetailTaskResult(task_id=result.task_detail_id, result=result.result, **msisdn_info.model_dump(exclude={'context_log'}))
            else:
                detail_result = DetailTaskResult(
                    task_id=result.task_detail_id,
                    result=result.result,
                    msisdn=result.msisdn,
                    message=result.message,
                )
            response.append(detail_result)
        except:
            print(results)
    return response


@shared_task()
def celery_task_handler(task_id: int,
                        msisdns: list[str],
                        hlr_products_external_id: list[int],
                        ) -> None:
    # создаем хттп клиента
    hlr_client = HlrClient(login=settings.HLR_LOGIN,
                           password=settings.HLR_PASSWORD,
                           base_url=settings.HLR_BASE_URL,
                           )
    # создаем главный таск
    main_task = DbTask.objects.get(pk=task_id)
    main_task.in_progress()
    main_task.save()

    hlr_sources = Product.objects.filter(pk__in=hlr_products_external_id)
    task_details = product(msisdns, hlr_sources)
    loop = asyncio.get_event_loop()
    hlr_tasks = []
    hlr_task_details = []
    # проходим по связкам тел. номер + источник
    for msisdn, hlr_source in task_details:
        # создаем таск в базе
        task = TaskDetail.objects.create(
            task=main_task,
            product=hlr_source,
            msisdn=msisdn,
        )
        # схема для отправки запроса
        hlr_task = Task(msisdn=msisdn,
                        provider_name=hlr_source.description,
                        provider_type=hlr_source.hlr.type,
                        task_detail_id=task.id,
                        )
        hlr_tasks.append(hlr_task)

        task.in_progress()
        task.save()
        hlr_task_details.append(task)
    handled_tasks = loop.run_until_complete(handle_task(hlr_tasks, hlr_client))

    for task_detail in handled_tasks:
        task: TaskDetail = next(filter(lambda task: task.id == task_detail.task_id, hlr_task_details))
        task.message = task_detail.message
        task.mccmnc = task_detail.mccmnc
        task.msisdn = task_detail.msisdn
        task.result = task_detail.result
        task.ported = task_detail.ported
        task.presents = task_detail.presents

        if task.result == 0:
            task.ready()
        else:
            task.failed()
        task.save()

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
