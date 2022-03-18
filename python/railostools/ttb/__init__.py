

import datetime
import typing
import pydantic
import railostools.ttb.services as ros_srv
import railostools.common.utilities as ros_util


class Element:
    def __str__(self) -> str:
        return self.__class__.__name__

    def __add__(self, other) -> str:
        if not isinstance(other, Element):
            raise ValueError("Can only add timetable elements to an element")
        return concat(self, other, join_type=Element)


class FinishType(Element):
    def __str__(self) -> str:
        return super().__str__()


class ActionType(Element):
    def __str__(self) -> str:
        return super().__str__()


class StartType(Element):
    def __str__(self) -> str:
        return super().__str__()


@ros_util.dictify
class Header(pydantic.BaseModel, Element):
    reference: ros_srv.Reference
    description: str
    start_speed: pydantic.conint(ge=0)
    max_speed: pydantic.conint(ge=0)
    mass: pydantic.conint(ge=0)
    power: pydantic.conint(ge=0)
    max_signaller_speed: typing.Optional[pydantic.conint(ge=0)]
    def __str__(self) -> str:
        _elements = [
            f"{self.reference}",
            self.description,
            f"{self.start_speed}",
            f"{self.max_speed}",
            f"{self.mass}",
            f"{self.power}",
        ]
        if self.max_signaller_speed:
            _elements.append(self.max_signaller_speed)

        return concat(*_elements)


@ros_util.dictify
class Service(pydantic.BaseModel):
    header: Header
    start_type: StartType
    finish_type: FinishType
    actions: typing.Optional[typing.Dict[int, ActionType]] = {}
    def __str__(self) -> str:
        _elements = [
            f"{self.header}",
            f"{self.start_type}"
        ]
        if self.actions:
            _elements.append(concat(*(
                self.actions[k] for k, _ in enumerate(self.actions)
            ), join_type=Element))
        _elements.append(f"{self.finish_type}")
        return concat(*_elements, join_type=Element)

    class Config:
        arbitrary_types_allowed = True


class Timetable(pydantic.BaseModel):
    start_time: datetime.time
    services: typing.List[Service]
    comments: typing.Optional[typing.Dict[int, str]] = None

    @pydantic.validator('start_time')
    def to_string(cls, v):
        return v.strftime("%H:%M")


def concat(*args, join_type=None) -> str:
    if not args:
        return ""
    if (join_type is Element) or isinstance(args[0], Element):
        return "\0".join(str(i) for i in args)
    else:
        return ";".join(str(i) for i in args)
