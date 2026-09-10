import datetime
from typing import override

import pydantic

import railostools.ttb.components as railos_comp


class Location(railos_comp.ActionType):
    end_time: datetime.time | None = None
    end_time_days: pydantic.NonNegativeInt = 0
    location: str

    @property
    def name(self) -> str:
        return self.location

    @property
    @override
    def _component_str(self) -> str:
        _time_str: str = railos_comp.time2str(self.time, self.time_days)
        _elements = [_time_str]

        if self.end_time:
            _end_time_str: str = railos_comp.time2str(self.end_time, self.end_time_days)
            _elements.append(_end_time_str)

        _elements.append(self.name)
        return railos_comp.concat(*_elements)


class dsc(railos_comp.ActionType, pydantic.BaseModel):
    description: str

    @property
    @override
    def _component_str(self) -> str:
        _time_str: str = railos_comp.time2str(self.time, self.time_days)
        return railos_comp.concat(_time_str, self.name, f"{self.description}")


class pas(railos_comp.ActionType, pydantic.BaseModel):
    location: str

    @property
    @override
    def _component_str(self) -> str:
        _time_str: str = railos_comp.time2str(self.time, self.time_days)
        return railos_comp.concat(_time_str, self.name, f"{self.location}")


class jbo(railos_comp.ActionType, pydantic.BaseModel):
    joining_service_ref: railos_comp.Reference

    @property
    @override
    def _component_str(self) -> str:
        _time_str: str = railos_comp.time2str(self.time, self.time_days)
        return railos_comp.concat(_time_str, self.name, f"{self.joining_service_ref}")


class fsp(railos_comp.ActionType, pydantic.BaseModel):
    new_service_ref: railos_comp.Reference

    @property
    @override
    def _component_str(self) -> str:
        _time_str: str = railos_comp.time2str(self.time, self.time_days)
        return railos_comp.concat(_time_str, self.name, f"{self.new_service_ref}")


class rsp(railos_comp.ActionType, pydantic.BaseModel):
    new_service_ref: railos_comp.Reference

    @property
    @override
    def _component_str(self) -> str:
        _time_str: str = railos_comp.time2str(self.time, self.time_days)
        return railos_comp.concat(_time_str, self.name, f"{self.new_service_ref}")


class cdt(railos_comp.ActionType, pydantic.BaseModel):
    pass


class cms(railos_comp.ActionType, pydantic.BaseModel):
    new_speed: pydantic.PositiveInt

    @property
    @override
    def _component_str(self) -> str:
        _time_str: str = railos_comp.time2str(self.time, self.time_days)
        return railos_comp.concat(_time_str, self.name, f"{self.new_speed}")
