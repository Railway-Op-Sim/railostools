import pytest
import pytest_mock
import os.path

import railostools.session as railos_sesh
import railostools.common.enumeration as railos_enum
import railostools.exceptions as railos_exc

SESSION_FILE = os.path.join(os.path.dirname(__file__), "data", "session.ini")

@pytest.mark.session
def test_session_no_ros() -> None:
    with pytest.raises(ros_exc.ProgramNotFoundError):
       railos_sesh.Session(os.path.dirname(SESSION_FILE))


@pytest.mark.session
def test_session_pass(mocker: pytest_mock.MockerFixture) -> None:
    mocker.patch("os.path.exists", lambda *args: True)
    _session = railos_sesh.Session(os.path.dirname(SESSION_FILE))
    _session.read()

    assert _session.railway == "Birmingham"
    assert _session.timetable == "Birmingham 0700 Start"
    assert _session.main_mode == railos_enum.Level1Mode(3)
    assert _session.operation_mode == railos_enum.Level2OperMode(3)
    assert _session.performance_file.split("\\")[-1] == "Log 23-03-2022 18.46.06; Birmingham; Birmingham 0700 Start.txt"

