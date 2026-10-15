"""HOMEWORK 2: two real questions, worked solution.

    python3 sessions/session-04/homework/solutions/questions.py
"""

import csv

PLAYS = "data/clean/plays.csv"


def load_rows(path):
    """Return the CSV at path as a list of dictionaries."""
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def average_minutes_by_genre(rows):
    """Return a dictionary of genre -> average minutes per play.

    This is the two-dictionary shape the homework hint is about: one counts
    the plays, one sums the minutes, and the answer is one divided by the
    other. In SQL this whole function is:

        SELECT genre, AVG(minutes_played) FROM ... GROUP BY genre
    """
    plays = {}
    minutes = {}

    for row in rows:
        genre = row["genre"]
        plays[genre] = plays.get(genre, 0) + 1
        minutes[genre] = minutes.get(genre, 0.0) + float(row["minutes_played"])

    averages = {}
    for genre in plays:
        averages[genre] = minutes[genre] / plays[genre]
    return averages


def plays_by_artist(rows, year=None):
    """Return a dictionary of artist -> play count, optionally for one year.

    The dates are text like "2025-04-17", so a year filter is just a check on
    how the string starts.
    """
    counts = {}
    for row in rows:
        if year is not None and not row["played_at"].startswith(str(year)):
            continue
        artist = row["artist_name"]
        counts[artist] = counts.get(artist, 0) + 1
    return counts


def top(counts, n=5):
    """Return the n highest (key, value) pairs, biggest first."""
    return sorted(counts.items(), key=lambda pair: pair[1], reverse=True)[:n]


rows = load_rows(PLAYS)

# --- question 1 -----------------------------------------------------------
averages = average_minutes_by_genre(rows)
print("Average minutes per play, by genre:\n")
for genre, mean in top(averages, n=len(averages)):
    print(f"  {genre:12} {mean:>6.2f}")

winner, best = top(averages, n=1)[0]
print(f"\n{winner} has the longest average play, at {best:.2f} minutes.")

# --- question 2 -----------------------------------------------------------
counts_2025 = plays_by_artist(rows, year=2025)
print("\nMost played artists in 2025:\n")
for artist, number in top(counts_2025):
    print(f"  {artist:24} {number:>4}")

artist, number = top(counts_2025, n=1)[0]
print(f"\n{artist} was the most played artist of 2025, with {number} plays.")


# ---------------------------------------------------------------------------
# Why the average matters, and the trap in question 1
#
# Electronic has by far the most plays and the most total minutes, so if you
# answer with SUM instead of AVG you get Electronic and it looks convincing.
# On the average, Jazz wins comfortably: far fewer plays, but much longer
# ones. "Highest total" and "highest average" are different questions, and
# reaching for the wrong one is the most common way to produce a confident
# wrong answer in data work.
#
# The year filter is worth a second look too. Filtering INSIDE the loop, with
# continue, means the count only ever sees 2025 rows. The alternative is to
# build a filtered list first and then count it:
#
#     rows_2025 = [r for r in rows if r["played_at"].startswith("2025")]
#     counts = plays_by_artist(rows_2025)
#
# Both are fine. The second reads better once you are comfortable with list
# comprehensions, and it is closer to how you will write it in pandas.
#
# One more thing, which is real and not planted: in 2025 Glass Tram and Sara
# Lindqvist are tied on 115 plays each. sorted() has to put one of them
# first, and it picks whichever it happened to meet first in the data, so
# "the most played artist of 2025" has an arbitrary winner.
#
# That is worth catching. Printing the top five makes the tie visible, while
# printing only the winner hides it completely. When a single answer comes
# out of a ranking, it is always worth a glance at second place to see how
# close it was.
