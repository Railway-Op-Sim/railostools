import typing

import pydantic
import pycountry


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
    contributors: typing.List[str] = typing.Field(
        None,
        title="Contributor List",
        description="Additional contributors to the project"
    )

    @pydantic.validator('country_code')
    def check_country_code(cls, value):
        _country_codes = [country.alpha_2 for country in pycountry.countries]
        _country_codes += ['UN']
        if value not in _country_codes:
            raise AssertionError(f"'{value}' is not a recognised country code")
        return value

    @pydantic.validator(
        'name',
        'rly_file',
        'ttb_files',
        'ssn_files',
        'country_code',
        'factual',
        'difficulty',
        'author')
    def check_name_exists(cls, name):
        if not name:
            raise AssertionError("Required key is empty")
        return name

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
