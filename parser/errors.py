class ContextLogParserError(Exception):
    pass


class InvalidContextLogError(ContextLogParserError):
    pass


class RawResponseNotFoundError(ContextLogParserError):
    pass


class InvalidRawResponseError(ContextLogParserError):
    pass
