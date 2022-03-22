import re

import railostools.ttb.components as ros_comp
import railostools.exceptions as ros_exc

import railostools.ttb.string as ros_ttb_str


def parse_reference(train_ref: str) -> ros_comp.Reference:
    """Parse a service reference identifier"""
    if len(train_ref) > 8 or len(train_ref) < 4:
        raise ros_exc.ParsingError(
            f"Length of ervice reference '{train_ref}' "
            "must be between 4 and 8"
        )
    _headcode = train_ref[-4:]
    _hc_service = _headcode[:2]
    _hc_id = int(_headcode[2:])

    _prefix = train_ref[:len(train_ref)-4] if len(train_ref) > 4 else None

    return ros_comp.Reference(prefix=_prefix, service=_hc_service, id=_hc_id)


def parse_header(header_str: str) -> ros_comp.Header:
    """Parse a service header"""
    _components = ros_ttb_str.split(header_str)
    if len(_components) not in (2, 7, 8):
        raise ros_exc.ParsingError(
            "Expected 2, 7 or 8 items in components "
            f"'{_components}' for service header"
        )

    if len(_components) > 2:
        start_speed=int(_components[2])
        max_speed=int(_components[3])
        mass=int(_components[4])
        power=int(_components[5])
    if len(_components) > 6:
        max_signaller_speed=int(_components[6])

    _reference = parse_reference(_components[0])

    return ros_comp.Header(
        reference=_reference,
        description=_components[1],
        start_speed=int(_components[2]),
        max_speed=int(_components[3]),
        mass=int(_components[4]),
        brake_force=int(_components[5]),
        power=int(_components[6]),
        max_signaller_speed=int(_components[7]) if len(_components) == 6 else None
    )


def parse_repeat(repeat_str: str) -> ros_comp.Repeat:
    """Parse a repeat statement"""
    if not re.findall(r"^R;", repeat_str):
        raise ros_exc.ParsingError(
            f"Invalid repeat statement '{repeat_str}'"
        )

    _components = ros_ttb_str.split(repeat_str)

    if len(_components) != 4:
        raise ros_exc.ParsingError(
            "Expected 4 items in components "
            f"'{_components}' for repeat statement"
        )

    return ros_comp.Repeat(
        mins=int(_components[1]),
        digits=int(_components[2]),
        repeats=int(_components[3])
    )
