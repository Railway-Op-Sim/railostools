import typing
import pydantic

import rostools.ttb.services as ros_srv
import rostools.common.coords as ros_coords
import rostools.ttb as ros_ttb


class Fns(pydantic.BaseModel, ros_ttb.Element):
    new_service_ref: ros_srv.Reference
    def __str__(self) -> str:
        return ros_ttb.concat(
            self.__class__.__name__.replace("_", "-"),
            f'{self.new_service_ref}',
            join_type=ros_ttb.Element
        )

class Fjo(pydantic.BaseModel, ros_ttb.Element):
    joining_service_ref: ros_srv.Reference
    def __str__(self) -> str:
        return ros_ttb.concat(
            self.__class__.__name__.replace("_", "-"),
            f'{self.joining_service_ref}',
            join_type=ros_ttb.Element
        )


class Fer(pydantic.BaseModel, ros_ttb.Element):
    exit_coords: typing.List[ros_coords.Coordinate]
    def __str__(self) -> str:
        return ros_ttb.concat(
            self.__class__.__name__.replace("_", "-"),
            " ".join(self.exit_coords),
            join_type=ros_ttb.Element
        )

