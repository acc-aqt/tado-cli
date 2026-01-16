# tado-temperature-offsrt

## Description

A small tool to set an offset temperature for tado thermostats, in order to improve temperature control.
The actual measured temperature of the the thermostat usually is way higher than the aberage room temperatue, as the sensor is placed right next to the heating source.
to compensate this, a temperature offset added to the temperature measured by the sensor may help.

## Prerequisites
Make sure you have `pip` and `python3` installed on your system. You can check by running on the command line:

```
python3 --version
pip --version
```

## Installation

This section needs to be updated!

Clone the repository and install the package using pip:

```
git clone https://github.com/acc-aqt/my-python-template
cd my-python-template
pip install .
```

As `my-python-template` is configured as a GitHub-template you can also use this template by clicking "use this template" on the GitHub page.

## Execution

Call `tado-temperature-offset  --help` to check the required arguments.

## Development Setup (if needed)

If you are developing or testing and need to use the source code directly:

- Run `make setup-venv` to create and activate a virtual environment. The python interpreter is located in `.venv/bin/python3`.

- Run `make install` to install the project in develop mode.

- Run `make test` to run the tests.