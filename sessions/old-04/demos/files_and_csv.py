"""The session 4 walkthrough: files and the csv module.

Run it from the repository root, or the relative path will not find the data:

    python3 sessions/session-04/demos/files_and_csv.py
"""

import csv
import os

PLAYS = "data/clean/plays.csv"

# --------------------------------------------------- where am I, actually?
# First thing to print when you get a FileNotFoundError. The file is almost
# always fine; Python is just looking somewhere else.
print("working directory:", os.getcwd())


# ------------------------------------------- reading a CSV into dictionaries
# list(...) matters: without it you get a reader you can only walk through
# once, and a second loop over it silently does nothing at all.
with open(PLAYS, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print("rows:", len(rows))               # 2183
print("columns:", list(rows[0].keys()))
print("first row:", rows[0])
print("one value:", rows[0]["genre"])   # Folk

# Peek at a few rows rather than printing two thousand lines.
for row in rows[:3]:
    print(row["played_at"], row["artist_name"], row["minutes_played"])


# ------------------------------------------- everything arrives as text
print(type(rows[0]["minutes_played"]))  # <class 'str'>

# total = 0
# for row in rows:
#     total += row["minutes_played"]    # TypeError: int + str

total_minutes = 0.0
for row in rows:
    total_minutes += float(row["minutes_played"])   # convert, then add
print(f"total: {total_minutes:,.0f} minutes")


# ------------------------------------------- the counting pattern
# The accumulate pattern from session 2, with a dictionary instead of one
# running total. In session 6 this same question is GROUP BY genre.
counts = {}
for row in rows:
    genre = row["genre"]
    counts[genre] = counts.get(genre, 0) + 1

for genre, n in sorted(counts.items(), key=lambda pair: pair[1], reverse=True):
    print(f"{genre:12} {n:>5}")


# ------------------------------------------- writing a CSV back out
os.makedirs("output", exist_ok=True)     # "w" fails if the folder is missing

# A list comprehension: build a new list from an old one, keeping matches.
# The same thing as a for loop with an append, on one line.
jazz = [row for row in rows if row["genre"] == "Jazz"]
print("jazz rows:", len(jazz))           # 154

with open("output/jazz.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(jazz)

print("wrote output/jazz.csv")

# Three arguments worth remembering on that open():
#   "w"           write, and it replaces the file without asking
#   newline=""    stops blank lines between rows on Windows
#   encoding=     so accented names survive the round trip
