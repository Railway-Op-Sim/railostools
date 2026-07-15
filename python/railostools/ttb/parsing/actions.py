import railostools.exceptions as railos_exc
import railostools.ttb.components as railos_comp
import railostools.ttb.components.actions as railos_act
import railostools.ttb.parsing.components as railos_parse_comp
from railostools.ttb.parsing.time import adjust_above_24hr


def parse_location(action_components: list[str]) -> railos_act.Location:
    """Parse a calling point string"""
    if len(action_components) not in (2, 3):
        raise railos_exc.ParsingError(
            "Expected 2 or 3 items in components " f"'{action_components}' for location"
        )

    _start_time, _start_days = adjust_above_24hr(
        action_components[0],
        "Expected time string for arrival time in location "
        f"but received '{action_components[0]}'",
    )
    _end_time: str | None = None
    _end_days: int | None = None

    if len(action_components) == 3:
        _end_time, _end_days = adjust_above_24hr(
            action_components[1],
            "Expected time string for departure time in location "
            f"but received '{action_components[1]}'",
        )
        _location = action_components[2]
    else:
        _location = action_components[1]

    return railos_act.Location(
        time=_start_time,
        end_time=_end_time,
        time_days=_start_days,
        end_time_days=_end_days or 0,
        location=_location,
    )


def parse_pas(action_components: list[str]) -> railos_act.Location:
    """Parse a pas statement"""
    if len(action_components) != 3:
        raise railos_exc.ParsingError(
            "Expected 3 items in components "
            f"'{action_components}' for 'pas' statement"
        )

    _time_str, _time_days = adjust_above_24hr(
        action_components[0],
        "Expected time string for 'pas'" f"but received '{action_components[0]}'",
    )

    return railos_act.pas(
        time=_time_str, time_days=_time_days, location=action_components[2]
    )


def parse_jbo(action_components: list[str]) -> railos_act.Location:
    """Parse a jbo statement"""
    if len(action_components) != 3:
        raise railos_exc.ParsingError(
            "Expected 3 items in components "
            f"'{action_components}' for 'jbo' statement"
        )

    _time_str, _time_days = adjust_above_24hr(
        action_components[0],
        "Expected time string for 'jbo'" f"but received '{action_components[0]}'",
    )

    _joined_ref = railos_parse_comp.parse_reference(action_components[2])

    return railos_act.jbo(
        time=_time_str, time_days=_time_days, joining_service_ref=_joined_ref
    )


def parse_fsp(action_components: list[str]) -> railos_act.fsp:
    """Parse a fsp statement"""
    if len(action_components) != 3:
        raise railos_exc.ParsingError(
            "Expected 3 items in components "
            f"'{action_components}' for 'fsp' statement"
        )

    _new_serv = railos_parse_comp.parse_reference(action_components[2])

    _time_str, _time_days = adjust_above_24hr(
        action_components[0],
        "Expected time string for 'fsp'" f"but received '{action_components[0]}'",
    )

    return railos_act.fsp(
        time=_time_str, time_days=_time_days, new_service_ref=_new_serv
    )


def parse_dsc(action_components: list[str]) -> railos_act.dsc:
    """Parse a dsc statement"""
    if len(action_components) != 3:
        raise railos_exc.ParsingError(
            "Expected 3 items in components "
            f"'{action_components}' for 'dsc' statement"
        )

    _description = action_components[2]

    _time_str, _time_days = adjust_above_24hr(
        action_components[0],
        "Expected time string for 'dsc'" f"but received '{action_components[0]}'",
    )

    return railos_act.dsc(
        time=_time_str, time_days=_time_days, description=_description
    )


def parse_cms(action_components: list[str]) -> railos_act.cms:
    """Parse a cms statement"""
    if len(action_components) != 3:
        raise railos_exc.ParsingError(
            "Expected 3 items in components "
            f"'{action_components}' for 'cms' statement"
        )

    _new_max_speed = action_components[2]

    _time_str, _time_days = adjust_above_24hr(
        action_components[0],
        "Expected time string for 'dsc'" f"but received '{action_components[0]}'",
    )

    return railos_act.cms(
        time=_time_str, time_days=_time_days, new_speed=int(_new_max_speed)
    )


def parse_rsp(action_components: list[str]) -> railos_act.rsp:
    """Parse an rsp statement"""
    if len(action_components) != 3:
        raise railos_exc.ParsingError(
            "Expected 3 items in components "
            f"'{action_components}' for 'rsp' statement"
        )

    _new_serv = railos_parse_comp.parse_reference(action_components[2])

    _time_str, _time_days = adjust_above_24hr(
        action_components[0],
        "Expected time string for 'rsp'" f"but received '{action_components[0]}'",
    )

    return railos_act.rsp(
        time=_time_str, time_days=_time_days, new_service_ref=_new_serv
    )


def parse_cdt(action_components: list[str]) -> railos_act.fsp:
    """Parse a cdt statement"""
    if len(action_components) != 2:
        raise railos_exc.ParsingError(
            "Expected 2 items in components "
            f"'{action_components}' for 'cdt' statement"
        )

    _time_str, _time_days = adjust_above_24hr(
        action_components[0],
        "Expected time string for 'cdt'" f"but received '{action_components[0]}'",
    )

    return railos_act.cdt(time=_time_str, time_days=_time_days)


def parse_action(action_str: str) -> railos_comp.ActionType:
    PARSE_DICT = {
        "pas": parse_pas,
        "jbo": parse_jbo,
        "fsp": parse_fsp,
        "rsp": parse_rsp,
        "cdt": parse_cdt,
        "cms": parse_cms,
        "dsc": parse_dsc,
    }

    try:
        _components = railos_comp.split(action_str)
    except IndexError as e:
        raise railos_exc.ParsingError(
            f"Failed to extract ttb components from '{action_str}'"
        ) from e

    if _components[0].upper().startswith("W"):
        _components[0] = _components[0][1:]

    for start_type, parser in PARSE_DICT.items():
        if start_type.replace("-", "_") in action_str:
            return parser(_components)
    return parse_location(_components)
