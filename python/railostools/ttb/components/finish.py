import datetime
import typing

import pydantic

import railostools.common.coords as railos_coords
import railostools.ttb.components as railos_comp
import railostools.ttb.string as railos_ttb_str


class Fns(railos_comp.FinishType, pydantic.BaseModel):
    time: datetime.time
    new_service_ref: railos_comp.Reference

    def __str__(self) -> str:
        return railos_ttb_str.concat(
            self.time, self.name, f"{self.new_service_ref}", join_type=railos_comp.Element
        )

    @pydantic.validator("time")
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "Fns"
        return vals


class Fjo(railos_comp.FinishType, pydantic.BaseModel):
    time: datetime.time
    joining_service_ref: railos_comp.Reference

    def __str__(self) -> str:
        return railos_ttb_str.concat(
            self.time,
            self.name,
            f"{self.joining_service_ref}",
            join_type=railos_comp.Element,
        )

    @pydantic.validator("time")
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "Fjo"
        return vals


class Fer(railos_comp.FinishType, pydantic.BaseModel):
    time: datetime.time
    exit_coords: typing.List[railos_coords.Coordinate]

    def __str__(self) -> str:
        return railos_ttb_str.concat(
            self.time, self.name, " ".join(self.exit_coords), join_type=railos_comp.Element
        )

    @pydantic.validator("time")
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "Fer"
        return vals


class Frh_sh(railos_comp.FinishType, pydantic.BaseModel):
    time: datetime.time
    linked_shuttle_ref: railos_comp.Reference

    def __str__(self) -> str:
        return railos_ttb_str.concat(
            self.time,
            self.name,
            f"{self.linked_shuttle_ref}",
            join_type=railos_comp.Element,
        )

    @pydantic.validator("time")
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "Frh-sh"
        return vals


class Fns_sh(railos_comp.FinishType, pydantic.BaseModel):
    time: datetime.time
    linked_shuttle_ref: railos_comp.Reference
    finishing_service_ref: railos_comp.Reference

    def __str__(self) -> str:
        return railos_ttb_str.concat(
            self.time,
            self.name,
            f"{self.linked_shuttle_ref}",
            f"{self.finishing_service_ref}",
            join_type=railos_comp.Element,
        )

    @pydantic.validator("time")
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "Fns-sh"
        return vals


class F_nshs(railos_comp.FinishType, pydantic.BaseModel):
    time: datetime.time
    linked_shuttle_ref: railos_comp.Reference

    def __str__(self) -> str:
        return railos_ttb_str.concat(
            self.time,
            self.name,
            f"{self.linked_shuttle_ref}",
            join_type=railos_comp.Element,
        )

    @pydantic.validator("time")
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "F-nshs"
        return vals


class Frh(railos_comp.FinishType, pydantic.BaseModel):
    def __str__(self) -> str:
        return self.__class__.__name__

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "Frh"
        return vals
