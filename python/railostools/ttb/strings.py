import typing

import railostools.ttb.components as ros_comp


def concat(*args, join_type=None) -> str:
    if not args:
        return ""
    if (join_type is ros_comp.Element) or isinstance(args[0], ros_comp.Element):
        return "\0".join(str(i) for i in args)
    else:
        return ";".join(str(i) for i in args)


def split(
    component_str: str, split_type=None
) -> typing.Union[typing.Tuple[typing.List[str], ...], typing.List[str]]:
    if split_type is ros_comp.Element:
        _split_char = "\0"
    elif split_type is ros_comp.Service:
        _split_char = ","
    else:
        _split_char = ";"
    return component_str.split(_split_char)
