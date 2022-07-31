import datetime
import typing
import bs4
import pandas
import requests
import tempfile
import re
import dataclasses
import railostools.rly as railos_rly
import railostools.ttb.components as railos_ttb_comp


@dataclasses.dataclass
class OTTService:
    headcode: str
    start_time: datetime.time
    service: pandas.DataFrame
    description: str
    train_type: typing.Optional[str] = None
    


def _clean_locations(data_frame: pandas.DataFrame) -> pandas.DataFrame:
    _locations: typing.List[str] = []
    _platforms: typing.List[str] = []
    for location in data_frame["Location"]:
        if "Platform" in location:
            _place, _platform = location.split("Platform")
            _platform_search = re.findall(r"(\d+)", _platform)
            _platform = _platform_search[0] or ""
            _locations.append(_place)
            _platforms.append(_platform)
        else:
            _locations.append(location)
            _platforms.append("")
    _out_frame = data_frame.assign(Location=_locations)
    _out_frame["Plat"] = _platforms
    return _out_frame


def _remove_abbreviations(data_frame: pandas.DataFrame) -> pandas.DataFrame:
    _locations: typing.List[str] = []

    _abbreviations: typing.Dict[str, str] = {
        "Jn.": "Junction",
        "Jn": "Junction",
    }

    for location in data_frame["Location"]:
        _new_loc: str = location
        for key, value in _abbreviations.items():
            _new_loc = _new_loc.replace(key, value)
        _locations.append(_new_loc)

    _out_frame = data_frame.assign(Location=_locations)

    return _out_frame


def _parse_times(data_frame: pandas.DataFrame, column_name: str, add_pass: bool = False) -> pandas.DataFrame:
    _new_col_1: typing.List[str] = []
    _new_col_2: typing.List[str] = []

    if add_pass:
        _pass_col: typing.List[bool] = []

    for time in data_frame[column_name]:
        try:
            _arr_times = re.findall(r"a\s*(\d{4})", time)
            _dep_times = re.findall(r"d\s*(\d{4})", time)
            _pass_times = re.findall(r"p\s*(\d{4})", time)
        except TypeError:
            _arr_times = []
            _dep_times = []
            _pass_times = []
        if add_pass:
            _pass_col.append(_pass_times[0] if _pass_times else "")
        _new_col_1.append(_arr_times[0] if _arr_times else "")
        _new_col_2.append(_dep_times[0] if _dep_times else "")
    _out_frame = data_frame.copy()
    del _out_frame[column_name]
    if add_pass:
        _out_frame["Pass"] = _pass_col
    _out_frame[f"{column_name} Arrival"] = _new_col_1
    _out_frame[f"{column_name} Departure"] = _new_col_2
    return _out_frame



def scrape(url: str) -> None:
    _data: str = requests.get(url).content
    _scraped = bs4.BeautifulSoup(_data, "html.parser")
    _schedule = _scraped.find(id="schedule")
    _ttype_search: str = re.findall(r"(Class\s\d+)", _scraped.text)
    _ttype: str = "" if not _ttype_search else _ttype_search[0]
    _title: str = _scraped.find("h1").string
    _time: str = re.findall(r"\d{4}", _title)[0]
    _id: str = _title.split()[0]
    _title: str = _title.replace(_id, "").replace(_time, "").strip()
    with tempfile.NamedTemporaryFile(suffix=".html") as tempf:
        with open(tempf.name, "w") as outf:
            outf.write(str(_schedule))
        _data_frames: typing.List[pandas.DataFrame]= pandas.read_html(tempf.name)
    _data_frame = _data_frames[0]
    del _data_frame["Path"]
    del _data_frame["Line"]
    _data_frame = _clean_locations(_data_frame)
    _data_frame = _remove_abbreviations(_data_frame)
    _data_frame = _parse_times(_data_frame, "GBTT")
    _data_frame = _parse_times(_data_frame, "WTT", True)
    _data_frame = _parse_times(_data_frame, "Actual")
    
    return OTTService(
        headcode=_id,
        start_time=datetime.datetime.strptime(_time, "%H%M").time(),
        service=_data_frame,
        description=_title,
        train_type=_ttype or None
    )


def build_timetable(start_time: str, urls: typing.List[str], railway_file: str) -> None:
    _parser = railos_rly.RlyParser()
    _parser.parse(railway_file)
    _locations: typing.Set[str] = _parser.named_locations

    _start: datetime.datetime = datetime.datetime.strptime(start_time, "%H:%M")

    _ott_services: typing.List[OTTService] = [scrape(i) for i in urls]


if __name__ in "__main__":
    print(scrape("https://www.opentraintimes.com/schedule/F42412/2022-07-27").service)