import typing
import logging

try:
    import wikidspark.query
except ImportError:
    raise ImportError(
        "Wikidata functionality is unavailable, the [wikidata] optional extra must be installed."
    )

import railostools.rly.parsing
import json
import os.path
import toml
import glob
import time

logging.basicConfig()


class MetadataExpander:
    def __init__(self, project_dir: str) -> None:
        if not os.path.exists(project_dir):
            raise FileNotFoundError(f"Project directory '{project_dir}' does not exist")
        self._project_dir: str = project_dir
        self._logger = logging.getLogger("MetadataExpander")
        self._toml_file: typing.Optional[str] = None
        self._metadata: typing.Optional[typing.MutableMapping] = None
        self._locations: typing.Optional[typing.List[str]] = None

        self._unpack_project()

        self._crs_codes: typing.Dict[str, str] = self._extract_crs_codes()

        self._get_wikidata(self._metadata["country_code"])

    def _unpack_project(self) -> bool:
        _metadata_dir: str = os.path.join(self._project_dir, "Metadata")
        _railway_dir: str = os.path.join(self._project_dir, "Railway")
        if not os.path.exists(_metadata_dir):
            raise FileNotFoundError("No metadata directory found for current project")

        self._toml_file: str = glob.glob(os.path.join(_metadata_dir, "*.toml"))[0]

        self._metadata = toml.load(self._toml_file)

        if not self._metadata:
            raise AssertionError("No existing metadata found!")

        _rly_file: str = glob.glob(os.path.join(_railway_dir, "*.rly"))[0]

        self._logger.info(f"Using Railway File '{_rly_file}'")

        rly_data = railostools.rly.parsing.RlyParser()
        rly_data.parse(_rly_file)
        self._locations = list(rly_data.named_locations.keys())

    def _extract_crs_codes(self) -> None:
        _crs_file: str = os.path.join(os.path.dirname(__file__), "tiploc.json")

        with open(_crs_file) as in_file:
            return json.load(in_file)["crs"]

    def _get_crs(self, search_str: str) -> typing.Optional[str]:
        return next(
            (crs for crs, loc in self._crs_codes.items() if loc == search_str.upper()),
            None,
        )

    def _get_wikidata(self, country_code: str) -> typing.Dict:
        _wd_query = wikidspark.query.QueryBuilder()
        _wd_metadata = {}
        if country_code != "GB":
            raise ValueError(f"Country code '{country_code}' not yet supported")
        for location in self._locations:
            self._logger.info(f"Searching location '{location}' on WikiData")
            _wd_query._query._clear()
            if _crs := self._get_crs(location):
                time.sleep(1)
                _wd_query.property_equals("P4755", _crs)
                _id = _wd_query.get().dataframe.iloc[0]["id"]
                _wd_metadata[location] = _id
                self._logger.info(f"Retrieved result: ID={_id}")
        self._metadata["identifiers"] = _wd_metadata

    def append_metadata(self) -> None:
        with open(self._toml_file, "w") as out_f:
            toml.dump(self._metadata, out_f)
