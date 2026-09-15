"""HOMEWORK 1: write a filtered CSV.

Read data/clean/plays.csv, keep only the rows matching a condition you choose,
and write them to output/.

Run from the repository root:

    python3 sessions/session-04/homework/filter_plays.py

Requirements:
  * print how many rows went in and how many came out
  * same columns, same order, with a header row
  * open the result afterwards and check it looks sensible

Watch out: "w" replaces the output file without asking, and the output folder
has to exist first. os.makedirs("output", exist_ok=True) sorts that out.
"""

import csv
import os

PLAYS = "data/clean/plays.csv"
OUT = "output/filtered.csv"


def load_rows(path):
    """Return the CSV at path as a list of dictionaries."""
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


rows = load_rows(PLAYS)
print(f"{len(rows)} rows in")

# TODO: pick your condition and keep only the rows that match it


# TODO: print how many came out


# TODO: write them to OUT with a header row
