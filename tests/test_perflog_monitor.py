import os.path
import asyncio
import tempfile
import shutil

import pytest
import logging

from rostools.performance import Monitor

TEST_LOG_DIR = os.path.join(
    os.path.dirname(__file__),
    'test_data'
)

logging.getLogger().setLevel(logging.DEBUG)


async def add_file(temporary_dir: str, **kwargs):
    await asyncio.sleep(1)
    shutil.copy(
        os.path.join(
            TEST_LOG_DIR,
            'Log_Antwerpen_Centraal.txt'
        ),
        os.path.join(
            temporary_dir,
            'Log_Antwerpen_Centraal.txt'
        )
    )


async def checker(monitor: Monitor):
    while monitor.running and not monitor.data:
        await asyncio.sleep(1)
    assert monitor.data
    monitor.stop()


@pytest.mark.perflog
def test_performance_monitor():
    with tempfile.TemporaryDirectory() as temp_dir:
        m = Monitor(temp_dir)
        assert not m.data
        m.exec_in_parallel(checker)
        m.exec_in_parallel(add_file, {'temporary_dir': temp_dir})
        m.run()
