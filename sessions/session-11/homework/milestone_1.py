"""Session 11 homework: milestone 1 of your project. It loads, it cleans, and you can prove it.

The script version of notebooks/03-milestone-1-homework.ipynb. Work it out here (or in the
notebook), then move the functions into project/pipeline.py. Run it from any folder:

    python sessions/session-11/homework/milestone_1.py
"""

from pathlib import Path

import pandas as pd

# Paths start from this file, as in session 10, so it runs from any folder.
# parents[0] is homework, [1] session-11, [2] sessions, [3] the repository root.
ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = ROOT / "project" / "data" / "YOUR-FILE-NAME.csv"      # TODO: your file
NEEDED = ["TODO", "your", "columns"]


def logged(df, *steps):
    """Run each step on df in turn, print rows before and after each, return the result."""
    # *steps means "any number of arguments, collected into a tuple".
    # Each one is a function, and step.__name__ is that function's name as text.
    print(f"{'start':32} {len(df):>7,} rows")
    for step in steps:
        before = len(df)
        df = step(df)
        dropped = before - len(df)
        print(f"{step.__name__:32} {len(df):>7,} rows   ({dropped:,} dropped)")
    return df


# TODO: your cleaning steps, one small function each, every one returning a DataFrame.
# def keep_needed_columns(df):
#     """Keep only the columns the question uses."""
#     return df[NEEDED].copy()


def clean(df):
    """Clean the data, printing one line per step."""
    return logged(df)          # TODO: logged(df, keep_needed_columns, ...)


def find_problems(df):
    """Return a list of problems with the cleaned data, as sentences. Empty means fine."""
    problems = []

    missing_columns = [c for c in NEEDED if c not in df.columns]
    if missing_columns:
        problems.append(f"missing columns: {missing_columns}")
        return problems

    # TODO: missing values, numbers that are numbers and in range, dates, duplicates

    return problems


def analyse(df):
    """Return the must output."""
    # TODO
    return None


def main():
    if not DATA_PATH.exists():
        print(f"{DATA_PATH} does not exist. Is the name right, extension and all?")
        return

    raw = pd.read_csv(DATA_PATH)       # TODO: the read_csv arguments your file needs

    print("problems in the raw data:", find_problems(raw))
    print()

    cleaned = clean(raw)
    problems = find_problems(cleaned)
    assert not problems, problems

    result = analyse(cleaned)
    print(result)

    # TODO: two asserts, two routes to the same number


if __name__ == "__main__":
    main()
