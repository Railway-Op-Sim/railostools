import datetime
import os.path
import re
import json
from textwrap import indent
import typing
import click
import railostools.ttb.components as ttb_comp
import railostools.ttb.string as ros_ttb_str
import railostools.exceptions as ros_exc

from railostools.ttb.parsing.start import parse_start
from railostools.ttb.parsing.finish import parse_finish
from railostools.ttb.parsing.actions import parse_action
from railostools.ttb.parsing.components import parse_reference, parse_header, parse_repeat


class TTBParser:
    def __init__(self, file_name: str) -> None:
        self._input_file = file_name
        if not os.path.exists(self._input_file):
            raise FileNotFoundError(
                f"Cannot parse file '{self._input_file}', file not found."
            )

        if os.path.splitext(self._input_file)[-1].lower() != ".ttb":
            raise AssertionError(
                f"Cannot parse file '{self._input_file}', file is not a valid timetable file."
            )
        with open(file_name) as in_f:
            self._file_lines = ros_ttb_str.split(in_f.read(), ttb_comp.Element)

    def is_comment(self, statement: str) -> bool:
        """Returns if a given statement is a comment"""
        return any(
            [
                statement.startswith('*'),
                ";" not in statement and len(statement.split()) > 2
            ]
        )

    def is_action(self, statement: str) -> bool:
        """Returns if a statement is an action statement"""
        try:
            parse_action(statement)
            return True
        except ros_exc.ParsingError as e:
            return False

    @property
    def start_time(self) -> datetime.time:
        """Retrieves the timetable start time"""
        return datetime.datetime.strptime(self._file_lines[0], "%H:%M").time()

    @property
    def comments(self) -> typing.Tuple[typing.Tuple[int, str], ...]:
        """Retrieves all timetable comments along with position in file"""
        return {
            i: c for i, c in enumerate(self._file_lines)
            if self.is_comment(c)
        }

    @property
    def services_str(self) -> typing.List[typing.List[str]]:
        """Retrieve individual service strings"""
        _service_list = []
        _non_comment_lines = [
            i for i in self._file_lines
            if i not in self.comments.values()
            and not re.findall(r"^\d{2}:\d{2}$", i)
        ]

        _service_list.extend(
            _service for line in _non_comment_lines if (
                _service := [
                    k.strip() for k in ros_ttb_str.split(line, ttb_comp.Service)
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

        _signaller_service = any([
            _header.max_signaller_speed,
            hasattr(_start_type, "under_signaller_control") and getattr(_start_type, "under_signaller_control")
        ])

        if _signaller_service:
            return ttb_comp.SignallerService(
                header=_header,
                start_type=_start_type
            )

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

        return ttb_comp.Service(
            header=_header,
            start_type=_start_type,
            finish_type=_finish_type,
            actions=_actions,
            repeats=_repeat
        )


    def __enter__(self) -> ttb_comp.Timetable:
        _services: typing.Dict[str, ttb_comp.Service] = {}
        for service in self.services_str:
            _srv = self._parse_service(service)
            _services[str(_srv.header.reference)] = _srv

    def __exit__(self, *args, **kwargs):
        pass


@click.command()
@click.argument("file_name")
def test_run(file_name: str):
    with TTBParser(file_name) as parser:
        pass

if __name__ in "__main__":
    test_run()