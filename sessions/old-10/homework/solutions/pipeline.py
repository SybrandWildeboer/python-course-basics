"""HOMEWORK 1: a second question for the same pipeline, worked solution.

The session's pipeline answers "which genre do I listen to most?". This one
also answers "how did my listening change month by month?", and the point is
what did NOT change: load_messy and clean_plays are untouched. A new question
is one new analyse function, one new save function, and three lines in main.

    python sessions/session-10/homework/solutions/pipeline.py

It writes four files into output/ at the repository root:

    output/genre_summary.csv      output/genre_minutes.png
    output/minutes_by_month.csv   output/minutes_by_month.png
"""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

# Every path is built from the location of this file, so the script finds
# its data whichever folder it is run from. parents[0] is the folder this
# file sits in (solutions), and each number goes one further up:
# [1] homework, [2] session-10, [3] sessions, [4] the repository root.
ROOT = Path(__file__).resolve().parents[4]
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


def minutes_by_month(plays):
    """Return one row per month ("2024-01" and so on): plays and minutes.

    played_at is YYYY-MM-DD text, so the month is its first seven characters:
    the session 4 played_at[:7] trick, done to the whole column with .str.
    As text, "2024-02" sorts before "2024-10", so the months come out in order.
    """
    month = plays["played_at"].str[:7]
    months = (plays.assign(month=month)
              .groupby("month")
              .agg(plays=("play_id", "count"), minutes=("minutes_played", "sum"))
              .reset_index())
    return months.round({"minutes": 1})


def save_month_chart(months, path):
    """Draw minutes per month as a line chart, titled with the busiest month."""
    busiest = months.loc[months["minutes"].idxmax()]
    label = pd.to_datetime(busiest["month"]).strftime("%B %Y")

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(months["month"], months["minutes"], color="#4f6ddb", linewidth=2, marker="o")
    ax.set_title(f"{label} was my busiest month: {busiest['minutes']:.1f} minutes")
    ax.set_ylabel("minutes played")
    ax.set_ylim(bottom=0)                       # an honest axis starts at zero
    ax.tick_params(axis="x", labelrotation=90)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()

    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)


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


def check_months(path, plays):
    """Read the monthly CSV back and confirm every play landed in a month."""
    back = pd.read_csv(path)
    assert len(back) == 24, "two years should be 24 months"
    assert back["plays"].sum() == len(plays), "plays went missing on the way"
    # 24 months each rounded to one decimal: allow up to 0.05 each.
    assert abs(back["minutes"].sum() - plays["minutes_played"].sum()) < 1.2


# --------------------------------------------------------------------- main


def main():
    """Run the whole pipeline: the outer layer, and the only part that prints.

    The stages are silent and main() is chatty: it prints a line after each
    stage, so a run shows how far it got and how many rows each stage left.
    """
    matplotlib.use("Agg")      # draw charts straight into files, never open a window
    raw = load_messy(MESSY)
    print(f"loaded  {len(raw):>5} rows from {MESSY.name}")
    plays = clean_plays(raw)
    print(f"cleaned {len(plays):>5} rows")
    summary = summarise_by_genre(plays)
    print(f"analysed{len(summary):>5} genres")

    csv_path = OUTPUT / "genre_summary.csv"
    png_path = OUTPUT / "genre_minutes.png"
    save_csv(summary, csv_path)
    print(f"wrote   {csv_path.relative_to(ROOT).as_posix()}")
    save_chart(summary, png_path)
    print(f"wrote   {png_path.relative_to(ROOT).as_posix()}")
    check_summary(csv_path, plays)
    print("checked  the file agrees with the cleaned plays")

    # The new question: a few lines, and nothing above them changed.
    months = minutes_by_month(plays)
    print(f"analysed{len(months):>5} months")
    month_csv = OUTPUT / "minutes_by_month.csv"
    month_png = OUTPUT / "minutes_by_month.png"
    save_csv(months, month_csv)
    print(f"wrote   {month_csv.relative_to(ROOT).as_posix()}")
    save_month_chart(months, month_png)
    print(f"wrote   {month_png.relative_to(ROOT).as_posix()}")
    check_months(month_csv, plays)
    print("checked  the monthly file agrees with the cleaned plays")

    print(f"top genre: {summary.iloc[0]['genre']}, {summary.iloc[0]['minutes']:,.1f} minutes")
    busiest = months.loc[months["minutes"].idxmax()]
    print(f"busiest month: {busiest['month']}, {busiest['minutes']:,.1f} minutes")


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# Expected output:
#
#   loaded   2223 rows from plays_messy.csv
#   cleaned  2183 rows
#   analysed    8 genres
#   wrote   output/genre_summary.csv
#   wrote   output/genre_minutes.png
#   checked  the file agrees with the cleaned plays
#   analysed   24 months
#   wrote   output/minutes_by_month.csv
#   wrote   output/minutes_by_month.png
#   checked  the monthly file agrees with the cleaned plays
#   top genre: Electronic, 2,753.2 minutes
#   busiest month: 2024-10, 531.2 minutes
#
# Why a line chart this time: the months are in order and the question is
# about change, so the eye should follow a line. Genres have no order, so
# they get bars. (Session 9: bar versus line.)
#
# What the line shows: a dip every summer. The three quietest months are
# all in summer 2025 (July 219.6, August 230.5, June 231.1 minutes), and
# 2024 dips in the same place. Same shape as the play counts in the
# session 4 stretch, which is a good sign: two routes, one story.
#
# set_ylim(bottom=0) matters. Without it matplotlib starts the axis near
# the lowest month, and a dip of a third looks like a collapse.
