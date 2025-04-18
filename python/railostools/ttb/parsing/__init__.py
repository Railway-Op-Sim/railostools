"""
RailOSTools TTB Parser
======================

This module provides a parser for Railway Operation Simulator (RailOS) timetable files.
It includes functionality to parse TTB files, extract timetable data, and convert it to JSON format.
"""

import datetime
import json
import logging
import os.path
import re
import typing
import io
import numpy

logging.basicConfig()

import railostools.exceptions as railos_exc
import railostools.ttb.components as ttb_comp
import railostools.ttb.string as railos_ttb_str
from railostools.ttb.parsing.actions import parse_action
from railostools.ttb.parsing.components import parse_header, parse_repeat
from railostools.ttb.parsing.finish import parse_finish
from railostools.ttb.parsing.start import parse_start


class TTBParser:
    """Parser for Railway Operation Simulator timetable files"""
    def __init__(self) -> None:
        """Initializes the TTBParser class"""
        self._logger = logging.getLogger("RailOSTools.TTBParser")
        self._data: dict[str, ttb_comp.Timetable] = {}
        self._file_lines: typing.List[str] = []
        self._current_file: typing.Optional[str] = None

    def __getitem__(self, item) -> ttb_comp.Timetable:
        return self._data[item]

    def is_comment(self, statement: str) -> bool:
        """Returns if a given statement is a comment"""
        return any(
            [
                statement.startswith("*"),
                ";" not in statement
                and len(statement.split()) > 2
                and not re.findall(r"^\d{2}:\d{2}", statement),
            ]
        )

    def is_start_time(self, statement: str) -> bool:
        """Returns if a statement is a start time statement"""
        return all(
            [
                re.findall(r"^\d{2}:\d{2}(?:;START)?", statement) or False,
                not self.is_comment(statement),
            ]
        )

    def is_action(self, statement: str) -> bool:
        """Returns if a statement is an action statement"""
        try:
            parse_action(statement)
            return True
        except railos_exc.ParsingError:
            return False

    @property
    def average_service_density(self) -> float:
        """Calculates the average service density of the timetable"""
        _times = []
        for service in self.data.services.values():
            _datetimes = [
                datetime.datetime.strptime(action.time, "%H:%M")
                for action in service.actions.values()
            ]
            _times.extend(
                (time.hour * 60 + time.minute) * 60
                + time.second
                for time in _datetimes
            )
        _times = numpy.array(_times)
        _binned_times: numpy.ndarray = numpy.bincount(_times).mean()
        return _binned_times

    @property
    def start_time(self) -> datetime.datetime:
        """Retrieves the timetable start time"""
        _index: int = 0

        if not self._file_lines:
            raise railos_exc.ParsingError("Cannot parse empty file.")

        while not self.is_start_time(self._file_lines[_index]):
            if _index >= len(self._file_lines) - 1:
                raise railos_exc.ParsingError("Failed to find timetable start time")
            _index += 1
        return datetime.datetime.strptime(
            re.findall(r"^\d{2}:\d{2}", self._file_lines[_index])[0], "%H:%M"
        ).time()

    @property
    def comments(self) -> typing.Dict[int, str]:
        """Retrieves all timetable comments along with position in file"""
        return {
            i: c for i, c in enumerate(self._file_lines) if self.is_comment(c)
        } or None

    @property
    def services_str(self) -> typing.List[typing.List[str]]:
        """Retrieve individual service strings"""
        _service_list = []
        _comments = self.comments or {}
        _non_comment_lines = [
            i
            for i in self._file_lines
            if i not in _comments.values() and not re.findall(r"^\d{2}:\d{2}(?:;START)?$", i)
        ]

        _service_list.extend(
            _service
            for line in _non_comment_lines
            if (
                _service := [
                    k.strip()
                    for k in railos_ttb_str.split(line, ttb_comp.Service)
                    if k.strip()
                ]
            )
        )
        return _service_list

    def keys(self):
        """Retrieve all timetable keys"""
        return self._data.keys()

    def _parse_service(self, service_components: typing.List[str]) -> ttb_comp.Service:
        """Parse a single service from the components"""
        _header = parse_header(service_components[0])
        _start_type = parse_start(service_components[1])

        _actions: typing.Dict[str, ttb_comp.ActionType] = {}

        _index = 2

        _signaller_service = any(
            [
                _header.max_signaller_speed,
                hasattr(_start_type, "under_signaller_control")
                and getattr(_start_type, "under_signaller_control"),
            ]
        )

        if _signaller_service:
            return ttb_comp.SignallerService(header=_header, start_type=_start_type)

        while self.is_action(component := service_components[_index]):
            _actions[_index] = parse_action(component)
            _index += 1
            if _index >= len(service_components):
                break

        if _index >= len(service_components):
            raise railos_exc.ParsingError(
                f"Failed to determine the finish type of service '{_header}'"
            )

        _finish_type = parse_finish(service_components[_index])

        if _index < len(service_components) - 1:
            _repeat = parse_repeat(service_components[-1])
        else:
            _repeat = None

        return ttb_comp.TimetabledService(
            header=_header,
            start_type=_start_type,
            finish_type=_finish_type,
            actions=_actions,
            repeats=_repeat,
        )

    def parse(self, file_name: str) -> None:
        """Parse a TTB file and extract timetable data"""
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"Cannot parse file '{file_name}', file not found.")

        if os.path.splitext(file_name)[-1].lower() != ".ttb":
            raise AssertionError(
                f"Cannot parse file '{file_name}', file is not a valid timetable file."
            )

        with open(file_name) as in_f:
            self._file_lines = railos_ttb_str.split(in_f.read(), ttb_comp.Element)
            self._file_lines = [i for i in self._file_lines if i]

        self._logger.info(f"Parsing input file '{file_name}'")
        self._current_file = file_name

        _services: typing.Dict[str, ttb_comp.Service] = {}
        for service in self.services_str:
            _srv = self._parse_service(service)
            _services[str(_srv.header.reference)] = _srv

        _key: str = os.path.splitext(os.path.basename(file_name))[0]

        self._data[_key] = ttb_comp.Timetable(
            start_time=self.start_time, services=_services, comments=self.comments
        )

        self._logger.info("Parsing successful, timetable is valid.")

    @property
    def data(self) -> ttb_comp.Timetable:
        """Retrieve the parsed timetable data"""
        if not self._current_file:
            raise RuntimeError("Could not identify current file")

        _key: str = os.path.splitext(os.path.basename(self._current_file))[0]
        return self._data[_key]

    def json(self, output_file: io.TextIOWrapper | str) -> None:
        """Dump metadata to a JSON file"""

        if isinstance(output_file, str):
            with open(output_file, "w") as out_f:
                json.dump(self._data, out_f, indent=2)
        else:
            _out_str = json.dumps(self._data, indent=2)
            output_file.write(_out_str)

        self._logger.info(f"SUCCESS: Output written to '{output_file}")
