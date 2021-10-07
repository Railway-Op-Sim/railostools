import pytest
import os
import toml

from rostools.metadata import Route

TEST_DATA_DIR = os.path.join(
    os.path.dirname(__file__),
    'test_data'
)


@pytest.mark.validation
def test_metadata_validation():
    _test_file = os.path.join(TEST_DATA_DIR, 'Antwerpen_Centraal.toml')
    Route(**toml.load(_test_file))
