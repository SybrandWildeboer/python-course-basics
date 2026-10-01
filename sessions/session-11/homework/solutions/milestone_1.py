"""Session 11 homework, worked: milestone 1 for the worked example.

data/clean/plays.csv stands in for "my own file". The shape is what matters: logged
cleaning steps, a list of problems, and two routes to one number.

    python sessions/session-11/homework/solutions/milestone_1.py
"""

from pathlib import Path

import pandas as pd

DATA_PATH = Path("data/clean/plays.csv")
OUT = Path("output") / "session-11"
NEEDED = ["play_id", "played_at", "genre", "minutes_played"]


def logged(df, *steps):
    """Run each step on df in turn, print rows before and after each, return the result."""
    print(f"{'start':32} {len(df):>7,} rows")
    for step in steps:
        before = len(df)
        df = step(df)
        dropped = before - len(df)
        print(f"{step.__name__:32} {len(df):>7,} rows   ({dropped:,} dropped)")
    return df


def keep_needed_columns(df):
    """Keep only the columns the question uses, plus the id that identifies a play."""
    return df[NEEDED].copy()


def parse_dates(df):
    """Turn played_at from text into real dates. Anything unreadable becomes NaT."""
    df = df.copy()
    df["played_at"] = pd.to_datetime(df["played_at"], format="%Y-%m-%d", errors="coerce")
    return df


def drop_incomplete_rows(df):
    """Drop rows missing a date, a genre or a number of minutes."""
    return df.dropna(subset=["played_at", "genre", "minutes_played"])


def keep_2024_and_2025(df):
    """Keep the two years the question compares, and add a year column."""
    df = df[df["played_at"].dt.year.isin([2024, 2025])].copy()
    df["year"] = df["played_at"].dt.year.astype(str)
    return df


def clean(df):
    """Clean the plays, printing one line per step."""
    return logged(df, keep_needed_columns, parse_dates, drop_incomplete_rows,
                  keep_2024_and_2025)


def find_problems(df):
    """Return a list of problems with the cleaned data, as sentences. Empty means fine."""
    problems = []

    missing_columns = [c for c in NEEDED if c not in df.columns]
    if missing_columns:
        problems.append(f"missing columns: {missing_columns}")
        return problems

    for column in NEEDED:
        n = df[column].isna().sum()
        if n:
            problems.append(f"{n} missing values in {column}")

    if not pd.api.types.is_numeric_dtype(df["minutes_played"]):
        problems.append("minutes_played is not a number column")
    else:
        out_of_range = ((df["minutes_played"] <= 0) | (df["minutes_played"] > 60)).sum()
        if out_of_range:
            problems.append(f"{out_of_range} plays outside 0 to 60 minutes")

    dates = pd.to_datetime(df["played_at"], format="%Y-%m-%d", errors="coerce")
    unreadable = dates.isna().sum() - df["played_at"].isna().sum()
    if unreadable:
        problems.append(f"{unreadable} dates not in YYYY-MM-DD form")
    months = dates.dt.strftime("%Y-%m").nunique()
    if months != 24:
        problems.append(f"dates cover {months} months, not the 24 the question needs")

    duplicated_ids = df["play_id"].duplicated().sum()
    if duplicated_ids:
        problems.append(f"{duplicated_ids} duplicated play_id values")

    return problems


def analyse(df):
    """Return minutes per genre per year, with the change, smallest change first."""
    result = df.groupby(["genre", "year"])["minutes_played"].sum().unstack("year").round(1)
    result["change"] = (result["2025"] - result["2024"]).round(1)
    return result.sort_values("change")


def main():
    raw = pd.read_csv(DATA_PATH)

    print("problems in the raw data:", find_problems(raw))
    print()

    cleaned = clean(raw)
    problems = find_problems(cleaned)
    assert not problems, problems
    print()

    result = analyse(cleaned)
    print(result)

    # Route 1: the parts add up to the whole (each cell was rounded, so allow a little).
    assert abs(result[["2024", "2025"]].sum().sum() - cleaned["minutes_played"].sum()) < 0.5
    # Route 2: one cell worked out with a filter instead of a groupby.
    folk = cleaned[(cleaned["genre"] == "Folk") & (cleaned["year"] == "2024")]
    assert round(folk["minutes_played"].sum(), 1) == result.loc["Folk", "2024"] == 832.3

    OUT.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUT / "genre_change.csv")
    print()
    print(f"both routes agree; wrote {OUT / 'genre_change.csv'}")


if __name__ == "__main__":
    main()

# Expected output, the start of it:
#
#   problems in the raw data: []
#
#   start                              2,183 rows
#   keep_needed_columns                2,183 rows   (0 dropped)
#   parse_dates                        2,183 rows   (0 dropped)
#   drop_incomplete_rows               2,183 rows   (0 dropped)
#   keep_2024_and_2025                 2,183 rows   (0 dropped)
#
# Nothing dropped: this is the clean file. Point DATA_PATH at data/messy/plays_messy.csv
# and the first line says: problems in the raw data: ["missing columns: ['minutes_played']"],
# because "minutes played " (with spaces) is not minutes_played. Then keep_needed_columns
# fails with KeyError: "['minutes_played'] not in index". The check told you why before
# the crash did. The fix is a rename step at the start of clean, as in session 9.
