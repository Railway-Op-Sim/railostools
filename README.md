# ROSTools
*Railway Operation Simulator Toolkit*

ROSTools provides a set of tools for working with Railway Operation Simulator program files.
The package is both an importable Python3.6+ module and a command line interface.

All command line tools are available under the parent `rostools` command:

```sh
$ rostools
Usage: rostools [OPTIONS] COMMAND [ARGS]...

  Python based utilities for Railway Operation Simulator

Options:
  --debug / --normal  Run in debug mode
  --help              Show this message and exit.

Commands:
  ttb2json  Extract ROS timetable file to json
```

## Timetable Parser

### `ttb2json`

Converts a `.ttb` file to a JSON file containing the metadata for the services. This allows for easier data
interpretation within other projects.

```sh
$ rostools ttb2json --help
Usage: rostools ttb2json [OPTIONS] TTB_FILE

  Extract ROS timetable file to json

Options:
  --output TEXT  JSON output file
  --help         Show this message and exit.
```


