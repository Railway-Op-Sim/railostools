import os.path
import pytest

import railostools.metadata as ros_meta

TEST_METADATA = os.path.join(os.path.dirname(__file__), "data", "Antwerpen_Centraal.toml")

@pytest.mark.metadata
def test_check_file() -> None:
    ros_meta.validate(TEST_METADATA)
