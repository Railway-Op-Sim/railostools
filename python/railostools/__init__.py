import logging
import os

import click

from railostools.metadata import validate
from railostools.rly import RlyParser
from railostools.ttb.parsing import TTBParser

logging.basicConfig()


@click.group()
@click.option("--debug/--normal", help="Run in debug mode", default=False)
def railostools(debug: bool = False) -> None:
    """Python based utilities for Railway Operation Simulator"""
    logging.getLogger("RailOSTools").setLevel(logging.DEBUG if debug else logging.INFO)

@railostools.group()
def rly():
    """Process a railway file"""
    pass

@railostools.group()
def ttb():
    """Process a timetable file"""
    pass


@ttb.command()
@click.argument("ttb_file")
@click.option("--output", help="JSON output file", default=None)
def json(ttb_file: str, output: str = "") -> None:
    """Extract ROS timetable file to json"""
    if not os.path.exists(ttb_file):
        raise FileNotFoundError(
            f"Cannot extract ttb file to json, file '{ttb_file}' does not exist"
        )

    if not output:
        output = f"{os.path.splitext(ttb_file)[0]}.json"

    ttb_parser = TTBParser()
    ttb_parser.parse(ttb_file)
    ttb_parser.json(output)


@railostools.command()
@click.argument("input_file")
def validate(input_file: str):
    """Validate Railway Operation Simulator file"""
    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"Cannot validate file '{input_file}', " "file not found."
        )
    if os.path.splitext(input_file)[1] == ".toml":
        validate(input_file)
    elif os.path.splitext(input_file)[1] == ".ttb":
        with TTBParser(input_file):
            pass
    elif os.path.splitext(input_file)[1] in [".rly"]:
        raise NotImplementedError(
            f"Validation of files of type '{os.path.splitext(input_file)[1]}' is not yet implemented"
        )
    else:
        raise TypeError(
            f"Validation of files of type '{os.path.splitext(input_file)[1]}' is not supported"
        )


@rly.command()
@click.argument("rly_file")
@click.option("--output", help="JSON output file", default=None)
def json(rly_file: str, output: str):
    """Extract Railway Operation Simulator railway file to json"""
    if not os.path.exists(rly_file):
        raise FileNotFoundError(
            f"Cannot extract rly file to json, file '{rly_file}' does not exist"
        )

    if not output:
        output = f"{os.path.splitext(rly_file)[0]}.json"

    _parser = RlyParser()
    _parser.parse(rly_file)
    _parser.dump(output)

@rly.command()
@click.argument("rly_file")
def signals(rly_file: str) -> None:
    """Print signal information"""
    if not os.path.exists(rly_file):
        raise FileNotFoundError(
            f"Cannot parse rly file, file '{rly_file}' does not exist"
        )

    _parser = RlyParser()
    _parser.parse(rly_file)
    print(_parser.tables.signals)
