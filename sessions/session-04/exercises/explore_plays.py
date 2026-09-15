"""LIVE EXERCISE: ask the listening log three questions.

Run it from the repository root so the relative path works:

    python3 sessions/session-04/exercises/explore_plays.py

Answer these, with printed output:

    1. How many plays are there in total?
    2. How many plays per device, biggest first?
    3. How many minutes were listened to in total, as a whole number?

Then, if that went smoothly:

    4. How many plays were skipped, and what percentage of the total is that?

Write each answer as a FUNCTION that returns its result, the way you did last
week, and do all the printing at the bottom.

Reminders:
  * encoding="utf-8" on the open, or accented artist names break it
  * everything from a CSV is text, so float() the minutes before adding
  * rows[:3] to peek without flooding your terminal
  * the skipped column holds the text "0" or "1", not a number
"""

import csv

PLAYS = "data/clean/plays.csv"


def load_rows(path):
    """Return the CSV at path as a list of dictionaries, one per row."""
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


rows = load_rows(PLAYS)
print(f"loaded {len(rows)} rows")
print(rows[0])


# TODO 1: how many plays in total?


# TODO 2: def count_by(rows, column) -> a dictionary of counts
#         then print it sorted, biggest first


# TODO 3: def total_minutes(rows) -> a number


# TODO 4: how many were skipped, and what percentage is that?
