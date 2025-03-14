import datetime
import typing

import pydantic

import railostools.exceptions as railos_exc
import railostools.ttb.components as railos_comp
import railostools.ttb.string as railos_ttb_str
from pydantic import Field, StringConstraints, ConfigDict
from typing_extensions import Annotated


class Element:
    def __str__(self) -> str:
        return self.__class__.__name__

    def __add__(self, other) -> str:
        if not isinstance(other, Element):
            raise ValueError("Can only add timetable elements to an element")
        return railos_ttb_str.concat(self, other, join_type=Element)


class FinishType(Element):
    def __str__(self) -> str:
        return super().__str__()


class ActionType(Element, pydantic.BaseModel):
    time: datetime.time
    warning: bool = False

    def __str__(self) -> str:
        return f'{"W" if self.warning else ""}{super().__str__()}'

    @pydantic.model_validator(mode="before")
    def check_for_warning(cls, vals: typing.Dict) -> typing.Dict:
        _time = vals["time"]
        if isinstance(_time, str) and _time.upper().startswith("W"):
            vals["warning"] = True
            vals["time"] = _time[1:]
        return vals


class StartType(Element):
    def __str__(self) -> str:
        return super().__str__()


class Reference(pydantic.BaseModel):
    prefix: typing.Optional[Annotated[str, StringConstraints(max_length=4)]] = None
    service: Annotated[str, StringConstraints(max_length=2, min_length=2)]
    id: typing.Union[
        Annotated[int, Field(ge=0, lt=100)], Annotated[str, StringConstraints(min_length=2, max_length=2)]
    ]

    def __str__(self) -> str:
        if isinstance(self.id, int):
            _id_str = str(self.id) if len(str(self.id)) == 2 else f"0{self.id}"
        else:
            _id_str = self.id
        return f'{self.prefix or ""}{self.service}{_id_str}'

    def __iadd__(self, num: int) -> None:
        if isinstance(self.id, str):
            raise railos_exc.InvalidOperationError(
                f"Cannot increment reference with ID '{self.id}'"
            )
        if self.id + num > 99:
            raise ValueError("ID must be between 0 and 99")
        self.id += num

    def __isub__(self, num: int) -> None:
        if isinstance(self.id, str):
            raise railos_exc.InvalidOperationError(
                f"Cannot decrement reference with ID '{self.id}'"
            )
        if self.id - num < 1:
            raise ValueError("ID must be between 0 and 99")
        self.id -= num


class Header(pydantic.BaseModel, Element):
    reference: railos_comp.Reference
    description: typing.Optional[str] = None
    start_speed: typing.Optional[Annotated[int, Field(ge=0)]] = None
    max_speed: typing.Optional[Annotated[int, Field(ge=0)]] = None
    mass: typing.Optional[Annotated[int, Field(ge=0)]] = None
    brake_force: typing.Optional[Annotated[int, Field(ge=0)]] = None
    power: typing.Optional[Annotated[int, Field(ge=0)]] = None
    max_signaller_speed: typing.Optional[Annotated[int, Field(ge=0)]] = None

    def __str__(self) -> str:
        _elements = [
            f"{self.reference}",
        ]
        if self.description:
            _elements.append(self.description)
        if self.max_speed:
            _elements += [
                f"{self.start_speed}",
                f"{self.max_speed}",
                f"{self.mass}",
                f"{self.power}",
            ]
        if self.max_signaller_speed:
            _elements.append(f"{self.max_signaller_speed}")

        return railos_ttb_str.concat(*_elements)


class Repeat(pydantic.BaseModel, Element):
    mins: Annotated[int, Field(gt=1)]
    digits: Annotated[int, Field(ge=0)]
    repeats: Annotated[int, Field(ge=1)]

    def __str__(self) -> str:
        return railos_ttb_str.concat(
            f"{self.mins}", f"{self.digits}", f"{self.repeats}"
        )


class Service(pydantic.BaseModel):
    header: Header
    start_type: StartType
    model_config = ConfigDict(arbitrary_types_allowed=True)


class TimetabledService(Service):
    header: Header
    start_type: StartType
    finish_type: FinishType
    actions: typing.Optional[typing.Dict[int, ActionType]] = {}
    repeats: typing.Optional[Repeat] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __str__(self) -> str:
        _elements = [f"{self.header}", f"{self.start_type}"]
        if self.actions:
            _elements.append(
                railos_ttb_str.concat(
                    *(self.actions[k] for k in sorted(self.actions.keys())),
                    join_type=Element,
                )
            )
        _elements.append(f"{self.finish_type}")
        return railos_ttb_str.concat(*_elements, join_type=Element)


class SignallerService(Service):
    header: Header
    start_type: StartType
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __str__(self) -> str:
        return railos_ttb_str.concat(f"{self.header}", f"{self.start_type}")


class Timetable(pydantic.BaseModel):
    start_time: datetime.time
    services: typing.Dict[str, TimetabledService | SignallerService]
    comments: typing.Optional[typing.Dict[int, str]] = None

    @pydantic.field_validator("start_time")
    def to_string(cls, v):
        return v.strftime("%H:%M")
