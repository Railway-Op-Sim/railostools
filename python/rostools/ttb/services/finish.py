import typing
import pydantic
import datetime

import rostools.ttb.services as ros_srv
import rostools.common.coords as ros_coords
import rostools.ttb as ros_ttb
import rostools.common.utilities as ros_util


@ros_util.dictify
class Fns(pydantic.BaseModel, ros_ttb.FinishType):
    time: datetime.time
    new_service_ref: ros_srv.Reference
    def __str__(self) -> str:
        return ros_ttb.concat(
            self.time,
            self.__class__.__name__.replace("_", "-"),
            f'{self.new_service_ref}',
            join_type=ros_ttb.Element
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")


@ros_util.dictify
class Fjo(pydantic.BaseModel, ros_ttb.FinishType):
    time: datetime.time
    joining_service_ref: ros_srv.Reference
    def __str__(self) -> str:
        return ros_ttb.concat(
            self.time,
            self.__class__.__name__.replace("_", "-"),
            f'{self.joining_service_ref}',
            join_type=ros_ttb.Element
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")


@ros_util.dictify
class Fer(pydantic.BaseModel, ros_ttb.FinishType):
    time: datetime.time
    exit_coords: typing.List[ros_coords.Coordinate]
    def __str__(self) -> str:
        return ros_ttb.concat(
            self.time,
            self.__class__.__name__.replace("_", "-"),
            " ".join(self.exit_coords),
            join_type=ros_ttb.Element
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")


@ros_util.dictify
class Frh_sh(pydantic.BaseModel, ros_ttb.FinishType):
    time: datetime.time
    linked_shuttle_ref: ros_srv.Reference
    def __str__(self) -> str:
        return ros_ttb.concat(
            self.time,
            self.__class__.__name__.replace("_", "-"),
            f"{self.linked_shuttle_ref}",
            join_type=ros_ttb.Element
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")


@ros_util.dictify
class Fns_sh(pydantic.BaseModel, ros_ttb.FinishType):
    time: datetime.time
    linked_shuttle_ref: ros_srv.Reference
    finishing_service_ref: ros_srv.Reference
    def __str__(self) -> str:
        return ros_ttb.concat(
            self.time,
            self.__class__.__name__.replace("_", "-"),
            f"{self.linked_shuttle_ref}",
            f"{self.finishing_service_ref}",
            join_type=ros_ttb.Element
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")


@ros_util.dictify
class F_nshs(pydantic.BaseModel, ros_ttb.FinishType):
    time: datetime.time
    linked_shuttle_ref: ros_srv.Reference
    def __str__(self) -> str:
        return ros_ttb.concat(
            self.time,
            self.__class__.__name__.replace("_", "-"),
            f"{self.linked_shuttle_ref}",
            join_type=ros_ttb.Element
        )

    @pydantic.validator('time')
    def to_string(cls, v):
        return v.strftime("%H:%M")


@ros_util.dictify
class Frh(pydantic.BaseModel, ros_ttb.FinishType):
    def __str__(self) -> str:
        return self.__class__.__name__
