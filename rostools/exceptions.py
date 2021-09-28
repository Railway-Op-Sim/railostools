from typing import Callable


class TimetableParsingError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class InvalidListenerError(Exception):
    def __init__(self, function: Callable):
        _msg = f"""Candidate function '{function.__name__}' is not a valid listener function.
Candidate function must be in the form:

def async listener_function(monitor: rostools.performance.Monitor, arg1, arg2, ...)

where 'monitor' is a mandatory argument label.
"""
        super().__init__(_msg)
