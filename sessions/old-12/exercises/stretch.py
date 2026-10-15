"""STRETCH: functions for the stretch notebook. The tests go in test_stretch.py.

Fill in the TODOs as the notebook reaches each one. Stretch 1 (else and
finally) happens in the notebook only.

    python -m pytest sessions/session-12/exercises/test_stretch.py
"""

import csv


def total(numbers):
    """Return the sum of a list of numbers."""
    running = 0
    for number in numbers:
        running += number
    return running


# --- 2. raising your own error ----------------------------------------------


def average(numbers):
    """Return the mean of a list of numbers.

    TODO: raise a ValueError with a helpful message for an empty list, instead
    of letting the ZeroDivisionError happen.
    """
    return total(numbers) / len(numbers)


# --- 3. floats (given, from your session 3 homework) ------------------------


def celsius_to_fahrenheit(c):
    """Return the Celsius temperature c converted to Fahrenheit."""
    return c * 9 / 5 + 32


# --- 4. one test, many cases (given, from the live exercise) ----------------


def to_minutes(text):
    """Return messy minutes text like "4.65" or "4.2 min" as a float, or None."""
    text = text.strip()
    if text.endswith(" min"):
        text = text[:-len(" min")]
    try:
        return float(text)
    except ValueError:
        return None


# --- 5. a test that needs a file (given, from session 4) --------------------


def load_rows(path):
    """Return the CSV at path as a list of dictionaries, one per row."""
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


# --- 6. pandas does not raise -----------------------------------------------


def skip_rate(plays, device):
    """Return the percentage of plays on device that were skipped, or None.

    TODO: plays is a DataFrame with "device" and "skipped" columns. Return
    None when the device has no plays at all.
    """
