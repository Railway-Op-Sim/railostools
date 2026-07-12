import datetime
import typing

import pydantic

import railostools.common.coords as railos_coords
import railostools.ttb.components as railos_comp
import railostools.ttb.string as railos_ttb_str


class Snt(railos_comp.StartType, pydantic.BaseModel):
    time: datetime.time
    time_days: int = 0
    rear_element_id: railos_coords.Coordinate
    front_element_id: railos_coords.Coordinate
    under_signaller_control: bool = False

    @typing.override
    def __str__(self) -> str:
        _time_str: str = railos_comp.time2str(self.time, self.time_days)
        _elements = [
            _time_str,
            self.name,
            f"{self.rear_element_id} {self.front_element_id}",
        ]
        if self.under_signaller_control:
            _elements += "S"
        return railos_comp.concat(*_elements)


class Sns(railos_comp.StartType, pydantic.BaseModel):
    time: datetime.time
    time_days: int = 0
    parent_service: railos_comp.Reference

    @typing.override
    def __str__(self) -> str:
        _time_str: str = railos_comp.time2str(self.time, self.time_days)
        return railos_comp.concat(_time_str, self.name, f"{self.parent_service}")


class Sfs(railos_comp.StartType, pydantic.BaseModel):
    time: datetime.time
    time_days: int = 0
    splitting_service: railos_comp.Reference

    @typing.override
    def __str__(self) -> str:
        _time_str: str = railos_comp.time2str(self.time, self.time_days)
        return railos_comp.concat(_time_str, self.name, f"{self.splitting_service}")


class Sns_fsh(railos_comp.StartType, pydantic.BaseModel):
    time: datetime.time
    time_days: int = 0
    shuttle_ref: railos_comp.Reference

    @typing.override
    def __str__(self) -> str:
        _time_str: str = railos_comp.time2str(self.time, self.time_days)
        return railos_comp.concat(_time_str, self.name, f"{self.shuttle_ref}")


class Snt_sh(railos_comp.StartType, pydantic.BaseModel):
    time: datetime.time
    time_days: int = 0
    rear_element_id: railos_coords.Coordinate
    front_element_id: railos_coords.Coordinate
    shuttle_ref: railos_comp.Reference

    @typing.override
    def __str__(self) -> str:
        _time_str: str = railos_comp.time2str(self.time, self.time_days)
        return railos_comp.concat(
            _time_str,
            self.name,
            f"{self.rear_element_id} {self.front_element_id}",
            f"{self.shuttle_ref}",
        )


class Sns_sh(railos_comp.StartType, pydantic.BaseModel):
    time: datetime.time
    time_days: int = 0
    feeder_ref: railos_comp.Reference
    linked_shuttle_ref: railos_comp.Reference

    @typing.override
    def __str__(self) -> str:
        _time_str: str = railos_comp.time2str(self.time, self.time_days)
        return railos_comp.concat(
            _time_str, self.name, f"{self.linked_shuttle_ref}", f"{self.feeder_ref}"
        )
