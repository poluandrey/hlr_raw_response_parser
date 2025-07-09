import uuid
from datetime import date
from typing import Any

import httpx

from alaris.enterprise_api.errors import EnterpriseApiError
from alaris.enterprise_api.schema import JsonRpcResponse, Carrier, Product, Account, RecurringFee, RecurringFeePeriod


class EnterpriseClient:

    def __init__(self, base_url: str, auth: str) -> None:
        self.client = httpx.Client(base_url=base_url)
        self.enterprise_cursor = EnterpriseCursor(client=self.client, auth=auth)
        self.enterprise_auto = EnterpriseAuto(client=self.client, auth=auth)
        self.carrier = CarrierClient(enterprise_cursor=self.enterprise_cursor)
        self.product = ProductClient(enterprise_cursor=self.enterprise_cursor)
        self.account = AccountClient(enterprise_cursor=self.enterprise_cursor)
        self.recurring_fee = RecurringFeeClient(enterprise_cursor=self.enterprise_cursor)
        self.recurring_fee_period = RecurringFeePeriodClient(enterprise_cursor=self.enterprise_auto)


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


class EnterpriseAuto:

    def __init__(self, client: httpx.Client, auth: str) -> None:
        self.client = client
        self.auth = auth

    def exec(self, method: str, params: dict[str, Any]) -> JsonRpcResponse:
        body = {
            'id': str(uuid.uuid4()),
            'jsonrpc': '2.0',
            'method': 'Enterprise.Auto',
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


class ProductClient:

    def __init__(self, enterprise_cursor: EnterpriseCursor) -> None:
        self.cursor = enterprise_cursor

    def get_all(self, product_type: str = 'hlr', product_direction: int = 1) -> list[Product]:
        payload = self.cursor.exec(
            method='get_product_list',
            params={
                'type': product_type,
                'direction': product_direction,
            },
        )
        return [Product(**product) for product in payload.result.data]


class AccountClient:

    def __init__(self, enterprise_cursor: EnterpriseCursor) -> None:
        self.cursor = enterprise_cursor

    def get_all(self, ) -> list[Account]:
        payload = self.cursor.exec(
            method='get_account_list',
            params={

            },
        )
        return [Account(**account) for account in payload.result.data]


class RecurringFeeClient:

    def __init__(self, enterprise_cursor: EnterpriseCursor) -> None:
        self.cursor = enterprise_cursor

    def get_all(self, acc_id: int, start_date1: date, start_date2: date, end_date1: date, end_date2: date) -> list[RecurringFee]:
        params = {'acc_id': acc_id}

        if start_date1:
            params['start_date1'] = start_date1.strftime('%Y.%m.%d')

        if start_date2:
            params['start_date2'] = start_date2.strftime('%Y.%m.%d')

        if end_date1:
            params['end_date1'] = end_date1.strftime('%Y.%m.%d')

        if end_date2:
            params['end_date2'] = end_date2.strftime('%Y.%m.%d')

        payload = self.cursor.exec(
            method='get_recur_fee_list',
            params=params,
        )
        print(params)
        return [RecurringFee(**recurring_fee) for recurring_fee in payload.result.data]


class RecurringFeePeriodClient:

    def __init__(self, enterprise_cursor: EnterpriseAuto) -> None:
        self.cursor = enterprise_cursor

    def get_period_list(self, id: int) -> list[RecurringFeePeriod]:
        params = {'subscr_id': id}

        payload = self.cursor.exec(
            method='get_recur_fee_period_list',
            params=params,
        )
        return [RecurringFeePeriod(**period) for period in payload.result.data]
