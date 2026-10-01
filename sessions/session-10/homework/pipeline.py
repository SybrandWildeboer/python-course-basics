"""HOMEWORK 1: give the pipeline a second question.

This is the session's genre pipeline, unchanged. Add a second question to it:
how did my listening change month by month?

    python sessions/session-10/homework/pipeline.py

The rule: do NOT touch load_messy or clean_plays. If the pipeline is built
well, a new question needs only

    1. minutes_by_month(plays)       returns one row per month, "2024-01" to
                                     "2025-12", with plays and minutes
    2. save_month_chart(months, path) draws it as a LINE chart, titled with
                                     the busiest month, and saves a PNG
    3. check_months(path, plays)     reads the CSV back: 24 rows, and the
                                     plays add up to every cleaned play
    4. a few lines in main() that call them, and save the table with the
       save_csv you already have

Hints:
  * played_at is text like "2024-10-17", so plays["played_at"].str[:7]
    gives "2024-10": the session 4 [:7] slice, on a whole column
  * months.loc[months["minutes"].idxmax()] is the row with the most minutes
  * ax.plot(x, y) draws a line where ax.barh drew bars
  * ax.set_ylim(bottom=0), and then think about why it is there
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Every path is built from the location of this file, so the script finds
# its data whichever folder it is run from. parents[0] is the folder this
# file sits in (homework), and each number goes one further up:
# [1] session-10, [2] sessions, [3] the repository root.
ROOT = Path(__file__).resolve().parents[3]
MESSY = ROOT / "data" / "messy" / "plays_messy.csv"
OUTPUT = ROOT / "output"


# --------------------------------------------------------------------- load
# load_messy and clean_plays are the session 9 functions, unchanged, from
# sessions/session-09/solutions/cleaning.py. A pipeline reuses work; it does
# not redo it.


def load_messy(path):
    """Return the messy CSV at path as a DataFrame, with nothing guessed.

    keep_default_na=False stops pandas turning "NA" and empty cells into
    missing values on its own. Every text column arrives exactly as it was
    written, and clean_plays decides what counts as missing.
    """
    return pd.read_csv(path, keep_default_na=False)


# -------------------------------------------------------------------- clean

# The column order of data/clean/plays.csv.
COLUMNS = [
    "play_id", "played_at", "artist_name", "track_name", "genre",
    "country", "minutes_played", "device", "skipped",
]

# The three ways a date is written in the messy file, tried in this order.
DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]


def parse_dates(text):
    """Return a column of dates written in any of DATE_FORMATS as datetimes.

    Each format is tried on purpose, one at a time. A single blanket parse
    reads 05/01/2024 as the 1st of May, without a word of warning.
    """
    dates = pd.to_datetime(text, format=DATE_FORMATS[0], errors="coerce")
    for date_format in DATE_FORMATS[1:]:
        dates = dates.fillna(pd.to_datetime(text, format=date_format, errors="coerce"))
    assert dates.notna().all(), "some dates are in none of DATE_FORMATS"
    return dates


def fill_from_artist(df, column):
    """Return column with its gaps filled from the same artist's other rows.

    Every artist has exactly one genre and one country, so a play with the
    country missing can borrow it from any other play by the same artist.
    This is the session 4 lookup dictionary, built with groupby.
    """
    lookup = df.dropna(subset=[column]).groupby("artist_name")[column].first()
    return df[column].fillna(df["artist_name"].map(lookup))


def clean_plays(df):
    """Return a cleaned copy of the messy plays, shaped like data/clean/plays.csv.

    The decisions, in order:
      * the "minutes played " column is renamed to minutes_played
      * exact duplicate rows are dropped (40 in the messy file), first,
        because they are exact copies and every later step is then smaller
      * genre is stripped and title-cased, device stripped and lower-cased
      * dates in three formats are parsed deliberately, then written back as
        YYYY-MM-DD text, which is how the clean file stores them
      * " min" and spaces are removed from minutes before converting; a blank
        stays missing (NaN), because nobody knows how long that play was
      * "NA" in country means missing here (no artist is from Namibia), and
        missing genre and country are filled from the artist's other plays
      * a missing device becomes "unknown", so those plays still get counted

    The input DataFrame is not changed.
    """
    df = df.rename(columns={"minutes played ": "minutes_played"})
    df = df.drop_duplicates().copy()
    assert df["play_id"].is_unique, "a play_id appears twice with different values"

    # Work from text in every damaged column, so this behaves the same even if
    # the file was read without keep_default_na=False.
    text_columns = ["played_at", "genre", "country", "device", "minutes_played"]
    df[text_columns] = df[text_columns].fillna("").astype(str)

    df["genre"] = df["genre"].str.strip().str.title().replace("", pd.NA)
    df["device"] = df["device"].str.strip().str.lower().replace("", "unknown")
    df["country"] = df["country"].str.strip().replace(["NA", ""], pd.NA)
    df["genre"] = fill_from_artist(df, "genre")
    df["country"] = fill_from_artist(df, "country")

    df["played_at"] = parse_dates(df["played_at"]).dt.strftime("%Y-%m-%d")

    # Remove " min", and any spaces: the export writes thousands as "1 234.50".
    # No play in this file is that long, but nothing else would catch it.
    minutes = df["minutes_played"].str.replace("min", "").str.replace(" ", "")
    df["minutes_played"] = pd.to_numeric(minutes, errors="coerce")

    # errors="coerce" never complains, so check it only blanked the blanks.
    unreadable = df["minutes_played"].isna() & (minutes != "")
    assert not unreadable.any(), "some minutes could not be read as numbers"

    return df[COLUMNS].sort_values("play_id").reset_index(drop=True)


# ------------------------------------------------------------------ analyse


def summarise_by_genre(plays):
    """Return one row per genre: plays, minutes, average minutes, skip rate.

    The session 3 shape: it calculates and returns. It prints nothing and
    writes nothing, so it can be checked in a notebook and reused anywhere.
    """
    summary = (plays.groupby("genre")
               .agg(plays=("play_id", "count"),
                    minutes=("minutes_played", "sum"),
                    average_minutes=("minutes_played", "mean"),
                    skip_rate=("skipped", "mean"))
               .sort_values("minutes", ascending=False)
               .reset_index())
    summary["skip_rate"] = summary["skip_rate"] * 100
    return summary.round({"minutes": 1, "average_minutes": 2, "skip_rate": 1})


# --------------------------------------------------------------------- save


def save_csv(summary, path):
    """Write the summary table to path as a CSV, making the folder if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(path, index=False)


def save_chart(summary, path):
    """Draw minutes per genre as a bar chart, titled with the answer, to path."""
    top = summary.iloc[0]
    share = top["minutes"] / summary["minutes"].sum() * 100

    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.barh(summary["genre"], summary["minutes"], color="#4f6ddb")
    ax.invert_yaxis()                                # biggest at the top
    ax.bar_label(bars, labels=[f"{m:,.1f}" for m in summary["minutes"]], padding=3)
    ax.set_title(f"{top['genre']} gets {share:.1f}% of my listening time")
    ax.set_xlabel("minutes played, 2024 to 2025")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()

    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)


# TODO: def minutes_by_month(plays):


# TODO: def save_month_chart(months, path):


# -------------------------------------------------------------------- check


def check_summary(path, plays):
    """Read the written CSV back and confirm it agrees with the cleaned plays.

    Returns nothing when the file is right, and stops the run with an
    AssertionError when it is not. A pipeline that writes a wrong file
    silently is worse than one that crashes.
    """
    back = pd.read_csv(path)
    file_minutes = back["minutes"].sum()
    data_minutes = plays["minutes_played"].sum()

    assert back["plays"].sum() == len(plays), "plays went missing on the way"
    # Each genre was rounded to one decimal, so allow a little difference.
    assert abs(file_minutes - data_minutes) < 1, "the minutes do not add up"


# TODO: def check_months(path, plays):


# --------------------------------------------------------------------- main


def main():
    """Run the whole pipeline: the outer layer, and the only part that prints."""
    raw = load_messy(MESSY)
    plays = clean_plays(raw)
    summary = summarise_by_genre(plays)

    csv_path = OUTPUT / "genre_summary.csv"
    png_path = OUTPUT / "genre_minutes.png"
    save_csv(summary, csv_path)
    save_chart(summary, png_path)
    check_summary(csv_path, plays)

    # TODO: the monthly question goes here: analyse, save, save, check

    print(f"loaded  {len(raw):>5} rows from {MESSY.name}")
    print(f"cleaned {len(plays):>5} rows")
    print(f"wrote   {csv_path.relative_to(ROOT).as_posix()}")
    print(f"wrote   {png_path.relative_to(ROOT).as_posix()}")
    print(f"top genre: {summary.iloc[0]['genre']}, {summary.iloc[0]['minutes']:,.1f} minutes")


if __name__ == "__main__":
    main()
