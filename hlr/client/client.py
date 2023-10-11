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
        message = hlr_response.get('error')

    raise HlrProxyInternalError(
        message=message,
        result=hlr_resp_result,
        message_id=hlr_response['message_id'],
    )




class HlrClient:

    def __init__(self, login: str, password: str, base_url: str) -> None:
        self.request_params: dict[str, str] = {
            'login': login,
            'password': password,
            'debug': '1',
        }
        self.client = httpx.Client(
            base_url=base_url,
            params=self.request_params,
        )

    def get_mccmnc_info(
            self,
            provider: str,
            msisdn: str,
    ) -> HlrResponse:
        params = {'dnis': msisdn, 'source_name': provider}
        try:
            with self.client as s:
                resp = s.get('mccmnc_request', params=params)
                resp.raise_for_status()
                hlr_resp = resp.json()
                return handle_hlr_response(hlr_resp)
        except httpx.HTTPStatusError as error:
            raise HlrClientHTTPError(
                error_code=error.response.status_code,
            ) from error
        except httpx.HTTPError as error:
            raise HlrClientError from error
