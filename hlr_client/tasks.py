from dataclasses import dataclass
from itertools import product

from hlr_client.client import (HlrClient, HlrFailedResponse,
                               HlrSuccessfulResponse)


@dataclass(kw_only=True, frozen=True, slots=True)
class Task:
    providers: list[str]
    msisdns: list[str]


@dataclass(kw_only=True, slots=True)
class TaskResult:
    failed: list[HlrFailedResponse]
    success: list[HlrSuccessfulResponse]

    def append_hlr_response(
            self,
            hlr_response: HlrFailedResponse | HlrSuccessfulResponse,
    ) -> None:
        if isinstance(hlr_response, HlrSuccessfulResponse):
            self.success.append(hlr_response)
            return

        self.failed.append(hlr_response)
        return


def handle_task(task: Task, hlr_client: HlrClient) -> TaskResult:
    task_result = TaskResult(
        failed=[],
        success=[],
    )
    for msisdn, provider in product(task.msisdns, task.providers):
        msisdn_info = hlr_client.get_mccmnc_info(
            msisdn=msisdn,
            provider=provider,
        )

        task_result.append_hlr_response(msisdn_info)

    return task_result
