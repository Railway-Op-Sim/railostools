import logging
import os

import click
import json

from railostools.metadata.validation import validate
from railostools.rly.parsing import RlyParser
from railostools.ttb.parsing import TTBParser
from railostools.metadata.wikidata import MetadataExpander
import railostools.exceptions as railos_exc

logging.basicConfig()


@click.group()
@click.option("--debug/--normal", help="Run in debug mode", default=False)
def railostools(debug: bool = False) -> None:
    """Python based utilities for Railway Operation Simulator"""
    logging.getLogger("RailOSTools").setLevel(
        logging.DEBUG if debug else logging.WARNING
    )


@railostools.command()
@click.argument("ttb_file")
@click.option("--output", help="JSON output file", default=None)
def ttb2json(ttb_file: str, output: str = "") -> None:
    """Extract RailOS timetable file to json"""
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
@click.option("--dump/--silent", help="Write out JSON to stdout", default=False)
def validate(input_file: str, dump: bool):
    """Validate Railway Operation Simulator file"""
    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"Cannot validate file '{input_file}', " "file not found."
        )
    if os.path.splitext(input_file)[1] == ".toml":
        validate(input_file)
    elif os.path.splitext(input_file)[1] == ".ttb":
        try:
            TTBParser().parse(input_file)
        except railos_exc.ParsingError as e:
            click.secho(
                f"Failed to parse file '{input_file}' with error: {e.args[0]}", fg="red"
            )
            raise click.Abort from e
        click.secho(
            f"Validation successful, file '{input_file}' passed all TTB file checks.",
            fg="green",
        )
    elif os.path.splitext(input_file)[1] in [".rly"]:
        try:
            _parser = RlyParser()
            _parser.parse(input_file)
            if dump:
                click.echo(json.dumps(_parser.data, indent=2))
        except railos_exc.ParsingError as e:
            click.secho(
                f"Failed to parse file '{input_file}' with error: {e.args[0]}", fg="red"
            )
            raise click.Abort from e
        click.secho(
            f"Validation successful, file '{input_file}' passed all RLY file checks.",
            fg="green",
        )
    else:
        raise TypeError(
            f"Validation of files of type '{os.path.splitext(input_file)[1]}' is not supported"
        )


@railostools.command()
@click.argument("rly_file")
@click.option("--output", help="JSON output file", default=None)
def rly2json(rly_file: str, output: str):
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


@railostools.command("metadata-expand")
@click.argument("project_directory")
def metadata_expander(project_directory: str) -> None:
    """Expand metadata for a Railway Operation Simulator project using Wikidata"""
    logging.getLogger().setLevel(logging.INFO)
    _expander = MetadataExpander(project_directory)
    _expander.append_metadata()
