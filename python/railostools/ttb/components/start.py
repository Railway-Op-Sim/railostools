import datetime

import pydantic

import railostools.common.coords as ros_coords
import railostools.ttb.components as ros_comp
import railostools.ttb.string as ros_ttb_str


class Snt(ros_comp.StartType, pydantic.BaseModel):
    time: datetime.time
    rear_element_id: ros_coords.Coordinate
    front_element_id: ros_coords.Coordinate
    under_signaller_control: bool = False

    def __str__(self) -> str:
        _elements = [
            self.time,
            self.name,
            f"{self.rear_element_id} {self.front_element_id}",
        ]
        if self.under_signaller_control:
            _elements += "S"
        return ros_ttb_str.concat(*_elements)

    @pydantic.validator("time")
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "Snt"
        return vals


class Sns(ros_comp.StartType, pydantic.BaseModel):
    time: datetime.time
    parent_service: ros_comp.Reference

    def __str__(self) -> str:
        return ros_ttb_str.concat(self.time, self.name, f"{self.parent_service}")

    @pydantic.validator("time")
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "Sns"
        return vals


class Sfs(ros_comp.StartType, pydantic.BaseModel):
    time: datetime.time
    splitting_service: ros_comp.Reference

    def __str__(self) -> str:
        return ros_ttb_str.concat(self.time, self.name, f"{self.splitting_service}")

    @pydantic.validator("time")
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "Sfs"
        return vals


class Sns_fsh(ros_comp.StartType, pydantic.BaseModel):
    time: datetime.time
    shuttle_ref: ros_comp.Reference

    def __str__(self) -> str:
        return ros_ttb_str.concat(self.time, self.name, f"{self.shuttle_ref}")

    @pydantic.validator("time")
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "Sns-fsh"
        return vals


class Snt_sh(ros_comp.StartType, pydantic.BaseModel):
    time: datetime.time
    rear_element_id: ros_coords.Coordinate
    front_element_id: ros_coords.Coordinate
    shuttle_ref: ros_comp.Reference

    def __str__(self) -> str:
        return ros_ttb_str.concat(
            self.time,
            self.name,
            f"{self.rear_element_id} {self.front_element_id}",
            f"{self.shuttle_ref}",
        )

    @pydantic.validator("time")
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "Snt-sh"
        return vals


class Sns_sh(ros_comp.StartType, pydantic.BaseModel):
    time: datetime.time
    feeder_ref: ros_comp.Reference
    linked_shuttle_ref: ros_comp.Reference

    def __str__(self) -> str:
        return ros_ttb_str.concat(
            self.time, self.name, f"{self.linked_shuttle_ref}", f"{self.feeder_ref}"
        )

    @pydantic.validator("time")
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "Sns-sh"
        return vals
