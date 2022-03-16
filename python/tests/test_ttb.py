import pytest

import rostools.ttb.services.start as ros_ttb_start
import rostools.common.coords as ros_coords

@pytest.mark.ttb_strings
def test_element_str():
    _start_service = ros_ttb_start.Snt(
        rear_element_id=ros_coords.Coordinate(10, -10),
        front_element_id=ros_coords.Coordinate(10, -11)
    )

    assert f'{_start_service}' == 'Snt;10-N10 10-N11'
