import typing

import railostools.exceptions as ros_exc
import railostools.ttb.components as ros_comp
import railostools.ttb.components.actions as ros_act
import railostools.ttb.parsing.components as ros_parse_comp
import railostools.ttb.string as ros_ttb_str
from railostools.ttb.parsing.time import adjust_above_24hr


def parse_location(action_components: typing.List[str]) -> ros_act.Location:
    """Parse a calling point string"""
    if len(action_components) not in (2, 3):
        raise ros_exc.ParsingError(
            "Expected 2 or 3 items in components " f"'{action_components}' for location"
        )

    _start_time, _start_days = adjust_above_24hr(
        action_components[0],
        "Expected time string for arrival time in location "
        f"but received '{action_components[0]}'",
    )
    _end_time: typing.Optional[str] = None
    _end_days: typing.Optional[int] = None

    if len(action_components) == 3:
        _end_time, _end_days = adjust_above_24hr(
            action_components[1],
            "Expected time string for departure time in location "
            f"but received '{action_components[1]}'",
        )
        _location = action_components[2]
    else:
        _location = action_components[1]

    return ros_act.Location(
        time=_start_time,
        end_time=_end_time,
        time_days=_start_days,
        end_days=_end_days,
        name=_location,
    )


def parse_pas(action_components: typing.List[str]) -> ros_act.Location:
    """Parse a pas statement"""
    if len(action_components) != 3:
        raise ros_exc.ParsingError(
            "Expected 3 items in components "
            f"'{action_components}' for 'pas' statement"
        )

    _time_str, _time_days = adjust_above_24hr(
        action_components[0],
        "Expected time string for 'pas'" f"but received '{action_components[0]}'",
    )

    return ros_act.pas(
        time=_time_str, time_days=_time_days, location=action_components[2]
    )


def parse_jbo(action_components: typing.List[str]) -> ros_act.Location:
    """Parse a jbo statement"""
    if len(action_components) != 3:
        raise ros_exc.ParsingError(
            "Expected 3 items in components "
            f"'{action_components}' for 'jbo' statement"
        )

    _time_str, _time_days = adjust_above_24hr(
        action_components[0],
        "Expected time string for 'jbo'" f"but received '{action_components[0]}'",
    )

    _joined_ref = ros_parse_comp.parse_reference(action_components[2])

    return ros_act.jbo(
        time=_time_str, time_days=_time_days, joining_service_ref=_joined_ref
    )


def parse_fsp(action_components: typing.List[str]) -> ros_act.fsp:
    """Parse a fsp statement"""
    if len(action_components) != 3:
        raise ros_exc.ParsingError(
            "Expected 3 items in components "
            f"'{action_components}' for 'fsp' statement"
        )

    _new_serv = ros_parse_comp.parse_reference(action_components[2])

    _time_str, _time_days = adjust_above_24hr(
        action_components[0],
        "Expected time string for 'fsp'" f"but received '{action_components[0]}'",
    )

    return ros_act.fsp(time=_time_str, time_days=_time_days, new_service_ref=_new_serv)


def parse_dsc(action_components: typing.List[str]) -> ros_act.fsp:
    """Parse a dsc statement"""
    if len(action_components) != 3:
        raise ros_exc.ParsingError(
            "Expected 3 items in components "
            f"'{action_components}' for 'dsc' statement"
        )

    _description = action_components[2]

    _time_str, _time_days = adjust_above_24hr(
        action_components[0],
        "Expected time string for 'dsc'" f"but received '{action_components[0]}'",
    )

    return ros_act.dsc(time=_time_str, time_days=_time_days, description=_description)


def parse_rsp(action_components: typing.List[str]) -> ros_act.rsp:
    """Parse an rsp statement"""
    if len(action_components) != 3:
        raise ros_exc.ParsingError(
            "Expected 3 items in components "
            f"'{action_components}' for 'rsp' statement"
        )

    _new_serv = ros_parse_comp.parse_reference(action_components[2])

    _time_str, _time_days = adjust_above_24hr(
        action_components[0],
        "Expected time string for 'rsp'" f"but received '{action_components[0]}'",
    )

    return ros_act.rsp(time=_time_str, time_days=_time_days, new_service_ref=_new_serv)


def parse_cdt(action_components: typing.List[str]) -> ros_act.fsp:
    """Parse a cdt statement"""
    if len(action_components) != 2:
        raise ros_exc.ParsingError(
            "Expected 2 items in components "
            f"'{action_components}' for 'cdt' statement"
        )

    _time_str, _time_days = adjust_above_24hr(
        action_components[0],
        "Expected time string for 'cdt'" f"but received '{action_components[0]}'",
    )

    return ros_act.cdt(time=_time_str, time_days=_time_days)


def parse_action(action_str: str) -> ros_comp.ActionType:
    PARSE_DICT = {
        "pas": parse_pas,
        "jbo": parse_jbo,
        "fsp": parse_fsp,
        "rsp": parse_rsp,
        "cdt": parse_cdt,
    }

    try:
        _components = ros_ttb_str.split(action_str)
    except IndexError as e:
        raise ros_exc.ParsingError(
            f"Failed to extract ttb components from '{action_str}'"
        ) from e

    if _components[0].upper().startswith("W"):
        _components[0] = _components[0][1:]

    for start_type, parser in PARSE_DICT.items():
        if start_type.replace("-", "_") in action_str:
            return parser(_components)
    return parse_location(_components)
