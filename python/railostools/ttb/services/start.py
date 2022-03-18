import pydantic
import datetime

import railostools.ttb.services as ros_srv
import railostools.common.coords as ros_coords
import railostools.ttb as ros_ttb
import railostools.common.utilities as ros_util

from pydantic.fields import ModelField


@ros_util.dictify
class Snt(pydantic.BaseModel, ros_ttb.StartType):
    time: datetime.time
    rear_element_id: ros_coords.Coordinate
    front_element_id: ros_coords.Coordinate
    under_signaller_control: bool = False
    def __str__(self) -> str:
        _elements = [
            self.time,
            self.__class__.__name__.replace("_", "-"),
            f'{self.rear_element_id} {self.front_element_id}',
        ]
        if self.under_signaller_control:
            _elements += 'S'
        return ros_ttb.concat(
            *_elements
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = cls.__class__.__name__
        return vals


@ros_util.dictify
class Sfs(pydantic.BaseModel, ros_ttb.StartType):
    time: datetime.time
    splitting_service: ros_srv.Reference
    def __str__(self) -> str:
        return ros_ttb.concat(
            self.time,
            self.__class__.__name__.replace("_", "-"),
            f'{self.splitting_service}'
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = cls.__class__.__name__
        return vals


@ros_util.dictify
class Sns_fsh(pydantic.BaseModel, ros_ttb.StartType):
    time: datetime.time
    shuttle_ref: ros_srv.Reference
    def __str__(self) -> str:
        return ros_ttb.concat(
            self.time,
            self.__class__.__name__.replace("_", "-"),
            f'{self.shuttle_ref}'
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = cls.__class__.__name__
        return vals


@ros_util.dictify
class Snt_sh(pydantic.BaseModel, ros_ttb.StartType):
    time: datetime.time
    rear_element_id: ros_coords.Coordinate
    front_element_id: ros_coords.Coordinate
    shuttle_ref: ros_srv.Reference
    def __str__(self) -> str:
        return ros_ttb.concat(
            self.time,
            self.__class__.__name__.replace("_", "-"),
            f'{self.rear_element_id} {self.front_element_id}',
            f'{self.shuttle_ref}'
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = cls.__class__.__name__
        return vals


@ros_util.dictify
class Sns_sh(pydantic.BaseModel, ros_ttb.StartType):
    time: datetime.time
    feeder_ref: ros_srv.Reference
    linked_shuttle_ref: ros_srv.Reference
    def __str__(self) -> str:
        return ros_ttb.concat(
            self.time,
            self.__class__.__name__.replace("_", "-"),
            f'{self.linked_shuttle_ref}',
            f'{self.feeder_ref}'
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = cls.__class__.__name__
        return vals
