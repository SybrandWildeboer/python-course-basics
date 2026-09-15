"""The session 9 material as a script: clean the messy data, save two charts.

The notebook is the better tool for the cleaning itself, because you want to
look at the damage as you find it. This file is what the same work becomes
once you know what the steps are, and it is a step toward session 10.

Run it from the repository root:

    python3 sessions/session-09/demos/clean_and_chart.py

It writes two PNGs into output/.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")          # save files, do not try to open a window
import matplotlib.pyplot as plt
import pandas as pd

MESSY = "data/messy/plays_messy.csv"
OUTPUT = Path("output")

TEXT_COLUMNS = ["artist_name", "track_name", "genre", "country", "device"]


def load_messy(path=MESSY):
    """Return the messy CSV exactly as it arrives, with nothing fixed yet."""
    return pd.read_csv(path)


def report(df, label):
    """Print the shape and the missing-value counts of a table."""
    missing = df.isna().sum()
    missing = missing[missing > 0]
    print(f"\n{label}: {df.shape[0]} rows, {df.shape[1]} columns")
    if len(missing):
        print("  missing values:")
        for column, count in missing.items():
            print(f"    {column:16} {count:>5}")
    else:
        print("  no missing values")


def clean(df):
    """Return a cleaned copy of the messy listening log.

    Every step here corresponds to a specific piece of damage in the file, and
    the order matters: strip the whitespace before comparing text, and fix the
    types before doing arithmetic.
    """
    df = df.copy()

    # 1. One column name arrived with a trailing space, which is invisible
    #    and makes df["minutes_played"] raise a KeyError.
    df = df.rename(columns={"minutes played ": "minutes_played"})

    # 2. Strip stray whitespace, then settle on one capitalisation per column.
    for column in TEXT_COLUMNS:
        df[column] = df[column].str.strip()
    df["genre"] = df["genre"].str.title()      # POP, pop, " Pop " -> Pop
    df["device"] = df["device"].str.lower()

    # 3. Minutes arrived as text, some with a " min" suffix and some with a
    #    space as a thousands separator. errors="coerce" turns anything still
    #    unparseable into NaN rather than stopping the program.
    df["minutes_played"] = (df["minutes_played"]
                            .str.replace(" min", "", regex=False)
                            .str.replace(" ", "", regex=False))
    df["minutes_played"] = pd.to_numeric(df["minutes_played"], errors="coerce")

    # 4. Dates arrived in three formats. Parse each one explicitly and combine.
    #    See the notebook for why the convenient one-liner is worse than
    #    useless here: it silently reads 2025-09-06 as the 9th of June.
    raw = df["played_at"].str.strip()
    df["played_at"] = (
        pd.to_datetime(raw, format="%Y-%m-%d", errors="coerce")
        .fillna(pd.to_datetime(raw, format="%d/%m/%Y", errors="coerce"))
        .fillna(pd.to_datetime(raw, format="%d-%m-%Y", errors="coerce"))
    )

    # 5. Exact duplicate rows.
    df = df.drop_duplicates()

    # 6. A play with no duration cannot answer a question about minutes, so
    #    those rows go. This is a DECISION, not a rule: see the notebook.
    df = df.dropna(subset=["minutes_played"])

    # 7. Missing categories are kept, labelled, because losing a whole play
    #    because nobody recorded the device would be worse.
    df["device"] = df["device"].fillna("unknown")
    df["genre"] = df["genre"].fillna("Unknown")
    df["country"] = df["country"].fillna("Unknown")

    return df.reset_index(drop=True)


def chart_minutes_by_month(df, path):
    """Save a line chart of total minutes per month."""
    monthly = (df.set_index("played_at")["minutes_played"]
                 .resample("MS").sum())

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(monthly.index, monthly.values, marker="o", linewidth=2)

    ax.set_title("Listening drops off every summer")
    ax.set_xlabel("Month")
    ax.set_ylabel("Minutes played")
    ax.set_ylim(bottom=0)          # start at zero, so the shape is honest
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  wrote {path}")


def chart_minutes_by_genre(df, path):
    """Save a bar chart of total minutes per genre."""
    by_genre = (df.groupby("genre")["minutes_played"]
                  .sum()
                  .sort_values(ascending=False))

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(by_genre.index, by_genre.values)

    ax.set_title("Electronic accounts for almost a third of all listening")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Total minutes")
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  wrote {path}")


def main():
    messy = load_messy()
    report(messy, "as it arrived")

    cleaned = clean(messy)
    report(cleaned, "after cleaning")

    lost = len(messy) - len(cleaned)
    print(f"\n{lost} rows removed ({lost / len(messy) * 100:.1f}% of the file)")
    print(f"total minutes: {cleaned['minutes_played'].sum():,.1f}")

    OUTPUT.mkdir(exist_ok=True)
    print("\ncharts:")
    chart_minutes_by_month(cleaned, OUTPUT / "minutes_by_month.png")
    chart_minutes_by_genre(cleaned, OUTPUT / "minutes_by_genre.png")


if __name__ == "__main__":
    main()
