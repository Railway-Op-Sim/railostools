import typing
from datetime import datetime

import railostools.common.coords as railos_coords
import railostools.exceptions as railos_exc
import railostools.ttb.components as railos_comp
import railostools.ttb.components.finish as railos_finish
import railostools.ttb.parsing.components as railos_parse_comp
import railostools.ttb.string as railos_ttb_str


def parse_Fns(finish_components: typing.List[str]) -> railos_finish.Fns:
    """Parse an Fns type string"""
    if len(finish_components) != 3:
        raise railos_exc.ParsingError(
            "Expected 3 items in components "
            f"'{finish_components}' for finish type 'Fns'"
        )

    try:
        datetime.strptime(finish_components[0], "%H:%M")
    except ValueError as e:
        raise railos_exc.ParsingError(
            "Expected time string for finish type 'Snt'"
            f"but received '{finish_components[0]}'"
        ) from e

    _new_srv = railos_parse_comp.parse_reference(finish_components[2])
    return railos_finish.Fns(time=finish_components[0], new_service_ref=_new_srv)


def parse_Fjo(finish_components: typing.List[str]) -> railos_finish.Fjo:
    """Parse an Fjo type string"""
    if len(finish_components) != 3:
        raise railos_exc.ParsingError(
            "Expected 3 items in components "
            f"'{finish_components}' for finish type 'Fjo'"
        )

    try:
        datetime.strptime(finish_components[0], "%H:%M")
    except ValueError as e:
        raise railos_exc.ParsingError(
            "Expected time string for finish type 'Fjo'"
            f"but received '{finish_components[0]}'"
        ) from e

    _joining_srv = railos_parse_comp.parse_reference(finish_components[2])
    return railos_finish.Fjo(
        time=finish_components[0], joining_service_ref=_joining_srv
    )


def parse_Fer(finish_components: typing.List[str]) -> railos_finish.Fer:
    """Parse an Fer type string"""
    if len(finish_components) != 3:
        raise railos_exc.ParsingError(
            "Expected 3 items in components "
            f"'{finish_components}' for finish type 'Fer'"
        )

    try:
        datetime.strptime(finish_components[0], "%H:%M")
    except ValueError as e:
        raise railos_exc.ParsingError(
            "Expected time string for finish type 'Fjo'"
            f"but received '{finish_components[0]}'"
        ) from e

    _exit_elements = [
        railos_coords.coord_from_str(i) for i in finish_components[2].split()
    ]

    return railos_finish.Fer(time=finish_components[0], exit_coords=_exit_elements)


def parse_Frh_sh(finish_components: typing.List[str]) -> railos_finish.Fer:
    """Parse an Frh-sh type string"""
    if len(finish_components) != 3:
        raise railos_exc.ParsingError(
            "Expected 3 items in components "
            f"'{finish_components}' for finish type 'Frh-sh'"
        )

    try:
        datetime.strptime(finish_components[0], "%H:%M")
    except ValueError as e:
        raise railos_exc.ParsingError(
            "Expected time string for finish type 'Frh-sh'"
            f"but received '{finish_components[0]}'"
        ) from e

    _linked_ref = railos_parse_comp.parse_reference(finish_components[2])

    return railos_finish.Frh_sh(
        time=finish_components[0], linked_shuttle_ref=_linked_ref
    )


def parse_Fns_sh(finish_components: typing.List[str]) -> railos_finish.Fer:
    """Parse an Fns-sh type string"""
    if len(finish_components) != 4:
        raise railos_exc.ParsingError(
            "Expected 4 items in components "
            f"'{finish_components}' for finish type 'Fns-sh'"
        )

    try:
        datetime.strptime(finish_components[0], "%H:%M")
    except ValueError as e:
        raise railos_exc.ParsingError(
            "Expected time string for finish type 'Fns-sh'"
            f"but received '{finish_components[0]}'"
        ) from e

    _linked_shuttle_ref = railos_parse_comp.parse_reference(finish_components[2])
    _finish_ref = railos_parse_comp.parse_reference(finish_components[3])

    return railos_finish.Fns_sh(
        time=finish_components[0],
        linked_shuttle_ref=_linked_shuttle_ref,
        finishing_service_ref=_finish_ref,
    )


def parse_F_nshs(finish_components: typing.List[str]) -> railos_finish.Fer:
    """Parse an F-nshs type string"""
    if len(finish_components) != 3:
        raise railos_exc.ParsingError(
            "Expected 3 items in components "
            f"'{finish_components}' for finish type 'F-nshs'"
        )

    try:
        datetime.strptime(finish_components[0], "%H:%M")
    except ValueError as e:
        raise railos_exc.ParsingError(
            "Expected time string for finish type 'F-nshs'"
            f"but received '{finish_components[0]}'"
        ) from e

    _linked_shuttle_ref = railos_parse_comp.parse_reference(finish_components[2])

    return railos_finish.F_nshs(
        time=finish_components[0], linked_shuttle_ref=_linked_shuttle_ref
    )


def parse_Frh(finish_components: typing.List[str]) -> railos_finish.Fer:
    """Parse an Frh type string"""
    if len(finish_components) != 1:
        raise railos_exc.ParsingError(
            "Expected one component " f"'{finish_components}' for finish type 'Frh'"
        )

    return railos_finish.Frh()


def parse_finish(finish_str: str) -> railos_comp.StartType:
    PARSE_DICT = {
        "Fjo": parse_Fjo,
        "Fer": parse_Fer,
        "Frh-sh": parse_Frh_sh,
        "Fns-sh": parse_Fns_sh,
        "Fns": parse_Fns,
        "F-nshs": parse_F_nshs,
        "Frh": parse_Frh,
    }

    try:
        _components = railos_ttb_str.split(finish_str)
    except IndexError as e:
        raise railos_exc.ParsingError(
            f"Failed to extract ttb components from '{finish_str}'"
        ) from e

    for finish_type, parser in PARSE_DICT.items():
        if finish_type in finish_str:
            return parser(_components)
    raise railos_exc.ParsingError(f"Failed to determine finish type for '{finish_str}'")
