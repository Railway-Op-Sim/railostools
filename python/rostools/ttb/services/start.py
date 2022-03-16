import pydantic

import rostools.ttb.services as ros_srv
import rostools.common.coords as ros_coords
import rostools.ttb as ros_ttb

class Snt(pydantic.BaseModel, ros_ttb.Element):
    rear_element_id: ros_coords.Coordinate
    front_element_id: ros_coords.Coordinate
    under_signaller_control: bool = False
    def __str__(self) -> str:
        _elements = [
            self.__class__.__name__.replace("_", "-"),
            f'{self.rear_element_id} {self.front_element_id}',
        ]
        if self.under_signaller_control:
            _elements += 'S'
        return ros_ttb.concat(
            *_elements,
            join_type=ros_ttb.Element
        )


class Sfs(pydantic.BaseModel, ros_ttb.Element):
    splitting_service: ros_srv.Reference
    def __str__(self) -> str:
        return ros_ttb.concat(
            self.__class__.__name__.replace("_", "-"),
            f'{self.splitting_service}',
            join_type=ros_ttb.Element
        )


class Sns_fsh(pydantic.BaseModel, ros_ttb.Element):
    shuttle_ref: ros_srv.Reference
    def __str__(self) -> str:
        return ros_ttb.concat(
            self.__class__.__name__.replace("_", "-"),
            f'{self.shuttle_ref}',
            join_type=ros_ttb.Element
        )


class Snt_sh(pydantic.BaseModel, ros_ttb.Element):
    rear_element_id: ros_coords.Coordinate
    front_element_id: ros_coords.Coordinate
    shuttle_ref: ros_srv.Reference
    def __str__(self) -> str:
        return ros_ttb.concat(
            self.__class__.__name__.replace("_", "-"),
            f'{self.rear_element_id} {self.front_element_id}',
            f'{self.shuttle_ref}',
            join_type=ros_ttb.Element
        )


class Sns_sh(pydantic.BaseModel, ros_ttb.Element):
    feeder_ref: ros_srv.Reference
    linked_shuttle_ref: ros_srv.Reference
    def __str__(self) -> str:
        return ros_ttb.concat(
            self.__class__.__name__.replace("_", "-"),
            f'{self.linked_shuttle_ref}',
            f'{self.feeder_ref}',
            join_type=ros_ttb.Element
        )
