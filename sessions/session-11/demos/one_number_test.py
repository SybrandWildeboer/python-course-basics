"""Session 11 walkthrough: from a scoped question to a first number.

The script version of notebooks/01-scoping-a-question.ipynb, on the worked example:
"Which genres did I listen to more in 2025 than in 2024, and which less?"

Run it from the repository root:

    python sessions/session-11/demos/one_number_test.py

It prints the first look, the table, the checks and the answer, and writes the table and a
rough chart to output/session-11/.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")             # a script saves its chart; it does not open a window
import matplotlib.pyplot as plt   # noqa: E402
import pandas as pd               # noqa: E402

PLAYS = Path("data/clean/plays.csv")
OUT = Path("output") / "session-11"


# --- step 1: the five-minute first look --------------------------------------

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


# --- the worked example, shaped like project/pipeline.py ----------------------

def load(path):
    """Read the plays CSV into a DataFrame."""
    return pd.read_csv(path)


def clean(df):
    """Keep the columns the question needs, and add a year column."""
    df = df[["played_at", "genre", "minutes_played"]].copy()
    df["year"] = df["played_at"].str[:4]
    return df


def analyse(df):
    """Return minutes per genre per year, with the change, smallest change first."""
    result = df.groupby(["genre", "year"])["minutes_played"].sum().unstack("year").round(1)
    result["change"] = (result["2025"] - result["2024"]).round(1)
    return result.sort_values("change")


def share_of_year(df):
    """Return each genre's share of each year's minutes, in percent, with the change."""
    minutes = df.groupby(["genre", "year"])["minutes_played"].sum().unstack("year")
    share = (minutes / minutes.sum() * 100).round(1)
    share["change"] = (share["2025"] - share["2024"]).round(1)
    return share.sort_values("change")


def chart(result, path):
    """Save a bar chart of the change per genre, with the answer in the title."""
    gained = result["change"].idxmax()
    lost = result["change"].idxmin()

    fig, ax = plt.subplots(figsize=(8, 4.5))
    colours = ["tab:red" if c < 0 else "tab:green" for c in result["change"]]
    ax.barh(result.index, result["change"], color=colours)
    ax.axvline(0, color="black", linewidth=0.8)
    for y, value in enumerate(result["change"]):
        ax.annotate(f"{value:+.1f}", (value, y), va="center",
                    ha="left" if value >= 0 else "right",
                    xytext=(4 if value >= 0 else -4, 0), textcoords="offset points")
    ax.set_title(f"{gained} grew most from 2024 to 2025, {lost} shrank most")
    ax.set_xlabel("change in minutes played, 2025 minus 2024")
    ax.set_xlim(-140, 90)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main():
    raw = load(PLAYS)
    first_look(raw, date_column="played_at")
    print()

    plays = clean(raw)
    result = analyse(plays)
    print(result)
    print()

    # Believe it, or not: the table must add up to the raw total.
    total_raw = raw["minutes_played"].sum()
    total_table = result["2024"].sum() + result["2025"].sum()
    print(f"raw total {total_raw:,.1f}, table total {total_table:,.1f}")
    assert abs(total_raw - total_table) < 0.5

    gained = result["change"].idxmax()
    lost = result["change"].idxmin()
    print(f"Most gained: {gained} ({result.loc[gained, 'change']:+.1f} minutes)")
    print(f"Most lost:   {lost} ({result.loc[lost, 'change']:+.1f} minutes)")
    assert (gained, lost) == ("Jazz", "Electronic")
    print()

    # The decision hiding in the question: minutes, or share of the year?
    share = share_of_year(plays)
    print("by share of each year's listening, in percent:")
    print(share)
    print(f"biggest loser by minutes: {lost}; by share: {share['change'].idxmin()}")
    assert share["change"].idxmin() == "Folk"

    OUT.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUT / "genre_change.csv")
    chart(result, OUT / "genre_change.png")
    print()
    print(f"wrote {OUT / 'genre_change.csv'} and {OUT / 'genre_change.png'}")


if __name__ == "__main__":
    main()

# Expected output, the parts that matter:
#
#   raw total 8,980.4, table total 8,980.5
#   Most gained: Jazz (+54.0 minutes)
#   Most lost:   Electronic (-106.1 minutes)
#   biggest loser by minutes: Electronic; by share: Folk
