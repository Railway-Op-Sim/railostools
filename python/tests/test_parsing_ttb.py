import os.path

import pytest
import railostools.ttb.parsing as railos_parse
import railostools.ttb.parsing.actions as railosparse_act
import railostools.ttb.parsing.finish as railosparse_finish
import railostools.ttb.parsing.start as railosparse_start
import railostools.ttb.string as railos_ttb_str

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


@pytest.mark.ttb_parsing
def test_snt_parse() -> None:
    TEST_STR = "10:23;Snt;1-34 1-35"
    railosparse_start.parse_Snt(railos_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_sfs_parse() -> None:
    TEST_STR = "10:23;Sfs;1U03"
    railosparse_start.parse_Sfs(railos_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_Sns_fsh() -> None:
    TEST_STR = "10:23;Sns-fsh;1U04"
    railosparse_start.parse_Sns_fsh(railos_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_Snt_sh() -> None:
    TEST_STR = "10:23;Snt-sh;1-45 1-46;1U04"
    railosparse_start.parse_Snt_sh(railos_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_Sns_sh() -> None:
    TEST_STR = "10:23;Sns-sh;1U02;1U04"
    railosparse_start.parse_Sns_sh(railos_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_Fns() -> None:
    TEST_STR = "10:23;Fns;1U03"
    railosparse_finish.parse_Fns(railos_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_Fer() -> None:
    TEST_STR = "10:23;Fer;1-94"
    railosparse_finish.parse_Fer(railos_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_Frh() -> None:
    TEST_STR = "Frh"
    railosparse_finish.parse_Frh(railos_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_Fjo() -> None:
    TEST_STR = "10:03;Fjo;1U05"
    railosparse_finish.parse_Fjo(railos_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_Frh_sh() -> None:
    TEST_STR = "10:03;Frh-sh;2U05"
    railosparse_finish.parse_Frh_sh(railos_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_Fns_sh() -> None:
    TEST_STR = "10:03;Frh-sh;2U05;1Z09"
    railosparse_finish.parse_Fns_sh(railos_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_F_nshs() -> None:
    TEST_STR = "10:03;F-nshs;2U05"
    railosparse_finish.parse_F_nshs(railos_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_pas() -> None:
    TEST_STR = "10:03;pas;Great Malvern"
    railosparse_act.parse_pas(railos_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_cdt() -> None:
    TEST_STR = "10:03;cdt"
    railosparse_act.parse_cdt(railos_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_fsp() -> None:
    TEST_STR = "10:03;fsp;1K98"
    railosparse_act.parse_fsp(railos_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_rsp() -> None:
    TEST_STR = "10:03;rsp;1K98"
    railosparse_act.parse_fsp(railos_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_location() -> None:
    TEST_STR = "10:11;10:12;Longbridge"
    railosparse_act.parse_location(railos_ttb_str.split(TEST_STR))
    TEST_STR = "10:11;Longbridge"
    railosparse_act.parse_location(railos_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_services_str() -> None:
    _parser = railos_parse.TTBParser()
    _parser.parse(os.path.join(TEST_DATA_DIR, "Birmingham_0700_Start.ttb"))
    _parser.services_str
