"""The session 10 pipeline: from the database to a chart and a CSV.

One script, four steps, one command. This is the template for the project.

    python3 sessions/session-10/solutions/pipeline.py

It writes two files into output/:

    output/minutes_by_genre.csv
    output/minutes_by_month.png

The shape to notice is load -> clean -> analyse -> output. Each step is a
function that takes something and returns something, so each one can be run
and checked on its own. Nothing here prints except main(), which reports
progress so you can see where it failed.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")          # save files, never try to open a window
import matplotlib.pyplot as plt
import pandas as pd

# --------------------------------------------------------------------------
# Constants and paths live at the top, not scattered through the file. When
# something needs changing, this is the only place to look.
#
# Paths are worked out from THIS FILE's location, so the script runs correctly
# from any folder. That is the fix for every FileNotFoundError in session 4.

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

    The join happens in SQL rather than in pandas, because the database is
    good at it and it means less data crosses into Python.
    """
    query = """
        SELECT p.play_id,
               p.played_at,
               p.track_name,
               p.minutes_played,
               p.device,
               p.skipped,
               a.artist_name,
               a.genre,
               a.country
        FROM plays p
        JOIN artists a USING (artist_id)
    """
    con = sqlite3.connect(db_path)
    try:
        return pd.read_sql(query, con, parse_dates=["played_at"])
    finally:
        con.close()            # a script tidies up after itself


# --------------------------------------------------------------------------
# 2. CLEAN


def clean(plays: pd.DataFrame) -> pd.DataFrame:
    """Return a tidied copy of the plays table.

    The database is already clean, so this is light. It exists anyway, for two
    reasons: the same pipeline should survive being pointed at a messier
    source, and having the step named makes it obvious where to add to it.
    """
    df = plays.copy()

    for column in ["artist_name", "track_name", "genre", "country", "device"]:
        df[column] = df[column].str.strip()

    df["minutes_played"] = pd.to_numeric(df["minutes_played"], errors="coerce")
    df = df.dropna(subset=["minutes_played", "played_at"])

    return df.reset_index(drop=True)


# --------------------------------------------------------------------------
# 3. ANALYSE


def minutes_by_genre(plays: pd.DataFrame) -> pd.DataFrame:
    """Return plays, minutes, average minutes and share for each genre.

    Returns a table rather than printing one, so the caller decides what to do
    with it. That is the session 3 lesson, and it is why write_csv below can
    exist without this function knowing anything about files.
    """
    summary = (plays.groupby("genre")
                    .agg(plays=("play_id", "count"),
                         minutes=("minutes_played", "sum"),
                         avg_minutes=("minutes_played", "mean"))
                    .round(2)
                    .sort_values("minutes", ascending=False)
                    .reset_index())

    summary["share_pct"] = (100 * summary["minutes"]
                            / summary["minutes"].sum()).round(1)
    return summary


def minutes_by_month(plays: pd.DataFrame) -> pd.DataFrame:
    """Return total minutes per calendar month, as a two-column table."""
    monthly = (plays.set_index("played_at")["minutes_played"]
                    .resample("MS")
                    .sum()
                    .round(1)
                    .reset_index())
    return monthly.rename(columns={"played_at": "month",
                                   "minutes_played": "minutes"})


# --------------------------------------------------------------------------
# 4. OUTPUT


def write_csv(summary: pd.DataFrame, path: Path = CSV_OUT) -> None:
    """Write the genre summary to a CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(path, index=False)


def write_chart(monthly: pd.DataFrame, path: Path = CHART_OUT) -> None:
    """Save a line chart of minutes per month."""
    path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(monthly["month"], monthly["minutes"], marker="o", linewidth=2)

    ax.set_title("Listening drops off every summer")
    ax.set_xlabel("Month")
    ax.set_ylabel("Minutes played")
    ax.set_ylim(bottom=0)
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


# --------------------------------------------------------------------------
# The part that runs when you run this file


def main() -> None:
    """Run the whole pipeline, reporting progress as it goes."""
    print(f"loading from {DB_PATH.relative_to(ROOT)} ...")
    plays = load()
    print(f"  {len(plays)} rows")

    print("cleaning ...")
    plays = clean(plays)
    print(f"  {len(plays)} rows after cleaning")

    print("analysing ...")
    summary = minutes_by_genre(plays)
    monthly = minutes_by_month(plays)
    print(f"  {len(summary)} genres, {len(monthly)} months")

    print("writing output ...")
    write_csv(summary)
    print(f"  {CSV_OUT.relative_to(ROOT)}")
    write_chart(monthly)
    print(f"  {CHART_OUT.relative_to(ROOT)}")

    print("\ndone. summary:")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
