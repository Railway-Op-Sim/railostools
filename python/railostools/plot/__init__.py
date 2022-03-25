

import datetime
import typing
import matplotlib.dates as mdates 
import matplotlib.pyplot as plt
import railostools.ttb.parsing as ttb_parse
import railostools.ttb.components.actions as ros_act
import railostools.ttb.components as ros_comp


def create_plot_data(timetable_file: str):
    """Build plot data for a given timetable"""
    _parser = ttb_parse.TTBParser()
    _parser.parse(timetable_file)

    # Need to collect all routes by looking at similar location
    # orderings within services
    _call_point_sets: typing.List[typing.List[str]] = []

    _services = _parser.data.services

    for service in _services.values():
        if not isinstance(service, ros_comp.TimetabledService):
            continue

        _calling_points = tuple(
            i.name for i in service.actions.values()
            if isinstance(i, ros_act.Location)
        )

        if len(set(_calling_points)) != len(_calling_points) or len(_calling_points) < 2:
            continue

        _current_sets_str = [str(i) for i in _call_point_sets]

        for set_c in _current_sets_str:
            _str_curr = str(_current_sets_str).replace("(", "").replace(")", "").strip()
            if _str_curr not in set_c:
                if set_c in _str_curr:
                    _call_point_sets.remove(set_c)
                _call_point_sets.append(_calling_points)

    for call_point_set in _call_point_sets:
        _legend = []
        for service in _services.values():
            if not isinstance(service, ros_comp.TimetabledService):
                continue


            _calling_points = tuple(
                i.name for i in service.actions.values()
                if isinstance(i, ros_act.Location)
            )

            _times = tuple(
                datetime.datetime.strptime(i.time, "%H:%M") for i in service.actions.values()
                if isinstance(i, ros_act.Location)
            )

            _str_curr = str(_calling_points).replace("(", "").replace(")", "").strip()

            if any([_str_curr in str(call_point_set), _str_curr in str(tuple(reversed(call_point_set)))]):
                plt.plot(_times, _calling_points, 'o-')
                _legend.append(str(service.header.reference))
        plt.legend(_legend)
        plt.show()

if __name__ in "__main__":
    create_plot_data("C:/Program Files/RailwayOperationSimulator/Railway/Program timetables/SunshineCoastLine_2022_03_02.ttb")