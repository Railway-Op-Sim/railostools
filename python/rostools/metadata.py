import typing
import os.path

import pydantic
import pycountry
import semver
import datetime


class Route(pydantic.BaseModel):
    name: str = pydantic.Field(
        ...,
        title="Project Name",
        description="Name of project for file system"
    )
    display_name: str = pydantic.Field(
        None,
        title="Display Name",
        description="Name of project as it would appear in listing"
    )
    description: str = pydantic.Field(
        None,
        title="Description",
        description="Single line summary of project"
    )
    rly_file: str = pydantic.Field(
        ...,
        title="Railway File",
        description="Railway map definition file name, .rly"
    )
    ttb_files: typing.List[str] = pydantic.Field(
        ...,
        title="Timetable Files",
        description="List of timetable files, .ttb"
    )
    ssn_files: typing.List[str] = pydantic.Field(
        None,
        title="Session Files",
        description="List of session files, .ssn"
    )
    img_files: typing.List[str] = pydantic.Field(
        None,
        title="Image Files",
        description="List of image files, .png"
    )
    doc_files: typing.List[str] = pydantic.Field(
        ...,
        title="Documentation Files",
        description="List of documenation files, .txt, .pdf, .md"
    )
    country_code: str = pydantic.Field(
        ...,
        title="Country Code",
        description="Two character country ISO code"
    )
    year: int = pydantic.Field(
        None,
        title="Year",
        description="Year simulation takes place"
    )
    factual: bool = pydantic.Field(
        ...,
        title="isFactual",
        description="Whether simulation is a factual representation"
    )
    difficulty: int = pydantic.Field(
        None,
        title="Difficulty Rating",
        description="Rating out of 5 for simulation difficulty"
    )
    author: str = pydantic.Field(
        ...,
        title="Author",
        description="Main author of the project"
    )
    contributors: typing.List[str] = pydantic.Field(
        None,
        title="Contributor List",
        description="Additional contributors to the project"
    )
    release_date: datetime.date = pydantic.Field(
        ...,
        title="Release Date",
        description="Date of release"
    )
    version: str = pydantic.Field(
        ...,
        title="Version",
        description="Semantic version of the project release"
    )

    @pydantic.validator('country_code')
    def check_country_code(cls, value):
        _country_codes = [country.alpha_2 for country in pycountry.countries]
        _country_codes += ['UN']
        if value not in _country_codes:
            raise AssertionError(f"'{value}' is not a recognised country code")
        return value

    @pydantic.validator('version')
    def check_semver(cls, version):
        semver.VersionInfo.parse(version)

    @pydantic.validator('rly_file')
    def check_rly_file(cls, rly_file):
        if any(i in rly_file for i in ['/', '\\']):
            raise AssertionError("RLY file cannot be a path")
        if not os.path.splitext(rly_file)[1].lower() == ".rly":
            raise AssertionError("RLY file must have suffix '.rly'")

    @pydantic.validator('ttb_files')
    def check_ttb_files(cls, ttb_files):
        for ttb_file in ttb_files:
            if any(i in ttb_file for i in ['/', '\\']):
                raise AssertionError("TTB file cannot be a path")
            if not os.path.splitext(ttb_file)[1].lower() == ".ttb":
                raise AssertionError("TTB file must have suffix '.ttb'")

    @pydantic.validator('ssn_files')
    def check_ssn_files(cls, ssn_files):
        if not ssn_files:
            return
        for ssn_file in ssn_files:
            if any(i in ssn_file for i in ['/', '\\']):
                raise AssertionError("SSN file cannot be a path")
            if not os.path.splitext(ssn_file)[1].lower() == ".ssn":
                raise AssertionError("SSN file must have suffix '.ssn'")

    @pydantic.validator('doc_files')
    def check_doc_files(cls, doc_files):
        for doc_file in doc_files:
            if any(i in doc_file for i in ['/', '\\']):
                raise AssertionError("DOC file cannot be a path")
            if os.path.splitext(doc_file)[1].lower() not in (".pdf", ".md", ".txt"):
                raise AssertionError("DOC file must have suffix '.txt', '.pdf' or '.md'")

    @pydantic.validator('img_files')
    def check_img_files(cls, img_files):
        if not img_files:
            return
        for img_file in img_files:
            if any(i in img_file for i in ['/', '\\']):
                raise AssertionError("IMG file cannot be a path")
            if os.path.splitext(img_file)[1].lower() not in (".bmp", ".png"):
                raise AssertionError("DOC file must have suffix '.bmp', '.png'")

    @pydantic.validator('year')
    def positive_year(cls, year):
        if year <= 0:
            raise AssertionError("Year must be a positive integer")
        return year

    @pydantic.validator('difficulty')
    def check_difficulty(cls, value):
        if 0 >= value > 5:
            raise AssertionError(f"Difficulty '{value}' does not satisfy constraint 0<x<=5")
        return value
