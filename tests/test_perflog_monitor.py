import os.path

import pytest

from rostools.performance import Monitor

TEST_LOG_DIR = os.path.join(
    os.path.dirname(__file__),
    'test_data'
)


@pytest.mark.perflog
def test_performance_monitor():
    Monitor(TEST_LOG_DIR, 5).run()
