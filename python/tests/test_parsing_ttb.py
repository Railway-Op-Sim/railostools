import pytest

import railostools.ttb.parsing.start as rosparse_start
import railostools.ttb.string as ros_ttb_str

@pytest.mark.ttb_parsing
def test_snt_parse() -> None:
    TEST_STR = "10:23;Snt;1-34 1-35"
    rosparse_start.parse_Snt(ros_ttb_str.split(TEST_STR))

@pytest.mark.ttb_parsing
def test_sfs_parse() -> None:
    TEST_STR = "10:23;Sfs;1U03"
    rosparse_start.parse_Sfs(ros_ttb_str.split(TEST_STR))
