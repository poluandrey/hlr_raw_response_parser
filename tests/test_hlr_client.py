import httpx
import pytest

from hlr_client.client import HlrClient
from hlr_client.errors import HlrVendorNotFoundError


class MockHTTPXResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data

    def raise_for_status(self):
        pass
    def json(self):
        return self.json_data


@pytest.fixture
def mock_hlr_response():
    # Create a mock response similar to the actual response
    mock_response_data = {
        "message_id": "befa5ba6-f50b-42ab-9e35-c83557731fd8",
        "result": -2,
        "ported": 0,
        "message": "Vendor not found",
        "dnis": "7911036721995",
        "cached": 0,
        "login": "alaris",
        "context_log": "..."
    }
    return MockHTTPXResponse(200, mock_response_data)

def test__HlrClient_get_mccmnc_info__raise_error_when_vendor_nod_found(mock_hlr_response):
    login = "your_login"
    password = "your_password"
    base_url = "http://example.com/api/"
    provider = "provider_name"
    msisdn = "7911036721995"

    hlr_client = HlrClient(login, password, base_url)
    hlr_client.session = httpx.Client()

    def mock_get(url, params):
        return mock_hlr_response

    hlr_client.session.get = mock_get

    with pytest.raises(HlrVendorNotFoundError):
        hlr_client.get_mccmnc_info(provider, msisdn)


def test__HlrClient_get_mccmnc_info__HlrVendorNotFoundError_contain_additional_info(mock_hlr_response):
    login = "your_login"
    password = "your_password"
    base_url = "http://example.com/api/"
    provider = "provider_name"
    msisdn = "7911036721995"

    hlr_client = HlrClient(login, password, base_url)
    hlr_client.session = httpx.Client()

    def mock_get(url, params):
        return mock_hlr_response

    hlr_client.session.get = mock_get
    try:
        hlr_client.get_mccmnc_info(provider, msisdn)
    except HlrVendorNotFoundError as error:
        assert error.msisdn == '7911036721995'
        assert error.result == -2
        assert error.message_id is not None
        assert error.message == 'Vendor not found'



