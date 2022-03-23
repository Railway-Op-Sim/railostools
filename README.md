# RailOSTools
[![RailOSTools](https://github.com/Railway-Op-Sim/railostools/actions/workflows/rostools.yml/badge.svg)](https://github.com/Railway-Op-Sim/railostools/actions/workflows/rostools.yml)[![codecov](https://codecov.io/gh/Railway-Op-Sim/rostools/branch/main/graph/badge.svg?token=ZDddjxt8v5)](https://codecov.io/gh/Railway-Op-Sim/rostools)

*Railway Operation Simulator Toolkit*

ROSTools provides a set of tools for working with Railway Operation Simulator program files.
The package is both an importable Python3.6+ module and a command line interface.

All command line tools are available under the parent `railostools` command:

```sh
$ railostools
Usage: railostools [OPTIONS] COMMAND [ARGS]...

  Python based utilities for Railway Operation Simulator

Options:
  --debug / --normal  Run in debug mode
  --help              Show this message and exit.

Commands:
  ttb2json  Extract ROS timetable file to json
```

## Command Line Interface

### Parsing `.ttb` Files

The command `ttb2json` converts a `.ttb` file to a JSON file containing the metadata for the services.
This allows for easier data interpretation within other projects.

```sh
$ railostools ttb2json --help
Usage: railostools ttb2json [OPTIONS] TTB_FILE

  Extract ROS timetable file to json

Options:
  --output TEXT  JSON output file
  --help         Show this message and exit.
```

### Parsing `.rly` Files

The command `rly2json` converts a `.rly` file to a JSON file containing the metadata for route elements.
This allows for easier data interpretation within other projects.

```sh
$ railostools rly2json --help
Usage: railostools rly2json [OPTIONS] RLY_FILE

  Extract ROS railway file to json

Options:
  --output TEXT  JSON output file
  --help         Show this message and exit.
```

## API

Features within `railostools` can also be accessed via the dedicated Python API.

### The `TTBParser` Class

```python3
from railostools.ttb import TTBParser

# Create a parser instance for parsing files
my_parser = TTBParser()

# Parse a timetable file
my_parser.parse('Enoshima_Week_2021.ttb')

# Can access various information
print(f'Timetable starts at {my_parser.start_time}')
print(my_parser.comments)

# Print out all data
print(my_parser.data)

# Save data as JSON file
my_parser.dump('Enoshima_Week_2021.json')
```

### The `RlyParser` Class

```python3
from railostools.rly import RlyParser

# Create a parser instance for parsing files
my_parser = RlyParser()

# Parse a timetable file
my_parser.parse('Antwerpen_Centraal.rly')

# Can access various information
print(f'Number of elements are {my_parser.n_active_elements+my_parser.n_inactive_elements}')

# Print out all data
print(my_parser.data)

# Save data as JSON file
my_parser.dump('Antwerpen_Centraal.json')
```

### Performance Log Monitoring
The performance log parsing module can asynchronously monitor the Railway Operation Simulator logs directory extracting
contents which can then be processed by applications live. The `Monitor` class is designed to only retrieve data when
it has been confirmed by file modification time that the log has been updated. These times are also used to fetch the
latest log during running. The class uses the Python `asyncio` library.

```python3
import railostools.performance
import asyncio
from railostools.performance import Monitor

ROS_LOG_DIR = 'C:\\Program Files (x86)\\RailwayOperationSimulator\\Railway\\Performance\ logs'

# Create a new monitor pointing to the ROS log directory
my_monitor = Monitor(ROS_LOG_DIR)

# Create a listener function which will just print the data
# MUST have 'monitor' as an argument, this is the monitor instance
async def listener(monitor: railostools.performance.Monitor, user_name: str) -> None:
    # Run until the monitor stops
    while monitor.running:
        print(f"Running for user '{user_name}'")
        print(monitor.data)
        await asyncio.sleep(10)

# Attach listener function to the async loop of the monitor
# arguments are given as a dictionary
my_monitor.exec_in_parallel(listener, {'user_name': 'John'})

# Finally run the monitor
my_monitor.run()
```
