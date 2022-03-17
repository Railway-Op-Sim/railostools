import typing
import pydantic
import rostools.common.utilities as ros_util


@ros_util.dictify
class Reference(pydantic.BaseModel):
    prefix: typing.Optional[pydantic.constr(max_length=4)] = None
    headcode: pydantic.constr(max_length=4, min_length=4)
    def __str__(self) -> str:
        return f'{self.prefix or ""}{self.headcode}'

