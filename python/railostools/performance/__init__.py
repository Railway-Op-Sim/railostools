import asyncio
import glob
import inspect
import logging
import os
import re
import typing
import datetime
import pydantic

import railostools.exceptions as rexc
import railostools.performance.components as ros_perf_comp


class Monitor:
    _logger = logging.getLogger("ROSTools.PerformanceMonitor")

    def __init__(self, railos_log_dir: str, time_out: int = 120) -> None:
        if not os.path.exists(railos_log_dir):
            raise FileNotFoundError(
                f"Cannot monitor performance output, "
                f"directory '{railos_log_dir}' does not exist"
            )
        self._log_dir = railos_log_dir  # RailOS Performance Log directory
        self._async_funcs: typing.List[
            typing.Tuple[typing.Callable, typing.Dict]
        ] = []  # Methods with args to run in sync with monitor
        self._time_out = time_out  # Time limit for typing.Listening
        self._data = {}  # Parsed log data
        self._is_running = False  # Status of monitor
        self._wait_interval: int = 5  # Wait period
        self._latest = ""  # Raw data of latest full log line

    async def _process_lines(self, file_lines: typing.List[str]) -> None:
        _is_ttb_perf = re.compile(
            r"\d{2}:\d{2}:\d{2}:\s[A-Z0-9]+\s[became|left|arrived|created|entered|departed]",
            re.IGNORECASE,
        )
        _service_lines = [line for line in file_lines if _is_ttb_perf.findall(line)]

        if not _service_lines:
            return

        # If the last service line is incomplete remove it
        if "\n" not in _service_lines[-1]:
            _service_lines = _service_lines[:-1]

        for line in _service_lines:
            _time = re.findall(r"(\d{2}:\d{2}:\d{2})", line)[0]
            try:
                _head_code = re.findall(r"\d{2}:\d{2}:\d{2}:\s([A-Z0-9]+)\s", line)[0]
            except IndexError:
                continue
            _msg = line.replace(_time, "").replace(_head_code, "")[1:].strip().rstrip()
            if _head_code not in self._data:
                self._data[_head_code] = []
            self._data[_head_code].append((_time, _msg))
        self._latest = _service_lines[-1]

    @property
    def running(self) -> bool:
        """Returns true if the monitor is currently running"""
        return self._is_running

    async def _examine_log_dir(self) -> None:
        self._is_running = True

        # Get the latest modification time for the log directory
        _dir_mod_time: float = os.path.getmtime(self._log_dir)

        # Used to count time duration
        _timer: int = 0

        # Used to store log file to be processed
        _log: str = ""

        # Used to store number of log files in directory
        _n_logs: int = 0

        # Store modification time of latest log
        _mod_time: int = 0

        try:
            while _timer < self._time_out and self._is_running:
                # If the log directory has not been modified this means that
                # no changes have been made to any logs
                if os.path.getmtime(self._log_dir) == _dir_mod_time:
                    await asyncio.sleep(self._wait_interval)
                    _timer += 5
                    continue

                _log_files = glob.glob(os.path.join(self._log_dir, "Log*.txt"))

                # If there are no log files in the given directory
                # then continue timer. Print warning every minute.
                if not _log_files:
                    if _timer % 60 == 0:
                        self._logger.warning(
                            "No log files currently found in directory '%s'",
                            self._log_dir,
                        )
                    await asyncio.sleep(self._wait_interval)
                    _timer += 5
                    continue

                # Check if a new log file has been created since monitor start
                if len(_log_files) > _n_logs:
                    _time_sorted_logs = sorted(_log_files, key=os.path.getmtime)
                    self._logger.info(
                        "New log file found, switching to '%s'", _time_sorted_logs[-1]
                    )
                    _mod_time = 0
                    _log = _time_sorted_logs[-1]

                _candidate_mod_time = os.path.getmtime(_log)

                # Check if the modification time has changed, if not the file has
                # no new lines so skip.
                if _candidate_mod_time == _mod_time:
                    await asyncio.sleep(self._wait_interval)
                    _timer += 5
                    continue

                # Clear the data ready to be re-read then process file
                self._data = {}

                with open(_log) as log_f:
                    _lines = log_f.readlines()

                await self._process_lines(_lines)
                await asyncio.sleep(self._wait_interval)
                _timer += 5
        except KeyboardInterrupt:
            self._is_running = False
            self._logger.info("Aborting session")
        self._is_running = False

    @property
    def latest(self) -> str:
        return self._latest

    @property
    def data(self) -> typing.Dict:
        return self._data

    def stop(self) -> None:
        """Force stop the monitor from running"""
        self._is_running = False

    def exec_in_parallel(self, function: typing.Callable, args: typing.Dict = None) -> None:
        if not args:
            args = {}

        if "monitor" not in inspect.signature(function).parameters:
            raise rexc.InvalidListenerError(function)
        self._async_funcs.append((function, args))

    async def _async_main(self) -> None:
        await asyncio.gather(
            self._examine_log_dir(),
            *[i[0](**i[1], monitor=self) for i in self._async_funcs],
        )

    def run(self) -> None:
        asyncio.run(self._async_main())


class PerformanceLogParser:
    def __init__(self) -> None:
        self._logger = logging.getLogger("RailOSTools.TTBParser")
        self.data: typing.Dict[str, typing.List[ros_perf_comp.ClockAdjustment | ros_perf_comp.ServiceEvent]] = {}
        self._file_lines: typing.List[str] = []
        self._current_file: typing.Optional[str] = None

    def __getitem__(self, item: str) -> typing.List[ros_perf_comp.ClockAdjustment | ros_perf_comp.ServiceEvent]:
        return self.data[item]

    def keys(self):
        return self.data.keys()

    def _parse_timetable_performance_even(self, time_str: str, line: str) -> ros_perf_comp.TimetableLogEvent:
        _file_data: typing.List[ros_perf_comp.TimetableLogEvent] = []
        _hours_orig: int = int(time_str.split(":")[0])
        _days: int = _hours_orig // 24
        _hours = _hours_orig - _days * 24
        time_str = time_str.replace(f"{_hours_orig}:", f"{_hours}:")
        for tt_event_type in ros_perf_comp.TimetableLogEvent.__members__.values():
            if tt_event_type.value in line:
                _offset = 0
                _offset_str = "on time"
                if "1 minute early" in line:
                    _offset = -1
                    _offset_str = "1 minute early"
                elif "1 minute late" in line:
                    _offset = 1
                    _offset_str = "1 minute late"
                elif _min_search := re.findall(r'(\d+) minutes early', line):
                    _offset = -1 * int(_min_search[0])
                    _offset_str = f"{_offset} minutes early"
                elif _min_search := re.findall(r'(\d+) minutes late', line):
                    _offset = int(_min_search[0])
                if (_error := "ERROR" in line):
                    line = line.replace(" ERROR", "")
                _head_code_re = re.findall(r"\d{2}:\d{2}:\d{2}[ WARNING]*:\s([A-Z0-9]+)\s", line)
                _head_code: str = _head_code_re[0]
                _line_no_action: str = line.replace(tt_event_type.value, "")
                _line_no_action = _line_no_action.replace("to", "")
                _line_no_action = _line_no_action.replace("from", "")
                _line_no_action = _line_no_action.replace(_head_code, "")
                _line_no_action = _line_no_action.replace(time_str, "")
                if _line_no_action[-1] == ",":
                    _line_no_action = _line_no_action[:-1]
                if _line_no_action[0] == ":":
                    _line_no_action = _line_no_action[1:]
                _location = _line_no_action.replace(_offset_str, "").strip()
                try:
                    _file_data.append(
                        ros_perf_comp.ServiceEvent(
                            time=time_str,
                            actual_offset=_offset,
                            headcode=_head_code,
                            action=tt_event_type,
                            location=_location,
                            error=_error,
                            time_days=_days
                        )
                    )
                except pydantic.ValidationError as e:
                    self._logger.error(
                        f"Failed to validate entry with data: time={time_str}, "
                        f"actual_offset={_offset}, headcode={_head_code}, "
                        f"action={tt_event_type}, location={_location}, "
                        f"error={_error}"
                    )
                    raise e
        return _file_data

    def _parse_score(self, lines: typing.List[str]) -> typing.Tuple[int | None, str | None]:
        _line_str: str = "\n".join(lines)
        _score_line_re = re.findall(r'Overall score: (\d+)%', _line_str)
        _score_rating_re = re.findall(r'Overall rating: (\w+)', _line_str)

        _score: int | None = int(_score_line_re[0]) if _score_line_re else None
        _rating: str | None = _score_rating_re[0] if _score_rating_re else None

        return _score, _rating

    @property
    def simulation_time_coverage(self) -> int:
        """Duration of player simulation in seconds

        Note this is the timetable event duration not the actual time spent by the player
        within RailOS (it does not include delays/early finishes)
        """

        if not self.data:
            return 0

        _key: str = os.path.splitext(os.path.basename(self._current_file))[0]
        _first_time: datetime.datetime = datetime.datetime.combine(datetime.date.today(), self.data[_key][0].time)
        _last_time: datetime.time = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=self.data[_key][-1].time_days), self.data[_key][-1].time)
        _interval: datetime.timedelta = _last_time - _first_time

        return _interval.seconds

    def parse(self, log_file: str) -> None:
        if not os.path.exists(log_file):
            raise FileNotFoundError(f"Cannot parse performance log '{log_file}', file not found")

        with open(log_file) as in_f:
            self._file_lines = in_f.readlines()

        self._current_file = log_file

        self.score, self.rating = self._parse_score(self._file_lines)

        _file_data: typing.List[ros_perf_comp.ClockAdjustment | ros_perf_comp.ServiceEvent] = []
        _line_time = re.compile(r'^\d{2}:\d{2}:\d{2}')

        for line in self._file_lines:
            if not (_time_re := _line_time.findall(line)):
                continue
            _time_str: str = _time_re[0]
            _hours_orig: int = int(_time_str.split(":")[0])
            _days: int = _hours_orig // 24
            _hours = _hours_orig - _days * 24
            _time_str = _time_str.replace(f"{_hours_orig}:", f"{_hours}:")
            _clock_increment: int | None = None

            if "clock speed" in line:
                for speed in ros_perf_comp.ClockSpeed.__members__.values():
                    if speed.value in line:
                        _file_data.append(
                            ros_perf_comp.ClockAdjustment(
                                time=_time_str,
                                speed=speed
                            )
                        )
            elif "clock incremeted" in line:
                _increment_min = re.findall(r'(\d+)m')
                _increment_hr = re.findall(r'(\d+)h')
                if _increment_min:
                    _clock_increment = int(_increment_min[0])
                elif _increment_hr:
                    _clock_increment = int(_increment_min[0]) * 60
                _file_data.append(
                    ros_perf_comp.ClockAdjustment(
                        time=_time_str,
                        offset=_clock_increment
                    )
                )
            else:
                _file_data += self._parse_timetable_performance_even(_time_str, line)
        _key: str = os.path.splitext(os.path.basename(log_file))[0]
        self.data[_key] = _file_data
