from unittest import mock

from hlr.client_errors import HlrVendorNotFoundError
from hlr.tasks import handle_task


def test__handle_task__task_with_empty_fields(hlr_task_empty, hlr_client):
    assert handle_task(task=hlr_task_empty, hlr_client=hlr_client) == ([], [])


def test__handle_task__valid_client_response_was_append_correctly(
        hlr_client,
        hlr_task,
        hlr_response_successful,
):
    with mock.patch('hlr.client.HlrClient.get_mccmnc_info') as get_mccmnc_info_mock:
        get_mccmnc_info_mock.return_value = hlr_response_successful
        task_result = handle_task(hlr_client=hlr_client, task=hlr_task)
        successfuls, failds = task_result

        assert len(successfuls) == 1
        assert len(failds) == 0


def test__handle_task__invalid_client_response_was_append_correctly(
        hlr_client,
        hlr_task,
):
    with mock.patch('hlr.client.HlrClient.get_mccmnc_info') as get_mccmnc_info_mock:
        get_mccmnc_info_mock.side_effect = HlrVendorNotFoundError(result=-2, message='test', message_id='test')
        task_result = handle_task(hlr_client=hlr_client, task=hlr_task)
        successfuls, failds = task_result

        assert len(successfuls) == 0
        assert len(failds) == 1


def test__handle_task__valid_and_invalid_client_response_handle_correctly(hlr_client,
                                                                          hlr_task_for_few_number,
                                                                          hlr_response_successful):
    with mock.patch('hlr.client.HlrClient.get_mccmnc_info') as get_mccmnc_info_mock:
        get_mccmnc_info_mock.side_effect = [hlr_response_successful, HlrVendorNotFoundError(result=-2,
                                                                                            message='test',
                                                                                            message_id='test',
                                                                                            ),
                                            ]
        task_result = handle_task(hlr_client=hlr_client, task=hlr_task_for_few_number)
        successfuls, failds = task_result

        assert len(successfuls) == 1
        assert len(failds) == 1
