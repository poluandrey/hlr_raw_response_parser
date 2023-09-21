from typing import TypeAlias

from hlr_client.client import HlrFailedResponse, HlrSuccessfulResponse

task: TypeAlias = list[HlrSuccessfulResponse | HlrFailedResponse]
