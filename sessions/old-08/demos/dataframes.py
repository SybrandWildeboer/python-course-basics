"""The session 8 walkthrough, part one: DataFrames.

Run it from the repository root, or the relative paths will not find the data:

    python3 sessions/session-08/demos/dataframes.py

In a notebook the last line of a cell displays itself. In a script nothing
appears unless you print it, which is why every look below is a print().
"""

import sqlite3

import pandas as pd

# Wide enough that a nine-column table prints on one line in a terminal.
pd.set_option("display.width", 120)


# ------------------------------------------- the shape you already know
# A list of dictionaries was a table in session 4. Hand it to pandas.
rows = [
    {"genre": "Folk", "minutes": 4.65},
    {"genre": "Jazz", "minutes": 7.10},
    {"genre": "Folk", "minutes": 2.42},
]
print(pd.DataFrame(rows))


# ------------------------------------------- loading, and the first looks
# No open(), no encoding, no list() around a reader.
plays = pd.read_csv("data/clean/plays.csv")

print(plays.head())          # the first five rows
print(plays.shape)           # (2183, 9): rows, columns
plays.info()                 # info() prints by itself
print(plays.dtypes)          # minutes_played is float64: converted for you


# ------------------------------------------- columns
print(plays["genre"].head())                          # one column: a Series
print(plays[["track_name", "minutes_played"]].head(3))  # a list of names: a DataFrame

# The session 4 float() loop, in one word.
print(round(plays["minutes_played"].sum(), 1))        # 8980.4


# ------------------------------------------- filtering rows
long_ones = plays["minutes_played"] > 9               # one True/False per row
print(long_ones.sum())                                # 32: True counts as 1
print(plays[long_ones].head())

# plays[(a) and (b)]  ->  ValueError: The truth value of a Series is ambiguous
# plays[a == x & b >= y]  ->  TypeError, because & happens before == and >=

speaker_2025 = (plays["device"] == "speaker") & (plays["played_at"] >= "2025-01-01")
print(speaker_2025.sum())                             # 174

# The one that runs and is wrong: & is worked out before |.
right = (plays["minutes_played"] > 5) & ((plays["device"] == "phone") | (plays["device"] == "laptop"))
wrong = (plays["minutes_played"] > 5) & (plays["device"] == "phone") | (plays["device"] == "laptop")
print(right.sum(), "with the extra brackets")          # 523
print(wrong.sum(), "without them")                     # 871: any laptop play at all

print(plays["device"].isin(["car", "tablet"]).sum())  # 284, the IN (...) of pandas


# ------------------------------------------- sorting
# sort_values returns a NEW table and leaves plays alone. Keep it by naming it.
longest = plays.sort_values("minutes_played", ascending=False)
print(longest.head(3))


# ------------------------------------------- counting and grouping
# Session 4's counting dictionary, session 6's GROUP BY genre. Same numbers.
print(plays["genre"].value_counts())

print(plays.groupby("genre")["minutes_played"].sum())

per_genre = plays.groupby("genre").agg(
    plays=("play_id", "count"),
    minutes=("minutes_played", "sum"),
    avg_min=("minutes_played", "mean"),
)
print(per_genre.sort_values("avg_min", ascending=False).round(2))   # Jazz 6.57 on top

# HAVING is just a filter on the line after the groupby.
print(per_genre[per_genre["plays"] > 300])


# ------------------------------------------- from the database
con = sqlite3.connect("data/music.db")
db_plays = pd.read_sql("SELECT * FROM plays", con)        # artist_id, no names
artists = pd.read_sql("SELECT * FROM artists", con)
print(db_plays.shape, artists.shape)

# Any SQL you like: let the database group, and bring back only the answer.
print(pd.read_sql("SELECT device, COUNT(*) AS plays FROM plays "
                  "GROUP BY device ORDER BY plays DESC", con))
con.close()


# ------------------------------------------- merge is JOIN
named = db_plays.merge(artists, on="artist_id")           # JOIN ... USING (artist_id)
print(len(db_plays), "rows before,", len(named), "after")  # 2183 and 2183: good
print(named[["played_at", "artist_name", "track_name", "country"]].head())

everyone = artists.merge(db_plays, on="artist_id", how="left")   # LEFT JOIN
print(len(everyone), "rows")                                      # 2185
print(everyone[everyone["play_id"].isna()][["artist_name", "genre"]])
# Iron Fernway and Gravel Choir. NaN is pandas' NULL, and isna() is IS NULL.
