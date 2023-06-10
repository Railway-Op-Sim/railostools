import pytest
import tempfile
import os.path

import railostools.ttb.builder as railos_ttb_build
import railostools.ttb.parsing as railos_ttb_parse

@pytest.mark.ttb_build
def test_build_service() -> None:
    _builder = railos_ttb_build.TimetableBuilder()
    _builder.start = "10:00"
    with pytest.raises(AssertionError):
        _builder.add_service("1N03", "Walsall to Bescot Stadium", "11:00")

    _builder.add_service("1N03", "Walsall to Bescot Stadium", "11:00", front_element_id="56-11", rear_element_id="57-11")
    _builder.finish_exit_railway("1N03", ["34-N1"], "12:32")

    with tempfile.TemporaryDirectory() as tempd:
        _file_name: str = os.path.join(tempd, "temp.ttb")
        with open(_file_name, "w") as out_f:
            out_f.write(_builder.timetable.__str__())
        railos_ttb_parse.TTBParser().parse(_file_name)
