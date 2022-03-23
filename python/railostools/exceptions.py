import typing


class ParsingError(Exception):
    """Exceptions relating to the parsing of strings"""

    def __init__(self, msg) -> None:
        super().__init__(msg)


class IOError(Exception):
    """Exceptions relating to the writing/reading of files"""

    def __init__(self, msg) -> None:
        super().__init__(msg)


class MetadataError(Exception):
    """Exceptions relating to project metadata"""

    def __init__(self, msg) -> None:
        super().__init__(msg)


class ProgramNotFoundError(Exception):
    """Exceptions relating to project metadata"""

    def __init__(self, location: str) -> None:
        super().__init__(
            f"Failed to locate Railway Operation Simulator in '{location}'"
        )


class SessionINIError(Exception):
    """Exceptions relating to reading of the session file"""

    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class RailwayParsingError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class InvalidListenerError(Exception):
    def __init__(self, function: typing.Callable):
        _msg = f"""Candidate function '{function.__name__}' is not a valid listener function.
Candidate function must be in the form:
def async listener_function(monitor: rostools.performance.Monitor, arg1, arg2, ...)
where 'monitor' is a mandatory argument label.
"""
        super().__init__(_msg)
