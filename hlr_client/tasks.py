from dataclasses import dataclass
from itertools import product

from hlr_client.client import HlrClient, HlrFailedResponse
from hlr_client.errors import (HlrClientHTTPError, HlrClientInternalError,
                               HlrProxyError)


@dataclass(kw_only=True, frozen=True, slots=True)
class Task:
    providers: list[str]
    msisdns: list[str]


def handle_task(task: Task, hlr_client: HlrClient) -> tuple[list, list]:
    details, errors = [], []
    for msisdn, provider in product(task.msisdns, task.providers):
        try:
            msisdn_info = hlr_client.get_mccmnc_info(
                msisdn=msisdn,
                provider=provider,
            )
            details.append(msisdn_info)

        except HlrProxyError as error:
            errors.append(
                HlrFailedResponse(
                    message=error.message,
                    msisdn=error.msisdn,
                    result=error.result,
                    message_id=error.message_id,
                ),
            )
        except HlrClientHTTPError as error:
            errors.append(
                HlrFailedResponse(
                    message='Internal HTTP error',
                    msisdn=msisdn,
                    provider=provider,
                    http_error=error.error_code,
                ),
            )
        except HlrClientInternalError as error:
            errors.append(
                HlrFailedResponse(
                    msisdn=msisdn,
                    provider=provider,
                    message=str(error),
                ),
            )

    return details, errors
