class HlrParserError(Exception):
    pass


class InvalidContextLogError(HlrParserError):
    pass


class RawResponseNotFoundError(HlrParserError):
    pass


class InvalidRawResponseError(HlrParserError):
    pass
