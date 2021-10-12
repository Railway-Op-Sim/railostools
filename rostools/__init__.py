import click
import os
import logging
import toml
from rostools.ttb import TTBParser
from rostools.rly import RlyParser

from rostools.metadata import Route
from rostools.metrics import difficulty_components

logging.basicConfig()


@click.group()
@click.option('--debug/--normal', help='Run in debug mode', default=False)
def rostools(debug: bool = False) -> None:
    """Python based utilities for Railway Operation Simulator"""
    logging.getLogger('ROSTools').setLevel(logging.DEBUG if debug else logging.INFO)


@rostools.command()
@click.argument('ttb_file')
@click.option('--output', help='JSON output file', default=None)
def ttb2json(ttb_file: str, output: str = '') -> None:
    """Extract ROS timetable file to json"""
    if not os.path.exists(ttb_file):
        raise FileNotFoundError(
            f"Cannot extract ttb file to json, file '{ttb_file}' does not exist"
        )

    if not output:
        output = f'{os.path.splitext(ttb_file)[0]}.json'

    _parser = TTBParser()
    _parser.parse(ttb_file)
    _parser.json(output)


@rostools.command()
@click.argument('input_file')
def validate(input_file: str):
    """Validate ROS file"""
    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"Cannot validate file '{input_file}', "
            "file not found."
        )
    if os.path.splitext(input_file)[1] == '.toml':
        _data = toml.load(input_file)
        Route(**_data)
    elif os.path.splitext(input_file)[1] in ['.rly', '.ttb']:
        raise NotImplementedError(
            f"Validation of files of type '{os.path.splitext(input_file)[1]}' is not yet implemented"
        )
    else:
        raise TypeError(
            f"Validation of files of type '{os.path.splitext(input_file)[1]}' is not supported"
        )


@rostools.command()
@click.argument('rly_file')
@click.option('--output', help='JSON output file', default=None)
def rly2json(rly_file: str, output: str):
    """Extract ROS railway file to json"""
    if not os.path.exists(rly_file):
        raise FileNotFoundError(
            f"Cannot extract rly file to json, file '{rly_file}' does not exist"
        )

    if not output:
        output = f'{os.path.splitext(rly_file)[0]}.json'

    _parser = RlyParser()
    _parser.parse(rly_file)
    _parser.json(output)


@rostools.command(name='difficulty')
@click.argument('rly_file')
@click.argument('ttb_file')
@click.option('--verbose/--normal', help='Show components of difficulty', default=False)
def get_difficulty(
        rly_file: click.Path(exists=True, readable=True, resolve_path=True),
        ttb_file: click.Path(exists=True, readable=True, resolve_path=True),
        verbose: bool
):
    _components = difficulty_components(ttb_file, rly_file)
    if verbose:
        print(_components)
    else:
        print(f'Calculated Difficulty: {_components["difficulty"]}')
