import pytest

import railostools.common.coords as railos_coords
import railostools.ttb.components as railos_comp
import railostools.ttb.components.start as railos_start
import railostools.ttb.components.finish as railos_end
import railostools.ttb.components.actions as railos_act

@pytest.mark.ttb_strings
def test_element_str():
    _start_service = railos_start.Snt(
        time="11:45",
        rear_element_id=railos_coords.Coordinate(X=10, Y=-10),
        front_element_id=railos_coords.Coordinate(X=10, Y=-11)
    )

    assert f'{_start_service}' == '11:45;Snt;10-N10 10-N11'


@pytest.mark.ttb_strings
def test_service_str():
    EXPECTED = "1U03;Test service;120;145;73;2002\x0011:23;Snt;10-23 10-24\x0011:34;11:35;Liverpool South Parkway\x00Frh"
    _service = railos_comp.TimetabledService(
        header=railos_comp.Header(
            reference=railos_comp.Reference(service="1U", id=3),
            description="Test service",
            start_speed=120,
            max_speed=145,
            mass=73,
            power=2002
        ),
        start_type=ros_start.Snt(
            time="11:23",
            rear_element_id=railos_coords.Coordinate(X=10, Y=23),
            front_element_id=railos_coords.Coordinate(X=10, Y=24)
        ),
        finish_type=ros_end.Frh(),
        actions={
            0: railos_act.Location(
                name="Liverpool South Parkway",
                time="11:34",
                end_time="11:35"
            )
        }
    )
    assert f'{_service}' == EXPECTED


@pytest.mark.ttb_strings
def test_dictify():
   railos_comp.TimetabledService(
        header=railos_comp.Header(
            reference=railos_comp.Reference(service="1U", id=3),
            description="Test service",
            start_speed=120,
            max_speed=145,
            mass=73,
            power=2002
        ),
        start_type=ros_start.Snt(
            time="11:23",
            rear_element_id=railos_coords.Coordinate(X=10, Y=23),
            front_element_id=railos_coords.Coordinate(X=10, Y=24)
        ),
        finish_type=ros_end.Fer(
            time="11:34",
            exit_coords=[railos_coords.Coordinate(X=23, Y=-12)]
        ),
        actions={
            0: railos_act.Location(
                name="Liverpool South Parkway",
                time="11:34",
                end_time="11:35"
            )
        }
    )
