import pytest
import json
import os
import tempfile

from railostools.rly.parsing import RlyParser

RLY_FILE = os.path.join(os.path.dirname(__file__), "data", "Antwerpen_Centraal.rly")


@pytest.fixture
def rly_parser():
    _rly_parser = RlyParser()
    _rly_parser.parse(RLY_FILE)
    return _rly_parser


@pytest.mark.rly_parsing
def test_parse_result(rly_parser: RlyParser):
    assert rly_parser.program_version == "v2.9.2"
    assert rly_parser.n_active_elements == 1274
    assert rly_parser.n_inactive_elements == 200

@pytest.mark.rly_parsing
def test_write(rly_parser: RlyParser):
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as out_f:
        rly_parser.dump(out_f)
        assert json.load(open(out_f.name))


@pytest.mark.rly_parsing
def test_found_neighbours(rly_parser: RlyParser):
    assert sorted(rly_parser.get_element_connected_neighbours((-28, 28))) == sorted(
        [(-28, 27), (-29, 28), (-28, 29)]
    )


@pytest.mark.rly_parsing
def test_plot_nodes(rly_parser: RlyParser):
    with tempfile.TemporaryDirectory() as temp_d:
        graph_file_name: str = os.path.join(temp_d, "temporary_graph.pdf")
        rly_parser.plot(graph_file_name)
        assert os.path.exists(graph_file_name)
