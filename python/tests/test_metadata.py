import os.path
import pytest

import railostools.metadata.validation as railos_meta_valid

TEST_METADATA = os.path.join(
    os.path.dirname(__file__), "data", "Antwerpen_Centraal.toml"
)
TEST_PROJECT = os.path.join(os.path.dirname(__file__), "data", "GB-Glasgow-Suburban")


@pytest.mark.metadata
def test_check_file() -> None:
    railos_meta_valid.validate(TEST_METADATA)


@pytest.mark.metadata
def test_extra_metadata() -> None:
    try:
        import railostools.metadata.wikidata as railos_meta_wiki
    except ImportError:
        pytest.skip("Missing extra dependencies")
    railos_meta_wiki.MetadataExpander(TEST_PROJECT)
