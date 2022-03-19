from datetime import datetime
import typing

import railostools.ttb.components as ros_comp
import railostools.ttb.components.start as ros_start
import railostools.exceptions as ros_exc
import railostools.ttb.string as ros_ttb_str
import railostools.common.coords as ros_coords

import railostools.ttb.parsing.components as ros_parse_comp


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

    if abs(_rear_element-_front_element) > 1:
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
        under_signaller_control=len(start_components) == 4
    )


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


def parse_start(start_str: str) -> ros_comp.StartType:
    PARSE_DICT = {
        "Snt": parse_Snt,
        "Sfs": parse_Sfs
    }

    try:
        _components = ros_ttb_str.split(start_str)
    except IndexError as e:
        raise ros_exc.ParsingError(
            f"Failed to extract ttb components from '{start_str}'"
        ) from e

    for start_type, parser in PARSE_DICT.items():
        if start_type in start_str:
            return parser()
