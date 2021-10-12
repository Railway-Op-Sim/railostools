import datetime
import os.path
import math
import copy
import typing

from rostools.rly import RlyParser
from rostools.ttb import TTBParser

from typing import List, Tuple, Dict


def avg_point_density(coords: List[Tuple[int]], _n_sub_region_axis: int = 5) -> float:
    # Firstly need to get subregions by finding the four extrema
    _min_x = -200
    _min_y = -200
    _max_x = 200
    _max_y = 200

    # Total number of regions
    N_A = 0

    # Interval Size
    _dx = int(math.ceil((_max_x - _min_x) / _n_sub_region_axis))
    _dy = int(math.ceil((_max_y - _min_y) / _n_sub_region_axis))

    # Intervals
    _interv_x = [(i * _dx, (i + 1) * _dx) for i in range(_n_sub_region_axis - 1)]
    _interv_y = [(i * _dy, (i + 1) * _dy) for i in range(_n_sub_region_axis - 1)]

    _sum_den = 0

    # calculate average track density
    for x_i in _interv_x:
        for y_i in _interv_y:
            _n_tai = sum(
                1 for i in coords
                if x_i[0] <= i[0] < x_i[1]
                if y_i[0] <= i[1] < y_i[1]
            )

            _sum_den += 0 if _n_tai == 0 else _n_tai / _dx * _dy
            N_A += 1

    return N_A / _sum_den


def _unpack_repeats(services: List[Dict]):
    _unpacked = []

    for service in services:
        _unpacked.append(service)
        if service['repeats']:
            _start_time = datetime.datetime.strptime(service['start']['time'], '%H:%M')
            _n_repeats = service['repeats']['n_repeats']
            _interval = datetime.timedelta(minutes=service['repeats']['interval'])
            _times = [
                datetime.datetime.strftime(_start_time + i * _interval, '%H:%M')
                for i in range(1, _n_repeats + 1)
            ]
            for time in _times:
                _new_service = copy.deepcopy(service)
                _new_service['start']['time'] = time
                _unpacked.append(_new_service)

    return _unpacked


def avg_service_density(services: List[Dict], bin_size: int = 5 * 60) -> float:
    _unpacked = _unpack_repeats(services)
    _starts = [
        datetime.datetime.strptime(i['start']['time'], '%H:%M')
        for i in _unpacked
    ]

    _starts = sorted(_starts)

    t = _starts[0] + datetime.timedelta(seconds=bin_size)
    i = 0
    _bins = []
    _bin = []

    while t < _starts[-1]:
        while _starts[i] < t:
            _bin.append(_starts[i])
            i += 1
        _bins.append(_bin)
        _bin = []
        t += datetime.timedelta(seconds=bin_size)

    _starts = sorted(_starts)
    _intervals = [abs(i - j).seconds for i, j in zip(_starts[:-1], _starts[1:])]

    _interv_sum = sum(_intervals) if sum(_intervals) > 0 else 1

    return 60 * len(_intervals) / _interv_sum


def junction_element_fraction(active_element_element_ids: List[Tuple[int]]):
    _junction_speedtags = list(range(1, 17)) + list(range(28, 48)) + list(range(132, 140))
    _junction_tags = [i for i in active_element_element_ids if i in _junction_speedtags]
    return len(_junction_tags) / len(active_element_element_ids)


def map_start_fraction(services: List[Dict], coord_type_map_data: Dict) -> float:
    _starts = [
        i['start'] for i in services if 'Snt' in i['start']['type']
    ]

    _entry_ids = list(range(80, 88))

    _starts_on_map = [
        i for i in _starts
        if coord_type_map_data[tuple(i['location'][0])] not in _entry_ids
           and coord_type_map_data[tuple(i['location'][1])] not in _entry_ids
    ]

    return len(_starts_on_map) / len(services)


def map_end_fraction(services: List[Dict], coord_type_map_data: Dict) -> float:
    _ends = [
        i['start'] for i in services if i['end']['type'] not in ['Fer', 'Frh']
    ]

    return len(_ends) / len(services)


def _get_coord_type_data(map_data: Dict) -> Dict:
    return {element['position']: element['element_id'] for element in map_data}


def difficulty_components(timetable_file: str, railway_file: str) -> typing.Dict:
    _ttb_parser = TTBParser()
    _ttb_parser.parse(timetable_file)
    _rly_parser = RlyParser()
    _rly_parser.parse(railway_file)
    _ttb_key = os.path.splitext(os.path.basename(timetable_file))[0]
    _rly_key = os.path.splitext(os.path.basename(railway_file))[0]

    _rly_active_element_coords = [
        i['position'] for i in
        _rly_parser.data[_rly_key]['elements']['active_elements']
    ]

    _speed_button_tags = [
        i['element_id'] for i in
        _rly_parser.data[_rly_key]['elements']['active_elements']
    ]

    avg_density_component = avg_point_density(_rly_active_element_coords)

    _coord_type_map_data = _get_coord_type_data(_rly_parser.data[_rly_key]['elements']['active_elements'])

    service_rate_component = avg_service_density(list(_ttb_parser.data[_ttb_key]['services'].values()))

    j_frac = junction_element_fraction(_speed_button_tags)

    sm_frac = map_start_fraction(list(_ttb_parser.data[_ttb_key]['services'].values()), _coord_type_map_data)

    fm_frac = map_end_fraction(list(_ttb_parser.data[_ttb_key]['services'].values()), _coord_type_map_data)

    return {
        'service_rate': service_rate_component,
        'average_density': avg_density_component,
        'junctions': j_frac,
        'start_on_map_fraction': sm_frac,
        'finish_on_map_fraction': fm_frac,
        'difficulty': int(avg_density_component*(1+j_frac) + (service_rate_component+0.01)*(1+sm_frac+fm_frac)*3.8+1)
    }

