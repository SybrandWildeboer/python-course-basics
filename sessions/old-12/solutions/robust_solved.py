"""LIVE EXERCISE: make it robust, worked solution.

The tests are in test_robust_solved.py, next door. Run them from the
repository root with:

    python -m pytest sessions/session-12/solutions

Running this file directly prints a few example answers:

    python sessions/session-12/solutions/robust_solved.py
"""

import csv

# --- given: the session 3 and session 4 functions, unchanged ---------------


def total(numbers):
    """Return the sum of a list of numbers."""
    running = 0
    for number in numbers:
        running += number
    return running


def average(numbers):
    """Return the mean of a list of numbers."""
    return total(numbers) / len(numbers)


def highest(numbers):
    """Return the largest value in a list of numbers."""
    best = numbers[0]
    for number in numbers:
        if number > best:
            best = number
    return best


def load_rows(path):
    """Return the CSV at path as a list of dictionaries, one per row."""
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def minutes_on(rows, device):
    """Return the minutes_played of every play on one device, as numbers."""
    return [float(row["minutes_played"]) for row in rows if row["device"] == device]


# --- 1. safe_highest --------------------------------------------------------


def safe_highest(numbers):
    """Return the largest value in a list, or None if the list is empty."""
    try:
        return highest(numbers)
    except IndexError:              # highest() does numbers[0] on its first line
        return None


# --- 2. to_minutes ----------------------------------------------------------


def to_minutes(text):
    """Return messy minutes text like "4.65" or "4.2 min" as a float, or None.

    Empty text, and anything else that is not a number, gives None.
    """
    text = text.strip()
    if text.endswith(" min"):
        text = text[:-len(" min")]
    try:
        return float(text)
    except ValueError:
        return None


# --- 3. summary_line: the outer layer ---------------------------------------


def summary_line(path, device):
    """Return one sentence about the average play on a device, whatever happens.

    This is the outer layer, so it is the one place that catches errors.
    load_rows and average let them travel up to here.
    """
    try:
        rows = load_rows(path)
    except FileNotFoundError:
        return f"No file at {path}. Check the spelling, and run from the repository root."

    minutes = minutes_on(rows, device)
    try:
        return (f"{len(minutes)} plays on the {device}, "
                f"{average(minutes):.2f} minutes on average")
    except ZeroDivisionError:
        return f"No plays on the {device}, so there is no average."


if __name__ == "__main__":
    from pathlib import Path

    # Run directly, the examples find the data from this file's location
    # (session 10), so they work from any folder. The tests pass paths from
    # the repository root instead, which is where pytest runs.
    CLEAN = Path(__file__).resolve().parents[3] / "data" / "clean"

    print(safe_highest([3, 10, 7]), safe_highest([]))
    print(to_minutes("4.65"), to_minutes("4.2 min"), to_minutes(""))
    print(summary_line(CLEAN / "plays.csv", "phone"))
    print(summary_line(CLEAN / "plays.csv", "radio"))
    print(summary_line(CLEAN / "play.csv", "phone"))


# ---------------------------------------------------------------------------
# Three things worth noticing.
#
# 1. safe_highest wraps highest() instead of changing it. highest() still
#    crashes on an empty list, which is the right behaviour for code that
#    should never see one. Callers that expect empty lists choose the safe
#    version. Both exist, and the name says which is which.
#
# 2. to_minutes only puts float() inside the try. The strip and the " min"
#    check cannot fail, so they stay outside. Keep a try block as small as
#    the one line that can actually raise; the more you put in it, the more
#    chance it catches something you did not mean it to.
#
# 3. summary_line has two separate try blocks, one per thing that can go
#    wrong, and each except names exactly one error. A single try around the
#    whole function with `except Exception` would also "work", and would
#    also turn a typo in a column name into "No file at ...". That is the
#    bare-except lie from the walkthrough, in a more respectable coat.
