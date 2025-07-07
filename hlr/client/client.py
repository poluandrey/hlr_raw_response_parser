from typing import Any, Optional
from asyncio import Semaphore

import httpx

from hlr.client.errors import (HlrClientError, HlrClientHTTPError,
                               HlrProxyInternalError, HlrVendorNotFoundError)
from hlr.client.schemas import HlrResponse

sem = Semaphore(10)


def handle_hlr_response(hlr_response: dict[str, Any]) -> HlrResponse:
    return HlrResponse(**hlr_response)

    # if hlr_resp_result == -2:
    #     raise HlrVendorNotFoundError(
    #         message=hlr_response['message'],
    #         result=hlr_resp_result,
    #         message_id=hlr_response['message_id'],
    #     )
    #
    # message = hlr_response.get('message')
    # if not message:
    #     message = hlr_response.get('failed_response')
    #
    # raise HlrProxyInternalError(
    #     msisdn=hlr_response.get('dnis'),
    #     message=message,
    #     result=hlr_resp_result,
    #     message_id=hlr_response['message_id'],
    #     provider=hlr_response['source_name']
    # )


class HlrClient:

    def __init__(self, login: str, password: str, base_url: str) -> None:
        self.limits = httpx.Limits(max_connections=None, max_keepalive_connections=None, keepalive_expiry=None)
        self.request_params: dict[str, str] = {
            'login': login,
            'password': password,
            'debug': '1',
        }
        self.client = httpx.AsyncClient(
            base_url=base_url,
            params=self.request_params,
            limits=self.limits
        )

    async def send_mccmnc_request(self,
                                  provider: str,
                                  msisdn: str,
                                  ):
        async with sem:
            timeout = httpx.Timeout(connect=5.0, read=15.0, write=10.0, pool=5.0)
            print(f'msisdn: {msisdn}')
            params = {'dnis': msisdn, 'source_name': provider}
            resp = await self.client.get('mccmnc_request', params=params, timeout=timeout)
            print(resp)
            return resp

    async def get_mccmnc_info(
            self,
            provider: str,
            msisdn: str,
            task_detail_id: Optional[int] = None,
    ) -> HlrResponse:
        resp = await self.send_mccmnc_request(provider=provider, msisdn=msisdn)
        resp.raise_for_status()
        hlr_resp = resp.json()
        return HlrResponse(task_detail_id=task_detail_id, **hlr_resp)
