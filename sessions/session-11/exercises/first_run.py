"""Session 11 live exercise, part 2: your data, your first number.

The script version of notebooks/02-first-run-exercise.ipynb. Fill in the TODOs, then run it
from any folder:

    python sessions/session-11/exercises/first_run.py

When it prints your rough answer, move the same code into project/pipeline.py: the steps are
in the notebook, part 3, and on the slides.
"""

from pathlib import Path

import pandas as pd

# Paths start from this file, as in session 10, so it runs from any folder.
# parents[0] is exercises, [1] session-11, [2] sessions, [3] the repository root.
ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = ROOT / "project" / "data" / "YOUR-FILE-NAME.csv"      # TODO: your file


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
    """Read the data file into a DataFrame."""
    # TODO: add sep=";", decimal="," or encoding="cp1252" if your file needs them
    return pd.read_csv(path)


def rough_answer(df):
    """Return the rough version of the must output: one number, or a small table."""
    # TODO: a filter, a value_counts, or a groupby. About fifteen lines at most.
    return None


def main():
    if not DATA_PATH.exists():
        print(f"{DATA_PATH} does not exist. Is the name right, extension and all?")
        print("What is in project/data:", [p.name for p in DATA_PATH.parent.glob("*")])
        return

    raw = load(DATA_PATH)
    first_look(raw)              # TODO: pass date_column="..." if you have one
    print()

    answer = rough_answer(raw)
    print(answer)

    # TODO: one assert that checks the answer against something you know independently
    # TODO: print the answer as a sentence, with :.1f or :, in an f-string


if __name__ == "__main__":
    main()
