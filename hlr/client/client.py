from typing import Any

import httpx

from hlr.client.errors import (HlrClientError, HlrClientHTTPError,
                               HlrProxyInternalError, HlrVendorNotFoundError)
from hlr.client.schemas import HlrResponse


def handle_hlr_response(hlr_response: dict[str, Any]) -> HlrResponse:
    hlr_resp_result = hlr_response['result']
    if hlr_resp_result == 0:
        return HlrResponse(**hlr_response)

    if hlr_resp_result == -2:
        raise HlrVendorNotFoundError(
            message=hlr_response['message'],
            result=hlr_resp_result,
            message_id=hlr_response['message_id'],
        )

    message = hlr_response.get('message')
    if not message:
        message = hlr_response.get('failed_response')

    raise HlrProxyInternalError(
        msisdn=hlr_response.get('dnis'),
        message=message,
        result=hlr_resp_result,
        message_id=hlr_response['message_id'],
        provider=hlr_response['source_name']
    )


class HlrClient:

    def __init__(self, login: str, password: str, base_url: str) -> None:
        self.limits = httpx.Limits(max_connections=None, max_keepalive_connections=None)
        self.request_params: dict[str, str] = {
            'login': login,
            'password': password,
            'debug': '1',
        }
        self.client = httpx.AsyncClient(
            base_url=base_url,
            params=self.request_params,

        )

    async def send_mccmnc_request(self,
                                  provider: str,
                                  msisdn: str,
                                  ):
        params = {'dnis': msisdn, 'source_name': provider}
        return await self.client.get('mccmnc_request', params=params)

    async def get_mccmnc_info(
            self,
            provider: str,
            msisdn: str,
    ) -> HlrResponse:
        try:
            resp = await self.send_mccmnc_request(provider=provider, msisdn=msisdn)
            resp.raise_for_status()
            hlr_resp = resp.json()
            return handle_hlr_response(hlr_resp)
        except httpx.HTTPStatusError as error:
            print(error)
            raise HlrClientHTTPError(
                error_code=error.response.status_code,
            ) from error
        except httpx.HTTPError as error:
            print(error)
            raise HlrClientError from error
        except HlrProxyInternalError as error:
            print(error)
