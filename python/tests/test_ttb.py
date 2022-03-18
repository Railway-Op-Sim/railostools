import pytest

import railostools.ttb.services.start as ros_ttb_start
import railostools.common.coords as ros_coords
import railostools.ttb as ros_ttb
import railostools.ttb.services as ros_srv
import railostools.ttb.services.start as ros_start
import railostools.ttb.services.finish as ros_end
import railostools.ttb.services.actions as ros_act

@pytest.mark.ttb_strings
def test_element_str():
    _start_service = ros_ttb_start.Snt(
        time="11:45",
        rear_element_id=ros_coords.Coordinate(10, -10),
        front_element_id=ros_coords.Coordinate(10, -11)
    )

    assert f'{_start_service}' == '11:45;Snt;10-N10 10-N11'


@pytest.mark.ttb_strings
def test_service_str():
    EXPECTED = "1U03;Test service;120;145;73;2002\x0011:23;Snt;10-23 10-24\x0011:34;11:35;Liverpool South Parkway\x00Frh"
    _service = ros_ttb.Service(
        header=ros_ttb.Header(
            reference=ros_srv.Reference(headcode="1U03"),
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
                start_time="11:34",
                end_time="11:35"
            )
        }
    )
    assert f'{_service}' == EXPECTED


@pytest.mark.ttb_strings
def test_dictify():
    _service = ros_ttb.Service(
        header=ros_ttb.Header(
            reference=ros_srv.Reference(headcode="1U03"),
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
                start_time="11:34",
                end_time="11:35"
            )
        }
    )
    print(_service.to_dict())
