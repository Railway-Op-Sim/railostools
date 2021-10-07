import datetime
import os.path

from rostools.rly import RlyParser
from rostools.ttb import TTBParser

from typing import List, Tuple, Dict


def avg_point_density(coords: List[Tuple[int]]) -> float:
    _total_distance = 0
    _n_combinations = 0
    for coord_1 in coords:
        for coord_2 in coords:
            _n_combinations += 1
            _total_distance += pow((coord_1[0]-coord_2[0])**2+(coord_1[1]-coord_2[1])**2, 0.5)
    return _n_combinations/_total_distance


def avg_service_rate(services: List[Dict]) -> float:
    _starts = [
        datetime.datetime.strptime(i['start']['time'], '%H:%M')
        for i in services
    ]
    _starts = sorted(_starts)
    _intervals = [abs(i-j).seconds for i, j in zip(_starts[:-1], _starts[1:])]
    return len(_intervals)/sum(_intervals)


def difficulty(timetable_file: str, railway_file: str) -> float:
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

    _avg_density = avg_point_density(_rly_active_element_coords)

    _finish_with_further_action = [
        i for i in _ttb_parser.data[_ttb_key]['services'].values()
        if i['end']['type'] not in ['Fer', 'Frh', 'Frh-sh']
    ]

    _f_fwfa = len(_finish_with_further_action)/len(_ttb_parser.data[_ttb_key]['services'].values())

    _service_rate = avg_service_rate(list(_ttb_parser.data[_ttb_key]['services'].values()))

    return 3E3*_avg_density+(7E3/_f_fwfa)*_service_rate

