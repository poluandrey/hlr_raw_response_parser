import pytest
import respx

from alaris.enterprise_api.errors import InvalidRequestBody


@pytest.mark.parametrize('request_type, expected_result',
                         [
                             ('get_carrier_list', True)
                         ],

                         )
def test__validate_request_body__return_true_for_valid_body(
        enterprise_client,
        make_enterprise_api_body,
        request_type,
        expected_result
):
    body = make_enterprise_api_body(request_type=request_type, valid=True)
    assert enterprise_client.validate_request_body(body=body) == expected_result





@pytest.mark.parametrize('request_type, valid',
                         [
                             ('get_carrier_list', False)
                         ],
                         )
def test__validate_request_body__raise_error_if_request_body_is_not_valid(
        enterprise_client,
        make_enterprise_api_body,
        request_type,
        valid,
):
    body = make_enterprise_api_body(request_type=request_type, valid=valid)
    with pytest.raises(InvalidRequestBody):
        enterprise_client.validate_request_body(body=body)



def test__get_carrier__if_response_was_successful_return_list_of_carriers(
        make_enterprise_api_response,
        enterprise_client,
        make_enterprise_api_body
):
    body = make_enterprise_api_body(request_type='get_carrier_list')
    response = make_enterprise_api_response(response_type='carrier_list')
    with respx.mock():
        respx.post('https://example.com/eapi').respond(
            json=response,
            status_code=200
        )
        carriers = enterprise_client.get_carrier(payload=body)

        assert isinstance(carriers, list)