import typing

import railostools.common.coords as railos_coords
import railostools.ttb.components as railos_comp

type Finish = typing.Literal[
    "Fns",
    "Frh",
    "Fns-sh",
    "Fjo",
    "F-nshs",
    "Fer",
]


class Fns(railos_comp.FinishType, railos_comp.TimedEvent):
    new_service_ref: railos_comp.Reference

    @typing.override
    def __str__(self) -> str:
        _time_str: str = railos_comp.time2str(self.time, self.time_days)
        return railos_comp.concat(_time_str, self.name, f"{self.new_service_ref}")


class Fjo(railos_comp.FinishType, railos_comp.TimedEvent):
    joining_service_ref: railos_comp.Reference

    @typing.override
    def __str__(self) -> str:
        _time_str: str = railos_comp.time2str(self.time, self.time_days)
        return railos_comp.concat(_time_str, self.name, f"{self.joining_service_ref}")


class Fer(railos_comp.FinishType, railos_comp.TimedEvent):
    exit_coords: list[railos_coords.Coordinate]

    @typing.override
    def __str__(self) -> str:
        _time_str: str = railos_comp.time2str(self.time, self.time_days)
        return railos_comp.concat(
            _time_str, self.name, " ".join([str(i) for i in self.exit_coords])
        )


class Frh_sh(railos_comp.FinishType, railos_comp.TimedEvent):
    linked_shuttle_ref: railos_comp.Reference

    @typing.override
    def __str__(self) -> str:
        _time_str: str = railos_comp.time2str(self.time, self.time_days)
        return railos_comp.concat(_time_str, self.name, f"{self.linked_shuttle_ref}")


class Fns_sh(railos_comp.FinishType, railos_comp.TimedEvent):
    linked_shuttle_ref: railos_comp.Reference
    finishing_service_ref: railos_comp.Reference

    @typing.override
    def __str__(self) -> str:
        _time_str: str = railos_comp.time2str(self.time, self.time_days)
        return railos_comp.concat(
            _time_str,
            self.name,
            f"{self.linked_shuttle_ref}",
            f"{self.finishing_service_ref}",
        )


class F_nshs(railos_comp.FinishType, railos_comp.TimedEvent):
    linked_shuttle_ref: railos_comp.Reference

    @typing.override
    def __str__(self) -> str:
        _time_str: str = railos_comp.time2str(self.time, self.time_days)
        return railos_comp.concat(_time_str, self.name, f"{self.linked_shuttle_ref}")


class Frh(railos_comp.FinishType):
    @typing.override
    def __str__(self) -> str:
        return self.name
