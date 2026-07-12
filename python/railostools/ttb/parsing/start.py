import railostools.common.coords as railos_coords
import railostools.exceptions as railos_exc
import railostools.ttb.components as railos_comp
import railostools.ttb.components.start as railos_start
import railostools.ttb.parsing.components as railos_parse_comp
from railostools.ttb.parsing.time import adjust_above_24hr


def parse_Snt(start_components: list[str]) -> railos_start.Snt:
    """Parse an Snt type string"""
    if len(start_components) not in (3, 4):
        raise railos_exc.ParsingError(
            "Expected either 3 or 4 items in components "
            f"'{start_components}' for start type 'Snt', "
            f"but received {len(start_components)}"
        )

    _time_str, _time_days = adjust_above_24hr(
        start_components[0],
        "Expected time string for 'Snt'" f"but received '{start_components[0]}'",
    )

    _start_pos_r, _start_pos_f = start_components[2].split()

    _rear_element = railos_coords.coord_from_str(_start_pos_r)
    _front_element = railos_coords.coord_from_str(_start_pos_f)

    if abs(_rear_element - _front_element) > 1:
        raise railos_exc.ParsingError(
            f"Rear and front elements [{_rear_element}, {_front_element}] must be adjacent"
        )

    if len(start_components) == 4 and start_components[-1] != "S":
        raise railos_exc.ParsingError(
            f"Invalid end term '{start_components[-1]}' "
            "for start type 'Snt', permitted value is 'S' for signaller control"
        )
    return railos_start.Snt(
        time=_time_str,
        time_days=_time_days,
        rear_element_id=_rear_element,
        front_element_id=_front_element,
        under_signaller_control=len(start_components) == 4,
    )


def parse_Sns(start_components: list[str]) -> railos_start.Sfs:
    if len(start_components) != 3:
        raise railos_exc.ParsingError(
            "Expected 3 items in components "
            f"'{start_components}' for start type 'Sns'"
        )
    _time_str, _time_days = adjust_above_24hr(
        start_components[0],
        "Expected time string for 'Sns'" f"but received '{start_components[0]}'",
    )
    _parent_srv = railos_parse_comp.parse_reference(start_components[2])
    return railos_start.Sns(
        time=_time_str, time_days=_time_days, parent_service=_parent_srv
    )


def parse_Sfs(start_components: list[str]) -> railos_start.Sfs:
    if len(start_components) != 3:
        raise railos_exc.ParsingError(
            "Expected 3 items in components "
            f"'{start_components}' for start type 'Sfs'"
        )
    _time_str, _time_days = adjust_above_24hr(
        start_components[0],
        "Expected time string for 'Sfs'" f"but received '{start_components[0]}'",
    )
    _split_srv = railos_parse_comp.parse_reference(start_components[2])
    return railos_start.Sfs(
        time=_time_str, time_days=_time_days, splitting_service=_split_srv
    )


def parse_Sns_fsh(start_components: list[str]) -> railos_start.Sns_fsh:
    if len(start_components) != 3:
        raise railos_exc.ParsingError(
            "Expected 3 items in components "
            f"'{start_components}' for start type 'Sns-fsh'"
        )
    _time_str, _time_days = adjust_above_24hr(
        start_components[0],
        "Expected time string for 'Sns-fsh'" f"but received '{start_components[0]}'",
    )
    _split_srv = railos_parse_comp.parse_reference(start_components[2])
    return railos_start.Sns_fsh(
        time=_time_str, time_days=_time_days, shuttle_ref=_split_srv
    )


def parse_Snt_sh(start_components: list[str]) -> railos_start.Snt_sh:
    if len(start_components) != 4:
        raise railos_exc.ParsingError(
            "Expected 4 items in components "
            f"'{start_components}' for start type 'Snt-sh'"
        )
    _time_str, _time_days = adjust_above_24hr(
        start_components[0],
        "Expected time string for 'Snt-sh'" f"but received '{start_components[0]}'",
    )
    _start_pos_r, _start_pos_f = start_components[2].split()

    _rear_element = railos_coords.coord_from_str(_start_pos_r)
    _front_element = railos_coords.coord_from_str(_start_pos_f)

    _shuttle_srv = railos_parse_comp.parse_reference(start_components[3])

    return railos_start.Snt_sh(
        time=_time_str,
        time_days=_time_days,
        rear_element_id=_rear_element,
        front_element_id=_front_element,
        shuttle_ref=_shuttle_srv,
    )


def parse_Sns_sh(start_components: list[str]) -> railos_start.Sns_sh:
    if len(start_components) != 4:
        raise railos_exc.ParsingError(
            "Expected 4 items in components "
            f"'{start_components}' for start type 'Sns-sh'"
        )
    _time_str, _time_days = adjust_above_24hr(
        start_components[0],
        "Expected time string for 'Sns-sh'" f"but received '{start_components[0]}'",
    )

    _feeder_srv = railos_parse_comp.parse_reference(start_components[3])
    _linked_srv = railos_parse_comp.parse_reference(start_components[2])

    return railos_start.Sns_sh(
        time=_time_str,
        time_days=_time_days,
        feeder_ref=_feeder_srv,
        linked_shuttle_ref=_linked_srv,
    )


def parse_start(start_str: str) -> railos_comp.StartType:
    PARSE_DICT = {
        "Sns-fsh": parse_Sns_fsh,
        "Snt-sh": parse_Snt_sh,
        "Sns-sh": parse_Sns_sh,
        "Sns": parse_Sns,
        "Snt": parse_Snt,
        "Sfs": parse_Sfs,
    }

    try:
        _components = railos_comp.split(start_str)
    except IndexError as e:
        raise railos_exc.ParsingError(
            f"Failed to extract ttb components from '{start_str}'"
        ) from e

    for start_type, parser in PARSE_DICT.items():
        if start_type in start_str:
            return parser(_components)

    raise railos_exc.ParsingError(f"Failed to determine start type for '{start_str}'")
