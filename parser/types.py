from typing import Any, TypeAlias
from parser.hlr_responses import (InfobipHlrResponse,
                                  TmtHlrResponse,
                                  XconnectHlrResponse,
                                  XconnectMnpResponse)

Json: TypeAlias = dict[str, Any] | list[dict[str, Any]]
HlrResponse: TypeAlias = (
        InfobipHlrResponse |
        TmtHlrResponse |
        XconnectHlrResponse |
        XconnectMnpResponse
)
