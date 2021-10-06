import typing

import pydantic
import pycountry


class Route(pydantic.BaseModel):
    name: str
    display_name: str
    description: str
    rly_file: str
    ttb_files: typing.List[str]
    ssn_files: typing.List[str]
    country_code: str
    year: int
    factual: bool
    difficulty: int
    author: str
    contributors: typing.List[str]

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
