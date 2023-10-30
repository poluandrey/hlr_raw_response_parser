import pytest
import respx

from hlr.client.errors import (HlrClientHTTPError, HlrProxyInternalError,
                               HlrVendorNotFoundError)
from hlr.client.schemas import HlrResponse
from tests.raw_responses import valid_context_log_str


def test__hlr_client_get_mccmnc_info__raise_error_when_vendor_not_found(hlr_client,
                                                                        hlr_response_vendor_not_found):
    provider = 'provider_name'
    msisdn = '7911036721995'

    with respx.mock:
        respx.get('https://example.com/api/mccmnc_request').respond(json=hlr_response_vendor_not_found, status_code=200)

        with pytest.raises(HlrVendorNotFoundError):
            hlr_client.get_mccmnc_info(provider, msisdn)


def test__hlr_client_get_mccmnc_info__hlr_vendor_not_found_error_contain_additional_info(hlr_client,
                                                                                         hlr_response_vendor_not_found):
    provider = 'provider_name'
    msisdn = '7911036721995'

    with respx.mock:
        respx.get('https://example.com/api/mccmnc_request').respond(json=hlr_response_vendor_not_found, status_code=200)

        try:
            hlr_client.get_mccmnc_info(provider, msisdn)
        except HlrVendorNotFoundError as error:
            assert error.result == -2
            assert error.message_id is not None
            assert error.message == 'Vendor not found'


def test__hlr_client_get_mccmnc_info__return_hlr_response_instance(hlr_client,
                                                                   hlr_response_successful_for_tmt_hlr):
    provider = 'provider_name'
    msisdn = '7911036721995'

    with respx.mock:
        respx.get('https://example.com/api/mccmnc_request').respond(json=hlr_response_successful_for_tmt_hlr,
                                                                    status_code=200)

        hlr_response = hlr_client.get_mccmnc_info(provider, msisdn)
        assert isinstance(hlr_response, HlrResponse)


def test__hlr_client_get_mccmnc_info__hlr_response_contain_required_data(hlr_client,
                                                                         hlr_response_successful_for_tmt_hlr,
                                                                         ):
    provider = 'provider_name'
    msisdn = '7911036721995'

    with respx.mock:
        respx.get('https://example.com/api/mccmnc_request').respond(json=hlr_response_successful_for_tmt_hlr,
                                                                    status_code=200)

        hlr_response = hlr_client.get_mccmnc_info(provider, msisdn)
        assert hlr_response.msisdn == '79216503431'
        assert hlr_response.message_id == 'b13439c5-3811-40b4-a001-531892df114c'
        assert hlr_response.result == 0
        assert hlr_response.message == 'message'
        assert hlr_response.ported == 1
        assert hlr_response.source_name == 'tmt_hlr'
        assert hlr_response.cached == 0
        assert hlr_response.mccmnc == '250001'
        assert hlr_response.context_log == valid_context_log_str


def test__hlr_client_get_mccmnc_info__raise_internal_hlr_proxy_error(
        hlr_client,
        hlr_response_hlr_proxy_internal_error_contain_error,
):
    provider = 'provider_name'
    msisdn = '7911036721995'

    with respx.mock:
        respx.get('https://example.com/api/mccmnc_request').respond(json=hlr_response_hlr_proxy_internal_error_contain_error,
                                                                    status_code=200)

        with pytest.raises(HlrProxyInternalError):
            hlr_client.get_mccmnc_info(provider=provider, msisdn=msisdn)


def test__hlr_client_get_mccmnc_info__internal_hlr_proxy_error_contain_required_data_when_message_provided_in_response(
        hlr_client,
        hlr_response_hlr_proxy_internal_error_contain_message,
):
    provider = 'provider_name'
    msisdn = '7911036721995'

    with respx.mock:
        respx.get('https://example.com/api/mccmnc_request').respond(json=hlr_response_hlr_proxy_internal_error_contain_message,
                                                                    status_code=200)

        try:
            hlr_client.get_mccmnc_info(provider=provider, msisdn=msisdn)
        except HlrProxyInternalError as error:
            assert error.message == 'Invalid Number'
            assert error.message_id == 'fd161140-0ed5-44c5-a125-140a2d281e06'
            assert error.result == -1


def test__hlr_client_get_mccmnc_info__internal_hlr_proxy_error_contain_required_data_when_error_provided_in_response(
        hlr_client,
        hlr_response_hlr_proxy_internal_error_contain_error,
):
    provider = 'provider_name'
    msisdn = '7911036721995'

    with respx.mock:
        respx.get('https://example.com/api/mccmnc_request').respond(json=hlr_response_hlr_proxy_internal_error_contain_error,
                                                                    status_code=200)

        try:
            hlr_client.get_mccmnc_info(provider=provider, msisdn=msisdn)
        except HlrProxyInternalError as error:
            assert error.message == 'Empty vendor response: null'
            assert error.message_id == '8b582f81-6238-4f2d-bacf-8b50bcf6e09d'
            assert error.result == -3


def test__hlr_client_get_mccmnc_info__raise_hlr_client_http_error_when_response_code_not_2xx(hlr_client):
    provider = 'provider_name'
    msisdn = '79999999999'

    with respx.mock:
        respx.get('https://example.com/api/mccmnc_request').respond(status_code=500)
        with pytest.raises(HlrClientHTTPError):
            hlr_client.get_mccmnc_info(provider=provider, msisdn=msisdn)
