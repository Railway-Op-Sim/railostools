import pytest
import os.path

import railostools.performance as railos_perf

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

@pytest.mark.perflog
def test_parse_log() -> None:
    _log_file: str = os.path.join(TEST_DATA_DIR, "Birmingham_Performance.log")
    _parser = railos_perf.PerformanceLogParser()
    _parser.parse(_log_file)

    assert _parser.score == 75
    assert _parser.rating == "Fair"
