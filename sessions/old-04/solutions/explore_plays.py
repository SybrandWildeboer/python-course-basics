"""LIVE EXERCISE: exploring the listening log, worked solution.

    python3 sessions/session-04/solutions/explore_plays.py
"""

import csv

PLAYS = "data/clean/plays.csv"


def load_rows(path):
    """Return the CSV at path as a list of dictionaries, one per row."""
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def count_by(rows, column):
    """Return a dictionary of how many rows fall into each value of column.

    This is the counting pattern: the accumulate idea from session 2, with a
    dictionary in place of a single running total.
    """
    counts = {}
    for row in rows:
        value = row[column]
        counts[value] = counts.get(value, 0) + 1
    return counts


def total_minutes(rows):
    """Return the total of the minutes_played column as a number."""
    total = 0.0
    for row in rows:
        total += float(row["minutes_played"])   # text -> number, every time
    return total


def count_skipped(rows):
    """Return how many rows were skipped.

    The column holds the text "1" or "0", so compare against a string. Using
    float(row["skipped"]) == 1 would work too; comparing text is clearer here.
    """
    skipped = 0
    for row in rows:
        if row["skipped"] == "1":
            skipped += 1
    return skipped


def show_counts(title, counts):
    """Print a dictionary of counts as an aligned table, biggest first."""
    print(f"\n{title}")
    for key, number in sorted(counts.items(), key=lambda pair: pair[1], reverse=True):
        print(f"  {key:12} {number:>5}")


rows = load_rows(PLAYS)

# 1. the total number of plays
print(f"{len(rows)} plays in the log")

# 2. plays per device
show_counts("plays per device", count_by(rows, "device"))

# 3. total minutes
print(f"\n{total_minutes(rows):,.0f} minutes listened in total")

# 4. skipped plays, and the percentage
skipped = count_skipped(rows)
print(f"{skipped} plays skipped, {skipped / len(rows) * 100:.1f}% of the total")

# The same function answers a question it was not written for, which is the
# whole argument for writing it as a function in the first place.
show_counts("plays per genre", count_by(rows, "genre"))


# ---------------------------------------------------------------------------
# Expected output:
#
#   2183 plays in the log
#
#   plays per device
#     phone         1039
#     laptop         524
#     speaker        336
#     car            179
#     tablet         105
#
#   8,980 minutes listened in total
#   258 plays skipped, 11.8% of the total
#
# Note that count_by takes the column NAME as an argument, so one function
# answers "per device", "per genre" and "per country". If you wrote three
# near-identical functions instead, that is a completely reasonable first
# draft; spotting that they differ by one word is the refactor to make.
