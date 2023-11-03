import uuid
from typing import Any

import httpx

from alaris.enterprise_api.errors import EnterpriseApiError
from alaris.enterprise_api.schema import JsonRpcResponse, Carrier


class EnterpriseClient:

    def __init__(self, base_url: str, auth: str) -> None:
        self.client = httpx.Client(base_url=base_url)
        self.enterprise_cursor = EnterpriseCursor(client=self.client, auth=auth)
        self.carrier = CarrierClient(enterprise_cursor=self.enterprise_cursor)


class EnterpriseCursor:

    def __init__(self, client: httpx.Client, auth: str) -> None:
        self.client = client
        self.auth = auth

    def exec(self, method: str, params: dict[str, Any]) -> JsonRpcResponse:
        body = {
            'id': str(uuid.uuid4()),
            'jsonrpc': '2.0',
            'method': 'Enterprise.Cursor',
            'params': {
                'name': method,
                'args': params,
                'auth': self.auth,
            },
        }
        try:
            resp = self.client.post(json=body, url='eapi/')
            resp.raise_for_status()
            payload = resp.json()
            result = JsonRpcResponse(**payload)

            if result.error:
                raise EnterpriseApiError(code=result.error.code, message=result.error.message)

            return result
        except httpx.HTTPStatusError as error:
            raise error


class CarrierClient:

    def __init__(self, enterprise_cursor: EnterpriseCursor) -> None:
        self.cursor = enterprise_cursor

    def get_all(self,
                car_id: int = None,
                car_inbound_allowed: bool = None,
                car_outbound_allowed: bool = None,
                ) -> list[Carrier]:
        inbound_allowed = int(car_inbound_allowed) if car_inbound_allowed in [True, False] else car_inbound_allowed
        outbound_allowed = int(car_outbound_allowed) if car_outbound_allowed in [True, False] else car_outbound_allowed
        payload = self.cursor.exec(
            method='get_carrier_list',
            params={
                'car_id': car_id,
                'car_inbound_allowed': inbound_allowed,
                'car_outbound_allowed': outbound_allowed,
            },
        )
        return [Carrier(**carrier) for carrier in payload.result.data]
