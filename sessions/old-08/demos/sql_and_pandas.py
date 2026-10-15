"""The session 8 walkthrough, part two: four queries, in SQL and in pandas.

Run it from the repository root:

    python3 sessions/session-08/demos/sql_and_pandas.py

Each pair ends with an assert that both languages gave the same answer. If
this script finishes, every number on the slides is true.
"""

import sqlite3

import pandas as pd

pd.set_option("display.width", 120)

con = sqlite3.connect("data/music.db")


def sql(query):
    """Run a query against music.db and return the result as a DataFrame."""
    return pd.read_sql(query, con)


plays = sql("SELECT * FROM plays")
artists = sql("SELECT * FROM artists")
awards = sql("SELECT * FROM awards")


# ===================================================== 1. filter and sort
# Session 6 ladder, rungs 4 and 5: speaker plays in 2025, longest first.
in_sql = sql("""
SELECT played_at, track_name, minutes_played
FROM plays
WHERE device = 'speaker'
  AND played_at BETWEEN '2025-01-01' AND '2025-12-31'
ORDER BY minutes_played DESC
""")

in_pandas = (
    plays[(plays["device"] == "speaker") & (plays["played_at"] >= "2025-01-01")]
    .sort_values("minutes_played", ascending=False)
    [["played_at", "track_name", "minutes_played"]]
)

assert len(in_sql) == len(in_pandas) == 174
assert list(in_sql["minutes_played"]) == list(in_pandas["minutes_played"])
print("1. both give 174 rows; longest:", in_pandas.iloc[0]["track_name"])   # Northern Lines


# ===================================================== 2. HAVING
# Session 6 ladder, rung 10: devices with more than 300 plays.
in_sql = sql("""
SELECT device, COUNT(*) AS plays
FROM plays
GROUP BY device
HAVING COUNT(*) > 300
ORDER BY plays DESC
""")

per_device = plays["device"].value_counts()
in_pandas = per_device[per_device > 300]          # no HAVING: just filter the counts

assert list(in_sql["device"]) == list(in_pandas.index) == ["phone", "laptop", "speaker"]
print("2. both give", list(in_pandas.index))


# ===================================================== 3. LEFT JOIN, COUNT
# Session 7: every artist, including the two never played.
in_sql = sql("""
SELECT a.artist_name, COUNT(p.play_id) AS plays
FROM artists a
LEFT JOIN plays p USING (artist_id)
GROUP BY a.artist_id
ORDER BY plays
LIMIT 4
""")

everyone = artists.merge(plays, on="artist_id", how="left")        # 2185 rows
right = everyone.groupby("artist_name")["play_id"].count()         # COUNT(p.play_id)
wrong = everyone.groupby("artist_name").size()                     # COUNT(*)

assert right["Iron Fernway"] == 0 and wrong["Iron Fernway"] == 1
assert set(in_sql["artist_name"].head(2)) == {"Iron Fernway", "Gravel Choir"}
print("3. count() says 0, size() says 1, for an artist with no plays at all")


# ===================================================== 4. fan-out
true_total = round(plays["minutes_played"].sum(), 1)
with_awards = plays.merge(awards, on="artist_id")
fan_total = round(with_awards["minutes_played"].sum(), 1)

fan_sql = sql("""
SELECT ROUND(SUM(p.minutes_played), 1) AS total
FROM plays p JOIN awards w ON w.artist_id = p.artist_id
""")["total"][0]

assert true_total == 8980.4
assert fan_total == fan_sql == 9732.1
assert len(plays) == 2183 and len(with_awards) == 2371
print(f"4. {true_total} becomes {fan_total}; {len(plays)} rows become {len(with_awards)}")

# Fjord & Flint, artist 35: 237 plays x 3 awards = 711 rows.
fjord_after = with_awards[with_awards["artist_id"] == 35]
assert len(fjord_after) == 711

# The fake fixes. drop_duplicates() removes nothing, because every row carries
# a different award. De-duplicating the minutes is SUM(DISTINCT) again: 680.6.
assert len(with_awards.drop_duplicates()) == 2371
assert round(fjord_after["minutes_played"].drop_duplicates().sum(), 1) == 680.6

# The real fix: aggregate first (the CTE is now just a named variable), then merge.
per_artist = (
    plays.groupby("artist_id")
    .agg(plays=("play_id", "count"), minutes=("minutes_played", "sum"))
    .reset_index()
)
awards_per_artist = awards.groupby("artist_id").size().rename("awards").reset_index()

summary = (
    per_artist
    .merge(artists[["artist_id", "artist_name"]], on="artist_id", validate="one_to_one")
    .merge(awards_per_artist, on="artist_id", how="left", validate="one_to_one")
)
summary["awards"] = summary["awards"].fillna(0).astype(int)     # COALESCE(x, 0)

print(summary.sort_values("minutes", ascending=False).head(3).round(1))
fjord = summary[summary["artist_name"] == "Fjord & Flint"].iloc[0]
assert round(fjord["minutes"], 1) == 846.2 and fjord["awards"] == 3

# The guard SQL does not have: say what the relationship should be.
try:
    plays.merge(awards, on="artist_id", validate="many_to_one")
except pd.errors.MergeError as error:
    print("MergeError:", error)
# Merge keys are not unique in right dataset; not a many-to-one merge

con.close()
print("\nevery pair agreed")
