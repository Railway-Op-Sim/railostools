import pytest
import railostools.rly.relations as railos_rly_rel
import railostools.common.enumeration as railos_enums


def test_example_connections() -> None:
    for i in railos_enums.Elements.__members__.values():
        assert i in railos_rly_rel.CONNECTIONS
    assert railos_rly_rel.can_connect(
        railos_enums.Elements.Junction_Up_Right_RightAngle,
        railos_enums.Elements.Horizontal,
    )
    assert not railos_rly_rel.can_connect(
        railos_enums.Elements.Junction_Up_Right_RightAngle,
        railos_enums.Elements.DiagonalUp,
    )
