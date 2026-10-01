"""STRETCH: worked solutions. The tests are in test_stretch_solved.py.

    python sessions/session-12/solutions/stretch_solved.py
    python -m pytest sessions/session-12/solutions/test_stretch_solved.py
"""

import csv
from pathlib import Path

import pandas as pd


# --- 1. else and finally ----------------------------------------------------


def describe(text):
    """Print which parts of a try statement run for one piece of text."""
    try:
        number = float(text)
    except ValueError:
        print(f"  {text!r}: except  -> not a number")
    else:
        print(f"  {text!r}: else    -> got {number}")
    finally:
        print(f"  {text!r}: finally -> always")


# --- 2. raising your own error, with a better message -----------------------


def total(numbers):
    """Return the sum of a list of numbers."""
    running = 0
    for number in numbers:
        running += number
    return running


def average(numbers):
    """Return the mean of a list of numbers.

    Raises ValueError for an empty list, with a message that says what the
    caller did, instead of a ZeroDivisionError that says what went wrong
    inside this function.
    """
    if len(numbers) == 0:
        raise ValueError("average() of an empty list: there is nothing to average")
    return total(numbers) / len(numbers)


# --- 3. floats that are nearly equal ----------------------------------------


def celsius_to_fahrenheit(c):
    """Return the Celsius temperature c converted to Fahrenheit."""
    return c * 9 / 5 + 32


# --- 4. one test, many cases ------------------------------------------------


def to_minutes(text):
    """Return messy minutes text like "4.65" or "4.2 min" as a float, or None."""
    text = text.strip()
    if text.endswith(" min"):
        text = text[:-len(" min")]
    try:
        return float(text)
    except ValueError:
        return None


# --- 5. a test that needs a file --------------------------------------------


def load_rows(path):
    """Return the CSV at path as a list of dictionaries, one per row."""
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


# --- 6. pandas does not raise -----------------------------------------------


def skip_rate(plays, device):
    """Return the percentage of plays on device that were skipped.

    Returns None when the device has no plays at all. Without the check,
    pandas would quietly return NaN rather than raise anything.
    """
    on_device = plays[plays["device"] == device]
    if len(on_device) == 0:
        return None
    return on_device["skipped"].mean() * 100


if __name__ == "__main__":
    print("1. else and finally")
    describe("4.5")
    describe("abc")

    print("\n2. a better error message")
    try:
        average([])
    except ValueError as error:
        print("  ValueError:", error)

    print("\n3. nearly equal")
    print("  celsius_to_fahrenheit(36.6) =", celsius_to_fahrenheit(36.6))

    print("\n6. pandas and the empty selection")
    # Built from this file's location (session 10), so it runs from any folder.
    root = Path(__file__).resolve().parents[3]
    plays = pd.read_csv(root / "data" / "clean" / "plays.csv")
    print(f"  car:   {skip_rate(plays, 'car'):.1f}% skipped")
    print(f"  radio: {skip_rate(plays, 'radio')}")
    print("  without the check:", plays[plays["device"] == "radio"]["skipped"].mean())
