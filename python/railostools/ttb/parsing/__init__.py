import datetime
import os.path
import typing
import click
import railostools.ttb.components as ttb_comp


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
            self._file_lines = in_f.read().split("\0")

    @property
    def start_time(self) -> datetime.time:
        """Retrieves the timetable start time"""
        return datetime.datetime.strptime(self._file_lines[0], "%H:%M").time()

    @property
    def comments(self) -> typing.Tuple[typing.Tuple[int, str], ...]:
        """Retrieves all timetable comments along with position in file"""
        return ((i, c) for i, c in enumerate(self._file_lines) if c.startswith('*'))

    def _parse_header(self, header_str) -> ttb_comp.Header:
        pass

    def _parse_service(self, service_str) -> ttb_comp.Service:
        pass

    def __enter__(self) -> ttb_comp.Timetable:
        with open(self._input_file) as in_f:
            # Retrieve services
            pass

    def __exit__(self, *args, **kwargs):
        pass


@click.command()
@click.argument("file_name")
def test_run(file_name: str):
    with TTBParser(file_name) as parser:
        pass

if __name__ in "__main__":
    test_run()