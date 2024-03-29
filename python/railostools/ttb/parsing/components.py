import re

import railostools.exceptions as railos_exc
import railostools.ttb.components as railos_comp
import railostools.ttb.string as railos_ttb_str


def parse_reference(train_ref: str) -> railos_comp.Reference:
    """Parse a service reference identifier"""
    if len(train_ref) > 8 or len(train_ref) < 4:
        raise railos_exc.ParsingError(
            f"Length of service reference '{train_ref}' " "must be between 4 and 8"
        )
    _headcode = train_ref[-4:]
    _hc_service = _headcode[:2]

    try:
        _hc_id = int(_headcode[2:])
    except ValueError:
        _hc_id = _headcode[2:]

    _prefix = train_ref[: len(train_ref) - 4] if len(train_ref) > 4 else None

    return railos_comp.Reference(prefix=_prefix, service=_hc_service, id=_hc_id)


def parse_header(header_str: str) -> railos_comp.Header:
    """Parse a service header"""
    _components = railos_ttb_str.split(header_str)
    if len(_components) not in (1, 2, 7, 8):
        raise railos_exc.ParsingError(
            "Expected 1, 2, 7 or 8 items in components "
            f"'{_components}' for service header"
        )

    description = _components[1] if len(_components) > 1 else None
    start_speed = int(_components[2]) if len(_components) > 2 else None
    max_speed = int(_components[3]) if len(_components) > 2 else None
    mass = int(_components[4]) if len(_components) > 2 else None
    brake_force = int(_components[5]) if len(_components) > 2 else None
    power = int(_components[6]) if len(_components) > 2 else None
    max_signaller_speed = int(_components[7]) if len(_components) > 7 else None

    _reference = parse_reference(_components[0])

    return railos_comp.Header(
        reference=_reference,
        description=description,
        start_speed=start_speed,
        max_speed=max_speed,
        mass=mass,
        brake_force=brake_force,
        power=power,
        max_signaller_speed=max_signaller_speed,
    )


def parse_repeat(repeat_str: str) -> railos_comp.Repeat:
    """Parse a repeat statement"""
    if not re.findall(r"^R;", repeat_str):
        raise railos_exc.ParsingError(f"Invalid repeat statement '{repeat_str}'")

    _components = railos_ttb_str.split(repeat_str)

    if len(_components) != 4:
        raise railos_exc.ParsingError(
            "Expected 4 items in components " f"'{_components}' for repeat statement"
        )
    return railos_comp.Repeat(
        mins=int(_components[1]),
        digits=int(_components[2]),
        repeats=int(_components[3]),
    )
