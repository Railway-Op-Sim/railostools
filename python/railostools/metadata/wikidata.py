import logging
import pathlib
import typing
from collections.abc import MutableMapping

try:
    import wikidspark.query
except ImportError:
    raise ImportError(
        "Wikidata functionality is unavailable, the [wikidata] optional extra must be installed."
    )

import glob
import json
import os.path
import time

import toml

import railostools.rly.parsing

logging.basicConfig()


class MetadataExpander:
    def __init__(self, project_dir: pathlib.Path) -> None:
        if not os.path.exists(project_dir):
            raise FileNotFoundError(f"Project directory '{project_dir}' does not exist")
        self._project_dir: pathlib.Path = project_dir
        self._logger = logging.getLogger("MetadataExpander")
        self._toml_file: pathlib.Path | None = (
            None  # pyright: ignore[reportAttributeAccessIssue]
        )
        self._metadata: MutableMapping[str, typing.Any] | None = None
        self._locations: list[str] | None = None

        self._metadata = self._unpack_project()

        self._crs_codes: dict[str, str] = self._extract_crs_codes()

        if self._metadata:
            self._metadata["identifiers"] = self._get_wikidata(
                self._metadata["country_code"]
            )

    def _unpack_project(self) -> dict[str, typing.Any]:
        _metadata_dir: str = os.path.join(self._project_dir, "Metadata")
        _railway_dir: str = os.path.join(self._project_dir, "Railway")
        if not os.path.exists(_metadata_dir):
            raise FileNotFoundError("No metadata directory found for current project")

        self._toml_file: str = glob.glob(os.path.join(_metadata_dir, "*.toml"))[0]

        _metadata = toml.load(self._toml_file)

        if not _metadata:
            raise AssertionError("No existing metadata found!")

        _rly_file: str = glob.glob(os.path.join(_railway_dir, "*.rly"))[0]

        self._logger.info(f"Using Railway File '{_rly_file}'")

        rly_data = railostools.rly.parsing.RlyParser()
        rly_data.parse(_rly_file)
        self._locations = list(rly_data.named_locations.keys())

        return _metadata

    def _extract_crs_codes(self) -> dict[str, typing.Any]:
        _crs_file: str = os.path.join(os.path.dirname(__file__), "tiploc.json")

        with open(_crs_file) as in_file:
            return json.load(in_file)["crs"]

    def _get_crs(self, search_str: str) -> str | None:
        return next(
            (crs for crs, loc in self._crs_codes.items() if loc == search_str.upper()),
            None,
        )

    def _get_wikidata(self, country_code: str) -> dict[str, typing.Any]:
        _wd_query = wikidspark.query.QueryBuilder()
        _wd_metadata: dict[str, typing.Any] = {}
        if country_code != "GB":
            raise ValueError(f"Country code '{country_code}' not yet supported")
        for location in self._locations or []:
            self._logger.info(f"Searching location '{location}' on WikiData")
            _wd_query._query._clear()
            if _crs := self._get_crs(location):
                time.sleep(1)
                _wd_query.property_equals("P4755", _crs)
                _id = _wd_query.get().dataframe.iloc[0]["id"]
                _wd_metadata[location] = _id
                self._logger.info(f"Retrieved result: ID={_id}")
        return _wd_metadata

    def append_metadata(self) -> None:
        if not self._toml_file:
            raise RuntimeError("No TOML file identified.")
        if not self._metadata:
            raise RuntimeError("No metadata in current project.")
        with self._toml_file.open("w") as out_f:
            _ = toml.dump(self._metadata, out_f)
