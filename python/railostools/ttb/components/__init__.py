import datetime
import typing
import pydantic
import railostools.ttb.string as ros_ttb_str
import railostools.ttb.components as ros_comp
import railostools.common.utilities as ros_util

class Element:
    def __str__(self) -> str:
        return self.__class__.__name__

    def __add__(self, other) -> str:
        if not isinstance(other, Element):
            raise ValueError("Can only add timetable elements to an element")
        return ros_ttb_str.concat(self, other, join_type=Element)


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
class Reference(pydantic.BaseModel):
    prefix: typing.Optional[pydantic.constr(max_length=4)] = None
    service: pydantic.constr(max_length=2, min_length=2)
    id: pydantic.conint(gt=0, lt=100)
    def __str__(self) -> str:
        _id_str = str(self.id) if len(str(self.id)) == 2 else f'0{self.id}'
        return f'{self.prefix or ""}{self.service}{_id_str}'
    def __iadd__(self, num: int) -> None:
        if self.id + num > 99:
            raise ValueError("ID must be between 0 and 99")
        self.id += num
    def __isub__(self, num: int) -> None:
        if self.id - num < 1:
            raise ValueError("ID must be between 0 and 99")
        self.id -= num


@ros_util.dictify
class Header(pydantic.BaseModel, Element):
    reference: ros_comp.Reference
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

        return ros_ttb_str.concat(*_elements)


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
            _elements.append(ros_ttb_str.concat(*(
                self.actions[k] for k, _ in enumerate(self.actions)
            ), join_type=Element))
        _elements.append(f"{self.finish_type}")
        return ros_ttb_str.concat(*_elements, join_type=Element)

    class Config:
        arbitrary_types_allowed = True


@ros_util.dictify
class Timetable(pydantic.BaseModel):
    start_time: datetime.time
    services: typing.List[Service]
    comments: typing.Optional[typing.Dict[int, str]] = None

    @pydantic.validator('start_time')
    def to_string(cls, v):
        return v.strftime("%H:%M")

