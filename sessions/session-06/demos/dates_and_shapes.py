"""The session 6 walkthrough, part three: dates and shapes, ready for charts.

Run it from the repository root, or the relative paths will not find the data:

    python sessions/session-06/demos/dates_and_shapes.py

Session 7 draws charts. Every chart needs real dates and a table in the right
shape, and this script makes both: a time series, a wide table per device,
and genre by year.
"""

import sys

import pandas as pd

pd.set_option("display.width", 120)

plays = pd.read_csv("data/clean/plays.csv")


# ------------------------------------------- text that looks like a date
print(plays["played_at"].dtype)                         # object: text
plays["played_at"] = pd.to_datetime(plays["played_at"], format="%Y-%m-%d")
print(plays["played_at"].dtype)                         # datetime64[ns]


# ------------------------------------------- .dt: ask every date at once
dates = plays["played_at"]
per_year = dates.dt.year.value_counts().sort_index()
assert per_year.to_dict() == {2024: 1122, 2025: 1061}
print(per_year)

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
per_weekday = dates.dt.day_name().value_counts().reindex(days)
assert (per_weekday.min(), per_weekday.max()) == (302, 333)    # no favourite day
print(per_weekday)


# ------------------------------------------- per month, two ways
month = dates.dt.to_period("M")                         # 2024-10-17 -> 2024-10
plays_per_month = plays.groupby(month).size()
assert len(plays_per_month) == 24
assert plays_per_month.max() == 127 and plays_per_month.min() == 57
print(plays_per_month)                                  # busiest 2024-10, quietest 2025-08

# resample needs the dates as the index. "MS" is month, labelled by its start,
# and it makes a row for every month in the range, even an empty one.
minutes_per_month = plays.set_index("played_at")["minutes_played"].resample("MS").sum()
assert round(minutes_per_month.max(), 1) == 554.6       # October 2024
assert round(minutes_per_month.min(), 1) == 231.1       # June 2025
print(minutes_per_month.round(1))


# ------------------------------------------- the sum of nothing is zero
# May 2024 on the tablet: one play, and its minutes were blank in the messy file.
sys.path.insert(0, "sessions/session-06/solutions")
from cleaning import clean_plays, load_messy

cleaned = clean_plays(load_messy("data/messy/plays_messy.csv"))
cleaned["played_at"] = pd.to_datetime(cleaned["played_at"], format="%Y-%m-%d")
tablet = cleaned[cleaned["device"] == "tablet"].set_index("played_at")["minutes_played"]

may = pd.Timestamp("2024-05-01")
print("\ntablet minutes, May 2024")
print("  sum:             ", tablet.resample("MS").sum()[may])               # 0.0, a claim
print("  mean:            ", tablet.resample("MS").mean()[may])              # nan
print("  sum, min_count=1:", tablet.resample("MS").sum(min_count=1)[may])    # nan, honest
assert tablet.resample("MS").sum()[may] == 0


# ------------------------------------------- long and wide
long = plays.groupby([month, "device"]).size()          # 120 rows: month and device
wide = long.unstack()                                   # 24 rows, one column per device
assert len(long) == 120 and wide.shape == (24, 5)
print(wide.head())

pivot = plays.pivot_table(index=month, columns="device", values="play_id", aggfunc="count")
assert pivot.equals(wide)                               # the same table, in one call

minutes_by_device = plays.pivot_table(index=month, columns="device",
                                      values="minutes_played", aggfunc="sum")
print(minutes_by_device.round(1).head())

# The session 4 stretch's genre-by-year table, in one line.
plays["year"] = dates.dt.year
genre_by_year = plays.pivot_table(index="genre", columns="year", values="play_id", aggfunc="count")
genre_by_year["change"] = genre_by_year[2025] - genre_by_year[2024]
assert genre_by_year.loc["Folk"].tolist() == [236, 202, -34]
print(genre_by_year.sort_values("change"))

# A gap in a table of counts really is zero: no rows means no plays.
by_artist = plays.groupby([month, "artist_name"]).size().unstack(fill_value=0)
assert by_artist.sum().sum() == len(plays)
print(f"\nplays per month per artist: {by_artist.shape[0]} months by {by_artist.shape[1]} artists")
