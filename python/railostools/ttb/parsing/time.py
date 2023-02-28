import typing
import re
import railostools.exceptions as ros_exc


def adjust_above_24hr(
    time_candidate: str, error_message: str
) -> typing.Tuple[str, int]:
    _time_regex: typing.Pattern = re.compile(r"\d+:\d+")
    _is_timestr: typing.List[str] = _time_regex.findall(time_candidate)

    if not _is_timestr:
        raise ros_exc.ParsingError(error_message)

    _time_hours: int = int(_is_timestr[0].split(":")[0])

    # Python does not support times >23:59 so need to manually handle that case
    # we add days to the time object
    time_days: int = 0
    if _time_hours > 23:
        time_days = _time_hours // 24
        _adj_hours = _time_hours - time_days * 24
        _adj_hours_str: str = f"{'0' if _adj_hours < 10 else ''}{_adj_hours}:"
        time_candidate = time_candidate.replace(f"{_time_hours}:", _adj_hours_str)

    return time_candidate, time_days
