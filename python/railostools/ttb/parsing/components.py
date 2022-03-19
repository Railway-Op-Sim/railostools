import railostools.ttb.components as ros_comp
import railostools.exceptions as ros_exc


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
