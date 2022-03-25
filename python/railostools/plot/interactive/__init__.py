import json
import typing
import bokeh
import bokeh.resources
import os.path
import glob

import railostools.ttb.parsing as ros_ttb_parse
import railostools.ttb.components as ros_comp
import railostools.exceptions as ros_exc


class Browser:
    def __init__(self, ros_location: str) -> None:
        if not os.path.isdir(ros_location):
            raise ros_exc.ProgramNotFoundError(ros_location)
        self._ttb = self._parse_files(ros_location)

    def _sanitize_filename(self, file_name: str) -> str:
        """Convert filename to a code friendly string"""
        for symbol in (" ", ";", "-"):
            file_name = file_name.replace(symbol, "_")
        return file_name.lower()

    def _get_timetables(self, ros_location: str) -> typing.List[str]:
        return glob.glob(os.path.join(
            ros_location,
            "Program timetables",
            "*.ttb"
        ))

    def _parse_files(self, ros_location: str) -> typing.Dict[str, ros_comp.Timetable]:
        """Parse all timetable files into metadata dictionaries"""
        _ttb_definitions: typing.Dict[str, ros_comp.Timetable] = {}
        _parser = ros_ttb_parse.TTBParser()
        for file in self._get_timetables(ros_location):
            try:
                _parser.parse(file)
            except ros_exc.ParsingError:
                continue
            _ttb_definitions[self._sanitize_filename(file)] = _parser.data
        return _ttb_definitions


if __name__ in "__main__":
    import railostools.plot.interactive.templates as rosplot_temp
    x = Browser("C:/Program Files/RailwayOperationSimulator/Railway")
    with open("test.html", "w") as out_f:
        out_f.write(
            rosplot_temp.load_html_template("browser").render(
                bokeh_headers=bokeh.resources.CDN
            )
        )