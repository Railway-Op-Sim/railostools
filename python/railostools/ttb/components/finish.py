import typing
import pydantic
import datetime

import railostools.ttb.components as ros_comp
import railostools.ttb.string as ros_ttb_str
import railostools.common.coords as ros_coords
import railostools.common.utilities as ros_util

from pydantic.fields import ModelField


@ros_util.dictify
class Fns(pydantic.BaseModel, ros_comp.FinishType):
    time: datetime.time
    new_service_ref: ros_comp.Reference
    def __str__(self) -> str:
        return ros_ttb_str.concat(
            self.time,
            self.__class__.__name__.replace("_", "-"),
            f'{self.new_service_ref}',
            join_type=ros_comp.Element
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = cls.__class__.__name__
        return vals


@ros_util.dictify
class Fjo(pydantic.BaseModel, ros_comp.FinishType):
    time: datetime.time
    joining_service_ref: ros_comp.Reference
    def __str__(self) -> str:
        return ros_ttb_str.concat(
            self.time,
            self.__class__.__name__.replace("_", "-"),
            f'{self.joining_service_ref}',
            join_type=ros_comp.Element
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = cls.__class__.__name__
        return vals


@ros_util.dictify
class Fer(pydantic.BaseModel, ros_comp.FinishType):
    time: datetime.time
    exit_coords: typing.List[ros_coords.Coordinate]
    def __str__(self) -> str:
        return ros_ttb_str.concat(
            self.time,
            self.__class__.__name__.replace("_", "-"),
            " ".join(self.exit_coords),
            join_type=ros_comp.Element
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = cls.__class__.__name__
        return vals


@ros_util.dictify
class Frh_sh(pydantic.BaseModel, ros_comp.FinishType):
    time: datetime.time
    linked_shuttle_ref: ros_comp.Reference
    def __str__(self) -> str:
        return ros_ttb_str.concat(
            self.time,
            self.__class__.__name__.replace("_", "-"),
            f"{self.linked_shuttle_ref}",
            join_type=ros_comp.Element
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = cls.__class__.__name__
        return vals


@ros_util.dictify
class Fns_sh(pydantic.BaseModel, ros_comp.FinishType):
    time: datetime.time
    linked_shuttle_ref: ros_comp.Reference
    finishing_service_ref: ros_comp.Reference
    def __str__(self) -> str:
        return ros_ttb_str.concat(
            self.time,
            self.__class__.__name__.replace("_", "-"),
            f"{self.linked_shuttle_ref}",
            f"{self.finishing_service_ref}",
            join_type=ros_comp.Element
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = cls.__class__.__name__
        return vals


@ros_util.dictify
class F_nshs(pydantic.BaseModel, ros_comp.FinishType):
    time: datetime.time
    linked_shuttle_ref: ros_comp.Reference
    def __str__(self) -> str:
        return ros_ttb_str.concat(
            self.time,
            self.__class__.__name__.replace("_", "-"),
            f"{self.linked_shuttle_ref}",
            join_type=ros_comp.Element
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = cls.__class__.__name__
        return vals


@ros_util.dictify
class Frh(pydantic.BaseModel, ros_comp.FinishType):
    def __str__(self) -> str:
        return self.__class__.__name__

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = cls.__class__.__name__
        return vals
