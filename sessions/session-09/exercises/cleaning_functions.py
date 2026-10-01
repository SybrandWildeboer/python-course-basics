"""LIVE EXERCISE: the cleaning, as two functions.

Run it from the repository root so the relative paths work:

    python sessions/session-09/exercises/cleaning_functions.py

The walkthrough cleaned the messy file one step at a time. Now keep those
steps, in the shape session 10 builds on:

    raw = load_messy("data/messy/plays_messy.csv")
    plays = clean_plays(raw)

    1. load_messy(path) reads the file and returns it untouched. Use
       keep_default_na=False, so pandas guesses nothing and every decision
       about what counts as missing is yours.

    2. clean_plays(df) returns a cleaned copy with exactly the columns,
       column order and types of data/clean/plays.csv.

    3. The checks at the bottom are written for you. Uncomment them. When
       they all pass, you are done.

The decisions, as a checklist (because load_messy keeps everything as text,
an empty cell arrives as "", not NaN):

  * rename "minutes played " to minutes_played
  * drop the exact duplicates
  * genre: strip and title-case; a blank genre is missing   .replace("", pd.NA)
  * device: strip and lower-case; a blank becomes "unknown"
  * country: "NA" and blanks are missing
  * fill missing genre and country from the same artist's other plays
  * dates: the three formats, one at a time, then .dt.strftime("%Y-%m-%d"),
    because the clean file stores dates as text
  * minutes: remove " min" BEFORE pd.to_numeric(..., errors="coerce")
  * the clean file's column order, sorted by play_id, .reset_index(drop=True)

The session 3 rule: the functions return, and only the bottom of the file
prints.
"""

import pandas as pd

MESSY = "data/messy/plays_messy.csv"
CLEAN = "data/clean/plays.csv"


# TODO: def load_messy(path):


# TODO (optional, recommended): def parse_dates(text):


# TODO (optional, recommended): def fill_from_artist(df, column):


# TODO: def clean_plays(df):


clean = pd.read_csv(CLEAN)
print(clean.dtypes)                     # the target

# raw = load_messy(MESSY)
# plays = clean_plays(raw)
#
# assert raw.shape == (2223, 9)
# assert len(plays) == 2183
# assert list(plays.columns) == list(clean.columns)
# assert (plays.dtypes == clean.dtypes).all()
# assert plays["play_id"].equals(clean["play_id"])
# assert raw.shape == (2223, 9)         # the input was not changed
#
# TODO: per column, how many cells match the clean file? Predict first.
