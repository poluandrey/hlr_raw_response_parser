import dataclasses
import os
from typing import Any
from urllib.parse import urljoin

import requests
from dotenv import load_dotenv

load_dotenv()

HLR_SERVICE_URL = os.getenv('HLR_SERVICE_BASE_URL')
HLR_SERVICE_LOGIN = os.getenv('HLR_SERVICE_LOGIN')
HLR_SERVICE_PASSWORD = os.getenv('HLR_SERVICE_PASSWORD')

if not all([HLR_SERVICE_URL, HLR_SERVICE_PASSWORD, HLR_SERVICE_LOGIN]):
    raise OSError('Not all environment variables specify')


@dataclasses.dataclass(kw_only=True, slots=True, frozen=True)
class HlrSuccessfulResponse:
    message_id: str
    msisdn: str
    provider: str | None
    mccmnc: str | None
    result: int
    ported: int | None
    cached: int | None
    context_log: str | None


@dataclasses.dataclass(kw_only=True, slots=True, frozen=True)
class HlrFailedResponse:
    msisdn: str
    provider: str
    http_error_code: int


@dataclasses.dataclass(kw_only=True, slots=True, frozen=True)
class Task:
    providers: list[str]
    msisdns: list[str]


class HlrApiClient:

    def __init__(self):
        self.payload = {
            'login': HLR_SERVICE_LOGIN,
            'password': HLR_SERVICE_PASSWORD,
            'debug': 1,
        }

    def send_mccmnc_request(
            self,
            provider: str,
            msisdn: str,
            session: requests.Session,
    ) -> dict[str, Any]:
        url = urljoin(HLR_SERVICE_URL, 'hlr/mccmnc_request')
        payload = {'dnis': msisdn, 'source_name': provider, **self.payload}
        with session as s:
            resp = s.get(url, params=payload)
            resp.raise_for_status()

        return resp.json()


class HlrSuccessfulResponseParser:

    def parse_response(self, resp: dict[str, Any]) -> HlrSuccessfulResponse:
        try:
            message_id = resp['message_id']
            msisdn = resp['dnis']
            source_name = resp.get('source_name')
            mccmnc = resp.get('mccmnc')
            result = resp['result']
            ported = resp.get('ported')
            cached = resp.get('ported')
            context_log = resp.get('context_log')

            return HlrSuccessfulResponse(
                message_id=message_id,
                mccmnc=mccmnc,
                msisdn=msisdn,
                provider=source_name,
                result=result,
                ported=ported,
                cached=cached,
                context_log=context_log,
            )
        except KeyError as error:
            raise error


class TaskHandler:

    def __init__(self, task: Task):
        self.task = task
        self.session = requests.Session()

    def handle_task(self) -> list[HlrSuccessfulResponse | HlrFailedResponse]:
        task_results: list[HlrSuccessfulResponse | HlrFailedResponse] = []
        api_client = HlrApiClient()
        params = (
            (msisdn, provider) for msisdn in self.task.msisdns
            for provider in self.task.providers
        )
        for msisdn, provider in params:
            try:
                resp = api_client.send_mccmnc_request(
                    msisdn=msisdn,
                    provider=provider,
                    session=self.session,
                )
                task_results.append(
                    HlrSuccessfulResponseParser().parse_response(
                        resp=resp,
                    ),
                )
            except requests.HTTPError as error:
                task_results.append(
                    HlrFailedResponse(
                        msisdn=msisdn,
                        provider=provider,
                        http_error_code=error.response.status_code,
                    ),
                )

        return task_results
