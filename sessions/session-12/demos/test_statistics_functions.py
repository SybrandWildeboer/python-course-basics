"""Your session 3 assert lines, turned into tests.

Run from the repository root:

    python -m pytest sessions/session-12/demos

pytest finds every file whose name starts with test_, and inside it every
function whose name starts with test_, calls each one, and reports. A test is
nothing more than a function with assert lines in it.

pytest is not part of Python. If `python -m pytest` says "No module named
pytest", install it into your project's virtual environment first:

    python -m pip install pytest
"""

import pytest

from statistics_functions import average, highest, lowest, total


# --- the asserts from session 3, one idea per test --------------------------

def test_total_of_a_short_list():
    assert total([1, 2, 3]) == 6


def test_average_of_two_numbers():
    assert average([2, 4]) == 3


def test_highest_with_only_negatives():
    # The session 2 bug: starting at 0 instead of at the first value.
    assert highest([-5, -2, -9]) == -2


def test_lowest_with_only_negatives():
    assert lowest([-5, -2, -9]) == -9


def test_highest_of_a_single_value():
    assert highest([7]) == 7


# --- new: the awkward cases, which session 3 left alone ---------------------

def test_total_of_an_empty_list_is_zero():
    # An empty total is genuinely 0, unlike an empty average.
    assert total([]) == 0


def test_average_of_an_empty_list_raises():
    # The test passes only if the error happens. No error means the test fails.
    with pytest.raises(ZeroDivisionError):
        average([])


def test_highest_of_an_empty_list_raises():
    with pytest.raises(IndexError):
        highest([])


# --- the real lists from session 3 ------------------------------------------

def test_summary_numbers_for_session_3_list():
    numbers = [12, 7, 41, 3, 28, 19, 7, 55, 2, 33]
    assert total(numbers) == 207
    assert average(numbers) == 20.7
    assert highest(numbers) == 55
    assert lowest(numbers) == 2
