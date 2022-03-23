import asyncio
import glob
import inspect
import logging
import os
import re
from typing import Callable, Dict, List, Tuple

import railostools.exceptions as rexc


class Monitor:
    _logger = logging.getLogger("ROSTools.PerformanceMonitor")

    def __init__(self, ros_log_dir: str, time_out: int = 120) -> None:
        if not os.path.exists(ros_log_dir):
            raise FileNotFoundError(
                f"Cannot monitor performance output, "
                f"directory '{ros_log_dir}' does not exist"
            )
        self._log_dir = ros_log_dir  # ROS Performance Log directory
        self._async_funcs: List[
            Tuple[Callable, Dict]
        ] = []  # Methods with args to run in sync with monitor
        self._time_out = time_out  # Time limit for listening
        self._data = {}  # Parsed log data
        self._is_running = False  # Status of monitor
        self._wait_interval: int = 5  # Wait period
        self._latest = ""  # Raw data of latest full log line

    async def _process_lines(self, file_lines: List[str]) -> None:
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
    def data(self) -> Dict:
        return self._data

    def stop(self) -> None:
        """Force stop the monitor from running"""
        self._is_running = False

    def exec_in_parallel(self, function: Callable, args: Dict = None) -> None:
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
