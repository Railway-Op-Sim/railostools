import datetime
import json
import logging
import os.path
import dataclasses
import pandas
import typing
import itertools
from typing import Any, Dict, List

from railostools.exceptions import RailwayParsingError
from railostools.common.enumeration import Elements
from railostools.rly.relations import can_connect


@dataclasses.dataclass
class RlyInfoTables:
    signals: pandas.DataFrame


@dataclasses.dataclass
class StartPosition:
    start_coordinate: typing.Tuple[int, int]
    end_coordinate: typing.Tuple[int, int]


@dataclasses.dataclass
class TimetableLocation:
    name: str
    start_positions: typing.List[StartPosition]


class RlyParser:
    _logger = logging.getLogger("RailOSTools.RlyParser")

    def __init__(self) -> None:
        self._logger.debug("Creating new RlyParser")
        self._rly_data = {}
        self._start_time: datetime.datetime = None
        self._current_file = None

    def parse(self, rly_file: str) -> None:
        self._logger.info(f"Parsing RLY file '{rly_file}'")
        if not os.path.exists(rly_file):
            raise FileNotFoundError(
                f"Cannot parse railway file '{rly_file}', " "file does not exist."
            )
        _key = os.path.splitext(os.path.basename(rly_file))[0]
        self._rly_data[_key] = self._get_rly_components(
            open(rly_file, encoding="latin-1").readlines()
        )
        self._current_file = rly_file

    @property
    def n_active_elements(self) -> int:
        if not self._current_file:
            raise RailwayParsingError("No file has been parsed yet")
        return self._rly_data[
            os.path.splitext(os.path.basename(self._current_file))[0]
        ]["metadata"]["n_active_elements"]

    @property
    def n_inactive_elements(self) -> int:
        if not self._current_file:
            raise RailwayParsingError("No file has been parsed yet")
        return self._rly_data[
            os.path.splitext(os.path.basename(self._current_file))[0]
        ]["metadata"]["n_inactive_elements"]

    @property
    def program_version(self) -> str:
        if not self._current_file:
            raise RailwayParsingError("No file has been parsed yet")
        return self._rly_data[
            os.path.splitext(os.path.basename(self._current_file))[0]
        ]["metadata"]["program_version"]

    @property
    def timetable_locations(self) -> typing.Dict[str, TimetableLocation]:
        """Returns list of timetable locations and coordinates

        NOTE: These are locations which are of size 2, i.e. would have the
        start and end point within the location region. Track sections outside
        of the domain of the location cannot be easily identified using this method.
        """

        # Retrieve timetable location names from data
        _location_names: typing.Set[str] = {
            n["active_element_name"]
            for n in self._rly_data[
                os.path.splitext(os.path.basename(self._current_file))[0]
            ]["active_elements"]
            if n["active_element_name"]
        }

        # Remove the -1 location if present
        if "-1" in _location_names:
            _location_names.remove("-1")

        _locations: typing.Dict[str, TimetableLocation] = {}

        # Iterate through all location names and find the coordinate pairs from which a
        # timetable could commence
        for location in _location_names:
            _locations[location] = TimetableLocation(location, [])
            _loc_elements: typing.Dict = {"element_types": [], "element_coords": []}

            # Iterate though all elements and collect the data needed for finding
            # timetable locations
            for element in self.active_elements + self.inactive_elements:
                if element.get("active_element_name") != location:
                    continue
                if not (element_int := element.get("element_id")):
                    continue
                element_type: Elements = Elements(element_int)
                _loc_elements["element_types"].append(element_type)
                _loc_elements["element_coords"].append(element["position"])

            # Get every combination of two elements for this location
            _combos = set(
                itertools.combinations(range(len(_loc_elements["element_types"])), 2)
            )

            for indices in _combos:
                if len(_loc_elements["element_types"]) < 2:
                    continue
                _combo_type: typing.Tuple[typing.Tuple[Elements, Elements]] = (
                    _loc_elements["element_types"][indices[0]],
                    _loc_elements["element_types"][indices[1]],
                )

                _combo_coords: typing.Tuple[typing.Tuple[Elements, Elements]] = (
                    _loc_elements["element_coords"][indices[0]],
                    _loc_elements["element_coords"][indices[1]],
                )

                # Check if this combination contains two elements which can
                # be joined together
                if can_connect(
                    element_one_type=_combo_type[0],
                    element_two_type=_combo_type[1],
                    coord_1=_combo_coords[0],
                    coord_2=_combo_coords[1],
                ):
                    _locations[location].start_positions.append(
                        StartPosition(_combo_coords[0], _combo_coords[1])
                    )

        return _locations

    @property
    def data(self) -> typing.Dict:
        if not self._current_file:
            raise RailwayParsingError("No file has been parsed yet")
        return self._rly_data

    @property
    def active_elements(self) -> typing.List[typing.Dict]:
        return self.data[os.path.splitext(os.path.basename(self._current_file))[0]][
            "active_elements"
        ]

    @property
    def inactive_elements(self) -> typing.List[typing.Dict]:
        return self.data[os.path.splitext(os.path.basename(self._current_file))[0]][
            "inactive_elements"
        ]

    def _make_signal_table(self) -> pandas.DataFrame:
        _df_dict = {col: [] for col in ["position", "signal"]}
        for element in self.active_elements:
            if not element["signal"]:
                continue
            for key in _df_dict:
                _df_dict[key].append(element[key])
        return pandas.DataFrame.from_dict(_df_dict)

    @property
    def tables(self) -> RlyInfoTables:
        return RlyInfoTables(signals=self._make_signal_table())

    def _parse_active_element(self, active_elem: List[str]) -> Dict:
        active_elem: typing.List[str] = [i.strip() for i in active_elem]
        return {
            "element_id": int(active_elem[1]),
            "position": (int(active_elem[2]), int(active_elem[3])),
            "length": (
                int(active_elem[4]),
                int(active_elem[5]) if active_elem[5] != "-1" else None,
            ),
            "speed_limit": (
                int(active_elem[6]),
                int(active_elem[7]) if active_elem[7] != "-1" else None,
            ),
            "location_name": active_elem[8] or None,
            "active_element_name": active_elem[9] or None,
        }

    def _parse_text(self, text_elem: List[str]) -> Dict:
        text_elem = [i.strip() for i in text_elem]
        return {
            "n_items": int(text_elem[0]),
            "position": (int(text_elem[2]), int(text_elem[3])),
            "text_string": text_elem[4],
            "font": {
                "name": text_elem[5],
                "size": int(text_elem[6]),
                "color": int(text_elem[7]),
                "charset": int(text_elem[8]),
                "style": int(text_elem[9]),
            },
        }

    def _parse_inactive_element(self, inactive_elem: List[str]) -> Dict:
        inactive_elem = [i.strip() for i in inactive_elem]
        return {
            "element_id": int(inactive_elem[1]),
            "position": (int(inactive_elem[2]), int(inactive_elem[3])),
            "location_name": inactive_elem[4] or None,
        }

    def _parse_metadata(self, metadata: List[str]) -> Dict:
        metadata = [i.strip() for i in metadata]
        return {
            "program_version": metadata[0],
            "home_position": (int(metadata[1]), int(metadata[2])),
            "n_active_elements": int(metadata[3]),
        }

    def _get_rly_components(self, railway_file_data: str) -> Dict[str, Any]:
        self._logger.debug("Retrieving components from extracted railway file data")
        _functions = {
            "metadata": lambda x: self._parse_metadata(x),
            "inactive_elements": lambda x: self._parse_inactive_element(x),
            "active_elements": lambda x: self._parse_active_element(x),
            "text": lambda x: self._parse_text(x),
        }
        _signals: typing.Dict[str, typing.Optional[str]] = {
            "G": "ground",
            "4": "4AT",
            "3": "3AT",
            "2": "2AT",
            "*": None,
        }
        _data_dict = {}
        _key = "metadata"
        _part = []
        _counter = 0
        for i, line in enumerate(railway_file_data):
            _counter += 1
            if "**Active elements**" in line:
                _data_dict[_key] = _functions[_key](_part)
                _key = "active_elements"
                _data_dict[_key] = []
                _part = []
                continue
            elif "**Inactive elements**" in line:
                _data_dict["metadata"]["n_inactive_elements"] = int(
                    railway_file_data[i - 1]
                )
                _key = "inactive_elements"
                _part = []
                _data_dict[_key] = []
                continue
            elif "***" in line:
                try:
                    _element = _functions[_key](_part)
                    _element["signal"] = _signals[line[0]]
                    _data_dict[_key].append(_element)
                except ValueError as e:
                    if _key != "inactive_elements":
                        raise e
                    _key = "text"
                    _part = []
                    _data_dict[_key] = []
                    continue
                _part = []
                continue
            _part.append(line.strip().replace("\0", ""))

        if _counter != len(railway_file_data):
            raise RailwayParsingError(
                f"Expected {len(railway_file_data)} statements from rly file but only {_counter} were recovered."
            )

        return _data_dict

    def dump(self, output_file) -> None:
        """Dump metadata to a JSON file"""

        if isinstance(output_file, str):
            with open(output_file, "w") as out_f:
                json.dump(self._rly_data, out_f, indent=2)
        else:
            _out_str = json.dumps(self._rly_data, indent=2)
            output_file.write(_out_str)

        self._logger.info(f"SUCCESS: Output written to '{output_file}")
