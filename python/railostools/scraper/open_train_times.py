import datetime
import json
import typing
import bs4
import pandas
import requests
import tempfile
import tqdm
import time
import re
import os.path
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
    previous: typing.Optional[str] = None
    next: typing.Optional[str] = None
    


def _clean_locations(data_frame: pandas.DataFrame) -> pandas.DataFrame:
    _locations: typing.List[str] = []
    _platforms: typing.List[str] = []
    for location in data_frame["Location"]:
        if "Platform " in location:
            _place, _platform = location.split("Platform ")
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


def _link_services(services: typing.Dict[str, OTTService]) -> None:
    _starts: typing.Dict[str, str] = {}
    _stops: typing.Dict[str, str] = {}
    for headcode, service in services.items():
        _final_loc: str = f'{service.service["Location"].iloc[-1]}:{service.service["Plat"].iloc[-1]}:{service.service["WTT Arrival"].iloc[-1]}'
        _stops[_final_loc] = headcode
        _start_loc: str = f'{service.service["Location"].iloc[0]}:{service.service["Plat"].iloc[0]}:{service.service["WTT Departure"].iloc[0]}'
        _starts[_start_loc] = headcode
    for start, headcode in _starts.items():
        if start in _stops:
            services[headcode].previous = _stops[start]
            services[_stops[start]].next = headcode


def build_timetable(start_time: str, urls: typing.List[str], railway_file: str) -> None:
    #_parser = railos_rly.RlyParser()
    #_parser.parse(railway_file)
    #_locations: typing.Set[str] = _parser.named_locations

    _start: datetime.datetime = datetime.datetime.strptime(start_time, "%H:%M")

    _ott_services: typing.Dict[str, OTTService] = {}

    for url in urls:
        _service: OTTService = scrape(url)
        _ott_services[_service.headcode] = _service

    _link_services(_ott_services)


def get_station_listings(crs_code: str, date: datetime.datetime) -> typing.List[OTTService]:
    with open(os.path.join(os.path.dirname(__file__), "tiploc.json")) as in_f:
        _json_dat: typing.Dict[str, typing.Dict[str, str]] = json.load(in_f)

    _station: str = _json_dat["crs"][crs_code]

    _search_str: str = date.strftime("%Y-%m-%d/%H:%M")

    _url: str = f"https://www.opentraintimes.com/location/{crs_code}/{_search_str}"

    _listing = requests.get(_url)

    _schedule_search: typing.List[str] = re.findall(r'href="(/schedule\/.+\/\d{4}-\d{2}-\d{2})"', _listing.text)

    if not _schedule_search:
        raise AssertionError(f"No results found using '{_url}'.")

    _besoup = bs4.BeautifulSoup(_listing.content, "html.parser")

    _listing = _besoup.find(id="schedules")

    # with tempfile.NamedTemporaryFile(suffix=".html") as tfile:
    #     with open(tfile.name, "w") as ofile:
    #         ofile.write(str(_listing))
    #     _data_frame: pandas.DataFrame = pandas.read_html(tfile.name)
    
    _results: typing.List[str, OTTService] = {}

    print("Retrieving schedules, retrieval will pause 10s between entries so as to not bombard server")
    for sched in tqdm.tqdm(_schedule_search[:5]):
        _url: str = f"https://www.opentraintimes.com{sched}"
        print(f"Retrieving from {_url}")
        _service: OTTService = scrape(_url)
        _results[_service.headcode] = _service
        time.sleep(10)

    return _results

    

if __name__ in "__main__":
    import pickle
    _services_8_10 = get_station_listings("RMD", datetime.datetime.strptime("08:00 2022-07-29", "%H:%M %Y-%m-%d"))
    _services_8_10.update(get_station_listings("RMD", datetime.datetime.strptime("09:00 2022-07-29", "%H:%M %Y-%m-%d")))
    _services_8_10.update(get_station_listings("RMD", datetime.datetime.strptime("10:00 2022-07-29", "%H:%M %Y-%m-%d")))
    _link_services(_services_8_10)
    with open("demo_file.pckl", "wb") as outf:
        pickle.dump(_services_8_10, outf)

