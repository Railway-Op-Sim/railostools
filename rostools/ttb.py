import datetime
import os
import jsbeautifier
import json
import logging

from typing import List, Any, Dict, OrderedDict, Tuple


class TTBParser:
    _logger = logging.getLogger('ROSTools.TTBParser')

    def __init__(self) -> None:
        self._logger.debug('Creating new TTBParser')
        self._ttb_data = {}
        self._start_time: datetime.datetime = None
        self._current_file = ''

    def _get_ttb_components(self, timetable_file_data: str) -> Dict[str, Any]:
        self._logger.debug('Retrieving components from extracted timetable data')
        _ttb_components: List[str] = timetable_file_data.split('\0')

        _services: Dict[str, Any] = {}

        _comments: List[str] = {}

        for i, line in enumerate(_ttb_components[1:]):
            self._logger.debug(f'Parsing line [{i+1:^4}] : {line}')
            if not line.strip():
                self._logger.debug('Line empty.')
                continue
            if line.strip() and line.strip()[0] == '*':
                self._logger.debug('Recognised comment.')
                _comments[i+1] = line.replace('*', '').strip()
                continue
            _id, _service_dict = self._parse_service(line)
            _services[_id] = _service_dict

        return {
            'comments': _comments,
            'services': _services,
            'start_time': _ttb_components[0]
        }

    def _parse_service(self, service: str) -> Tuple[str, OrderedDict]:
        self._logger.debug('Parsing service.')
        _service_definitions = service.split(',')

        _service_dict = {'properties': {}}

        if len(_service_definitions[0].split(';')) > 2:
            (
                _service_id,
                _service_dict['description'],
                _service_dict['properties']['start_speed'],
                _service_dict['properties']['max_speed'],
                _service_dict['properties']['mass'],
                _service_dict['properties']['brake_force'],
                _service_dict['properties']['power']
            ) = _service_definitions[0].split(';')
            self._logger.debug(f"Service '{_service_id}' initialisation statement found.")
        else:
            _service_id, _service_dict['service_desc'] = _service_definitions[0].split(';')
            self._logger.debug(f"Continuation service '{_service_id}' found.")

        for key in ['start_speed', 'max_speed', 'mass', 'brake_force', 'power']:
            try:
                _service_dict['properties'][key] = int(_service_dict['properties'][key])
            except KeyError:
                pass

        _start_definitions = _service_definitions[1].split(';')

        _service_dict['start'] = {
            'time': _start_definitions[0],
            'type': _start_definitions[1],
            'location': None,
            'from_service': None,
        }

        self._logger.debug(f"Parsed start metadata: {_service_dict['start']}")

        if _service_dict['start']['type'] in ['Snt', 'Snt-sh']:
            _service_dict['start']['location'] = tuple(
                tuple(int(j.replace('N', '-')) for j in i.split('-'))
                for i in _start_definitions[2].split()
            )
        elif _service_dict['start']['type'] in ['Sfs', 'Sns', 'Sns-fsh']:
            _service_dict['start']['from_service'] = _start_definitions[2]
        elif _service_dict['start']['type'] in ['Sns-sh', 'Snt-sh']:
            _service_dict['start']['from_service'] = _start_definitions[3]

        if ';' in _service_definitions[-1] and _service_definitions[-1].split(';')[0] == 'R':
            _, _interval, _digits, _number = _service_definitions[-1].split(';')

            _service_dict['repeats'] = {
                'interval': _interval,
                'digits': _digits,
                'n_repeats': _number
            }

            _service_definitions = _service_definitions[2:-1]
        else:
            _end_components = _service_definitions[-1].split(';')

            _service_dict['end'] = {
                'time': _end_components[0],
                'type': _end_components[1],
                'form_service': None,
                'shuttle_partner': None
            }

            if _service_dict['end']['type'] in ['Frh-sh', 'Fns-sh', 'F-nshs']:
                _service_dict['end']['shuttle_partner'] = _end_components[2]

            if _service_dict['end']['type'] == 'Fns-sh':
                _service_dict['end']['form_service'] = _end_components[3]
            elif _service_dict['end']['type'] == 'Fns':
                _service_dict['end']['form_service'] = _end_components[2]

            _service_definitions = _service_definitions[2:-1]

        _service_dict['schedule'] = tuple(i.split(';') for i in _service_definitions[2:-1])

        return _service_id, _service_dict

    def get_start_time(self):
        return self._ttb_data[self._current_file]['start_time']

    def get_comments(self):
        return self._ttb_data[self._current_file]['comments']

    def parse(self, ttb_file: str) -> None:
        self._logger.info(f"Parsing TTB file '{ttb_file}'")
        if not os.path.exists(ttb_file):
            raise FileNotFoundError(
                f"Cannot parse timetable file '{ttb_file}', "
                "file does not exist."
            )

        self._current_file = ttb_file
        self._ttb_data[ttb_file] = self._get_ttb_components(open(ttb_file).read())

        self._logger.debug("Filling in remaining service properties from existing entries")
        for service, value in self._ttb_data[ttb_file]['services'].items():
            if not value['properties'] and value['start']['from_service']:
                _properties = self._ttb_data[ttb_file]['services'][value['start']['from_service']]['properties']
                if _properties:
                    self._ttb_data[ttb_file]['services'][service]['properties'] = _properties

    def json(self, output_file) -> None:
        """Dump metadata to a JSON file"""
        _beautifier_opts = jsbeautifier.default_options()
        _beautifier_opts.indent_size = 2

        if isinstance(output_file, str):
            with open(output_file, 'w') as out_f:
                out_f.write(jsbeautifier.beautify(json.dumps(self._ttb_data), _beautifier_opts))
        else:
            _out_str = jsbeautifier.beautify(json.dumps(self._ttb_data), _beautifier_opts)
            output_file.write(_out_str)

        self._logger.info(f"SUCCESS: Output written to '{output_file}")

