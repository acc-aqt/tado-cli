"""Testcases for example_module.py go here."""

from example_package.example_module import my_sum


def test_my_sum_one_plus_one_is_two() -> None:
    """An exemplary testcase for my_sum()."""
    assert my_sum(1, 1) == 2
