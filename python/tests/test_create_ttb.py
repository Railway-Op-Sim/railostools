import datetime

import pytest

from railostools.common.coords import Coordinate, coordinate
from railostools.ttb.components import Reference
from railostools.ttb.create import Service


@pytest.mark.ttb_create
def test_new_service() -> None:
    _service = (
        Service(
            start_position=(coordinate(10, 21), coordinate(10, 22)),
            reference=Reference.from_str("1A27"),
            start_speed=10,
            max_speed=125,
            power=1000,
            brake_force=345,
            mass=546,
            start_time=datetime.datetime.strptime("11:38", "%H:%S").time(),
        )
        .call_at("Gunnislake", "11:34")
        .call_at("Calstock", "11:25")
        .become("1A34", "11:26")
    )
