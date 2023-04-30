import pydantic
import datetime
import enum
import typing

class TimetableLogEvent(str, enum.Enum):
    CHANGED_DIRECTION = "changed direction"
    PASSED = "passed"
    DEPARTED = "departed"
    ARRIVED = "arrived"
    ENTERED_RAILWAY = "entered railway"
    LEFT_RAILWAY = "left railway"
    SPLIT_FROM_REAR = "split from rear"
    SPLIT_FROM_FRONT = "split from front"


class ClockSpeed(str, enum.Enum):
    NORMAL = "normal"
    TWICE_NORMAL = "twice normal"
    FOUR_TIMES_NORMAL = "for times normal"
    EIGHT_TIMES_NORMAL = "eight times normal"
    SIXTEEN_TIMES_NORMAL = "sixteen times normal"

class ClockAdjustment(pydantic.BaseModel):
    time: datetime.time
    offset: typing.Optional[datetime.timedelta]=None
    speed: typing.Optional[ClockSpeed]=None

class ServiceEvent(pydantic.BaseModel):
    time: datetime.time
    actual_offset: int
    headcode: str
    action: TimetableLogEvent
    location: typing.Optional[str]
