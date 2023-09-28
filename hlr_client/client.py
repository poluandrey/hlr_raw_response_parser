import dataclasses

import httpx
from pydantic import BaseModel, Field

from hlr_client.errors import (HlrClientHTTPError, HlrClientInternalError,
                               HlrProxyInternalError, HlrVendorNotFoundError)


class HlrSuccessfulResponse(BaseModel):
    message_id: str
    msisdn: str = Field(alias='dnis')
    source_name: str | None = None
    mccmnc: str | None = None
    result: int
    ported: int | None = None
    cached: int | None = None
    context_log: str | None = None
    message: str | None = None


@dataclasses.dataclass(kw_only=True, slots=True, frozen=True)
class HlrFailedResponse:
    msisdn: str = Field(alias='dnis')
    result: int | None = None
    message_id: str | None = None
    message: str
    provider: str | None = None
    http_error: int | None = None


class HlrClient:

    def __init__(self, login: str, password: str, base_url: str) -> None:
        self.request_params: dict[str, str] = {
            'login': login,
            'password': password,
            'debug': '1',
        }
        self.session = httpx.Client(
            base_url=base_url,
            params=self.request_params,
        )

    def get_mccmnc_info(
            self,
            provider: str,
            msisdn: str,
    ) -> HlrSuccessfulResponse:
        params = {'dnis': msisdn, 'source_name': provider}
        try:
            with self.session as s:
                resp = s.get('mccmnc_request', params=params)
                resp.raise_for_status()
                hlr_resp = HlrSuccessfulResponse(**resp.json())
                if hlr_resp.result == 0:
                    return hlr_resp

                if hlr_resp.result == -2:
                    raise HlrVendorNotFoundError(
                        msisdn=hlr_resp.msisdn,
                        message=hlr_resp.message,
                        result=hlr_resp.result,
                        message_id=hlr_resp.message_id,
                    )
                raise HlrProxyInternalError(
                    msisdn=hlr_resp.msisdn,
                    message=hlr_resp.message,
                    result=hlr_resp.result,
                    message_id=hlr_resp.message_id,
                )
        except httpx.HTTPStatusError as error:
            raise HlrClientHTTPError(
                error_code=error.response.status_code,
            ) from error
        except httpx.HTTPError as error:
            # тут наверное должна логироваться ошибка
            raise HlrClientInternalError from error
