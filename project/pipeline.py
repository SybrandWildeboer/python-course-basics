"""Your project pipeline: load -> clean -> analyse -> save.

Out of the box it answers one question about the course's music data: which
genre do I spend most of my listening time on? It is the session 10 pipeline,
and it is here so you start from something that runs, not from a blank file.

Run it from anywhere, ideally with the project's virtual environment active:

    python project/pipeline.py          (from the repository root)
    python pipeline.py                  (from inside project/)

It writes into project/output/, which git ignores:

    output/summary.csv     the table that answers the question
    output/chart.png       the chart that answers the question

To make it yours, work down the file and change each place marked
MAKE IT YOURS. Change one stage at a time, and run the whole thing after
each change. A pipeline that ran five minutes ago is easy to fix.
"""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------------------------------------------- settings
# Every path starts from the folder this file is in, so the script works
# from any folder you run it in.
PROJECT = Path(__file__).resolve().parent
OUTPUT = PROJECT / "output"

# MAKE IT YOURS: put your file in project/data/ and point INPUT at it, e.g.
#     INPUT = PROJECT / "data" / "my_export.csv"
INPUT = PROJECT.parent / "data" / "messy" / "plays_messy.csv"

# MAKE IT YOURS: the question, in one sentence. It goes in your README too.
QUESTION = "Which genre do I spend most of my listening time on?"


# --------------------------------------------------------------------- load


def load(path):
    """Return the raw data at path as a DataFrame, exactly as it is on disk.

    MAKE IT YOURS: a CSV with a semicolon needs sep=";". JSON needs
    pd.read_json. Excel needs pd.read_excel, which also needs the openpyxl
    package: it is not in requirements.txt, so install it and add it there.
    """
    return pd.read_csv(path)


# -------------------------------------------------------------------- clean


def parse_dates(text):
    """Return a column of date text as real dates, trying each known format."""
    dates = pd.to_datetime(text, format="%Y-%m-%d", errors="coerce")
    dates = dates.fillna(pd.to_datetime(text, format="%d/%m/%Y", errors="coerce"))
    dates = dates.fillna(pd.to_datetime(text, format="%d-%m-%Y", errors="coerce"))
    return dates


def parse_minutes(text):
    """Return a column like "4.65", "1 234.50" or "4.2 min" as numbers."""
    cleaned = text.str.replace(" min", "", regex=False).str.replace(" ", "", regex=False)
    return pd.to_numeric(cleaned, errors="coerce")


def clean(df):
    """Return a cleaned copy of the raw data, ready to analyse.

    MAKE IT YOURS: this is the stage that changes most. Look at your data in
    notebooks/explore.ipynb first, write down every problem you find, and
    fix them here one at a time. Write each decision in this docstring, the
    way the music version does below, because each one changes the answer.

    The decisions for the music data:
      * the column "minutes played " gets its proper name back
      * exact duplicate rows go
      * genre and device lose stray spaces and get one spelling each
      * dates and minutes become real dates and numbers
      * a missing genre or country is filled in from the same artist's
        other plays, because every artist has exactly one of each
      * a missing device becomes "unknown"; missing minutes stay missing
    """
    df = df.rename(columns={"minutes played ": "minutes_played"})
    df = df.drop_duplicates().copy()

    df["genre"] = df["genre"].str.strip().str.title()
    df["device"] = df["device"].str.strip().str.lower()
    df["played_at"] = parse_dates(df["played_at"])
    df["minutes_played"] = parse_minutes(df["minutes_played"])

    for column in ["genre", "country"]:
        # Fill only the gaps: a value that is already there is never replaced.
        known = df.groupby("artist_name")[column].transform("first")
        df[column] = df[column].fillna(known)
    df["device"] = df["device"].fillna("unknown")

    return df.sort_values("play_id").reset_index(drop=True)


# ------------------------------------------------------------------ analyse


def analyse(data):
    """Return the table that answers QUESTION: one row per genre.

    MAKE IT YOURS: group by the thing your question is about, and add up,
    count or average the thing you want to know. It returns a table; it
    never prints and never writes, so you can check it in a notebook.
    """
    summary = (data.groupby("genre")
               .agg(plays=("play_id", "count"),
                    minutes=("minutes_played", "sum"),
                    average_minutes=("minutes_played", "mean"))
               .sort_values("minutes", ascending=False)
               .reset_index())
    return summary.round({"minutes": 1, "average_minutes": 2})


# --------------------------------------------------------------------- save


def save_csv(summary, path):
    """Write the summary table to path as a CSV, making the folder if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(path, index=False)


def save_chart(summary, path):
    """Draw the answer as a bar chart, with the answer as its title.

    MAKE IT YOURS: change the two column names and the title. A title that
    states the answer ("Electronic gets 32.0% ...") beats one that names
    the topic ("Minutes per genre").
    """
    label_column, value_column = "genre", "minutes"
    top = summary.iloc[0]
    share = top[value_column] / summary[value_column].sum() * 100

    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.barh(summary[label_column], summary[value_column], color="#4f6ddb")
    ax.invert_yaxis()                                # biggest at the top
    ax.bar_label(bars, labels=[f"{v:,.1f}" for v in summary[value_column]], padding=3)
    ax.set_title(f"{top[label_column]} gets {share:.1f}% of my listening time")
    ax.set_xlabel("minutes played")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()

    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)


# -------------------------------------------------------------------- check


def check(path, data):
    """Read the written CSV back and stop the run if it disagrees with the data.

    MAKE IT YOURS: keep at least one check that compares a total in the file
    with the same total worked out from the cleaned data.
    """
    back = pd.read_csv(path)
    assert back["plays"].sum() == len(data), "rows went missing on the way"


# --------------------------------------------------------------------- main


def main():
    """Run every stage in order. The outer layer, and the only part that prints.

    It prints a line after each stage, so you can see how far a run got and
    how many rows each stage left. If cleaning suddenly drops half the rows,
    you see it here, before the chart quietly shows the wrong thing.
    """
    matplotlib.use("Agg")      # draw charts straight into files, never open a window
    print(QUESTION)

    raw = load(INPUT)
    print(f"  loaded   {len(raw):>5} rows from {INPUT.name}")
    data = clean(raw)
    print(f"  cleaned  {len(data):>5} rows")
    summary = analyse(data)
    print(f"  analysed {len(summary):>5} rows in the summary")

    csv_path = OUTPUT / "summary.csv"
    png_path = OUTPUT / "chart.png"
    save_csv(summary, csv_path)
    print(f"  wrote    {csv_path.relative_to(PROJECT).as_posix()}")
    save_chart(summary, png_path)
    print(f"  wrote    {png_path.relative_to(PROJECT).as_posix()}")
    check(csv_path, data)
    print("  checked  the summary adds up to the cleaned rows")


if __name__ == "__main__":
    main()
