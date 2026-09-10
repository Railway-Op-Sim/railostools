import configparser
import pathlib
import typing
from functools import cached_property

import pydantic
import toml

import railostools.common.enumeration as railos_enum
import railostools.exceptions as railos_exc


class Session:
    SESSION_FILE: str = "session.ini"
    RAILOS_BINARIES: tuple[str, ...] = ("railway.exe", "RailOS64.exe", "RailOS32.exe")
    _parser: configparser.ConfigParser = configparser.ConfigParser()

    @pydantic.validate_call
    def __init__(self, railway_op_sim_dir: pydantic.DirectoryPath) -> None:
        self._railos_loc: pathlib.Path = railway_op_sim_dir
        if not any(self._railos_loc.joinpath(b).exists() for b in self.RAILOS_BINARIES):
            raise railos_exc.ProgramNotFoundError(self._railos_loc)

    def _check_for_metadata(self, route: str) -> dict[str, typing.Any]:
        """Check if metadata is available."""
        if not self._railos_loc.joinpath("Metadata").exists():
            return {}

        _meta_list = [
            meta_file.stem
            for meta_file in self._railos_loc.joinpath("Metadata").glob("*.toml")
        ]

        if (_route_name := pathlib.Path(route).stem) not in _meta_list:
            return {}

        # By default the metadata file for a route should be the same prefix
        # as the route file
        _candidate_meta_file = self._railos_loc.joinpath(
            "Metadata",
            f"{_route_name}.toml",
        )

        _data: dict[str, typing.Any] | None = {}

        if _candidate_meta_file.exists():
            _data = toml.load(_candidate_meta_file)
        else:
            for meta_file in _meta_list:
                _mf_data = toml.load(meta_file)
                if _mf_data.get("rly_file", None) == route:
                    _data = _mf_data

        return _data

    def read(self) -> list[str]:
        """Read current session metadata"""
        return self._parser.read(self._railos_loc.joinpath("session.ini"))

    @cached_property
    def metadata(self) -> dict[str, typing.Any]:
        """Retrieve session metadata."""
        if not self.railway:
            return {}
        return self._check_for_metadata(self.railway)

    @property
    def railway(self) -> str | None:
        try:
            return self._parser.get("session", "railway")
        except configparser.NoOptionError:
            return None
        except configparser.NoSectionError as e:
            raise railos_exc.SessionINIError(
                "Expected section 'session' in session file"
            ) from e

    @property
    def running(self) -> bool:
        try:
            return self._parser.getboolean("session", "running")
        except configparser.NoOptionError:
            return False
        except configparser.NoSectionError as e:
            raise railos_exc.SessionINIError(
                "Expected section 'session' in session file"
            ) from e

    @property
    def main_mode(self) -> railos_enum.Level1Mode | None:
        """Return the main program mode"""
        try:
            return railos_enum.Level1Mode(self._parser.getint("session", "main_mode"))
        except configparser.NoOptionError:
            return None
        except configparser.NoSectionError as e:
            raise railos_exc.SessionINIError(
                "Expected section 'session' in session file"
            ) from e

    @property
    def operation_mode(self) -> railos_enum.Level2OperMode | None:
        """Return the program operation mode"""
        try:
            return railos_enum.Level2OperMode(
                self._parser.getint("session", "operation_mode")
            )
        except configparser.NoOptionError:
            return None
        except configparser.NoSectionError as e:
            raise railos_exc.SessionINIError(
                "Expected section 'session' in session file"
            ) from e

    @property
    def performance_file(self) -> pathlib.Path | pathlib.WindowsPath | None:
        """Return the performance log file"""
        try:
            _file = self._parser.get("session", "performance_file")
        except configparser.NoOptionError:
            return None
        except configparser.NoSectionError as e:
            raise railos_exc.SessionINIError(
                "Expected section 'session' in session file"
            ) from e
        if not _file:
            return None
        _perf_file = pathlib.Path(_file)
        if _perf_file.exists():
            return _perf_file

        _search = _perf_file.glob("*.txt")

        return next(_search, None)

    @property
    def timetable(self) -> str | None:
        """Return the current timetable file"""
        try:
            _file = self._parser.get("session", "timetable")
            if not _file:
                return None
            return _file
        except configparser.NoOptionError:
            return None
        except configparser.NoSectionError as e:
            raise railos_exc.SessionINIError(
                "Expected section 'session' in session file"
            ) from e
