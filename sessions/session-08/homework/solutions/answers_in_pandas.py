"""HOMEWORK: your session 6 answers, in pandas, worked solution.

    python3 sessions/session-08/homework/solutions/answers_in_pandas.py

Every answer is pinned with an assert to the figure in the session 6 worked
answers (sessions/session-06/homework/solutions/answers.sql), so the two
languages are checked against each other each time this runs.
"""

import pandas as pd

pd.set_option("display.width", 120)

plays = pd.read_csv("data/clean/plays.csv")
artists = pd.read_csv("data/clean/artists.csv")


# 1. How many artists?  40
assert len(artists) == 40
print("1.", len(artists), "artists")


# 2. Artists from the Netherlands. Filter, pick columns, sort: in the order
#    they happen.
dutch = artists[artists["country"] == "Netherlands"][["artist_name", "genre"]]
dutch = dutch.sort_values("artist_name")
assert list(dutch["artist_name"]) == ["DJ Kompas", "Neon Harbour", "The Long Commute"]
print("\n2.\n", dutch, sep="")


# 3. Unknown formed_year.  Rosewood Lane, Cassette Revival.
#
#    A TRAP PANDAS SHARES WITH SQL. formed_year is float64, a decimal, because
#    a missing value (NaN) is a decimal, so any number column with a gap is
#    stored as decimals. And == None finds nothing, silently, exactly like
#    = NULL did: a missing value is not equal to anything.
assert len(artists[artists["formed_year"] == None]) == 0      # noqa: E711
unknown = artists[artists["formed_year"].isna()][["artist_name", "country", "genre"]]
assert set(unknown["artist_name"]) == {"Rosewood Lane", "Cassette Revival"}
print("\n3.\n", unknown, sep="")


# 4. The five longest plays. sort_values + head is ORDER BY ... LIMIT.
#    plays.nlargest(5, "minutes_played") is a shortcut to the same rows.
longest = plays.sort_values("minutes_played", ascending=False).head(5)
assert list(longest["track_name"]) == [
    "Paper Avenue", "Harbour Season", "Broken Lines", "Static Wires", "Northern Window",
]
print("\n4.\n", longest[["track_name", "played_at", "minutes_played"]], sep="")


# 5. Plays per year.  2024: 1122, 2025: 1061.
#    .str[:4] is substr(played_at, 1, 4), on every row at once. sort_index()
#    puts the years in order, otherwise the bigger count comes first.
per_year = plays["played_at"].str[:4].value_counts().sort_index()
assert per_year.to_dict() == {"2024": 1122, "2025": 1061}
print("\n5.\n", per_year, sep="")


# 6. Tracks played more than 40 times. Count, then filter the counts: that is
#    HAVING, with no special keyword.
track_counts = plays["track_name"].value_counts()
popular = track_counts[track_counts > 40]
assert popular.to_dict() == {
    "Broken Lines": 67, "Salt Lines": 63, "Amber Ferry": 55, "Broken Mornings": 52, "Open Orbit": 44,
}
print("\n6.\n", popular, sep="")


# 7. Minutes per device, to the nearest minute. round() leaves 4308.0;
#    astype(int) makes it 4308.
device_minutes = plays.groupby("device")["minutes_played"].sum().round().astype(int)
device_minutes = device_minutes.sort_values(ascending=False)
assert device_minutes.to_dict() == {"phone": 4308, "laptop": 2144, "speaker": 1335, "car": 778, "tablet": 416}
print("\n7.\n", device_minutes, sep="")


# 8. Genres with five or more artists. Electronic 7, Indie 6, then four on 5.
#    Among a tie, value_counts' order is whatever it happens to be; sort by
#    two columns to settle it, as ORDER BY artists DESC, genre did in SQL.
genre_artists = artists["genre"].value_counts()
big = genre_artists[genre_artists >= 5].rename("artists").reset_index()
big = big.sort_values(["artists", "genre"], ascending=[False, True])
assert list(big["genre"]) == ["Electronic", "Indie", "Folk", "Jazz", "Latin", "Rock"]
print("\n8.\n", big, sep="")


# 9. Skip rate per device.
#
#    THE TRAP SQL HAD AND PANDAS DOES NOT. In SQLite 19 / 179 was 0. In
#    Python 3, / always gives the decimal answer, so no 100.0 is needed.
skips = plays.groupby("device").agg(plays=("play_id", "count"), skipped=("skipped", "sum"))
skips["skipped_pct"] = (100 * skips["skipped"] / skips["plays"]).round(1)
skips = skips.sort_values("skipped_pct", ascending=False)
assert skips["skipped_pct"].to_dict() == {"speaker": 14.0, "tablet": 13.3, "laptop": 11.5, "phone": 11.4, "car": 10.6}
print("\n9.\n", skips, sep="")

#    Shortcut: skipped is 0 or 1, so its mean IS the rate.
rate = (100 * plays.groupby("device")["skipped"].mean()).round(1)
assert rate.to_dict() == skips["skipped_pct"].to_dict()


# 10. The busiest day.  2024-03-24, 11 plays.
#     A TRAP PANDAS SHARES WITH SQL: a single winner hides how close it was.
#     Second place has 10, then three days on 8. head(5), not head(1).
per_day = plays["played_at"].value_counts()
assert per_day.index[0] == "2024-03-24" and per_day.iloc[0] == 11
assert per_day.iloc[1] == 10
print("\n10.\n", per_day.head(5), sep="")


# ---------------------------------------------------------------------------
# TASK 2, an example: does listening get longer as the year goes on?
#
# Plays per calendar month swing from 120 to 239, with June, July and August
# the quietest. The average play length only moves between 3.93 and 4.46. The
# seasonal effect is in how MUCH gets played, not how long each play lasts:
# the same answer as the SQL version in session 6.
plays["month"] = plays["played_at"].str[5:7]
by_month = plays.groupby("month").agg(
    plays=("play_id", "count"),
    avg_min=("minutes_played", "mean"),
).round(2)
assert set(by_month["plays"].nsmallest(3).index) == {"06", "07", "08"}
assert (by_month["plays"].min(), by_month["plays"].max()) == (120, 239)
assert (by_month["avg_min"].min(), by_month["avg_min"].max()) == (3.93, 4.46)
print("\nTask 2 example\n", by_month, sep="")

# Easier in pandas: 5 (.str[:4] beats remembering strftime), 6 and 8 (no
#                   HAVING), 9 (no integer division to trip over).
# Easier in SQL:    2, slightly: WHERE country = 'Netherlands' reads more like
#                   English than the double brackets do.
# About the same:   the rest. Same ideas, different punctuation.
