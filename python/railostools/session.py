import configparser
import glob
import os.path
import typing

import toml

import railostools.common.enumeration as railos_enum
import railostools.exceptions as railos_exc


class Session:
    SESSION_FILE = "session.ini"
    _parser = configparser.ConfigParser()

    def __init__(self, railway_op_sim_dir: str) -> None:
        self._ros_loc = railway_op_sim_dir
        if not os.path.exists(os.path.join(self._ros_loc, "railway.exe")):
            raise railos_exc.ProgramNotFoundError(self._ros_loc)

    def _check_for_metadata(self, route: str) -> typing.Dict:
        """Check if metadata is available"""
        if not os.path.exists(os.path.join(self._ros_loc, "Metadata")):
            return {}

        _meta_list = [
            os.path.splitext(os.path.basename(i))[0]
            for i in glob.glob(os.path.join(self._ros_loc, "Metadata", "*.toml"))
        ]

        if os.path.splitext(os.path.basename(route))[0] not in _meta_list:
            return {}

        # By default the metadata file for a route should be the same prefix
        # as the route file
        _candidate_meta_file = os.path.join(
            self._ros_loc,
            "Metadata",
            f"{os.path.splitext(os.path.basename(route))[0]}.toml",
        )

        _data: typing.Optional[typing.Dict] = {}

        if os.path.exists(_candidate_meta_file):
            _data = toml.load(_candidate_meta_file)
        else:
            for meta_file in _meta_list:
                _mf_data = toml.load(meta_file)
                if _mf_data.get("rly_file", None) == route:
                    _data = _mf_data

        return _data

    def read(self) -> None:
        """Read current session metadata"""
        self._parser.read(os.path.join(self._ros_loc, "session.ini"))

    @property
    def railway(self) -> typing.Optional[str]:
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
    def main_mode(self) -> railos_enum.Level1Mode:
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
    def operation_mode(self) -> railos_enum.Level2OperMode:
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
    def performance_file(self) -> str:
        """Return the performance log file"""
        try:
            _file = self._parser.get("session", "performance_file")
            if not _file:
                return None
        except configparser.NoOptionError:
            return None
        except configparser.NoSectionError as e:
            raise railos_exc.SessionINIError(
                "Expected section 'session' in session file"
            ) from e
        if os.path.exists(_file):
            return _file
        _search = glob.glob(os.path.join(_file, "*.txt"))
        return _search[0] if _search else None

    @property
    def timetable(self) -> str:
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
