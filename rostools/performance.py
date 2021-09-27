import asyncio
import os
import re
import logging
import glob
import sys
import random

from typing import List

class Monitor:
    _logger = logging.getLogger('ROSTools.PerformanceMonitor')
    def __init__(self, ros_log_dir: str, time_out: int = 120) -> None:
        if not os.path.exists(ros_log_dir):
            raise FileNotFoundError(
                f"Cannot monitor performance output, "
                f"directory '{ros_log_dir}' does not exist"
            )
        self._log_dir = ros_log_dir
        self._time_out = time_out
        self._data = {}

    async def _process_lines(self, file_lines: List[str]) -> None:
        _data_dict = {}
        _is_ttb_perf = re.compile(
            r'\d{2}\:\d{2}\:\d{2}\:\s[A-Z0-9]+\s[became|left|arrived|created|entered|departed]',
            re.IGNORECASE
        )
        _service_lines = [l for l in file_lines if _is_ttb_perf.findall(l)]

        for line in _service_lines:
            print(line)
            _time = re.findall(r'(\d{2}\:\d{2}\:\d{2})', line)[0]
            try:
                _head_code = re.findall(r'\d{2}\:\d{2}\:\d{2}\:\s([A-Z0-9]+)\s', line)[0]
            except IndexError:
                continue
            _msg = line.replace(_time, '').replace(_head_code, '')[1:].strip().rstrip()
            if _head_code not in self._data:
                self._data[_head_code] = []
            self._data[_head_code].append((_time, _msg))

    async def _read_latest_log(self) -> None:
        _log = None
        _n_lines = 0
        _timer = 0
        try:
            while _timer < self._time_out:
                _logs = glob.glob(os.path.join(self._log_dir, 'Log*.txt'))
                _logs = sorted(_logs, key=os.path.getmtime)
                if not _logs:
                    raise FileNotFoundError(f"No log files found in '{self._log_dir}'")
                elif _logs[-1] != _log:
                    self._logger.info(f"Reading performance from '{_logs[-1]}'")
                    self._data = {}
                    _log = _logs[-1]
                _lines = open(_log).readlines()
                if len(_lines) > _n_lines:
                    _timer = 0
                _n_lines = len(_lines)
                await self._process_lines(_lines)
                await asyncio.sleep(5)
                _timer += 5
        except KeyboardInterrupt:
            self._logger.info("Closing session")
            sys.exit(0)

    async def _async_main(self) -> None:
        await asyncio.gather(self._read_latest_log())

    def run(self) -> None:
        asyncio.run(self._async_main())

