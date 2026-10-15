"""The session 9 cleaning steps, written as two functions.

Run it from the repository root:

    python sessions/session-09/solutions/cleaning.py

Everything the walkthrough did one cell at a time ends up here, in the shape
session 10 reuses: one function that loads, one that cleans. They follow the
session 3 rule. They calculate and return; only the bottom of the file prints.

    raw = load_messy("data/messy/plays_messy.csv")
    plays = clean_plays(raw)

clean_plays returns the same nine columns, in the same order and with the
same types, as data/clean/plays.csv read with pd.read_csv. So anything you
wrote for the clean file in session 8 works on the cleaned messy file too.
"""

import pandas as pd

MESSY = "data/messy/plays_messy.csv"
CLEAN = "data/clean/plays.csv"

# The column order of data/clean/plays.csv.
COLUMNS = [
    "play_id", "played_at", "artist_name", "track_name", "genre",
    "country", "minutes_played", "device", "skipped",
]

# The three ways a date is written in the messy file, tried in this order.
DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]


def load_messy(path):
    """Return the messy CSV at path as a DataFrame, with nothing guessed.

    keep_default_na=False stops pandas turning "NA" and empty cells into
    missing values on its own. Every text column arrives exactly as it was
    written, and clean_plays decides what counts as missing.
    """
    return pd.read_csv(path, keep_default_na=False)


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


if __name__ == "__main__":
    raw = load_messy(MESSY)
    plays = clean_plays(raw)
    clean = pd.read_csv(CLEAN)

    print(f"messy file:   {len(raw):,} rows")
    print(f"after clean:  {len(plays):,} rows, the clean file has {len(clean):,}")

    # Same columns, same types, same play_ids.
    assert list(plays.columns) == list(clean.columns)
    assert (plays.dtypes == clean.dtypes).all()
    assert plays["play_id"].equals(clean["play_id"])

    print("\ncells that match the clean file, per column:")
    for column in COLUMNS:
        same = (plays[column] == clean[column]).sum()
        print(f"  {column:15} {same:>5} of {len(clean)}")

    lost = clean.loc[plays["minutes_played"].isna(), "minutes_played"].sum()
    print(f"\ntotal minutes: {plays['minutes_played'].sum():,.1f} "
          f"(clean file {clean['minutes_played'].sum():,.1f})")
    print(f"the gap is the {plays['minutes_played'].isna().sum()} plays with no minutes, "
          f"which in the clean file add up to {lost:.1f}")

    assert len(plays) == 2183
    assert plays["minutes_played"].isna().sum() == 94
    assert (plays["device"] == "unknown").sum() == 69


# ---------------------------------------------------------------------------
# What comes out, and why it is not identical to the clean file
#
#     messy file:   2,223 rows
#     after clean:  2,183 rows, the clean file has 2,183
#
# Seven of the nine columns match the clean file in every one of the 2,183
# rows: every date, every genre and every country came back. Two cannot:
#
#   * minutes_played: 94 plays had a blank. The number is gone, and no
#     amount of cleaning brings it back. NaN says "unknown" honestly; 0 would
#     say "listened for no time at all", which is a different, false claim.
#   * device: 69 plays had a blank, and they are now "unknown". Same idea:
#     a label of their own, so they are still counted and still visible.
#
# Cleaning recovers what the file still knows (the genre is on the artist's
# other rows) and labels what it does not. It never makes things up.
