import typing
import railostools.ttb.components as ros_comp


def concat(*args, join_type=None) -> str:
    if not args:
        return ""
    if (join_type is ros_comp.Element) or isinstance(args[0], ros_comp.Element):
        return "\0".join(str(i) for i in args)
    else:
        return ";".join(str(i) for i in args)


def split(component_str: str) -> typing.Union[typing.Tuple[typing.List[str], ...], typing.List[str]]:
    _lines = component_str.split("\0")
    if len(_lines) == 1:
        return _lines[0].split(";")
    return (
        i.split(";") for i in _lines
    )
