class HlrClientBaseError(Exception):
    pass


class HlrClientHTTPError(HlrClientBaseError):

    def __init__(self, error_code: int) -> None:
        self.error_code = error_code


class HlrClientInternalError(HlrClientBaseError):
    pass


class HlrProxyError(Exception):
    def __init__(
            self,
            msisdn: str,
            result: int,
            message_id: str,
            message: str,
    ) -> None:
        self.msisdn = msisdn
        self.result = result
        self.message_id = message_id
        self.message = message


class HlrVendorNotFoundError(HlrProxyError):
    pass


class HlrProxyInternalError(HlrProxyError):
    pass
