import typing
import pydantic
import datetime

import railostools.ttb.components as ros_comp
import railostools.ttb.string as ros_ttb_str
import railostools.common.coords as ros_coords


class Fns(ros_comp.FinishType, pydantic.BaseModel):
    time: datetime.time
    new_service_ref: ros_comp.Reference
    def __str__(self) -> str:
        return ros_ttb_str.concat(
            self.time,
            self.name,
            f'{self.new_service_ref}',
            join_type=ros_comp.Element
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "Fns"
        return vals


class Fjo(ros_comp.FinishType, pydantic.BaseModel):
    time: datetime.time
    joining_service_ref: ros_comp.Reference
    def __str__(self) -> str:
        return ros_ttb_str.concat(
            self.time,
            self.name,
            f'{self.joining_service_ref}',
            join_type=ros_comp.Element
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "Fjo"
        return vals


class Fer(ros_comp.FinishType, pydantic.BaseModel):
    time: datetime.time
    exit_coords: typing.List[ros_coords.Coordinate]
    def __str__(self) -> str:
        return ros_ttb_str.concat(
            self.time,
            self.name,
            " ".join(self.exit_coords),
            join_type=ros_comp.Element
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "Fer"
        return vals


class Frh_sh(ros_comp.FinishType, pydantic.BaseModel):
    time: datetime.time
    linked_shuttle_ref: ros_comp.Reference
    def __str__(self) -> str:
        return ros_ttb_str.concat(
            self.time,
            self.name,
            f"{self.linked_shuttle_ref}",
            join_type=ros_comp.Element
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "Frh-sh"
        return vals


class Fns_sh(ros_comp.FinishType, pydantic.BaseModel):
    time: datetime.time
    linked_shuttle_ref: ros_comp.Reference
    finishing_service_ref: ros_comp.Reference
    def __str__(self) -> str:
        return ros_ttb_str.concat(
            self.time,
            self.name,
            f"{self.linked_shuttle_ref}",
            f"{self.finishing_service_ref}",
            join_type=ros_comp.Element
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "Fns-sh"
        return vals


class F_nshs(ros_comp.FinishType, pydantic.BaseModel):
    time: datetime.time
    linked_shuttle_ref: ros_comp.Reference
    def __str__(self) -> str:
        return ros_ttb_str.concat(
            self.time,
            self.name,
            f"{self.linked_shuttle_ref}",
            join_type=ros_comp.Element
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "F-nshs"
        return vals


class Frh(ros_comp.FinishType, pydantic.BaseModel):
    def __str__(self) -> str:
        return self.__class__.__name__

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "Frh"
        return vals
