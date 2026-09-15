"""LIVE EXERCISE: the pipeline.

One file, four steps, one command, two output files.

    python3 sessions/session-10/exercises/pipeline.py

Build it in this order, and RUN IT after every function, even when it barely
does anything yet. A pipeline that has never run is very hard to debug all at
once.

    1. load()              the session 7 query, through pd.read_sql
    2. clean()             lift your session 9 function in
    3. minutes_by_genre()  returns a table
    4. write_csv()         writes that table
    5. write_chart()       saves a PNG
    6. main()              calls them in order and prints progress

The skeleton below has the docstrings and the constants already. Fill in the
bodies.

Two rules to keep:
  * the functions RETURN their results. Only main() prints.
  * no paths typed out in the middle of a function. They live at the top.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")          # save files, never try to open a window
import matplotlib.pyplot as plt
import pandas as pd

# --------------------------------------------------------------------------
# Constants and paths. Worked out from THIS FILE's location, so the script
# runs correctly from any folder.

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

DB_PATH = ROOT / "data" / "music.db"
OUTPUT_DIR = ROOT / "output"

CSV_OUT = OUTPUT_DIR / "minutes_by_genre.csv"
CHART_OUT = OUTPUT_DIR / "minutes_by_month.png"


# --------------------------------------------------------------------------
# 1. LOAD


def load(db_path: Path = DB_PATH) -> pd.DataFrame:
    """Return every play, with its artist details, from the database.

    Do the join in SQL rather than in pandas: the database is good at it, and
    it means less data crosses into Python.
    """
    # TODO: the query, then pd.read_sql with parse_dates=["played_at"]
    # Remember to close the connection when you are done.
    raise NotImplementedError


# --------------------------------------------------------------------------
# 2. CLEAN


def clean(plays: pd.DataFrame) -> pd.DataFrame:
    """Return a tidied copy of the plays table."""
    # TODO: your session 9 cleaning, adapted. The database is already fairly
    #       clean, so this is light, but the step exists so there is an
    #       obvious place to add to it.
    raise NotImplementedError


# --------------------------------------------------------------------------
# 3. ANALYSE


def minutes_by_genre(plays: pd.DataFrame) -> pd.DataFrame:
    """Return plays, minutes, average minutes and share for each genre."""
    # TODO: groupby, agg, sort. Return the table, do not print it.
    raise NotImplementedError


def minutes_by_month(plays: pd.DataFrame) -> pd.DataFrame:
    """Return total minutes per calendar month, as a two-column table."""
    # TODO: resample("MS") on a date index, or group by the year and month
    raise NotImplementedError


# --------------------------------------------------------------------------
# 4. OUTPUT


def write_csv(summary: pd.DataFrame, path: Path = CSV_OUT) -> None:
    """Write the genre summary to a CSV."""
    # TODO: make the folder if it is missing, then to_csv(index=False)
    raise NotImplementedError


def write_chart(monthly: pd.DataFrame, path: Path = CHART_OUT) -> None:
    """Save a line chart of minutes per month."""
    # TODO: fig, ax = plt.subplots(...), plot, title, labels, savefig, close
    #       Title states the finding. Both axes labelled. y starts at zero.
    raise NotImplementedError


# --------------------------------------------------------------------------
# The part that runs when you run this file


def main() -> None:
    """Run the whole pipeline, reporting progress as it goes."""
    # TODO: call the steps in order, printing the row count after each one.
    #       That is how you find out both where a crash happened and whether
    #       a step quietly threw away half your data.
    raise NotImplementedError


if __name__ == "__main__":
    main()
