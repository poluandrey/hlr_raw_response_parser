class HlrClientError(Exception):
    pass


class HlrClientHTTPError(HlrClientError):

    def __init__(self, error_code: int) -> None:
        self.error_code = error_code


class HlrProxyError(HlrClientError):
    def __init__(
            self,
            result: int,
            message_id: str,
            message: str | None,

    ) -> None:
        self.result = result
        self.message_id = message_id
        self.message = message


class HlrVendorNotFoundError(HlrProxyError):
    pass


class HlrProxyInternalError(HlrProxyError):
    def __init__(self, result: int,
                 message_id: str,
                 message: str | None,
                 msisdn: str):
        super().__init__(result,
                         message_id,
                         message)
        self.msisdn = msisdn

