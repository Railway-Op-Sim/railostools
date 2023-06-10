import pytest

import railostools.common.coords as railos_coords
import railostools.ttb.components as railos_ttb_comp


@pytest.mark.components
@pytest.mark.parametrize(
    "coord_1,coord_2,passes",
    [
        ("1-32", "1-33", True),
        ("11-N4", "11-N4", False),
        ("N45-N34", "N81-N2", False),
        ("N26-7", "N27-7", True),
        ("N44-N34", "N45-N33", True)
    ],
    ids=lambda x: str(x).replace("-", "_")
)
def test_coords(coord_1: str, coord_2: str, passes: bool) -> None:
    _coord_1 = railos_coords.Coordinate.from_string(coord_1)
    _coord_2 = railos_coords.Coordinate.from_string(coord_2)

    assert _coord_1.is_neighbour(_coord_2) == passes


@pytest.mark.components
@pytest.mark.parametrize(
    "headcode,prefix,service,id",
    [
        ("1N03", None, "1N", 3),
        ("FDKLR01", "FDK", "LR", 1)
    ]
)
def test_header_parsing(headcode: str, prefix: str, service: str, id: int) -> None:
    _ref = railos_ttb_comp.Reference.from_string(headcode)
    assert _ref.prefix == prefix
    assert _ref.id == id
    assert _ref.service == service
    assert _ref.__str__() == headcode