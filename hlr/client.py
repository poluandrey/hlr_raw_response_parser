import dataclasses

import httpx
from pydantic import BaseModel, Field

from hlr.client_errors import (HlrClientError, HlrClientHTTPError,
                               HlrProxyInternalError, HlrVendorNotFoundError)


class HlrResponse(BaseModel):
    message_id: str
    msisdn: str = Field(alias='dnis')
    source_name: str
    mccmnc: str
    result: int
    ported: int
    cached: int
    context_log: str
    message: str


@dataclasses.dataclass(kw_only=True, slots=True, frozen=True)
class HlrFailedResponse:
    msisdn: str = Field(alias='dnis')
    result: int
    message_id: str | None = None
    message: str
    provider: str
    http_error: int | None = None


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
                hlr_resp_result = hlr_resp['result']
                if hlr_resp_result == 0:
                    return HlrResponse(**hlr_resp)

                if hlr_resp_result == -2:
                    raise HlrVendorNotFoundError(
                        message=hlr_resp['message'],
                        result=hlr_resp_result,
                        message_id=hlr_resp['message_id'],
                    )

                message = hlr_resp.get('message')
                if not message:
                    message = hlr_resp.get('error')

                raise HlrProxyInternalError(
                    message=message,
                    result=hlr_resp_result,
                    message_id=hlr_resp['message_id'],
                )
        except httpx.HTTPStatusError as error:
            raise HlrClientHTTPError(
                error_code=error.response.status_code,
            ) from error
        except httpx.HTTPError as error:
            raise HlrClientError from error
