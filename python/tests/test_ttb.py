import pytest

import railostools.common.coords as ros_coords
import railostools.ttb.components as ros_comp
import railostools.ttb.components.start as ros_start
import railostools.ttb.components.finish as ros_end
import railostools.ttb.components.actions as ros_act

@pytest.mark.ttb_strings
def test_element_str():
    _start_service = ros_start.Snt(
        time="11:45",
        rear_element_id=ros_coords.Coordinate(10, -10),
        front_element_id=ros_coords.Coordinate(10, -11)
    )

    assert f'{_start_service}' == '11:45;Snt;10-N10 10-N11'


@pytest.mark.ttb_strings
def test_service_str():
    EXPECTED = "1U03;Test service;120;145;73;2002\x0011:23;Snt;10-23 10-24\x0011:34;11:35;Liverpool South Parkway\x00Frh"
    _service = ros_comp.TimetabledService(
        header=ros_comp.Header(
            reference=ros_comp.Reference(service="1U", id=3),
            description="Test service",
            start_speed=120,
            max_speed=145,
            mass=73,
            power=2002
        ),
        start_type=ros_start.Snt(
            time="11:23",
            rear_element_id=ros_coords.Coordinate(10, 23),
            front_element_id=ros_coords.Coordinate(10, 24)
        ),
        finish_type=ros_end.Frh(),
        actions={
            0: ros_act.Location(
                name="Liverpool South Parkway",
                time="11:34",
                end_time="11:35"
            )
        }
    )
    assert f'{_service}' == EXPECTED


@pytest.mark.ttb_strings
def test_dictify():
    ros_comp.Service(
        header=ros_comp.Header(
            reference=ros_comp.Reference(service="1U", id=3),
            description="Test service",
            start_speed=120,
            max_speed=145,
            mass=73,
            power=2002
        ),
        start_type=ros_start.Snt(
            time="11:23",
            rear_element_id=ros_coords.Coordinate(10, 23),
            front_element_id=ros_coords.Coordinate(10, 24)
        ),
        finish_type=ros_end.Fer(
            time="11:34",
            exit_coords=[ros_coords.Coordinate(23, -12)]
        ),
        actions={
            0: ros_act.Location(
                name="Liverpool South Parkway",
                time="11:34",
                end_time="11:35"
            )
        }
    )
