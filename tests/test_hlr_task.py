import respx

from hlr.tasks import Task, handle_task, handle_client_error


def test__handle_task__task_with_empty_fields(hlr_task_empty, hlr_client):
    assert handle_task(task=hlr_task_empty, hlr_client=hlr_client) == ([], [])


def test__handle_task__valid_client_response(hlr_client, hlr_task, hlr_response_successful_for_tmt_hlr):
    with respx.mock:
        respx.get('https://example.com/api/mccmnc_request').respond(json=hlr_response_successful_for_tmt_hlr,
                                                                    status_code=200)
        task_details = handle_task(task=hlr_task, hlr_client=hlr_client)

        successful_result, failed_result = task_details
        assert len(successful_result) == 1
        assert len(failed_result) == 0


def test__handle_task__invalid_client_response(hlr_client, hlr_task, hlr_response_vendor_not_found):
    with respx.mock:
        respx.get('https://example.com/api/mccmnc_request',).respond(json=hlr_response_vendor_not_found,
                                                                    status_code=200)
        task_details = handle_task(task=hlr_task, hlr_client=hlr_client)

        successful_result, failed_result = task_details
        assert len(successful_result) == 0
        assert len(failed_result) == 1


def test__handle_task__valid_and_invalid_client_response(
        hlr_client,
        hlr_task_for_few_number,
        hlr_response_successful_for_tmt_hlr,
        hlr_response_vendor_not_found,
                                                         ):
    pass
