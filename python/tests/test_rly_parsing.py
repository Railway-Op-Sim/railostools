import pytest
import json
import os
import tempfile

from rostools.rly import RlyParser

RLY_FILE = os.path.join(os.path.dirname(__file__), 'test_data', 'Antwerpen_Centraal.rly')


@pytest.fixture
def rly_parser():
    _rly_parser = RlyParser()
    _rly_parser.parse(RLY_FILE)
    return _rly_parser


@pytest.mark.rlyparser
def test_parse_time(rly_parser: RlyParser):
    assert rly_parser.program_version == 'v2.9.2'


@pytest.mark.rlyparser
def test_parse_time(rly_parser: RlyParser):
    assert rly_parser.n_active_elements == 1274


@pytest.mark.rlyparser
def test_parse_time(rly_parser: RlyParser):
    assert rly_parser.n_inactive_elements == 200


@pytest.mark.ttbparser
def test_write(rly_parser: RlyParser):
    with tempfile.NamedTemporaryFile(suffix='.json', mode='w', delete=False) as out_f:
        rly_parser.json(out_f)
        assert json.load(open(out_f.name))

