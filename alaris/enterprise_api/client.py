from typing import Any

import httpx
import pydantic
from httpx import HTTPStatusError

from alaris.enterprise_api.errors import InvalidRequestBody
from alaris.enterprise_api.schema import (ResponseCarrierListBase, ResponseErrorBase,
                                          RequestCarrierFilterArgs, RequestBody, ResponseCarrier)


class EnterpriseApiClient:

    def __init__(self, url: str) -> None:
        self.client = httpx.Client()
        self.url = url

    def validate_request_body(
            self,
            body: dict[str, Any],
    ) -> bool:
        try:
            RequestBody(**body)
            return True
        except pydantic.ValidationError as error:
            raise InvalidRequestBody from error

    def get_carrier(
            self,
            payload: dict[str, Any],
    ) -> list[ResponseCarrier] | ResponseErrorBase:
        if self.validate_request_body(payload):
            try:
                resp = self.client.post(url=self.url, json=payload)
                resp.raise_for_status()
            except HTTPStatusError as error:
                raise error

        resp_json = resp.json()

        if 'error' in resp_json.keys():
            return ResponseErrorBase(**resp_json)

        return ResponseCarrierListBase(**resp_json).result.data


