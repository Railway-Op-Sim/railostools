import os.path

import pytest
import railostools.ttb.parsing as ros_parse
import railostools.ttb.parsing.actions as rosparse_act
import railostools.ttb.parsing.finish as rosparse_finish
import railostools.ttb.parsing.start as rosparse_start
import railostools.ttb.string as ros_ttb_str

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


@pytest.mark.ttb_parsing
def test_snt_parse() -> None:
    TEST_STR = "10:23;Snt;1-34 1-35"
    rosparse_start.parse_Snt(ros_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_sfs_parse() -> None:
    TEST_STR = "10:23;Sfs;1U03"
    rosparse_start.parse_Sfs(ros_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_Sns_fsh() -> None:
    TEST_STR = "10:23;Sns-fsh;1U04"
    rosparse_start.parse_Sns_fsh(ros_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_Snt_sh() -> None:
    TEST_STR = "10:23;Snt-sh;1-45 1-46;1U04"
    rosparse_start.parse_Snt_sh(ros_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_Sns_sh() -> None:
    TEST_STR = "10:23;Sns-sh;1U02;1U04"
    rosparse_start.parse_Sns_sh(ros_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_Fns() -> None:
    TEST_STR = "10:23;Fns;1U03"
    rosparse_finish.parse_Fns(ros_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_Fer() -> None:
    TEST_STR = "10:23;Fer;1-94"
    rosparse_finish.parse_Fer(ros_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_Frh() -> None:
    TEST_STR = "Frh"
    rosparse_finish.parse_Frh(ros_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_Fjo() -> None:
    TEST_STR = "10:03;Fjo;1U05"
    rosparse_finish.parse_Fjo(ros_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_Frh_sh() -> None:
    TEST_STR = "10:03;Frh-sh;2U05"
    rosparse_finish.parse_Frh_sh(ros_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_Fns_sh() -> None:
    TEST_STR = "10:03;Frh-sh;2U05;1Z09"
    rosparse_finish.parse_Fns_sh(ros_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_F_nshs() -> None:
    TEST_STR = "10:03;F-nshs;2U05"
    rosparse_finish.parse_F_nshs(ros_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_pas() -> None:
    TEST_STR = "10:03;pas;Great Malvern"
    rosparse_act.parse_pas(ros_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_cdt() -> None:
    TEST_STR = "10:03;cdt"
    rosparse_act.parse_cdt(ros_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_fsp() -> None:
    TEST_STR = "10:03;fsp;1K98"
    rosparse_act.parse_fsp(ros_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_rsp() -> None:
    TEST_STR = "10:03;rsp;1K98"
    rosparse_act.parse_fsp(ros_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_location() -> None:
    TEST_STR = "10:11;10:12;Longbridge"
    rosparse_act.parse_location(ros_ttb_str.split(TEST_STR))
    TEST_STR = "10:11;Longbridge"
    rosparse_act.parse_location(ros_ttb_str.split(TEST_STR))


@pytest.mark.ttb_parsing
def test_services_str() -> None:
   _parser = ros_parse.TTBParser()
   _parser.parse(os.path.join(TEST_DATA_DIR, "Birmingham_0700_Start.ttb"))
   _parser.services_str
