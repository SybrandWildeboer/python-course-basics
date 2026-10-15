"""HOMEWORK 1: a decision diary. Which device gets skipped most?

Run from the repository root:

    python sessions/session-09/homework/decisions.py

Answer the question five times, once after each decision:

    1. the messy file exactly as loaded
    2. device stripped and lower-cased, blank devices left out, duplicates in
    3. the same, with duplicates dropped
    4. the full clean_plays, with "unknown" as a device
    5. the clean file

Write skip_rates(df) first: one row per device, a "plays" column and a
"rate" column (percentage skipped), highest rate first. Hint:

    df.groupby("device")["skipped"].agg(plays="size", rate="mean")

Then, in a comment at the bottom: which decision changed the answer most,
what to do about "unknown", and whether a minimum of 30 plays would have
rescued step 1.
"""

import sys

import pandas as pd

# sys.path is where Python looks for imports. Adding the solutions folder
# lets this file use cleaning.py. Paste your own functions in instead if
# they passed every check in the live exercise.
sys.path.insert(0, "sessions/session-09/solutions")
from cleaning import clean_plays, load_messy

raw = load_messy("data/messy/plays_messy.csv")
plays = clean_plays(raw)
clean = pd.read_csv("data/clean/plays.csv")


# TODO: def skip_rates(df):


# TODO step 1: as loaded


# TODO step 2: device text cleaned, blanks left out, duplicates still in


# TODO step 3: duplicates dropped too


# TODO step 4: the full clean_plays


# TODO step 5: the clean file


# Your diary and answers:
#
#
