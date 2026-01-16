# tado-cli

## Description

A command line interface to set an offset temperature for tado thermostats, in order to improve temperature control.
The actual measured temperature of the the thermostat usually is way higher than the average room temperatue, as the sensor is placed right next to the heating source.
To compensate this, a temperature offset added to the temperature measured by the sensor may help.

## Prerequisites
Make sure you have `pip` and `python3` installed on your system. You can check by running on the command line:

```
python3 --version
pip --version
```

## Installation

Clone the repository and install the package using pip:

```
git clone git@github.com:acc-aqt/tado-cli.git
cd tado-cli
pip install .
```

## Execution

Call `tado-cli  --help` to check the required arguments.

```
Tado thermostat utilities

positional arguments:
  {list-thermostats,set-offset}
    list-thermostats    Print thermostat device IDs
    set-offset          Set temperature offset on thermostats

options:
  -h, --help            show this help message and exit
  ```
  

## Development Setup (if needed)

If you are developing or testing and need to use the source code directly:

- Run `make setup-venv` to create and activate a virtual environment. The python interpreter is located in `.venv/bin/python3`.

- Run `make install` to install the project in develop mode.

- Run `make test` to run the tests.
