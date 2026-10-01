"""LIVE EXERCISE: from a notebook-shaped script to a pipeline, worked solution.

The question: which device do I skip most on?

    load  ->  clean  ->  analyse  ->  save  ->  check

Run it from anywhere:

    python sessions/session-10/solutions/device_pipeline.py
    cd sessions/session-10 && python solutions/device_pipeline.py

It writes output/device_skip_rate.csv and output/device_skip_rate.png at the
repository root, whichever folder you ran it from.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# parents[0] is solutions, [1] session-10, [2] sessions, [3] the repo root.
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


def skip_rate_by_device(plays):
    """Return one row per device: plays, skipped, and the skip rate in percent.

    Every device is kept, "unknown" included, so the table still adds up to
    every play. Leaving things out is a job for the chart, not the numbers.
    """
    rates = (plays.groupby("device")
             .agg(plays=("play_id", "count"), skipped=("skipped", "sum"))
             .reset_index())
    rates["skip_rate"] = (rates["skipped"] / rates["plays"] * 100).round(1)
    return rates.sort_values("skip_rate", ascending=False).reset_index(drop=True)


# --------------------------------------------------------------------- save


def save_csv(table, path):
    """Write a table to path as a CSV, making the folder if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(path, index=False)


def save_chart(rates, path):
    """Draw the skip rate per real device as a bar chart, titled with the answer."""
    known = rates[rates["device"] != "unknown"]
    top = known.iloc[0]

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.barh(known["device"], known["skip_rate"], color="#4f6ddb")
    ax.invert_yaxis()
    ax.bar_label(bars, labels=[f"{r:.1f}%" for r in known["skip_rate"]], padding=3)
    ax.set_title(f"The {top['device']} gets skipped most: {top['skip_rate']:.1f}% of plays")
    ax.set_xlabel("plays skipped, %")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()

    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)


# -------------------------------------------------------------------- check


def check_rates(path, plays):
    """Read the written CSV back and confirm it agrees with the cleaned plays."""
    back = pd.read_csv(path)
    assert back["plays"].sum() == len(plays), "plays went missing on the way"
    assert back["skipped"].sum() == plays["skipped"].sum(), "skips went missing"


# --------------------------------------------------------------------- main


def main():
    """Run the pipeline. The outer layer: the only function that prints."""
    raw = load_messy(MESSY)
    plays = clean_plays(raw)
    rates = skip_rate_by_device(plays)

    csv_path = OUTPUT / "device_skip_rate.csv"
    png_path = OUTPUT / "device_skip_rate.png"
    save_csv(rates, csv_path)
    save_chart(rates, png_path)
    check_rates(csv_path, plays)

    print(f"{len(raw)} rows in, {len(plays)} after cleaning")
    print(rates.to_string(index=False))
    print(f"wrote {csv_path.relative_to(ROOT).as_posix()} "
          f"and {png_path.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# Expected output:
#
#   2223 rows in, 2183 after cleaning
#    device  plays  skipped  skip_rate
#   unknown     69       11       15.9
#   speaker    326       46       14.1
#    tablet    101       14       13.9
#    laptop    510       58       11.4
#     phone   1004      111       11.1
#       car    173       18       10.4
#   wrote output/device_skip_rate.csv and output/device_skip_rate.png
#
# Look at the top row. The device with the highest skip rate is "unknown":
# 69 plays whose device was blank in the messy file, which clean_plays
# labelled for us. It is not a device. It is a category made by a cleaning
# decision, and it came top. That is why the chart leaves it out while the
# CSV keeps it: the table has to add up to every play, the chart has to
# answer the question about devices.
#
# Where the data allows it, check against the clean file: there the speaker
# is 14.0% and the car 10.6%. Same order, slightly different numbers, because
# the 69 unknown plays are spread over real devices that we cannot recover.
#
# The structure is the point of the exercise, not the numbers:
#   * each step is a function you can call and check on its own, in a notebook
#   * only main() prints; the others return or write
#   * paths come from __file__, so the folder you run it from does not matter
#   * the check reads the file back, so a run that "worked" has to prove it
