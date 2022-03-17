import pydantic
import typing
import datetime

import rostools.ttb.services as ros_srv
import rostools.common.coords as ros_coords
import rostools.ttb as ros_ttb
import rostools.common.utilities as ros_util


@ros_util.dictify
class Location(pydantic.BaseModel, ros_ttb.ActionType):
    start_time: datetime.time
    end_time: typing.Optional[datetime.time]
    name: str
    def __str__(self) -> str:
        _elements = [self.start_time]
        if self.end_time:
            _elements.append(self.end_time)
        _elements.append(self.name)
        return ros_ttb.concat(*_elements)

    @pydantic.validator('start_time', 'end_time')
    def to_string(cls, v):
        return v.strftime("%H:%M")


@ros_util.dictify
class pas(pydantic.BaseModel, ros_ttb.ActionType):
    time: typing.Optional[datetime.time]
    location: ros_coords.Coordinate
    def __str__(self) -> str:
        return ros_ttb.concat(
            self.time,
            self.__class__.__name__.replace("_", "-"),
            f'{self.location}',
            join_type=ros_ttb.Element
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")


@ros_util.dictify
class jbo(pydantic.BaseModel, ros_ttb.ActionType):
    joining_service_ref: ros_srv.Reference
    def __str__(self) -> str:
        return ros_ttb.concat(
            self.__class__.__name__.replace("_", "-"),
            f'{self.joining_service_ref}',
            join_type=ros_ttb.Element
        )


@ros_util.dictify
class fsp(pydantic.BaseModel, ros_ttb.ActionType):
    new_service_ref: ros_srv.Reference
    def __str__(self) -> str:
        return ros_ttb.concat(
            self.__class__.__name__.replace("_", "-"),
            f'{self.new_service_ref}',
            join_type=ros_ttb.Element
        )


@ros_util.dictify
class rsp(pydantic.BaseModel, ros_ttb.ActionType):
    new_service_ref: ros_srv.Reference
    def __str__(self) -> str:
        return ros_ttb.concat(
            self.__class__.__name__.replace("_", "-"),
            f'{self.new_service_ref}',
            join_type=ros_ttb.Element
        )


@ros_util.dictify
class cdt(pydantic.BaseModel, ros_ttb.ActionType):
    def __str__(self) -> str:
        return self.__class__.__name__
