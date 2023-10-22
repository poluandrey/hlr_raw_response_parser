from unittest import mock

from hlr.client.errors import HlrVendorNotFoundError
from hlr.tasks import handle_task


def test__handle_task__valid_client_response_was_append_correctly(
        hlr_client,
        hlr_task,
        hlr_response_successful,
):
    with mock.patch('hlr.client.client.HlrClient.get_mccmnc_info') as get_mccmnc_info_mock:
        get_mccmnc_info_mock.return_value = hlr_response_successful
        task_result = handle_task(hlr_client=hlr_client, task=hlr_task)
        successfuls, failds = task_result

        assert len(successfuls) == 1
        assert len(failds) == 0


def test__handle_task__invalid_client_response_was_append_correctly(
        hlr_client,
        hlr_task,
):
    with mock.patch('hlr.client.client.HlrClient.get_mccmnc_info') as get_mccmnc_info_mock:
        get_mccmnc_info_mock.side_effect = HlrVendorNotFoundError(result=-2, message='test', message_id='test')
        task_result = handle_task(hlr_client=hlr_client, task=hlr_task)
        successfuls, failds = task_result

        assert len(successfuls) == 0
        assert len(failds) == 1
