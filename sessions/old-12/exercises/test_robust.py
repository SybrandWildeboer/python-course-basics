"""LIVE EXERCISE part 2: tests for robust.py.

Run from the repository root:

    python -m pytest sessions/session-12/exercises

Write at least two tests per function, and include the awkward case each
time. Name every test as a sentence that says what should be true.
"""

import pytest

from robust import load_rows, safe_highest, summary_line, to_minutes

PLAYS = "data/clean/plays.csv"


def test_safe_highest_of_a_normal_list():
    assert safe_highest([3, 10, 7]) == 10


# TODO: safe_highest of an empty list should be None


# TODO: at least three tests for to_minutes: a plain number, one ending in
#       " min", and empty text


# TODO: load_rows on a file that does not exist should RAISE
#       FileNotFoundError. Use:
#
#           with pytest.raises(FileNotFoundError):
#               ...


# TODO: summary_line for the phone, for a device with no plays, and for a
#       missing file
