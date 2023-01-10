import os.path
import pytest

import railostools.metadata.validation as ros_meta_valid
import railostools.metadata.wikidata as ros_meta_wiki

TEST_METADATA = os.path.join(os.path.dirname(__file__), "data", "Antwerpen_Centraal.toml")
TEST_PROJECT = os.path.join(os.path.dirname(__file__), "data", "GB-Glasgow-Suburban")

@pytest.mark.metadata
def test_check_file() -> None:
   railos_meta_valid.validate(TEST_METADATA)

@pytest.mark.metadata
def test_extra_metadata() -> None:
   railos_meta_wiki.MetadataExpander(TEST_PROJECT)
