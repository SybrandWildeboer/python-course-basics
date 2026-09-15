"""HOMEWORK 1: write a filtered CSV, worked solution.

Keeps every play longer than five minutes.

    python3 sessions/session-04/homework/solutions/filter_plays.py
"""

import csv
import os

PLAYS = "data/clean/plays.csv"
OUT = "output/long_plays.csv"
THRESHOLD_MINUTES = 5.0


def load_rows(path):
    """Return the CSV at path as a list of dictionaries."""
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def longer_than(rows, minutes):
    """Return only the rows whose minutes_played is above minutes."""
    kept = []
    for row in rows:
        if float(row["minutes_played"]) > minutes:      # text -> number first
            kept.append(row)
    return kept


def write_rows(path, rows):
    """Write rows to a CSV at path, with a header, using the same columns."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


rows = load_rows(PLAYS)
kept = longer_than(rows, THRESHOLD_MINUTES)

print(f"{len(rows)} rows in")
print(f"{len(kept)} rows out ({len(kept) / len(rows) * 100:.1f}%)")

write_rows(OUT, kept)
print(f"wrote {OUT}")


# ---------------------------------------------------------------------------
# Expected: 2183 rows in, 732 rows out (33.5%).
#
# Two things worth noticing:
#
# 1. float() is not optional. Without it you are comparing text to a number,
#    and Python refuses with a TypeError. Even if it did not, text sorts
#    alphabetically: "10.5" < "9.0" is True, which would be quietly wrong.
#
# 2. write_rows takes rows[0].keys() as the column order, so it never needs
#    to know which columns this particular file has. The same function
#    writes any list of dictionaries, which is why it is worth being a
#    function at all.
#
#    It does assume the list is not empty. If your filter matches nothing,
#    rows[0] raises an IndexError. Worth a guard clause if you are feeling
#    thorough:  if not rows: print("nothing matched"); return
