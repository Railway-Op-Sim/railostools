from collections.abc import Mapping
import datetime
from typing import Any, ClassVar, Iterator, Self, cast
import pydantic

from railostools.common.coords import Coordinate
from railostools.ttb.components import Element, Reference, StartType, TimedEvent
from railostools.ttb.components.actions import Location, cms, dsc, jbo, pas, rsp

from .components.finish import Finish, Fjo
from .components.start import Sns, Snt, Start
from .parsing.time import TimeStr, adjust_above_24hr


class Service(pydantic.BaseModel, Mapping):
    start_type: Start = "Snt"
    reference: Reference
    parent_reference: Reference | None = None
    start_time: datetime.time
    start_speed: pydantic.NonNegativeInt | None = None
    max_speed: pydantic.PositiveInt
    mass: pydantic.PositiveInt
    brake_force: pydantic.PositiveInt
    power: pydantic.PositiveInt
    start_position: tuple[Coordinate, Coordinate] | None = None

    model_config: ClassVar[pydantic.ConfigDict] = {
        "arbitrary_types_allowed": True,
        "extra": "forbid",
    }
    _actions: dict[datetime.time, Element] = pydantic.PrivateAttr(
        default_factory=dict[datetime.time, Element]
    )
    _finish_type: Finish | None = pydantic.PrivateAttr(None)

    @pydantic.model_validator(mode="after")
    def _set_start_action(self) -> Self:
        """Assign given start type."""
        _start: StartType

        if self.start_type == "Snt":
            if not self.start_position:
                raise ValueError("A start position must be provided for type 'Snt'")
            _start: StartType = Snt(
                time=self.start_time,
                rear_element_id=self.start_position[0],
                front_element_id=self.start_position[1],
            )
        elif self.start_type == "Sns":
            if not self.parent_reference:
                raise ValueError("A parent reference must be provided for type 'Sns'")
            _start = Sns(
                time=self.start_time,
                parent_service=self.parent_reference,
            )
        else:
            raise ValueError(f"Unrecognised start type '{self.start_type}'.")

        self._actions[_start.time] = _start
        return self

    def __getitem__(self, key: str | datetime.time, /) -> Element:
        _key: datetime.time
        if isinstance(key, str):
            _key, _ = adjust_above_24hr(
                time_candidate=key,
                error_message="Failed to convert key for item retrieval",
            )
        return self._actions.__getitem__(_key)

    def __len__(self) -> int:
        return len(self._actions)

    def add_item(self, item: TimedEvent) -> None:
        if self.finish_type is not None:
            raise AttributeError("Cannot append item to finalised service.")
        if item.time in self._actions:
            raise KeyError(f"Cannot have multiple events at same time: {item.time}")
        self._actions[item.time] = item

    @property
    def finish_type(self) -> Finish:
        return self._finish_type

    @property
    def specifications(self) -> dict[str, pydantic.PositiveInt]:
        """Get specs of current service."""
        return {
            "max_speed": self.max_speed,
            "brake_force": self.brake_force,
            "power": self.power,
            "mass": self.mass,
        }

    def _location(
        self, location: str, time: TimeStr, end_time: TimeStr | None = None
    ) -> Self:
        _location = Location(
            location=location,
            time=cast(datetime.time, time),
            end_time=cast(datetime.time | None, end_time),
        )
        self.add_item(_location)
        return self

    def call_at(self, location: str, arrive: TimeStr, depart: TimeStr) -> Self:
        return self._location(location=location, time=arrive, end_time=depart)

    def depart(self, location: str, time: TimeStr) -> Self:
        return self._location(location=location, time=time)

    def arrive(self, location: str, time: TimeStr) -> Self:
        return self._location(location=location, time=time)

    def pass_location(self, location: str, time: TimeStr) -> Self:
        """Pass a location at the given time."""
        _pass = pas(location=location, time=cast(datetime.time, time))
        self.add_item(_pass)
        return self

    def rear_split(self, reference: str, time: TimeStr) -> "Service":
        _rsplit = rsp(time=cast(datetime.time, time), new_service_ref=Reference.from_str(reference))
        self.add_item(_rsplit)
        return self.__class__(
            start_type="Sns",
            reference=Reference.from_str(reference),
            start_time=cast(datetime.time, time),
            **self.specifications,
        )

    def front_split(self, reference: str, time: str) -> "Service":
        _start, _offset = adjust_above_24hr(
            time_candidate=time, error_message="Failed to split time"
        )
        _fsplit = fsp(time=_start, time_days=_offset, new_service_ref=reference)
        self.add_item(_fsplit)
        return self.__class__(
            start_type="Sns",
            reference=reference,
            start_time=time,
            **self.specifications,
        )

    def join_other(self, other: "Service", time: str) -> "Service":
        """End this service by joining to another."""
        _time, _offset = adjust_above_24hr(
            time_candidate=time, error_message="Invalid time for service join."
        )
        _end = Fjo(time=_time, time_days=_offset, joining_service_ref=other.reference)
        self._finish_type = "Fjo"
        self.add_item(_end)
        _jbo = jbo(time=_time, time_days=_offset, joining_service_ref=self.reference)
        other.add_item(_jbo)
        return other

    def change_description(self, description: str, time: str) -> Self:
        """Change description during service."""
        _time, _offset = adjust_above_24hr(
            time_candidate=time, error_message="Invalid time for service join."
        )
        _dsc = dsc(time=_time, time_days=_offset, description=description)
        self.add_item(_dsc)
        return self

    def change_max_speed(self, new_speed: pydantic.PositiveInt, time: str) -> Self:
        """Change the maximum speed at a given time."""
        _time, _offset = adjust_above_24hr(
            time_candidate=time, error_message="Invalid time for service join."
        )
        _csp = cms(time=_time, time_days=_offset, new_speed=new_speed)
        self.add_item(_csp)
        return self

    def become(self, new_reference: str, time: str) -> "Service":
        """Finish current service and form new."""
        _time, _offset = adjust_above_24hr(
            time_candidate=time, error_message="Invalid time for service join."
        )
        return self.__class__(
            start_type="Sns",
            start_time=_time,
            reference=Reference.from_str(new_reference),
            parent_reference=self.reference,
            **self.specifications,
        )


class TTB:
    def __init__(self, start_time: str) -> None:
        self._services: dict[str, Service] = {}
        self._start_time: datetime.time
        self._start_time, _ = adjust_above_24hr(
            time_candidate=start_time, error_message="Invalid start time."
        )

    def add_service(
        self,
        reference: str,
        *,
        start_time: str,
        start_speed: pydantic.NonNegativeInt,
        max_speed: pydantic.PositiveInt,
        brake_force: pydantic.PositiveInt,
        power: pydantic.PositiveInt,
        mass: pydantic.PositiveInt,
        start_position: tuple[Coordinate, Coordinate],
        offset_days: pydantic.NonNegativeInt = 0,
    ) -> Service:
        if self._services.get(reference):
            raise NotImplementedError(
                f"Failed to initialise service '{reference}', "
                "Creation of multiple services with the same reference is not supported."
            )
        _time, _ = adjust_above_24hr(
            time_candidate=start_time, error_message="Invalid service start time."
        )
        _service = Service(
            reference=Reference.from_str(reference),
            start_time=_time,
            start_speed=start_speed,
            brake_force=brake_force,
            mass=mass,
            power=power,
            max_speed=max_speed,
            start_position=start_position,
            offset_days=offset_days,
        )
        self._services[reference] = _service
        return self._services[reference]
