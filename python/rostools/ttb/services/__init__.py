import typing
import pydantic


class Reference(pydantic.BaseModel):
    prefix: typing.Optional[pydantic.constr(max_length=4)] = None
    headcode: pydantic.constr(max_length=4, min_length=4)
    def __str__(self) -> str:
        return f'{self.prefix}{self.headcode}'
