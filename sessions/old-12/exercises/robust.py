"""LIVE EXERCISE: make it robust, then prove it.

Part 1. Fill in the three functions marked TODO, using try / except. Each
one catches ONE named error. No bare `except:`.

    safe_highest([3, 10, 7])                        ->  10
    safe_highest([])                                ->  None

    to_minutes("4.65")                              ->  4.65
    to_minutes("4.2 min")                           ->  4.2
    to_minutes("")                                  ->  None

    summary_line("data/clean/plays.csv", "phone")   ->  "1039 plays on the phone, 4.15 minutes on average"
    summary_line("data/clean/plays.csv", "radio")   ->  "No plays on the radio, so there is no average."
    summary_line("data/clean/play.csv", "phone")    ->  "No file at data/clean/play.csv. ..."

Part 2. Write the tests in test_robust.py, next door, and run them from the
repository root:

    python -m pytest sessions/session-12/exercises

One test is already written, and it fails until safe_highest works. That is
on purpose: watch it go from F to a dot.
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


# --- your turn --------------------------------------------------------------


def safe_highest(numbers):
    """Return the largest value in a list, or None if the list is empty."""
    # TODO: call highest(numbers), and catch the error it raises on an empty
    #       list. Which line of highest() raises it, and which error is it?


def to_minutes(text):
    """Return messy minutes text like "4.65" or "4.2 min" as a float, or None."""
    # TODO: strip the spaces, take " min" off the end if it is there, then
    #       try float(). Keep the try around the one line that can fail.


def summary_line(path, device):
    """Return one sentence about the average play on a device, whatever happens."""
    # TODO: the outer layer. Two things can go wrong: the file is missing,
    #       and the device has no plays. One try block for each, each with
    #       its own named except.
