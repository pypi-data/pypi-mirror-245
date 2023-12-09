class AdvocoException(Exception):
    pass


class NoTokenError(AdvocoException):
    pass


class SampleTextNotFound(AdvocoException):
    pass


class DateOutOfRangeError(AdvocoException):
    pass


class WrongAnswerMcFly(AdvocoException):
    pass


class PuzzleNotAvailableError(AdvocoException):
    pass


class PartNotDefined(AdvocoException):
    pass
