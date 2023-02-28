import typing
from datetime import datetime

import railostools.exceptions as ros_exc
import railostools.ttb.components as ros_comp
import railostools.ttb.components.actions as ros_act
import railostools.ttb.parsing.components as ros_parse_comp
import railostools.ttb.string as ros_ttb_str


def parse_location(action_components: typing.List[str]) -> ros_act.Location:
    """Parse a calling point string"""
    if len(action_components) not in (2, 3):
        raise ros_exc.ParsingError(
            "Expected 2 or 3 items in components " f"'{action_components}' for location"
        )

    if len(action_components) == 3:
        try:
            datetime.strptime(action_components[1], "%H:%M")
        except ValueError as e:
            if (
                ":" in action_components[1]
                and int(action_components[1].split(":")[0]) > 23
            ):
                raise NotImplementedError(
                    f"Time '{action_components[1]}' exceeds 24hr limit"
                ) from e
            raise ros_exc.ParsingError(
                "Expected time string for departure time in location "
                f"but received '{action_components[1]}'"
            ) from e
        _depart = action_components[1]
        _location = action_components[2]
    else:
        _depart = None
        _location = action_components[1]

    return ros_act.Location(time=action_components[0], end_time=_depart, name=_location)


def parse_pas(action_components: typing.List[str]) -> ros_act.Location:
    """Parse a pas statement"""
    if len(action_components) != 3:
        raise ros_exc.ParsingError(
            "Expected 3 items in components "
            f"'{action_components}' for 'pas' statement"
        )

    return ros_act.pas(time=action_components[0], location=action_components[2])


def parse_jbo(action_components: typing.List[str]) -> ros_act.Location:
    """Parse a jbo statement"""
    if len(action_components) != 3:
        raise ros_exc.ParsingError(
            "Expected 3 items in components "
            f"'{action_components}' for 'jbo' statement"
        )

    _joined_ref = ros_parse_comp.parse_reference(action_components[2])

    return ros_act.jbo(time=action_components[0], joining_service_ref=_joined_ref)


def parse_fsp(action_components: typing.List[str]) -> ros_act.fsp:
    """Parse a fsp statement"""
    if len(action_components) != 3:
        raise ros_exc.ParsingError(
            "Expected 3 items in components "
            f"'{action_components}' for 'fsp' statement"
        )

    _new_serv = ros_parse_comp.parse_reference(action_components[2])

    return ros_act.fsp(time=action_components[0], new_service_ref=_new_serv)


def parse_rsp(action_components: typing.List[str]) -> ros_act.fsp:
    """Parse an rsp statement"""
    if len(action_components) != 3:
        raise ros_exc.ParsingError(
            "Expected 3 items in components "
            f"'{action_components}' for 'rsp' statement"
        )

    _new_serv = ros_parse_comp.parse_reference(action_components[2])

    return ros_act.fsp(time=action_components[0], new_service_ref=_new_serv)


def parse_cdt(action_components: typing.List[str]) -> ros_act.fsp:
    """Parse a cdt statement"""
    if len(action_components) != 2:
        raise ros_exc.ParsingError(
            "Expected 2 items in components "
            f"'{action_components}' for 'cdt' statement"
        )

    return ros_act.cdt(time=action_components[0])


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
