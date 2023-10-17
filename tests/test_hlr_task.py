from unittest import mock

from hlr.client.errors import HlrVendorNotFoundError
from hlr.tasks import handle_task


def test__handle_task__task_with_empty_fields(hlr_task_empty, hlr_client):
    assert handle_task(task=hlr_task_empty, hlr_client=hlr_client) == ([], [])


def test__handle_task__valid_client_response_was_append_correctly(
        hlr_client_mock,
        hlr_task,
        hlr_response_successful,
):
    hlr_client_mock.get_mccmnc_info.return_value = hlr_response_successful
    task_result = handle_task(hlr_client=hlr_client_mock, task=hlr_task)
    successfuls, failds = task_result

    assert hlr_client_mock.get_mccmnc_info.call_count == 1
    assert len(successfuls) == 1
    assert len(failds) == 0


def test__handle_task__invalid_client_response_was_append_correctly(
        hlr_client_mock,
        hlr_task,
):
    hlr_client_mock.get_mccmnc_info.side_effect = HlrVendorNotFoundError(result=-2, message='test', message_id='test')
    task_result = handle_task(hlr_client=hlr_client_mock, task=hlr_task)
    successfuls, failds = task_result

    assert hlr_client_mock.get_mccmnc_info.call_count == 1
    assert len(successfuls) == 0
    assert len(failds) == 1


def test__handle_task__valid_and_invalid_client_response_handle_correctly(hlr_client_mock,
                                                                          hlr_task_for_few_number,
                                                                          hlr_response_successful):
    hlr_client_mock.get_mccmnc_info.side_effect = [hlr_response_successful, HlrVendorNotFoundError(result=-2,
                                                                                                   message='test',
                                                                                                   message_id='test',
                                                                                                   ),
                                                   ]
    task_result = handle_task(hlr_client=hlr_client_mock, task=hlr_task_for_few_number)
    successfuls, failds = task_result

    assert hlr_client_mock.get_mccmnc_info.call_count == 2
    assert len(successfuls) == 1
    assert len(failds) == 1
