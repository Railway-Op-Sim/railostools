import railostools.ttb.components as ttb_comp
import railostools.ttb.components.start as ttb_start
import railostools.ttb.components.finish as ttb_finish
import railostools.common.coords as railos_coords
import railostools.ttb.parsing.time as ttb_time
import datetime
import typing


class TimetableBuilder:
    def __init__(self) -> None:
        self._timetable = ttb_comp.Timetable(
            start_time=datetime.time(5, 00),
            services={}
        )

    def __getitem__(self, headcode: str) -> ttb_comp.Service:
        return self._timetable.services[headcode]

    def _parse_time_str(self, time: str) -> typing.Tuple[datetime.time, int]:
        time, days = ttb_time.adjust_above_24hr(time, f"could not convert time string '{time}'")
        return datetime.datetime.strptime(time, "%H:%M").time(), days

    @property
    def start(self) -> datetime.time:
        return self._timetable.start_time

    @start.setter
    def start(self, time: typing.Union[datetime.time, str]) -> None:
        if isinstance(time, str):
            self._timetable.start_time, _ = self._parse_time_str(time)
        else:
            self._timetable.start_time = time

    @property
    def timetable(self) -> ttb_comp.Timetable:
        return self._timetable

    def _headcode_err(self, headcode: str) -> None:
        if headcode not in self._timetable.services:
            raise KeyError(f"Cannot access service '{headcode}' as it does not exist")

    def _modification_error(self, headcode: str, property: str) -> None:
        if (_start := self._timetable.services[headcode].start_type) not in (
            ttb_start.Snt,
            ttb_start.Snt_sh,
        ):
            raise TypeError(
                f"Cannot modify property '{property}' for service of type '{_start.__class__.__name__}'"
            )

    def add_service(
        self, headcode: str, description: str, start_time: typing.Union[str, datetime.time], **kwargs
    ) -> None:
        _time_days: int = 0

        if isinstance(start_time, str):
            start_time, _time_days = self._parse_time_str(start_time)


        if start_time < self._timetable.start_time:
            raise AssertionError(
                "Service start time cannot be earlier than timetable start"
            )

        _header = ttb_comp.Header(reference=ttb_comp.Reference.from_string(headcode), description=description)

        _start_type: ttb_comp.StartType

        if(_rear_element_id := kwargs.get("rear_element_id")) and isinstance(_rear_element_id, str):
            _rear_element_id = railos_coords.Coordinate.from_string(_rear_element_id)

        if(_front_element_id := kwargs.get("front_element_id")) and isinstance(_front_element_id, str):
            _front_element_id = railos_coords.Coordinate.from_string(_front_element_id)

        _under_signaller_control = kwargs.get("under_signaller_id", False)
        _time_days = kwargs.get("time_days", 0)
        _parent_service = kwargs.get("parent_ref")

        if all([_rear_element_id, _front_element_id]):
            _start_type = ttb_start.Snt(
                time=start_time,
                time_days=_time_days,
                rear_element_id=_rear_element_id,
                front_element_id=_front_element_id,
                under_signaller_control=_under_signaller_control,
            )
        elif _parent_service:
            _start_type = ttb_start.Sns(
                time=start_time,
                time_days=_time_days,
                parent_service=ttb_comp.Reference.from_string(headcode),
            )
        else:
            raise AssertionError("Could not determine start type")

        self._timetable.services[headcode] = ttb_comp.TimetabledService(
            header=_header, start_type=_start_type, finish_type=ttb_finish.Frh()
        )

    def form_new_service(
        self,
        headcode: str,
        new_service_headcode: str,
        time: typing.Union[str, datetime.time],
        description: str,
        time_days: int = 0
    ) -> None:
        self._timetable.services[headcode].finish_type = ttb_finish.Fns(
            time=time,
            time_days=time_days,
            new_service_ref=ttb_comp.Reference.from_string(new_service_headcode)
        )
        self.add_service(
            start_time=time,
            headcode=new_service_headcode,
            description=description,
            parent_ref=headcode,
        )

    def finish_exit_railway(
        self,
        headcode: str,
        element_ids: typing.List[str],
        time: typing.Union[str, datetime.time],
        time_days: int = 0
    ) -> None:
        if isinstance(time, str):
            time, time_days = self._parse_time_str(time)

        if time < self._timetable.services[headcode].start_type.time:
            raise AssertionError("Cannot terminate service at time before service start time")

        self._timetable.services[headcode].finish_type = ttb_finish.Fer(
            time=time,
            time_days=time_days,
            exit_coords=[railos_coords.Coordinate.from_string(i) for i in element_ids]
        )

    def set_service_start_type(
        self, headcode: str, start_type: ttb_comp.StartType
    ) -> None:
        self._headcode_err(headcode)
        self._timetable.services[headcode].start_type = start_type

        # If the new type is a child service type then it should inherit properties from the
        # parent service, not have its own
        if self._timetable.services[headcode].start_type not in (
            ttb_start.Snt,
            ttb_start.Snt_sh,
        ):
            self._timetable.services[headcode].header.max_speed = None
            self._timetable.services[headcode].header.mass = None
            self._timetable.services[headcode].header.max_signaller_speed = None
            self._timetable.services[headcode].header.power = None

    def set_service_max_speed(self, max_speed: int, headcode: str) -> None:
        self._headcode_err(headcode)
        self._modification_error(headcode, "max_speed")
        self._timetable.services[headcode].header.max_speed = max_speed

    def set_service_max_speed(
        self, max_signaller_speed: int | None, headcode: str
    ) -> None:
        self._headcode_err(headcode)
        self._modification_error(headcode, "max_signaller_speed")
        self._timetable.services[
            headcode
        ].header.max_signaller_speed = max_signaller_speed

    def set_service_mass(self, mass: int, headcode: str) -> None:
        self._headcode_err(headcode)
        self._modification_error(headcode, "mass")
        self._timetable.services[headcode].header.mass = mass

    def set_service_max_power(self, max_power: int, headcode: str) -> None:
        self._headcode_err(headcode)
        self._modification_error(headcode, "max_power")
        self._timetable.services[headcode].header.power = max_power

    def set_service_description(self, headcode: str, description: str) -> None:
        self._headcode_err(headcode)
        self._timetable.services[headcode].header.description = description

    def validate(self, headcode: str) -> None:
        """Pass the service back through the validator to check it"""
        self._headcode_err(headcode)
        ttb_comp.TimetabledService(**self._timetable.services[headcode].dict())
