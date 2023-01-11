import datetime
import json
import logging
import os.path
import re
import typing

import railostools.exceptions as railos_exc
import railostools.ttb.components as ttb_comp
import railostools.ttb.string as railos_ttb_str
from railostools.ttb.parsing.actions import parse_action
from railostools.ttb.parsing.components import parse_header, parse_repeat
from railostools.ttb.parsing.finish import parse_finish
from railostools.ttb.parsing.start import parse_start


class TTBParser:
    def __init__(self) -> None:
        self._logger = logging.getLogger("RailOSTools.TTBParser")
        self._data: typing.Optional[ttb_comp.Timetable] = None
        self._file_lines: typing.List[str] = []

    def is_comment(self, statement: str) -> bool:
        """Returns if a given statement is a comment"""
        return any(
            [
                statement.startswith("*"),
                ";" not in statement and len(statement.split()) > 2,
            ]
        )

    def is_action(self, statement: str) -> bool:
        """Returns if a statement is an action statement"""
        try:
            parse_action(statement)
            return True
        except railos_exc.ParsingError as e:
            return False

    @property
    def start_time(self) -> datetime.time:
        """Retrieves the timetable start time"""
        _index: int = 0
        while self.is_comment(self._file_lines[_index]):
            if _index >= len(self._file_lines):
                raise railos_exc.ParsingError("Failed to retrieve timetable start time")
            _index += 1
        return datetime.datetime.strptime(self._file_lines[_index], "%H:%M").time()

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
            if i not in _comments.values() and not re.findall(r"^\d{2}:\d{2}$", i)
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
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"Cannot parse file '{file_name}', file not found.")

        if os.path.splitext(file_name)[-1].lower() != ".ttb":
            raise AssertionError(
                f"Cannot parse file '{file_name}', file is not a valid timetable file."
            )
        with open(file_name) as in_f:
            self._file_lines = railos_ttb_str.split(in_f.read(), ttb_comp.Element)

        _services: typing.Dict[str, ttb_comp.Service] = {}
        for service in self.services_str:
            _srv = self._parse_service(service)
            _services[str(_srv.header.reference)] = _srv

        self._data = ttb_comp.Timetable(
            start_time=self.start_time, services=_services, comments=self.comments
        )

    def json(self, output_file) -> None:
        """Dump metadata to a JSON file"""

        if isinstance(output_file, str):
            with open(output_file, "w") as out_f:
                json.dump(self._data.dict(), out_f, indent=2)
        else:
            _out_str = json.dumps(self._data.dict(), indent=2)
            output_file.write(_out_str)

        self._logger.info(f"SUCCESS: Output written to '{output_file}")
