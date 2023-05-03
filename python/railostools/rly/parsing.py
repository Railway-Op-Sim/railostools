import datetime
import json
import logging
import os.path
import dataclasses
import pandas
import pydantic
import semver
import typing
import igraph
import functools
import itertools
import tqdm
import re
import matplotlib.pyplot as plt

from railostools.exceptions import RailwayParsingError
from railostools.common.enumeration import Elements
from railostools.rly.relations import can_connect
import railostools.exceptions as railos_exc


def coordinate_to_position_identifier(position: typing.Tuple[int, int]) -> str:
    return (
        f"{'N' if position[0] < 0 else ''}{abs(position[0])}"
        f"-{'N' if position[1] < 0 else ''}{abs(position[1])}"
    )

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



class RlyElement(pydantic.BaseModel):
    element_id: Elements
    position: pydantic.conlist(pydantic.conint(), max_items=2, min_items=2)
    location_name: typing.Optional[str] = None

    @property
    def position_id(self) -> str:
        return coordinate_to_position_identifier(self.position)


class InactiveElement(RlyElement):
    pass


class ActiveElement(RlyElement):
    length: typing.Tuple[pydantic.conint(ge=0), pydantic.conint(ge=0) | None]
    speed_limit: typing.Tuple[pydantic.conint(ge=0), pydantic.conint(ge=0) | None]
    active_element_name: typing.Optional[str] = None
    signal: typing.Optional[str] = None
    neighbours: typing.List["ActiveElement"] = []


class Font(pydantic.BaseModel):
    name: str
    size: int
    color: int
    charset: int
    style: int


class Text(pydantic.BaseModel):
    position: pydantic.conlist(pydantic.conint(), max_items=2, min_items=2)
    text_string: str
    font: Font


class Metadata(pydantic.BaseModel):
    program_version: str
    home_position: pydantic.conlist(pydantic.conint(), max_items=2, min_items=2)
    n_active_elements: int
    n_inactive_elements: typing.Optional[int] = None

    @pydantic.validator("program_version", check_fields=False)
    def validate_version(cls, version: str) -> str:
        try:
            semver.VersionInfo.parse(version.replace("v", ""))
        except ValueError as e:
            raise railos_exc.MetadataError(
                f"Invalid semantic version '{version}'"
            ) from e
        return version


class RlyData(pydantic.BaseModel):
    active_elements: typing.List[ActiveElement]
    inactive_elements: typing.List[InactiveElement]
    metadata: Metadata
    text: typing.Optional[typing.List[Text]]=None


class RlyParser:
    _logger = logging.getLogger("RailOSTools.RlyParser")

    def __init__(self) -> None:
        self._logger.debug("Creating new RlyParser")
        self._rly_data: typing.Dict[str, RlyData] = {}
        self._start_time: datetime.time = None
        self._current_file = None
        self._node_map: typing.Dict[str, igraph.Graph] = {}

    def parse(self, rly_file: str) -> None:
        self._logger.info(f"Parsing RLY file '{rly_file}'")
        if not os.path.exists(rly_file):
            raise FileNotFoundError(
                f"Cannot parse railway file '{rly_file}', " "file does not exist."
            )

        if not open(rly_file).readlines():
            raise railos_exc.ParsingError("Cannot parse empty file.")

        _key = os.path.splitext(os.path.basename(rly_file))[0]
        self._rly_data[_key] = self._get_rly_components(
            open(rly_file, encoding="latin-1").readlines()
        )

        if not self._rly_data[_key]:
            raise railos_exc.ParsingError("Failed to retrieve data from file.")

        self._current_file = rly_file

        self._assign_neighbours()
        self._node_map[_key] = self._build_node_map()

        self._logger.info("Parsing successful, railway is valid.")

    def keys(self):
        return self._rly_data.keys()

    def __getitem__(self, item) -> RlyData:
        return self._rly_data[item]

    @property
    def n_active_elements(self) -> int:
        if not self._current_file:
            raise RailwayParsingError("No file has been parsed yet")
        return self._rly_data[
            os.path.splitext(os.path.basename(self._current_file))[0]
        ].metadata.n_active_elements

    @property
    def n_inactive_elements(self) -> int:
        if not self._current_file:
            raise RailwayParsingError("No file has been parsed yet")
        return self._rly_data[
            os.path.splitext(os.path.basename(self._current_file))[0]
        ].metadata.n_inactive_elements

    @property
    def program_version(self) -> str:
        if not self._current_file:
            raise RailwayParsingError("No file has been parsed yet")
        return self._rly_data[
            os.path.splitext(os.path.basename(self._current_file))[0]
        ].metadata.program_version

    @property
    def n_signals(self) -> int:
        return self.tables.signals.size

    @property
    def n_level_crossings(self) -> int:
        return len([i for i in self.active_elements if i.element_id == Elements.Level_Crossing])

    @property
    def n_stations(self) -> int:
        return len(self.named_locations)

    @property
    def n_points(self) -> int:
        _points: typing.List[ActiveElement] = [
            i for i in self.active_elements
            if i.element_id in (
                Elements.Junction_Right_Up_RightAngle,
                Elements.Junction_Left_Up_RightAngle,
                Elements.Junction_Right_Down_RightAngle,
                Elements.Junction_Left_Down_RightAngle,
                Elements.Junction_Up_Left_RightAngle,
                Elements.Junction_Up_Right_RightAngle,
                Elements.Junction_Down_Left_RightAngle,
                Elements.Junction_Down_Right_RightAngle,
                Elements.Junction_Right_Up_45Angle,
                Elements.Junction_Left_Up_45Angle,
                Elements.Junction_Right_Down_45Angle,
                Elements.Junction_Left_Down_45Angle,
                Elements.Junction_Up_Left_45Angle,
                Elements.Junction_Up_Right_45Angle,
                Elements.Junction_Down_Left_45Angle,
                Elements.Junction_Down_Right_45Angle,
                Elements.Junction_DiagonalDown_Up_45Angle,
                Elements.Junction_DiagonalUp_Up_45Angle,
                Elements.Junction_DiagonalUp_Down_45Angle,
                Elements.Junction_DiagonalDown_Down_45Angle,
                Elements.Junction_DiagonalDown_Left_45Angle,
                Elements.Junction_DiagonalUp_Right_45Angle,
                Elements.Junction_DiagonalUp_Left_45Angle,
                Elements.Junction_DiagonalDown_Right_45Angle
            )
        ]
        return len(_points)

    def get_element_at(
        self, coordinates: typing.Tuple[int, int]
    ) -> typing.Optional[Elements]:
        for element in self.active_elements + self.inactive_elements:
            if tuple(element.position) == tuple(coordinates):
                if _id := element.element_id:
                    return Elements(_id)
        return None

    def get_element_connected_neighbours(
        self, coordinates: typing.Tuple[int, int]
    ) -> typing.List[typing.Tuple[int, int]]:
        if not (_this_element := self.get_element_at(coordinates)):
            raise RailwayParsingError(f"No element found at '{coordinates}'")
        _neighbour_coords = (
            (coordinates[0], coordinates[1] + 1),
            (coordinates[0], coordinates[1] - 1),
            (coordinates[0] + 1, coordinates[1]),
            (coordinates[0] - 1, coordinates[1]),
            (coordinates[0] + 1, coordinates[1] + 1),
            (coordinates[0] - 1, coordinates[1] + 1),
            (coordinates[0] + 1, coordinates[1] - 1),
            (coordinates[0] - 1, coordinates[1] - 1),
        )

        _found_neighbours = [i for i in _neighbour_coords if self.get_element_at(i)]

        return [
            i
            for i in _found_neighbours
            if can_connect(_this_element, self.get_element_at(i), coordinates, i)
        ]

    @property
    def named_locations(self) -> typing.Dict[str, TimetableLocation]:
        """Returns list of timetable locations and coordinates

        NOTE: These are locations which are of size 2, i.e. would have the
        start and end point within the location region. Track sections outside
        of the domain of the location cannot be easily identified using this method.
        """

        # Retrieve timetable location names from data
        _location_names: typing.Set[str] = {
            n.active_element_name
            for n in self._rly_data[
                os.path.splitext(os.path.basename(self._current_file))[0]
            ].active_elements
            if n.active_element_name
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
            for element in self.active_elements:
                if element.active_element_name != location:
                    continue
                if not (element_int := element.element_id):
                    continue
                element_type: Elements = Elements(element_int)
                _loc_elements["element_types"].append(element_type)
                _loc_elements["element_coords"].append(element.position)

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
    def data(self) -> typing.Dict[str, RlyData]:
        if not self._current_file:
            raise RailwayParsingError("No file has been parsed yet")
        return self._rly_data

    @property
    def active_elements(self) -> typing.List[ActiveElement]:
        return self.data[os.path.splitext(os.path.basename(self._current_file))[0]].active_elements

    @property
    def inactive_elements(self) -> typing.List[InactiveElement]:
        return self.data[os.path.splitext(os.path.basename(self._current_file))[0]].inactive_elements

    @property
    def nodes(self) -> igraph.Graph:
        return self._node_map[os.path.splitext(os.path.basename(self._current_file))[0]]

    def _make_signal_table(self) -> pandas.DataFrame:
        _df_dict = {col: [] for col in ["position", "signal"]}
        for element in self.active_elements:
            if not element.signal:
                continue
            for key in _df_dict:
                _df_dict[key].append(getattr(element, key))
        return pandas.DataFrame.from_dict(_df_dict)

    @property
    def tables(self) -> RlyInfoTables:
        return RlyInfoTables(signals=self._make_signal_table())

    def _parse_active_element(self, active_elem: typing.List[str]) -> ActiveElement:
        active_elem: typing.List[str] = [i.strip() for i in active_elem]
        return ActiveElement(
            element_id=int(active_elem[1]),
            position=(int(active_elem[2]), int(active_elem[3])),
            length=(
                int(active_elem[4]),
                int(active_elem[5]) if active_elem[5] != "-1" else None,
            ),
            speed_limit=(
                int(active_elem[6]),
                int(active_elem[7]) if active_elem[7] != "-1" else None,
            ),
            location_name=active_elem[8] or None,
            active_element_name=active_elem[9] or None,
        )

    def _parse_text(self, text_elem: typing.List[str]) -> Text:
        text_elem = [i.strip() for i in text_elem]
        return Text(
            n_items=int(text_elem[0]),
            position=(int(text_elem[2]), int(text_elem[3])),
            text_string=text_elem[4],
            font=Font(
                name=text_elem[5],
                size=int(text_elem[6]),
                color=int(text_elem[7]),
                charset=int(text_elem[8]),
                style=int(text_elem[9]),
            ),
        )

    def _parse_inactive_element(self, inactive_elem: typing.List[str]) -> InactiveElement:
        if inactive_elem := [i.strip() for i in inactive_elem]:
            return InactiveElement(
                element_id=int(inactive_elem[1]),
                position=(int(inactive_elem[2]), int(inactive_elem[3])),
                location_name=inactive_elem[4] or None,
            )
        else:
            raise railos_exc.ParsingError("No inactive elements were found.")

    def _parse_metadata(self, metadata: typing.List[str]) -> Metadata:
        if metadata := [i.strip() for i in metadata]:
            _prog_version_re = re.findall(r'(v\d+\.\d+\.\d+)', metadata[0])
            return Metadata(
                program_version=_prog_version_re[0],
                home_position=(int(metadata[1]), int(metadata[2])),
                n_active_elements=int(metadata[3]),
            )
        else:
            raise railos_exc.ParsingError("Failed to retrieve railway metadata.")

    def _get_rly_components(self, railway_file_data: str) -> RlyData:
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
        _data_dict: typing.Dict[str, typing.Union[Text, ActiveElement, InactiveElement, Metadata]] = {}
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
                _data_dict["metadata"].n_inactive_elements = int(
                    railway_file_data[i - 1]
                )
                _key = "inactive_elements"
                _part = []
                _data_dict[_key] = []
                continue
            elif "***" in line and _key != "inactive_elements":
                try:
                    _element: ActiveElement = _functions[_key](_part)
                    _element.signal = _signals[line[0]]
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

        return RlyData(**_data_dict)

    def _assign_neighbours(self) -> None:
        for element in self.active_elements:
            element.neighbours = self.get_element_connected_neighbours(element.position)

    def _build_node_map(self) -> igraph.Graph:
        _node_connections: typing.List[typing.Tuple[int, int]] = []
        _node_graph = igraph.Graph()
        for element in tqdm.tqdm(self.active_elements):
            for coordinate in element.neighbours:
                _coord_str: typing.Tuple[str, str] = (element.position_id, coordinate_to_position_identifier(coordinate))
                _rev_coord_str: typing.Tuple[str, str] = tuple(reversed(_coord_str))
                if _coord_str not in _node_connections and _rev_coord_str not in _node_connections:
                    _node_connections.append(_coord_str)
            _node_graph.add_vertex(element.position_id, x=element.position[0], y=element.position[1], label="")
        _node_graph.add_edges(_node_connections)
        return _node_graph

    def plot(self, target_file: str, map_key: typing.Optional[str]=None) -> None:
        """Plot the node map for the railway"""
        if not self._node_map:
            raise RailwayParsingError("No file parsed yet.")

        if not map_key:
            _map = self.nodes
        else:
            _map = self._node_map[map_key]

        _figure, _axis = plt.subplots()
        igraph.plot(_map, layout=_map.layout("auto"), target=_axis)
        _figure.savefig(target_file)

    def dump(self, output_file) -> None:
        """Dump metadata to a JSON file"""

        if isinstance(output_file, str):
            with open(output_file, "w") as out_f:
                json.dump(self._rly_data, out_f, indent=2)
        else:
            _out_str = json.dumps({k: v.dict() for k, v in self._rly_data.items()}, indent=2)
            output_file.write(_out_str)

        self._logger.info(f"SUCCESS: Output written to '{output_file}")
