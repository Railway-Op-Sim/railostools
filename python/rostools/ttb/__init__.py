

import typing


class Statement:
    def __init__(self):
        self.elements: typing.List[Element] = []

    def __str__(self) -> str:
        return concat(*self.elements)

    def __add__(self, other) -> str:
        if not isinstance(other, Element):
            raise ValueError("Can only add timetable statements to a statement")
        return concat(self, other)

class Element:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return self.__class__.__name__

    def __add__(self, other) -> str:
        if not isinstance(other, Element):
            raise ValueError("Can only add timetable elements to an element")
        return concat(self, other)


def concat(*args, join_type=None) -> str:
    if not args:
        return ""
    if (join_type is Element) or isinstance(args[0], Element):
        return ";".join(str(i) for i in args)
    elif (join_type is Statement) or isinstance(args[0], Statement):
        return "\0".join(str(i) for i in args)
    else:
        raise ValueError(f"Invalid type '{type(args[0])}' for timetable concatenation")
