"""Provide testcases for the entry points.."""

from io import StringIO
from unittest.mock import patch

from example_package.main import entry_point


@patch("sys.stdout", new_callable=StringIO)  # capture prints
@patch("sys.argv", ["entry_point", "2", "3"])  # Mock cli arguments
def test_entry_point(mock_stdout: StringIO) -> None:
    """An exemplary testcase for the entry point."""
    entry_point()

    # Check if the output is correct
    output = mock_stdout.getvalue().strip()  # Capture printed output
    assert output == "5.0"  # Expecting the sum of 2 and 3 (5.0)
