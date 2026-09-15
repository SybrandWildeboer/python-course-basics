"""HOMEWORK 2: two real questions about the listening log.

Run from the repository root:

    python3 sessions/session-04/homework/questions.py

Question 1. Which genre has the highest AVERAGE minutes per play?

    Not the highest total. A genre with 500 short plays should not beat a
    genre with 100 long ones.

    The hint: you need TWO dictionaries. One counting plays per genre, one
    adding up minutes per genre. Then divide one by the other, genre by
    genre. That shape is exactly what GROUP BY does for you in session 6.

Question 2. Which artist was played most in 2025 only?

    The dates are text like "2025-04-17", and text has a .startswith()
    method. Print the top five artists with their counts, not just the
    winner.
"""

import csv

PLAYS = "data/clean/plays.csv"


def load_rows(path):
    """Return the CSV at path as a list of dictionaries."""
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


rows = load_rows(PLAYS)


# TODO question 1: average minutes per genre, highest first


# TODO question 2: top five artists in 2025
