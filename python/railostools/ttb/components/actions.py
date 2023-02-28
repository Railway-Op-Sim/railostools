import datetime
import typing

import pydantic

import railostools.ttb.components as railos_comp
import railostools.ttb.string as railos_ttb_str


class Location(railos_comp.ActionType, pydantic.BaseModel):
    time: datetime.time
    end_time: typing.Optional[datetime.time]
    time_days: int = 0
    end_time_days: typing.Optional[int] = 0
    name: str

    def __str__(self) -> str:
        _time: datetime.time = datetime.datetime.strptime(self.time, "%H:%M")
        _hour: int = _time.hour + self.time_days * 24
        _min: int = _time.minute
        _time_str: str = (
            f"{'0' if _hour < 10 else ''}{_hour}:{'0' if _min < 10 else ''}{_min}"
        )

        _elements = [_time_str]

        if self.end_time:
            _time: datetime.time = datetime.datetime.strptime(self.end_time, "%H:%M")
            _hour: int = _time.hour + self.time_days * 24
            _min: int = _time.minute
            _time_str: str = (
                f"{'0' if _hour < 10 else ''}{_hour}:{'0' if _min < 10 else ''}{_min}"
            )
            _end_time: datetime.time = datetime.datetime.strptime(
                self.end_time, "%H:%M"
            )
            _elements.append(_time_str)

        _elements.append(self.name)
        return railos_ttb_str.concat(*_elements)

    @pydantic.validator("time", "end_time")
    def to_string(cls, v: datetime.time):
        return v.strftime("%H:%M") if v else v


class pas(railos_comp.ActionType, pydantic.BaseModel):
    time: datetime.time
    time_days: int = 0
    location: str

    def __str__(self) -> str:
        _time: datetime.time = datetime.datetime.strptime(self.time, "%H:%M")
        _hour: int = _time.hour + self.time_days * 24
        _min: int = _time.minute
        _time_str: str = (
            f"{'0' if _hour < 10 else ''}{_hour}:{'0' if _min < 10 else ''}{_min}"
        )
        return railos_ttb_str.concat(_time_str, self.name, f"{self.location}")

    @pydantic.validator("time")
    def to_string(cls, v):
        return v.strftime("%H:%M")

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "pas"
        return vals


class jbo(railos_comp.ActionType, pydantic.BaseModel):
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

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "jbo"
        return vals

    @pydantic.validator("time")
    def to_string(cls, v):
        return v.strftime("%H:%M")


class fsp(railos_comp.ActionType, pydantic.BaseModel):
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

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "fsp"
        return vals

    @pydantic.validator("time")
    def to_string(cls, v):
        return v.strftime("%H:%M")


class rsp(railos_comp.ActionType, pydantic.BaseModel):
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

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "rsp"
        return vals

    @pydantic.validator("time")
    def to_string(cls, v):
        return v.strftime("%H:%M")


class cdt(railos_comp.ActionType, pydantic.BaseModel):
    time: datetime.time
    time_days: int = 0

    def __str__(self) -> str:
        _time: datetime.time = datetime.datetime.strptime(self.time, "%H:%M")
        _hour: int = _time.hour + self.time_days * 24
        _min: int = _time.minute
        _time_str: str = (
            f"{'0' if _hour < 10 else ''}{_hour}:{'0' if _min < 10 else ''}{_min}"
        )
        return railos_ttb_str.concat(_time_str, self.name)

    @pydantic.root_validator
    def add_name_as_field(cls, vals):
        vals["name"] = "cdt"
        return vals

    @pydantic.validator("time")
    def to_string(cls, v):
        return v.strftime("%H:%M")
