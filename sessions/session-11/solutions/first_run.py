"""Session 11 live exercise, part 2, worked: the first number for the worked example.

data/clean/plays.csv stands in for "my own file" here. Yours lives in project/data/.

    python sessions/session-11/solutions/first_run.py
"""

from pathlib import Path

import pandas as pd

DATA_PATH = Path("data/clean/plays.csv")


def first_look(df, date_column=None):
    """Print the four things to check on any new dataset."""
    print(f"rows: {len(df):,}   columns: {len(df.columns)}")
    print()
    print("types and missing values per column:")
    summary = pd.DataFrame({"type": df.dtypes, "missing": df.isna().sum()})
    print(summary)
    if date_column is not None:
        print()
        print(f"{date_column}: {df[date_column].min()} to {df[date_column].max()}")


def load(path):
    """Read the data file into a DataFrame. A plain comma-separated UTF-8 file needs no extras."""
    return pd.read_csv(path)


def rough_answer(df):
    """Return minutes per genre per year, with the change, smallest change first."""
    df = df.copy()
    df["year"] = df["played_at"].str[:4]
    table = df.groupby(["genre", "year"])["minutes_played"].sum().unstack("year").round(1)
    table["change"] = (table["2025"] - table["2024"]).round(1)
    return table.sort_values("change")


def main():
    if not DATA_PATH.exists():
        print(f"{DATA_PATH} does not exist. Run this from the repository root.")
        return

    raw = load(DATA_PATH)
    first_look(raw, date_column="played_at")
    print()

    answer = rough_answer(raw)
    print(answer)
    print()

    # Two routes to one number: the parts add up to the whole, and one cell by a filter.
    assert abs(answer[["2024", "2025"]].sum().sum() - raw["minutes_played"].sum()) < 0.5
    jazz_2025 = raw[(raw["genre"] == "Jazz") & (raw["played_at"].str[:4] == "2025")]
    assert round(jazz_2025["minutes_played"].sum(), 1) == answer.loc["Jazz", "2025"] == 533.2

    gained = answer["change"].idxmax()
    lost = answer["change"].idxmin()
    print(f"From 2024 to 2025 I listened to {gained} for "
          f"{answer.loc[gained, 'change']:.1f} minutes more, and to {lost} for "
          f"{-answer.loc[lost, 'change']:.1f} minutes less.")


if __name__ == "__main__":
    main()

# Expected last line:
#
#   From 2024 to 2025 I listened to Jazz for 54.0 minutes more, and to Electronic for
#   106.1 minutes less.
