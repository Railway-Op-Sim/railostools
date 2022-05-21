import typing
from datetime import datetime

import railostools.common.coords as ros_coords
import railostools.exceptions as ros_exc
import railostools.ttb.components as ros_comp
import railostools.ttb.components.start as ros_start
import railostools.ttb.parsing.components as ros_parse_comp
import railostools.ttb.string as ros_ttb_str


def parse_Snt(start_components: typing.List[str]) -> ros_start.Snt:
    """Parse an Snt type string"""
    if len(start_components) not in (3, 4):
        raise ros_exc.ParsingError(
            "Expected either 3 or 4 items in components "
            f"'{start_components}' for start type 'Snt', "
            f"but received {len(start_components)}"
        )

    try:
        datetime.strptime(start_components[0], "%H:%M")
    except ValueError as e:
        raise ros_exc.ParsingError(
            "Expected time string for start type 'Snt'"
            f"but received '{start_components[0]}'"
        ) from e

    _start_pos_r, _start_pos_f = start_components[2].split()

    _rear_element = ros_coords.coord_from_str(_start_pos_r)
    _front_element = ros_coords.coord_from_str(_start_pos_f)

    if abs(_rear_element - _front_element) > 1:
        raise ros_exc.ParsingError(
            f"Rear and front elements [{_rear_element}, {_front_element}] must be adjacent"
        )

    if len(start_components) == 4 and start_components[-1] != "S":
        raise ros_exc.ParsingError(
            f"Invalid end term '{start_components[-1]}' "
            "for start type 'Snt', permitted value is 'S' for signaller control"
        )

    return ros_start.Snt(
        time=start_components[0],
        rear_element_id=_rear_element,
        front_element_id=_front_element,
        under_signaller_control=len(start_components) == 4,
    )


def parse_Sns(start_components: typing.List[str]) -> ros_start.Sfs:
    if len(start_components) != 3:
        raise ros_exc.ParsingError(
            "Expected 3 items in components "
            f"'{start_components}' for start type 'Sns'"
        )
    try:
        datetime.strptime(start_components[0], "%H:%M")
    except ValueError as e:
        raise ros_exc.ParsingError(
            "Expected time string for start type 'Sns'"
            f"but received '{start_components[0]}'"
        ) from e
    _parent_srv = ros_parse_comp.parse_reference(start_components[2])
    return ros_start.Sns(time=start_components[0], parent_service=_parent_srv)


def parse_Sfs(start_components: typing.List[str]) -> ros_start.Sfs:
    if len(start_components) != 3:
        raise ros_exc.ParsingError(
            "Expected 3 items in components "
            f"'{start_components}' for start type 'Sfs'"
        )
    try:
        datetime.strptime(start_components[0], "%H:%M")
    except ValueError as e:
        raise ros_exc.ParsingError(
            "Expected time string for start type 'Snt'"
            f"but received '{start_components[0]}'"
        ) from e
    _split_srv = ros_parse_comp.parse_reference(start_components[2])
    return ros_start.Sfs(time=start_components[0], splitting_service=_split_srv)


def parse_Sns_fsh(start_components: typing.List[str]) -> ros_start.Sns_fsh:
    if len(start_components) != 3:
        raise ros_exc.ParsingError(
            "Expected 3 items in components "
            f"'{start_components}' for start type 'Sns-fsh'"
        )
    try:
        datetime.strptime(start_components[0], "%H:%M")
    except ValueError as e:
        raise ros_exc.ParsingError(
            "Expected time string for start type 'Sns-fsh'"
            f"but received '{start_components[0]}'"
        ) from e
    _split_srv = ros_parse_comp.parse_reference(start_components[2])
    return ros_start.Sfs(time=start_components[0], splitting_service=_split_srv)


def parse_Snt_sh(start_components: typing.List[str]) -> ros_start.Snt_sh:
    if len(start_components) != 4:
        raise ros_exc.ParsingError(
            "Expected 4 items in components "
            f"'{start_components}' for start type 'Snt-sh'"
        )
    try:
        datetime.strptime(start_components[0], "%H:%M")
    except ValueError as e:
        raise ros_exc.ParsingError(
            "Expected time string for start type 'Snt-sh'"
            f"but received '{start_components[0]}'"
        ) from e
    _start_pos_r, _start_pos_f = start_components[2].split()

    _rear_element = ros_coords.coord_from_str(_start_pos_r)
    _front_element = ros_coords.coord_from_str(_start_pos_f)

    _shuttle_srv = ros_parse_comp.parse_reference(start_components[3])

    return ros_start.Snt_sh(
        time=start_components[0],
        rear_element_id=_rear_element,
        front_element_id=_front_element,
        shuttle_ref=_shuttle_srv,
    )


def parse_Sns_sh(start_components: typing.List[str]) -> ros_start.Sns_sh:
    if len(start_components) != 4:
        raise ros_exc.ParsingError(
            "Expected 4 items in components "
            f"'{start_components}' for start type 'Sns-sh'"
        )
    try:
        datetime.strptime(start_components[0], "%H:%M")
    except ValueError as e:
        raise ros_exc.ParsingError(
            "Expected time string for start type 'Sns-sh'"
            f"but received '{start_components[0]}'"
        ) from e

    _feeder_srv = ros_parse_comp.parse_reference(start_components[2])
    _linked_srv = ros_parse_comp.parse_reference(start_components[3])

    return ros_start.Sns_sh(
        time=start_components[0], feeder_ref=_feeder_srv, linked_shuttle_ref=_linked_srv
    )


def parse_start(start_str: str) -> ros_comp.StartType:
    PARSE_DICT = {
        "Snt": parse_Snt,
        "Sfs": parse_Sfs,
        "Sns-fsh": parse_Sns_fsh,
        "Snt-sh": parse_Snt_sh,
        "Sns-sh": parse_Sns_sh,
        "Sns": parse_Sns,
    }

    try:
        _components = ros_ttb_str.split(start_str)
    except IndexError as e:
        raise ros_exc.ParsingError(
            f"Failed to extract ttb components from '{start_str}'"
        ) from e

    for start_type, parser in PARSE_DICT.items():
        if start_type in start_str:
            return parser(_components)

    raise ros_exc.ParsingError(f"Failed to determine start type for '{start_str}'")
