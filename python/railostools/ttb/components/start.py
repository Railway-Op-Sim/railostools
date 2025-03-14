import datetime

import pydantic

import railostools.common.coords as railos_coords
import railostools.ttb.components as railos_comp
import railostools.ttb.string as railos_ttb_str


class Snt(railos_comp.StartType, pydantic.BaseModel):
    name: str | None = pydantic.Field(None)
    model_config = pydantic.ConfigDict(validate_default=True)
    time: datetime.time
    time_days: int = 0
    rear_element_id: railos_coords.Coordinate
    front_element_id: railos_coords.Coordinate
    under_signaller_control: bool = False

    def __str__(self) -> str:
        _time: datetime.time = datetime.datetime.strptime(self.time, "%H:%M")
        _hour: int = _time.hour + self.time_days * 24
        _min: int = _time.minute
        _time_str: str = (
            f"{'0' if _hour < 10 else ''}{_hour}:{'0' if _min < 10 else ''}{_min}"
        )
        _elements = [
            _time_str,
            self.name,
            f"{self.rear_element_id} {self.front_element_id}",
        ]
        if self.under_signaller_control:
            _elements += "S"
        return railos_ttb_str.concat(*_elements)

    @pydantic.field_validator("time")
    @classmethod
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.model_validator(mode="after")
    @classmethod
    def add_name_as_field(cls, vals):
        vals.name = "Snt"
        return vals


class Sns(railos_comp.StartType, pydantic.BaseModel):
    name: str | None = pydantic.Field(None)
    model_config = pydantic.ConfigDict(validate_default=True)
    time: datetime.time
    time_days: int = 0
    parent_service: railos_comp.Reference

    def __str__(self) -> str:
        _time: datetime.time = datetime.datetime.strptime(self.time, "%H:%M")
        _hour: int = _time.hour + self.time_days * 24
        _min: int = _time.minute
        _time_str: str = (
            f"{'0' if _hour < 10 else ''}{_hour}:{'0' if _min < 10 else ''}{_min}"
        )
        return railos_ttb_str.concat(_time_str, self.name, f"{self.parent_service}")

    @pydantic.field_validator("time")
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.model_validator(mode="after")
    @classmethod
    def add_name_as_field(cls, vals):
        vals.name = "Sns"
        return vals


class Sfs(railos_comp.StartType, pydantic.BaseModel):
    name: str | None = pydantic.Field(None)
    model_config = pydantic.ConfigDict(validate_default=True)
    time: datetime.time
    time_days: int = 0
    splitting_service: railos_comp.Reference

    def __str__(self) -> str:
        _time: datetime.time = datetime.datetime.strptime(self.time, "%H:%M")
        _hour: int = _time.hour + self.time_days * 24
        _min: int = _time.minute
        _time_str: str = (
            f"{'0' if _hour < 10 else ''}{_hour}:{'0' if _min < 10 else ''}{_min}"
        )
        return railos_ttb_str.concat(_time_str, self.name, f"{self.splitting_service}")

    @pydantic.field_validator("time")
    @classmethod
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.model_validator(mode="after")
    @classmethod
    def add_name_as_field(cls, vals):
        vals.name = "Sfs"
        return vals


class Sns_fsh(railos_comp.StartType, pydantic.BaseModel):
    name: str | None = pydantic.Field(None)
    model_config = pydantic.ConfigDict(validate_default=True)
    time: datetime.time
    time_days: int = 0
    shuttle_ref: railos_comp.Reference

    def __str__(self) -> str:
        _time: datetime.time = datetime.datetime.strptime(self.time, "%H:%M")
        _hour: int = _time.hour + self.time_days * 24
        _min: int = _time.minute
        _time_str: str = (
            f"{'0' if _hour < 10 else ''}{_hour}:{'0' if _min < 10 else ''}{_min}"
        )
        return railos_ttb_str.concat(_time_str, self.name, f"{self.shuttle_ref}")

    @pydantic.field_validator("time")
    @classmethod
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.model_validator(mode="after")
    @classmethod
    def add_name_as_field(cls, vals):
        vals.name = "Sns-fsh"
        return vals


class Snt_sh(railos_comp.StartType, pydantic.BaseModel):
    name: str | None = pydantic.Field(None)
    model_config = pydantic.ConfigDict(validate_default=True)
    time: datetime.time
    time_days: int = 0
    rear_element_id: railos_coords.Coordinate
    front_element_id: railos_coords.Coordinate
    shuttle_ref: railos_comp.Reference

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
            f"{self.rear_element_id} {self.front_element_id}",
            f"{self.shuttle_ref}",
        )

    @pydantic.field_validator("time")
    @classmethod
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.model_validator(mode="after")
    @classmethod
    def add_name_as_field(cls, vals):
        vals.name = "Snt-sh"
        return vals


class Sns_sh(railos_comp.StartType, pydantic.BaseModel):
    name: str | None = pydantic.Field(None)
    model_config = pydantic.ConfigDict(validate_default=True)
    time: datetime.time
    time_days: int = 0
    feeder_ref: railos_comp.Reference
    linked_shuttle_ref: railos_comp.Reference

    def __str__(self) -> str:
        _time: datetime.time = datetime.datetime.strptime(self.time, "%H:%M")
        _hour: int = _time.hour + self.time_days * 24
        _min: int = _time.minute
        _time_str: str = (
            f"{'0' if _hour < 10 else ''}{_hour}:{'0' if _min < 10 else ''}{_min}"
        )
        return railos_ttb_str.concat(
            _time_str, self.name, f"{self.linked_shuttle_ref}", f"{self.feeder_ref}"
        )

    @pydantic.field_validator("time")
    @classmethod
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.model_validator(mode="after")
    @classmethod
    def add_name_as_field(cls, vals):
        vals.name = "Sns-sh"
        return vals
