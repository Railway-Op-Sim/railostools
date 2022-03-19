import pydantic
import typing
import datetime

import railostools.ttb.components as ros_comp
import railostools.common.coords as ros_coords
import railostools.ttb.string as ros_ttb_str
import railostools.common.utilities as ros_util


@ros_util.dictify
class Location(pydantic.BaseModel, ros_comp.ActionType):
    start_time: datetime.time
    end_time: typing.Optional[datetime.time]
    name: str
    def __str__(self) -> str:
        _elements = [self.start_time]
        if self.end_time:
            _elements.append(self.end_time)
        _elements.append(self.name)
        return ros_ttb_str.concat(*_elements)

    @pydantic.validator('start_time', 'end_time')
    def to_string(cls, v):
        return v.strftime("%H:%M") if v else v


@ros_util.dictify
class pas(pydantic.BaseModel, ros_comp.ActionType):
    time: datetime.time
    location: str
    def __str__(self) -> str:
        return ros_ttb_str.concat(
            self.time,
            self.__class__.__name__.replace("_", "-"),
            f'{self.location}',
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
class jbo(pydantic.BaseModel, ros_comp.ActionType):
    time: datetime.time
    joining_service_ref: ros_comp.Reference
    def __str__(self) -> str:
        return ros_ttb_str.concat(
            self.__class__.__name__.replace("_", "-"),
            f'{self.joining_service_ref}',
            join_type=ros_comp.Element
        )

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = cls.__class__.__name__
        return vals


@ros_util.dictify
class fsp(pydantic.BaseModel, ros_comp.ActionType):
    time: datetime.time
    new_service_ref: ros_comp.Reference
    def __str__(self) -> str:
        return ros_ttb_str.concat(
            self.__class__.__name__.replace("_", "-"),
            f'{self.new_service_ref}',
            join_type=ros_comp.Element
        )

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = cls.__class__.__name__
        return vals


@ros_util.dictify
class rsp(pydantic.BaseModel, ros_comp.ActionType):
    time: datetime.time
    new_service_ref: ros_comp.Reference
    def __str__(self) -> str:
        return ros_ttb_str.concat(
            self.__class__.__name__.replace("_", "-"),
            f'{self.new_service_ref}',
            join_type=ros_comp.Element
        )

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = cls.__class__.__name__
        return vals


@ros_util.dictify
class cdt(pydantic.BaseModel, ros_comp.ActionType):
    time: datetime.time
    def __str__(self) -> str:
        return self.__class__.__name__

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = cls.__class__.__name__
        return vals
