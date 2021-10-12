import datetime
import logging
import os.path
import jsbeautifier
import json

from typing import Any, Dict, List

from rostools.exceptions import RailwayParsingError


class RlyParser:
    _logger = logging.getLogger('ROSTools.RlyParser')

    def __init__(self) -> None:
        self._logger.debug('Creating new RlyParser')
        self._rly_data = {}
        self._start_time: datetime.datetime = None
        self._current_file = None

    def parse(self, rly_file: str) -> None:
        self._logger.info(f"Parsing RLY file '{rly_file}'")
        if not os.path.exists(rly_file):
            raise FileNotFoundError(
                f"Cannot parse railway file '{rly_file}', "
                "file does not exist."
            )
        _key = os.path.splitext(os.path.basename(rly_file))[0]
        self._rly_data[_key] = self._get_rly_components(open(rly_file).read())
        self._current_file = rly_file

    @property
    def n_active_elements(self) -> int:
        if not self._current_file:
            raise RailwayParsingError("No file has been parsed yet")
        return self._rly_data[os.path.splitext(os.path.basename(self._current_file))[0]]['n_active_elements']

    @property
    def n_inactive_elements(self) -> int:
        if not self._current_file:
            raise RailwayParsingError("No file has been parsed yet")
        return self._rly_data[os.path.splitext(os.path.basename(self._current_file))[0]]['n_inactive_elements']

    @property
    def program_version(self) -> str:
        if not self._current_file:
            raise RailwayParsingError("No file has been parsed yet")
        return self._rly_data[os.path.splitext(os.path.basename(self._current_file))[0]]['program_version']

    @property
    def data(self):
        if not self._current_file:
            raise RailwayParsingError("No file has been parsed yet")
        return self._rly_data

    def _parse_map(self, component_data: List[str]):
        _map_dict = {'active_elements': [], 'inactive_elements': []}

        _n_inactive = 0
        _end = 0

        for i in range(0, len(component_data), 3):
            if 'Inactive elements' in component_data[i][2]:
                _n_inactive = int(component_data[i][1])
                _end = i
                break
            _element_id = int(component_data[i][2])

            _position = (int(component_data[i][3]), int(component_data[i][4]))

            _length = (
                int(component_data[i][5]),
                int(component_data[i][6])
                if component_data[i][6] != '-1' else None
            )

            _speed_limits = (
                int(component_data[i][7]),
                int(component_data[i][8])
                if component_data[i][8] != '-1' else None
            )

            _map_dict['active_elements'].append(
                {
                    'element_id': _element_id,
                    'position': _position,
                    'length': _length,
                    'speed_limit': _speed_limits,
                    'location_name': component_data[i + 1][1] or None,
                    'active_element_name': component_data[i + 2][0] or None,
                }
            )

        for i in range(_end + 1, len(component_data), 3):
            if '****' in component_data[i][1]:
                break
            _element_id = int(component_data[i][1])
            _position = (int(component_data[i][2]), int(component_data[i][3]))

            _map_dict['inactive_elements'].append(
                {
                    'element_id': _element_id,
                    'position': _position,
                    'location_name': component_data[i + 1][0] or None,
                }
            )

        return {'n_inactive_elements': int(_n_inactive), 'elements': _map_dict}

    def _get_rly_components(self, railway_file_data: str) -> Dict[str, Any]:
        self._logger.debug('Retrieving components from extracted railway file data')
        _rly_components: List[str] = railway_file_data.split('\0')
        _rly_components = [i.split('\n') for i in _rly_components]

        _program_version = _rly_components[0][0]
        _home_position = (int(_rly_components[1][1]), int(_rly_components[1][2]))
        _n_elements = _rly_components[1][3]
        _data_dict = {
            'program_version': _program_version,
            'home_position': _home_position,
            'n_active_elements': int(_n_elements),
            'user_graphics': _rly_components[1][4][-1] == '1'
        }
        _data_dict.update(self._parse_map(_rly_components[2:]))
        return _data_dict

    def json(self, output_file) -> None:
        """Dump metadata to a JSON file"""
        _beautifier_opts = jsbeautifier.default_options()
        _beautifier_opts.indent_size = 2

        if isinstance(output_file, str):
            with open(output_file, 'w') as out_f:
                out_f.write(jsbeautifier.beautify(json.dumps(self._rly_data), _beautifier_opts))
        else:
            _out_str = jsbeautifier.beautify(json.dumps(self._rly_data), _beautifier_opts)
            output_file.write(_out_str)

        self._logger.info(f"SUCCESS: Output written to '{output_file}")
