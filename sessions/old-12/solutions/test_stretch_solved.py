"""STRETCH: the tests, worked solutions.

    python -m pytest sessions/session-12/solutions/test_stretch_solved.py

Add -v to see every test by name, and -k to run only some of them:

    python -m pytest sessions/session-12/solutions/test_stretch_solved.py -v -k minutes
"""

import math

import pandas as pd
import pytest

from stretch_solved import (
    average,
    celsius_to_fahrenheit,
    load_rows,
    skip_rate,
    to_minutes,
)


# --- 2. raising your own error ----------------------------------------------

def test_average_of_an_empty_list_says_why():
    # match= checks the message too, not just the type of error.
    with pytest.raises(ValueError, match="empty list"):
        average([])


def test_average_still_works_normally():
    assert average([2, 4]) == 3


# --- 3. floats ---------------------------------------------------------------

def test_body_temperature_in_fahrenheit():
    # celsius_to_fahrenheit(36.6) is 97.88000000000001, so == 97.88 fails.
    assert celsius_to_fahrenheit(36.6) == pytest.approx(97.88)


def test_average_of_tenths():
    assert average([0.1, 0.2]) == pytest.approx(0.15)


def test_freezing_point_is_exact():
    # Whole numbers are exact, so plain == is right here. Use approx only
    # where floats are involved.
    assert celsius_to_fahrenheit(0) == 32


# --- 4. one test, many cases -------------------------------------------------

@pytest.mark.parametrize("text, expected", [
    ("4.65", 4.65),
    ("4.2 min", 4.2),
    (" 3.5 ", 3.5),
    ("0.32 min", 0.32),
    ("12", 12.0),
])
def test_to_minutes_reads_numbers(text, expected):
    assert to_minutes(text) == expected


@pytest.mark.parametrize("text", ["", "   ", "min", "about four", "4,2"])
def test_to_minutes_gives_none_for_non_numbers(text):
    assert to_minutes(text) is None


# --- 5. a test that needs a file ---------------------------------------------

def test_load_rows_reads_a_small_file(tmp_path):
    # tmp_path is a fresh, empty folder that pytest makes for this test and
    # cleans up afterwards. Asking for it by name is all it takes.
    path = tmp_path / "plays.csv"
    path.write_text("device,minutes_played\nphone,4.65\ncar,3.10\n", encoding="utf-8")

    rows = load_rows(path)

    assert len(rows) == 2
    assert rows[0] == {"device": "phone", "minutes_played": "4.65"}   # still text


def test_load_rows_of_a_header_only_file_is_empty(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("device,minutes_played\n", encoding="utf-8")
    assert load_rows(path) == []


def test_load_rows_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_rows(tmp_path / "not_there.csv")


# --- 6. pandas does not raise ------------------------------------------------

@pytest.fixture
def plays():
    """Four plays you can check in your head: phone 1 of 2 skipped, car 0 of 2."""
    return pd.DataFrame({
        "device": ["phone", "phone", "car", "car"],
        "skipped": [1, 0, 0, 0],
    })


def test_skip_rate_on_the_phone(plays):
    assert skip_rate(plays, "phone") == 50


def test_skip_rate_can_be_zero(plays):
    assert skip_rate(plays, "car") == 0


def test_skip_rate_with_no_plays_is_none(plays):
    assert skip_rate(plays, "radio") is None


def test_pandas_mean_of_nothing_is_nan_not_an_error(plays):
    # The reason skip_rate needs its check: no exception to catch, just NaN.
    assert math.isnan(plays[plays["device"] == "radio"]["skipped"].mean())


def test_skip_rate_on_the_real_data():
    real = pd.read_csv("data/clean/plays.csv")
    assert round(skip_rate(real, "car"), 1) == 10.6      # 19 of 179
