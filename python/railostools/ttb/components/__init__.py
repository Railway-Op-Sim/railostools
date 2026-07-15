import datetime
import typing

import pydantic

import railostools.exceptions as railos_exc
import railostools.ttb.components as railos_comp
from pydantic import Field, StringConstraints, ConfigDict
from typing_extensions import Annotated


def concat(*args: "Element | str", join_type: type | None = None) -> str:
    if not args:
        return ""
    if (join_type is Element) or isinstance(args[0], Element):
        return "\0".join(str(i) for i in args)
    else:
        return ";".join(str(i) for i in args)


def split(component_str: str, split_type: type | None = None) -> list[str]:
    if split_type is Element:
        _split_char = "\0"
    elif split_type is Service:
        _split_char = ","
    else:
        _split_char = ";"
    return component_str.split(_split_char)


class Element:
    def __str__(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        """Return object name."""
        return self.__class__.__name__.replace("_", "-")

    def __add__(self, other) -> str:
        if not isinstance(other, Element):
            raise ValueError("Can only add timetable elements to an element")
        return concat(self, other, join_type=Element)


@pydantic.validate_call
def time2str(time: datetime.time, time_days: int) -> str:
    """Return RailOS string form for time."""
    _hour: int = time.hour + time_days * 24
    _min: int = time.minute
    _time_str: str = (
        f"{'0' if _hour < 10 else ''}{_hour}:{'0' if _min < 10 else ''}{_min}"
    )
    return _time_str


class TimedEvent(Element, pydantic.BaseModel):
    time: datetime.time
    time_days: pydantic.NonNegativeInt = 0
    warning: bool = False

    @typing.override
    def __str__(self) -> str:
        return f'{"W" if self.warning else ""}{self._component_str}'

    @property
    def _component_str(self) -> str:
        _time_str: str = time2str(self.time, self.time_days)
        return concat(_time_str, self.name)

    @pydantic.model_validator(mode="before")
    def check_for_warning(cls, vals: dict[str, float | str]) -> dict[str, float | str]:
        _time = vals["time"]
        if isinstance(_time, str) and _time.upper().startswith("W"):
            vals["warning"] = True
            vals["time"] = _time[1:]
        return vals


class ComponentCommonType(Element, pydantic.BaseModel):
    model_config = pydantic.ConfigDict(validate_default=True, extra="forbid")


class StartType(ComponentCommonType, TimedEvent):
    pass


class FinishType(ComponentCommonType):
    pass


class ActionType(ComponentCommonType, TimedEvent):
    pass


class Reference(pydantic.BaseModel):
    prefix: Annotated[str, StringConstraints(max_length=4)] | None = None
    service: Annotated[str, StringConstraints(max_length=2, min_length=2)]
    id: (
        Annotated[int, Field(ge=0, lt=100)]
        | Annotated[str, StringConstraints(min_length=2, max_length=2)]
    )

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
    description: str | None = None
    start_speed: Annotated[int, Field(ge=0)] | None = None
    max_speed: Annotated[int, Field(ge=0)] | None = None
    mass: Annotated[int, Field(ge=0)] | None = None
    brake_force: Annotated[int, Field(ge=0)] | None = None
    power: Annotated[int, Field(ge=0)] | None = None
    max_signaller_speed: Annotated[int, Field(ge=0)] | None = None

    @typing.override
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

        return concat(*_elements)


class Repeat(pydantic.BaseModel, Element):
    mins: Annotated[int, Field(gt=1)]
    digits: Annotated[int, Field(ge=0)]
    repeats: Annotated[int, Field(ge=1)]

    @typing.override
    def __str__(self) -> str:
        return concat(f"{self.mins}", f"{self.digits}", f"{self.repeats}")


class Service(pydantic.BaseModel):
    header: Header
    start_type: StartType
    model_config: pydantic.ConfigDict = ConfigDict(arbitrary_types_allowed=True)


class TimetabledService(Service):
    header: Header
    start_type: StartType
    finish_type: FinishType
    actions: dict[int, ActionType] | None = {}
    repeats: Repeat | None = None

    @typing.override
    def __str__(self) -> str:
        _elements = [f"{self.header}", f"{self.start_type}"]
        if self.actions:
            _elements.append(
                concat(
                    *(self.actions[k] for k in sorted(self.actions.keys())),
                    join_type=Element,
                )
            )
        _elements.append(f"{self.finish_type}")
        return concat(*_elements, join_type=Element)


class SignallerService(Service):
    header: Header
    start_type: StartType

    @typing.override
    def __str__(self) -> str:
        return concat(f"{self.header}", f"{self.start_type}")


class Timetable(pydantic.BaseModel):
    start_time: datetime.time
    services: dict[str, TimetabledService | SignallerService]
    comments: dict[int, str] | None = None
