import datetime
import json
import os
import typing

import pycountry
import pydantic
import railostools.exceptions as ros_exc
import semver
import toml


class Metadata(pydantic.BaseModel):
    name: str = pydantic.Field(..., description="title of the simulation project")
    rly_file: str = pydantic.Field(
        ..., description=".rly filename of the simulation itself"
    )
    ttb_files: typing.List[str] = pydantic.Field(
        ..., description="list of timetable .ttb. files"
    )
    doc_files: typing.List[str] = pydantic.Field(
        ..., description="list of documentation files (.pdf, .md, .txt)"
    )
    country_code: str = pydantic.Field(
        ..., description="if factual simulation alpha-2 country code, else FN"
    )
    year: int = pydantic.Field(
        None, description="year simulation takes place if applicable"
    )
    factual: bool = pydantic.Field(
        ..., description="is the simulation based on a real or fictional network"
    )
    author: str = pydantic.Field(
        ..., description="leading developer/author (must match RailOS site author name)"
    )
    version: str = pydantic.Field(
        ..., description="semantic version of the form MAJOR.MINOR.PATCH"
    )
    release_date: str = pydantic.Field(
        ..., description="release date in the form YYYY-MM-DD"
    )
    display_name: typing.Optional[str] = pydantic.Field(
        None,
        description="alternative name (name that would be used for display purposes)",
    )
    description: typing.Optional[str] = pydantic.Field(
        None, description="a brief line summary of the project"
    )
    ssn_files: typing.Optional[typing.List[str]] = pydantic.Field(
        None, description="list of session .ssn files"
    )
    img_files: typing.Optional[typing.List[str]] = pydantic.Field(
        None, description="list of image files"
    )
    graphic_files: typing.Optional[typing.List[str]] = pydantic.Field(
        None, description="list of graphic files"
    )
    difficulty: int = pydantic.Field(
        None, description="estimate of the simulation difficulty"
    )
    contributors: typing.Optional[typing.List[str]] = pydantic.Field(
        None,
        description="other contributing authors as list (must match RailOS site author names)",
    )
    minimum_required: str = pydantic.Field(
        None, description="minimum required RailOS version"
    )

    @pydantic.validator("year")
    def validate_year(cls, year) -> typing.Optional[int]:
        if not year:
            return year
        if year < 1700:
            raise ros_exc.MetadataError("Expected year value to be > 1700")

    @pydantic.validator("difficulty")
    def validate_difficulty(cls, difficulty) -> typing.Optional[int]:
        if not difficulty:
            return difficulty
        if difficulty < 1 or difficulty > 5:
            raise ros_exc.MetadataError("Difficulty must be in range [1, 5]")
        return difficulty

    @pydantic.validator("country_code")
    def validate_country_code(cls, country_code) -> str:
        country_code = country_code.upper()
        _alpha_2 = [i.alpha_2 for i in pycountry.countries]
        if country_code == "FN" or country_code in _alpha_2:
            return country_code
        raise ros_exc.MetadataError(f"Invalid country code '{country_code}'")

    @pydantic.validator("release_date")
    def validate_release_date(cls, release_date: str) -> datetime.date:
        try:
            return datetime.datetime.strptime(release_date, "%Y-%m-%d")
        except ValueError as e:
            raise ros_exc.MetadataError(
                "Expected 'release_date' in the form 'YYYY-MM-DD'"
            ) from e

    @pydantic.validator("version", "minimum_required", check_fields=False)
    def validate_version(cls, version: str) -> str:
        try:
            semver.VersionInfo.parse(version)
        except ValueError as e:
            raise ros_exc.MetadataError(f"Invalid semantic version '{version}'") from e
        return version

    def __str__(self) -> str:
        return json.dumps(self.__dict__, indent=2)

    def write(self, outfile_name: str) -> None:
        """Write to output file"""
        if os.path.splitext(outfile_name) != ".toml":
            raise ros_exc.IOError(
                "Invalid filename for metadata file, expected TOML file"
            )
        toml.dump(self.__dict__, open(outfile_name, "w"))

    class Config:
        extra = "forbid"


def validate(input_file: str) -> None:
    Metadata(**toml.load(input_file))
