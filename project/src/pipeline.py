"""PROJECT TEMPLATE: the pipeline.

Copy the shape, replace the content. Four steps, one command:

    python3 src/pipeline.py

The rules worth keeping:
  * constants and paths at the top, never in the middle of a function
  * every function takes something and returns something
  * only main() prints
  * the analysis functions do not know that files exist, and the output
    functions do not know where the numbers came from
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")          # save files, never try to open a window
import matplotlib.pyplot as plt
import pandas as pd

# --------------------------------------------------------------------------
# Constants and paths, worked out from THIS FILE's location so the script runs
# from any folder. Never a path like /Users/you/Documents/project/data.csv.

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"

DB_PATH = DATA_DIR / "music.db"          # or a CSV, or whatever you are using
CSV_OUT = OUTPUT_DIR / "summary.csv"
CHART_OUT = OUTPUT_DIR / "chart.png"


# --------------------------------------------------------------------------
# 1. LOAD


def load(db_path: Path = DB_PATH) -> pd.DataFrame:
    """Return the raw data for this project.

    If your data is in a database, do the joining and filtering in SQL: it is
    good at it, and less data has to cross into Python. If it is a CSV, this
    is one pd.read_csv with parse_dates.
    """
    query = """
        SELECT *
        FROM plays
    """
    con = sqlite3.connect(db_path)
    try:
        return pd.read_sql(query, con, parse_dates=["played_at"])
    finally:
        con.close()


# --------------------------------------------------------------------------
# 2. CLEAN


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Return a tidied copy of the data.

    Record your DECISIONS in this docstring, not just the steps. Anybody
    reading your numbers later needs to know what you dropped and why.
    """
    df = df.copy()
    # TODO: types, whitespace, duplicates, missing values
    return df.reset_index(drop=True)


# --------------------------------------------------------------------------
# 3. ANALYSE


def summarise(df: pd.DataFrame) -> pd.DataFrame:
    """Return the table that answers your question.

    One function per question. Return the table; do not print it.
    """
    # TODO: groupby, agg, sort
    raise NotImplementedError


# --------------------------------------------------------------------------
# 4. OUTPUT


def write_csv(summary: pd.DataFrame, path: Path = CSV_OUT) -> None:
    """Write a summary table to a CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(path, index=False)


def write_chart(summary: pd.DataFrame, path: Path = CHART_OUT) -> None:
    """Save the chart that answers your question.

    Title states the finding, both axes labelled, and a bar chart starts at
    zero.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(9, 4.5))
    # TODO: plot something
    ax.set_title("Say the finding here, not the column names")
    ax.set_xlabel("...")
    ax.set_ylabel("...")
    ax.set_ylim(bottom=0)
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


# --------------------------------------------------------------------------
# The part that runs when you run this file


def main() -> None:
    """Run the whole pipeline, reporting progress as it goes."""
    print("loading ...")
    df = load()
    print(f"  {len(df)} rows")

    print("cleaning ...")
    df = clean(df)
    print(f"  {len(df)} rows after cleaning")

    print("analysing ...")
    summary = summarise(df)
    print(f"  {len(summary)} rows in the summary")

    print("writing output ...")
    write_csv(summary)
    write_chart(summary)
    print(f"  {CSV_OUT.name} and {CHART_OUT.name}")

    print("\ndone")


if __name__ == "__main__":
    main()
