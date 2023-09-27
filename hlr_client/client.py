import dataclasses

import httpx
from pydantic import BaseModel


class HlrSuccessfulResponse(BaseModel):
    message_id: str
    dnis: str
    source_name: str | None = None
    mccmnc: str | None = None
    result: int
    ported: int | None = None
    cached: int | None = None
    context_log: str | None = None


@dataclasses.dataclass(kw_only=True, slots=True, frozen=True)
class HlrFailedResponse:
    msisdn: str
    provider: str
    http_error_code: int | None


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
    ) -> HlrSuccessfulResponse | HlrFailedResponse:
        params = {'dnis': msisdn, 'source_name': provider}
        try:
            with self.session as s:
                resp = s.get('mccmnc_request', params=params)
                resp.raise_for_status()

            return HlrSuccessfulResponse(**resp.json())
        except httpx.HTTPStatusError as error:
            return HlrFailedResponse(
                msisdn=msisdn,
                provider=provider,
                http_error_code=error.response.status_code,
            )
        except httpx.HTTPError:
            # тут наверное должна логироваться ошибка
            return HlrFailedResponse(
                msisdn=msisdn,
                provider=provider,
                http_error_code=500,
            )
