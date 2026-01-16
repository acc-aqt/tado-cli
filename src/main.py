"""Contains CLI entry points for Tado thermostat utilities."""
import argparse

from tado_client import TadoClient



def list_thermostats(_: argparse.Namespace) -> None:
    """List thermostat device IDs."""
    
    client = TadoClient()
    for tid in client.get_thermostat_ids():
        print(tid)


def set_offset(args: argparse.Namespace) -> None:
    """Set temperature offset on thermostats."""
    client = TadoClient()

    devices = args.devices or client.get_thermostat_ids()

    for device in devices:
        client.set_temperature_offset(device, args.offset)


def main() -> None:
    """Set up CLI argument parsing and dispatch to appropriate functions."""
    
    parser = argparse.ArgumentParser(
        description="Tado thermostat utilities"
    )
    subparsers = parser.add_subparsers(required=True)

    # list-thermostats
    p_list = subparsers.add_parser(
        "list-thermostats",
        help="Print thermostat device IDs",
    )
    p_list.set_defaults(func=list_thermostats)

    # set-offset
    p_offset = subparsers.add_parser(
        "set-offset",
        help="Set temperature offset on thermostats",
    )
    p_offset.add_argument(
        "--offset",
        type=float,
        required=True,
        help="Temperature offset in degree Celsius",
    )
    p_offset.add_argument(
        "--devices",
        nargs="+",
        help="Optional list of thermostat serial numbers",
    )
    p_offset.set_defaults(func=set_offset)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
    