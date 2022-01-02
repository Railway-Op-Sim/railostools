import pytest
import json
import os
import tempfile

from rostools.ttb import TTBParser

TEST_TTB_FILE = os.path.join(os.path.dirname(__file__), 'test_data', 'Enoshima_Week_2021.ttb')


@pytest.fixture
def ttb_parser():
    _ttb_parser = TTBParser()
    _ttb_parser.parse(TEST_TTB_FILE)
    return _ttb_parser


@pytest.mark.ttbparser
def test_parse_time(ttb_parser: TTBParser):
    assert ttb_parser.start_time == '05:07'


@pytest.mark.ttbparser
def test_comments(ttb_parser: TTBParser):
    _expect = ['Empty Stock', 'Towards Kamakura', 'Towards Fujisawa']
    assert list(ttb_parser.comments.values()) == _expect


@pytest.mark.ttbparser
def test_write(ttb_parser: TTBParser):
    with tempfile.NamedTemporaryFile(suffix='.json', mode='w', delete=False) as out_f:
        ttb_parser.json(out_f)
        assert json.load(open(out_f.name))
