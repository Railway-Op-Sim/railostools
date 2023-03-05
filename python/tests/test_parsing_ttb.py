import os.path

import pytest
import railostools.ttb.parsing as railos_parse
import railostools.ttb.parsing.actions as railosparse_act
import railostools.ttb.parsing.finish as railosparse_finish
import railostools.ttb.parsing.start as railosparse_start
import railostools.ttb.string as railos_ttb_str

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


@pytest.mark.ttb_parsing
@pytest.mark.parametrize("hour", (10, 27), ids=("<24hr", ">24hr"))
def test_snt_parse(hour: int) -> None:
    TEST_STR = f"{hour}:23;Snt;1-34 1-35"
    _result = railosparse_start.parse_Snt(railos_ttb_str.split(TEST_STR))
    assert str(_result) == TEST_STR


@pytest.mark.ttb_parsing
@pytest.mark.parametrize("hour", (10, 27), ids=("<24hr", ">24hr"))
def test_sfs_parse(hour: int) -> None:
    TEST_STR = f"{hour}:23;Sfs;1U03"
    _result = railosparse_start.parse_Sfs(railos_ttb_str.split(TEST_STR))
    assert str(_result) == TEST_STR


@pytest.mark.ttb_parsing
@pytest.mark.parametrize("hour", (10, 27), ids=("<24hr", ">24hr"))
def test_Sns_fsh(hour: int) -> None:
    TEST_STR = f"{hour}:23;Sns-fsh;1U04"
    _result = railosparse_start.parse_Sns_fsh(railos_ttb_str.split(TEST_STR))
    assert str(_result) == TEST_STR


@pytest.mark.ttb_parsing
@pytest.mark.parametrize("hour", (10, 27), ids=("<24hr", ">24hr"))
def test_Snt_sh(hour: int) -> None:
    TEST_STR = f"{hour}:23;Snt-sh;1-45 1-46;1U04"
    _result = railosparse_start.parse_Snt_sh(railos_ttb_str.split(TEST_STR))
    assert str(_result) == TEST_STR


@pytest.mark.ttb_parsing
@pytest.mark.parametrize("hour", (10, 27), ids=("<24hr", ">24hr"))
def test_Sns_sh(hour: int) -> None:
    TEST_STR = f"{hour}:23;Sns-sh;1U02;1U04"
    _result = railosparse_start.parse_Sns_sh(railos_ttb_str.split(TEST_STR))
    assert str(_result) == TEST_STR


@pytest.mark.ttb_parsing
@pytest.mark.parametrize("hour", (10, 27), ids=("<24hr", ">24hr"))
def test_Fns(hour: int) -> None:
    TEST_STR = f"{hour}:23;Fns;1U03"
    _result = railosparse_finish.parse_Fns(railos_ttb_str.split(TEST_STR))
    assert str(_result) == TEST_STR


@pytest.mark.ttb_parsing
@pytest.mark.parametrize("hour", (10, 27), ids=("<24hr", ">24hr"))
def test_Fer(hour: int) -> None:
    TEST_STR = f"{hour}:23;Fer;1-94"
    _result = railosparse_finish.parse_Fer(railos_ttb_str.split(TEST_STR))
    assert str(_result) == TEST_STR


@pytest.mark.ttb_parsing
@pytest.mark.parametrize("hour", (10, 27), ids=("<24hr", ">24hr"))
def test_Frh(hour: int) -> None:
    TEST_STR = "Frh"
    _result = railosparse_finish.parse_Frh(railos_ttb_str.split(TEST_STR))
    assert str(_result) == TEST_STR


@pytest.mark.ttb_parsing
@pytest.mark.parametrize("hour", (10, 27), ids=("<24hr", ">24hr"))
def test_Fjo(hour: int) -> None:
    TEST_STR = f"{hour}:03;Fjo;1U05"
    _result = railosparse_finish.parse_Fjo(railos_ttb_str.split(TEST_STR))
    assert str(_result) == TEST_STR


@pytest.mark.ttb_parsing
@pytest.mark.parametrize("hour", (10, 27), ids=("<24hr", ">24hr"))
def test_Frh_sh(hour: int) -> None:
    TEST_STR = f"{hour}:03;Frh-sh;2U05"
    _result = railosparse_finish.parse_Frh_sh(railos_ttb_str.split(TEST_STR))
    assert str(_result) == TEST_STR


@pytest.mark.ttb_parsing
@pytest.mark.parametrize("hour", (10, 27), ids=("<24hr", ">24hr"))
def test_Fns_sh(hour: int) -> None:
    TEST_STR = f"{hour}:03;Fns-sh;2U05;1Z09"
    _result = railosparse_finish.parse_Fns_sh(railos_ttb_str.split(TEST_STR))
    assert str(_result) == TEST_STR


@pytest.mark.ttb_parsing
@pytest.mark.parametrize("hour", (10, 27), ids=("<24hr", ">24hr"))
def test_F_nshs(hour: int) -> None:
    TEST_STR = f"{hour}:03;F-nshs;2U05"
    _result = railosparse_finish.parse_F_nshs(railos_ttb_str.split(TEST_STR))
    assert str(_result) == TEST_STR


@pytest.mark.ttb_parsing
@pytest.mark.parametrize("hour", (10, 27), ids=("<24hr", ">24hr"))
def test_pas(hour: int) -> None:
    TEST_STR = f"{hour}:03;pas;Great Malvern"
    _result = railosparse_act.parse_pas(railos_ttb_str.split(TEST_STR))
    assert str(_result) == TEST_STR


@pytest.mark.ttb_parsing
@pytest.mark.parametrize("hour", (10, 27), ids=("<24hr", ">24hr"))
def test_cdt(hour: int) -> None:
    TEST_STR = f"{hour}:03;cdt"
    _result = railosparse_act.parse_cdt(railos_ttb_str.split(TEST_STR))
    assert str(_result) == TEST_STR


@pytest.mark.ttb_parsing
@pytest.mark.parametrize("hour", (10, 27), ids=("<24hr", ">24hr"))
def test_fsp(hour: int) -> None:
    TEST_STR = f"{hour}:03;fsp;1K98"
    _result = railosparse_act.parse_fsp(railos_ttb_str.split(TEST_STR))
    assert str(_result) == TEST_STR


@pytest.mark.ttb_parsing
@pytest.mark.parametrize("hour", (10, 27), ids=("<24hr", ">24hr"))
def test_rsp(hour: int) -> None:
    TEST_STR = f"{hour}:03;rsp;1K98"
    _result = railosparse_act.parse_rsp(railos_ttb_str.split(TEST_STR))
    assert str(_result) == TEST_STR


@pytest.mark.ttb_parsing
@pytest.mark.parametrize("hour", (10, 27), ids=("<24hr", ">24hr"))
def test_location(hour: int) -> None:
    TEST_STR = f"{hour}:03;dsc;This is a new description"
    _result = railosparse_act.parse_dsc(railos_ttb_str.split(TEST_STR))
    assert str(_result) == TEST_STR


@pytest.mark.ttb_parsing
@pytest.mark.parametrize("hour", (10, 27), ids=("<24hr", ">24hr"))
def test_dsc(hour: int) -> None:
    TEST_STR = f"{hour}:11;{hour}:12;Longbridge"
    _result = railosparse_act.parse_location(railos_ttb_str.split(TEST_STR))
    assert str(_result) == TEST_STR
    TEST_STR = f"{hour}:11;Longbridge"
    _result = railosparse_act.parse_location(railos_ttb_str.split(TEST_STR))
    assert str(_result) == TEST_STR


@pytest.mark.ttb_parsing
@pytest.mark.parametrize(
    "file_name", ("Birmingham_0700_Start.ttb", "SouthWestMainLine.ttb")
)
def test_services_str(file_name: str) -> None:
    _parser = railos_parse.TTBParser()
    _parser.parse(os.path.join(TEST_DATA_DIR, file_name))
    _parser.services_str
