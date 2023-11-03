import pytest
import respx
from httpx import HTTPStatusError

from alaris.enterprise_api.errors import EnterpriseApiError
from alaris.enterprise_api.schema import JsonRpcResponse, Carrier


def test__enterprise_cursor_exec__raise_error_if_response_contain_error(enterprise_client, faker, make_enterprise_api_response):
    payload = make_enterprise_api_response(method=faker.pystr(), is_successfully=False)

    with respx.mock:
        respx.post('https://eapi.lancktele.com/eapi/').respond(status_code=200, json=payload)
        with pytest.raises(EnterpriseApiError):
            enterprise_client.enterprise_cursor.exec(method=faker.pystr(), params={})


def test__enterprise_cursor_exec__raise_http_error(enterprise_client, faker):
    with respx.mock:
        respx.post('https://eapi.lancktele.com/eapi/').respond(status_code=404)
        with pytest.raises(HTTPStatusError):
            enterprise_client.enterprise_cursor.exec(method=faker.pystr(), params={})


def test__enterprise_cursor_exec__return_jsonrps_response_(enterprise_client, faker, make_enterprise_api_response):
    payload = make_enterprise_api_response(method='any_valid_method')
    with respx.mock:
        respx.post('https://eapi.lancktele.com/eapi/').respond(status_code=200, json=payload)

        result = enterprise_client.enterprise_cursor.exec(method=faker.pystr(), params={})

        assert isinstance(result, JsonRpcResponse)


def test__carrier_client_get_all__return_list_of_carriers(
        enterprise_client,
        make_exec_response,
        mock_enterprise_cursor_exec,
):
    payload = make_exec_response(method='get_carrier_list')
    mock_enterprise_cursor_exec.return_value = payload

    results = enterprise_client.carrier.get_all()

    assert isinstance(results, list)
    assert all([isinstance(carrier, Carrier) for carrier in results])
