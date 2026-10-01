"""HOMEWORK 2: one chart that answers one question, worked example.

    python sessions/session-09/homework/solutions/my_chart.py

My question: which artists got the most minutes in 2025?
"""

import os
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, "sessions/session-09/solutions")
from cleaning import clean_plays, load_messy

plays = clean_plays(load_messy("data/messy/plays_messy.csv"))
os.makedirs("output", exist_ok=True)


def top_artists_by_minutes(plays, year, n=8):
    """Return the n artists with the most minutes in a year, biggest first."""
    in_year = plays[plays["played_at"].str.startswith(str(year))]
    minutes = in_year.groupby("artist_name")["minutes_played"].sum()
    return minutes.sort_values(ascending=False).head(n)


def missing_minutes(plays, year, artists):
    """Return how many plays in a year have no minutes, for each of the given artists."""
    in_year = plays[plays["played_at"].str.startswith(str(year))]
    missing = in_year[in_year["minutes_played"].isna()]
    return missing["artist_name"].value_counts().reindex(artists, fill_value=0)


top = top_artists_by_minutes(plays, 2025)
gap = top.iloc[0] - top.iloc[1]
unknown = missing_minutes(plays, 2025, top.index[:2])

print(top.round(1))
print(f"\ngap between the top two: {gap:.1f} minutes")
print("plays in 2025 with no minutes recorded:")
print(unknown)

# DJ Kompas has 6 plays with no minutes and Glass Tram 2. Any one of them is
# likely to be longer than the 3.5-minute gap, so the data cannot say who won.
# The title says what the data supports, not what would be more exciting.
ranked = top.sort_values()                      # barh draws from the bottom up

fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.barh(ranked.index, ranked.values, color="#4f6ddb")
ax.set_title(f"DJ Kompas and Glass Tram were neck and neck in 2025, {gap:.1f} minutes apart")
ax.set_xlabel("minutes played in 2025")
ax.bar_label(bars, fmt="{:,.1f}", padding=3)
ax.spines[["top", "right"]].set_visible(False)

fig.savefig("output/top_artists_2025.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("\nsaved output/top_artists_2025.png")

assert list(top.index[:2]) == ["DJ Kompas", "Glass Tram"]
assert round(gap, 1) == 3.5
assert list(unknown) == [6, 2]


# ---------------------------------------------------------------------------
# What I would say about it in a meeting:
#
#   "Two artists dominated my 2025, DJ Kompas and Glass Tram, with over 535
#   minutes each, and the gap between them is smaller than the minutes we
#   failed to record."
#
# The choices:
#   * horizontal bars, because artist names are long; still bars, because
#     artists are categories
#   * sorted ascending before barh, so the biggest ends up at the top
#   * the top eight, not all 38: the question is about the top
#
# The clean file, which you would never have in real life, says DJ Kompas
# 570.9 and Glass Tram 545.5. So DJ Kompas did win, by 25.4 minutes, and a
# title claiming it would have been right by luck. "Neck and neck" was the
# honest reading of the data we had.
