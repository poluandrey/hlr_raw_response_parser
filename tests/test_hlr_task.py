from unittest import mock

from hlr.client.errors import HlrVendorNotFoundError
from hlr.tasks import handle_task, create_task_detail_and_hlr_task, insert_successful_check, insert_failed_check


def test__handle_task__valid_client_response_was_append_correctly(
        hlr_client,
        hlr_task,
        hlr_response_successful,
):
    with mock.patch('hlr.client.client.HlrClient.get_mccmnc_info') as get_mccmnc_info_mock:
        get_mccmnc_info_mock.return_value = hlr_response_successful
        task_result = handle_task(hlr_client=hlr_client, task=hlr_task)
        successful, fail = task_result

        assert successful
        assert fail is None


def test__handle_task__invalid_client_response_was_append_correctly(
        hlr_client,
        hlr_task,
):
    with mock.patch('hlr.client.client.HlrClient.get_mccmnc_info') as get_mccmnc_info_mock:
        get_mccmnc_info_mock.side_effect = HlrVendorNotFoundError(result=-2, message='test', message_id='test')
        task_result = handle_task(hlr_client=hlr_client, task=hlr_task)
        successful, fail = task_result

        assert successful is None
        assert fail


def test__create_task_detail_and_hlr_task__create_correct_count_of_detail_task_and_task(task, make_hlr_task_data):
    created_data = list(create_task_detail_and_hlr_task(task=task, hlr_task_data=make_hlr_task_data(msisdn_count=3)))
    assert len(created_data) == 3


def test__insert_successful_check__insert_data_correctly(successfully_handled_response, task_detail):
    insert_successful_check(msisdn_info=successfully_handled_response, task_detail=task_detail)
    assert task_detail.result == 0
    assert task_detail.mccmnc == successfully_handled_response.mccmnc
    assert task_detail.ported == successfully_handled_response.ported
    assert task_detail.presents == successfully_handled_response.presents


def test__insert_failed_check__insert_data_correctly(failed_handled_response, task_detail):
    insert_failed_check(failed_response=failed_handled_response, task_detail=task_detail)
    assert task_detail.ported is None
    assert task_detail.mccmnc is None
    assert task_detail.result == failed_handled_response.result
    assert task_detail.presents is None
    assert task_detail.request_id == failed_handled_response.message_id
    assert task_detail.message == failed_handled_response.message
    assert task_detail.http_error_code == failed_handled_response.http_error

