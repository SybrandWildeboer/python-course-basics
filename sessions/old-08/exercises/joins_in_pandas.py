"""LIVE EXERCISE: session 7, in pandas.

Run it from the repository root so the relative path works:

    python3 sessions/session-08/exercises/joins_in_pandas.py

The questions come from session 7's live exercise, so keep your joins.sql
open next to this. Your own SQL is the answer key.

Part 1: get the answers

    1. How many plays lasted more than 5 minutes AND were on the phone OR the
       laptop? Write it with & and |, then again with isin(), and check they
       agree.
    2. Total minutes per country, highest first. (plays has no country: merge
       artists on first, and check the row count.)
    3. The top three artists in 2025 only, by minutes, with their plays.

Part 2: break it, then explain it

    4. Take query 2 and merge awards onto it as well.
    5. Write down the numbers before and after, including the ROW COUNT and
       the number of countries.
    6. Explain WHY, in a comment, in your own words.
    7. Fix it by aggregating the plays to one row per artist first, then
       merging. assert that the totals match query 2 again.
    8. Add validate="many_to_one" to the broken merge and read the error.
       Then add validate= to every merge in your fix.

Reminders:
  * & and |, never and/or, and every condition in its own brackets
  * merge(..., on="artist_id") is JOIN ... USING (artist_id)
  * print len() before and after every merge
  * in a script nothing shows unless you print() it
"""

import sqlite3

import pandas as pd

pd.set_option("display.width", 120)

con = sqlite3.connect("data/music.db")
plays = pd.read_sql("SELECT * FROM plays", con)
artists = pd.read_sql("SELECT * FROM artists", con)
awards = pd.read_sql("SELECT * FROM awards", con)
con.close()

print(plays.shape, artists.shape, awards.shape)


# TODO 1: long plays on the phone or the laptop, two ways


# TODO 2: total minutes per country, highest first


# TODO 3: the top three artists in 2025, by minutes


# TODO 4: query 2, with awards merged on as well


# TODO 5: before:
#         after:


# TODO 6: WHY?
#


# TODO 7: aggregate first, then merge, and assert it matches query 2


# TODO 8: validate=
