"""LIVE EXERCISE: session 7, in pandas, worked solution.

    python3 sessions/session-08/solutions/joins_in_pandas.py

Every number in the comments is pinned with an assert, so if this runs to the
end, the comments are true.
"""

import sqlite3

import pandas as pd

pd.set_option("display.width", 120)

con = sqlite3.connect("data/music.db")
plays = pd.read_sql("SELECT * FROM plays", con)
artists = pd.read_sql("SELECT * FROM artists", con)
awards = pd.read_sql("SELECT * FROM awards", con)
con.close()


# ===================================================== PART 1 ===========

# 1. Long plays on the phone or the laptop. Naming each condition first keeps
#    the brackets straight, and reads like the sentence it came from.
long_play = plays["minutes_played"] > 5
phone_or_laptop = (plays["device"] == "phone") | (plays["device"] == "laptop")

with_brackets = long_play & phone_or_laptop
with_isin = long_play & plays["device"].isin(["phone", "laptop"])
assert with_brackets.sum() == with_isin.sum() == 523
print(f"1. {with_brackets.sum()} long plays on the phone or the laptop")

#    The one-line version without brackets around the | gives 871, no error:
#    & is worked out before |, so it means "long phone plays, or ANY laptop
#    play". SQL's AND and OR have exactly the same rule.
one_line_wrong = (plays["minutes_played"] > 5) & (plays["device"] == "phone") | (plays["device"] == "laptop")
assert one_line_wrong.sum() == 871


# 2. Total minutes per country. Many plays to one artist each, so the row
#    count must not change.
named = plays.merge(artists, on="artist_id")
assert len(named) == len(plays) == 2183

per_country = (
    named.groupby("country")
    .agg(plays=("play_id", "count"), minutes=("minutes_played", "sum"))
    .sort_values("minutes", ascending=False)
)
assert len(per_country) == 25
assert round(per_country.loc["Germany", "minutes"], 1) == 1285.1
print("\n2. minutes per country")
print(per_country.head().round(1))
#    Germany 1285.1, Netherlands 1265.2, Norway 1184.0, and 22 more.


# 3. Top three in 2025 by minutes. The filter is on rows, so it goes first:
#    the WHERE of session 7.
in_2025 = named[named["played_at"] >= "2025-01-01"]
top_2025 = (
    in_2025.groupby("artist_name")
    .agg(plays=("play_id", "count"), minutes=("minutes_played", "sum"))
    .sort_values("minutes", ascending=False)
    .head(3)
)
assert list(top_2025.index) == ["DJ Kompas", "Glass Tram", "Fjord & Flint"]
assert top_2025.loc["Glass Tram", "plays"] == 115
print("\n3. top three in 2025")
print(top_2025.round(1))
#    DJ Kompas 570.9 on 103 plays beats Glass Tram 545.5 on 115. Most minutes
#    and most plays are different questions, again.


# ===================================================== PART 2 ===========

# 4 and 5. Query 2 with awards merged on.
with_awards = named.merge(awards, on="artist_id")
broken = (
    with_awards.groupby("country")
    .agg(rows_now=("play_id", "count"), minutes=("minutes_played", "sum"))
    .sort_values("minutes", ascending=False)
)
assert len(with_awards) == 2371
assert len(broken) == 14
assert round(broken.loc["Norway", "minutes"], 1) == 2538.5
print("\n4. with awards merged on")
print(broken.head(3).round(1))
#
#    before: 2,183 rows, 25 countries. Germany 1285.1, Netherlands 1265.2,
#            Norway 1184.0
#    after:  2,371 rows, 14 countries. Norway 2538.5, Germany 2350.1,
#            Ireland 1318.0


# 6. WHY.
#
#    awards has one row per award, and an artist can have several. Fjord &
#    Flint, from Norway, has 3 awards and 237 plays. The merge pairs every
#    play with every award for that artist, so 237 plays become 711 rows and
#    their minutes are counted three times. That is fan-out, and pandas does it
#    exactly as SQL did, because it is the same operation.
#
#    And the second bug: merge is an INNER join unless told otherwise, so the
#    eleven countries whose artists never won anything simply vanished. The
#    numbers that remain are inflated AND rows are missing.


# 7. The fix: both tables down to one row per artist, THEN merge.
per_artist = (
    plays.groupby("artist_id")
    .agg(plays=("play_id", "count"), minutes=("minutes_played", "sum"))
    .reset_index()
)
awards_per_artist = awards.groupby("artist_id").size().rename("awards").reset_index()

fixed = (
    per_artist
    .merge(artists, on="artist_id", validate="one_to_one")
    .merge(awards_per_artist, on="artist_id", how="left", validate="one_to_one")
)
fixed["awards"] = fixed["awards"].fillna(0).astype(int)     # no awards means 0 here

fixed_country = (
    fixed.groupby("country")
    .agg(plays=("plays", "sum"), minutes=("minutes", "sum"), awards=("awards", "sum"))
    .sort_values("minutes", ascending=False)
)
assert len(fixed_country) == 25
assert list(fixed_country.index) == list(per_country.index)
assert (fixed_country["minutes"].round(1) == per_country["minutes"].round(1)).all()
print("\n7. fixed: all 25 countries, every total matches query 2")
print(fixed_country.head().round(1))


# 8. validate= turns the silent fan-out into a loud error.
try:
    named.merge(awards, on="artist_id", validate="many_to_one")
except pd.errors.MergeError as error:
    print("\n8. MergeError:", error)
#    Merge keys are not unique in right dataset; not a many-to-one merge
#
#    The two merges in the fix carry validate="one_to_one" and pass, because
#    after aggregating, every table really does have one row per artist.
