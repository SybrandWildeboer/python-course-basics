"""LIVE EXERCISE part 2: the tests, worked solution.

Run from the repository root:

    python -m pytest sessions/session-12/solutions

The tests that read files use paths from the repository root, like everything
else in the course, so run pytest from there.
"""

import pytest

from robust_solved import load_rows, safe_highest, summary_line, to_minutes

PLAYS = "data/clean/plays.csv"


# --- safe_highest -----------------------------------------------------------

def test_safe_highest_of_a_normal_list():
    assert safe_highest([3, 10, 7]) == 10


def test_safe_highest_with_only_negatives():
    assert safe_highest([-5, -2, -9]) == -2


def test_safe_highest_of_an_empty_list_is_none():
    assert safe_highest([]) is None


# --- to_minutes -------------------------------------------------------------

def test_to_minutes_plain_number():
    assert to_minutes("4.65") == 4.65


def test_to_minutes_with_min_on_the_end():
    assert to_minutes("4.2 min") == 4.2


def test_to_minutes_ignores_surrounding_spaces():
    assert to_minutes(" 3.5 ") == 3.5


def test_to_minutes_empty_text_is_none():
    assert to_minutes("") is None


def test_to_minutes_words_are_none():
    assert to_minutes("about four") is None


# --- load_rows and summary_line ---------------------------------------------

def test_load_rows_missing_file_raises():
    # load_rows should NOT hide a missing file. The outer layer deals with it.
    with pytest.raises(FileNotFoundError):
        load_rows("data/clean/no_such_file.csv")


def test_summary_line_for_the_phone():
    assert summary_line(PLAYS, "phone") == "1039 plays on the phone, 4.15 minutes on average"


def test_summary_line_for_a_device_with_no_plays():
    assert summary_line(PLAYS, "radio") == "No plays on the radio, so there is no average."


def test_summary_line_for_a_missing_file():
    assert summary_line("data/clean/play.csv", "phone").startswith("No file at")


# ---------------------------------------------------------------------------
# The test worth looking at twice is test_load_rows_missing_file_raises. It
# checks that a function DOES crash. That feels backwards at first, but it
# pins down a decision: load_rows must never quietly return an empty list for
# a missing file, and if somebody "helpfully" adds a try/except to it later,
# this test fails and tells them why that is a bad idea.
