import datetime
import typing

import pydantic

import railostools.common.coords as railos_coords
import railostools.ttb.components as railos_comp
import railostools.ttb.string as railos_ttb_str


class Fns(railos_comp.FinishType, pydantic.BaseModel):
    name: str | None = pydantic.Field(None)
    model_config = pydantic.ConfigDict(validate_default=True)
    time: datetime.time
    time_days: int = 0
    new_service_ref: railos_comp.Reference

    def __str__(self) -> str:
        _time: datetime.time = datetime.datetime.strptime(self.time, "%H:%M")
        _hour: int = _time.hour + self.time_days * 24
        _min: int = _time.minute
        _time_str: str = (
            f"{'0' if _hour < 10 else ''}{_hour}:{'0' if _min < 10 else ''}{_min}"
        )
        return railos_ttb_str.concat(_time_str, self.name, f"{self.new_service_ref}")

    @pydantic.field_validator("time")
    @classmethod
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.model_validator(mode="after")
    @classmethod
    def add_name_as_field(cls, vals):
        vals.name = "Fns"
        return vals


class Fjo(railos_comp.FinishType, pydantic.BaseModel):
    name: str | None = pydantic.Field(None)
    model_config = pydantic.ConfigDict(validate_default=True)
    time: datetime.time
    time_days: int = 0
    joining_service_ref: railos_comp.Reference

    def __str__(self) -> str:
        _time: datetime.time = datetime.datetime.strptime(self.time, "%H:%M")
        _hour: int = _time.hour + self.time_days * 24
        _min: int = _time.minute
        _time_str: str = (
            f"{'0' if _hour < 10 else ''}{_hour}:{'0' if _min < 10 else ''}{_min}"
        )
        return railos_ttb_str.concat(
            _time_str, self.name, f"{self.joining_service_ref}"
        )

    @pydantic.field_validator("time")
    @classmethod
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.model_validator(mode="after")
    @classmethod
    def add_name_as_field(cls, vals):
        vals.name = "Fjo"
        return vals


class Fer(railos_comp.FinishType, pydantic.BaseModel):
    name: str | None = pydantic.Field(None)
    model_config = pydantic.ConfigDict(validate_default=True)
    time: datetime.time
    time_days: int = 0
    exit_coords: typing.List[railos_coords.Coordinate]

    def __str__(self) -> str:
        _time: datetime.time = datetime.datetime.strptime(self.time, "%H:%M")
        _hour: int = _time.hour + self.time_days * 24
        _min: int = _time.minute
        _time_str: str = (
            f"{'0' if _hour < 10 else ''}{_hour}:{'0' if _min < 10 else ''}{_min}"
        )
        return railos_ttb_str.concat(
            _time_str, self.name, " ".join([str(i) for i in self.exit_coords])
        )

    @pydantic.field_validator("time")
    @classmethod
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.model_validator(mode="after")
    @classmethod
    def add_name_as_field(cls, vals):
        vals.name = "Fer"
        return vals


class Frh_sh(railos_comp.FinishType, pydantic.BaseModel):
    name: str | None = pydantic.Field(None)
    model_config = pydantic.ConfigDict(validate_default=True)
    time: datetime.time
    time_days: int = 0
    linked_shuttle_ref: railos_comp.Reference

    def __str__(self) -> str:
        _time: datetime.time = datetime.datetime.strptime(self.time, "%H:%M")
        _hour: int = _time.hour + self.time_days * 24
        _min: int = _time.minute
        _time_str: str = (
            f"{'0' if _hour < 10 else ''}{_hour}:{'0' if _min < 10 else ''}{_min}"
        )
        return railos_ttb_str.concat(_time_str, self.name, f"{self.linked_shuttle_ref}")

    @pydantic.field_validator("time")
    @classmethod
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.model_validator(mode="after")
    @classmethod
    def add_name_as_field(cls, vals):
        vals.name = "Frh-sh"
        return vals


class Fns_sh(railos_comp.FinishType, pydantic.BaseModel):
    name: str | None = pydantic.Field(None)
    model_config = pydantic.ConfigDict(validate_default=True)
    time: datetime.time
    time_days: int = 0
    linked_shuttle_ref: railos_comp.Reference
    finishing_service_ref: railos_comp.Reference

    def __str__(self) -> str:
        _time: datetime.time = datetime.datetime.strptime(self.time, "%H:%M")
        _hour: int = _time.hour + self.time_days * 24
        _min: int = _time.minute
        _time_str: str = (
            f"{'0' if _hour < 10 else ''}{_hour}:{'0' if _min < 10 else ''}{_min}"
        )
        return railos_ttb_str.concat(
            _time_str,
            self.name,
            f"{self.linked_shuttle_ref}",
            f"{self.finishing_service_ref}",
        )

    @pydantic.field_validator("time")
    @classmethod
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.model_validator(mode="after")
    @classmethod
    def add_name_as_field(cls, vals):
        vals.name = "Fns-sh"
        return vals


class F_nshs(railos_comp.FinishType, pydantic.BaseModel):
    name: str | None = pydantic.Field(None)
    model_config = pydantic.ConfigDict(validate_default=True)
    time: datetime.time
    time_days: int = 0
    linked_shuttle_ref: railos_comp.Reference

    def __str__(self) -> str:
        _time: datetime.time = datetime.datetime.strptime(self.time, "%H:%M")
        _hour: int = _time.hour + self.time_days * 24
        _min: int = _time.minute
        _time_str: str = (
            f"{'0' if _hour < 10 else ''}{_hour}:{'0' if _min < 10 else ''}{_min}"
        )
        return railos_ttb_str.concat(_time_str, self.name, f"{self.linked_shuttle_ref}")

    @pydantic.field_validator("time")
    @classmethod
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.model_validator(mode="after")
    @classmethod
    def add_name_as_field(cls, vals):
        vals.name = "F-nshs"
        return vals


class Frh(railos_comp.FinishType, pydantic.BaseModel):
    name: str | None = pydantic.Field(None)
    model_config = pydantic.ConfigDict(validate_default=True)
    def __str__(self) -> str:
        return self.__class__.__name__

    @pydantic.model_validator(mode="after")
    @classmethod
    def add_name_as_field(cls, vals):
        vals.name = "Frh"
        return vals
