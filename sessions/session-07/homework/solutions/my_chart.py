"""HOMEWORK 1: one chart that answers one question, worked example.

    python sessions/session-07/homework/solutions/my_chart.py

My question: which artists got the most minutes in 2025?
"""

import os

import matplotlib.pyplot as plt
import pandas as pd

plays = pd.read_csv("data/clean/plays.csv")
plays["year"] = plays["played_at"].str[:4].astype(int)
os.makedirs("output", exist_ok=True)


def top_artists_by_minutes(plays, year, n=8):
    """Return the n artists with the most minutes in a year, biggest first."""
    in_year = plays[plays["year"] == year]
    minutes = in_year.groupby("artist_name")["minutes_played"].sum()
    return minutes.sort_values(ascending=False).head(n)


top = top_artists_by_minutes(plays, 2025)
gap = top.iloc[0] - top.iloc[1]
print(top.round(1))
print(f"\ngap between the top two: {gap:.1f} minutes")

# How sure is that? The messy file is what you would really have had, and
# 94 of its plays have no minutes. Rank again without them.
messy = pd.read_csv("data/messy/plays_messy.csv", keep_default_na=False)
no_minutes = messy.loc[messy["minutes played "].str.strip() == "", "play_id"].unique()
top_known = top_artists_by_minutes(plays[~plays["play_id"].isin(no_minutes)], 2025)
gap_known = top_known.iloc[0] - top_known.iloc[1]
lost = (plays[(plays["year"] == 2025) & plays["play_id"].isin(no_minutes)]["artist_name"]
        .value_counts().reindex(top.index[:2]))
print(f"gap with only the minutes the messy file knew: {gap_known:.1f}")
print("plays in 2025 with no minutes in the messy file:")
print(lost)

ranked = top.sort_values()                      # barh draws from the bottom up
colours = ["#4f6ddb" if name in top.index[:2] else "#b8bec9" for name in ranked.index]

fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.barh(ranked.index, ranked.values, color=colours)
ax.set_title(f"DJ Kompas edged out Glass Tram in 2025, by {gap:.1f} minutes")
ax.set_xlabel("minutes played in 2025")
ax.bar_label(bars, fmt="{:,.1f}", padding=3)
ax.set_xlim(0, top.iloc[0] * 1.15)
ax.spines[["top", "right"]].set_visible(False)

fig.savefig("output/top_artists_2025.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("\nsaved output/top_artists_2025.png")

assert list(top.index[:2]) == ["DJ Kompas", "Glass Tram"]
assert round(gap, 1) == 25.4
assert len(no_minutes) == 94
assert round(gap_known, 1) == 3.5
assert list(lost) == [6, 2]
assert top.iloc[1] > 540


# ---------------------------------------------------------------------------
# What I would say about it in a meeting:
#
#   "Two artists dominated my 2025, DJ Kompas and Glass Tram, with over 540
#   minutes each, and the next one is 140 minutes behind."
#
# What this chart does not show:
#
#   How often each artist was played (this is minutes, not plays), anything
#   about 2024, and how fragile the order of the top two is. In the messy
#   file, DJ Kompas has 6 plays in 2025 with no minutes and Glass Tram 2,
#   and with only the minutes it knew the gap was 3.5, smaller than one song.
#
# The choices:
#   * horizontal bars, because artist names are long; still bars, because
#     artists are categories
#   * sorted ascending before barh, so the biggest ends up at the top
#   * the top eight, not all 38: the question is about the top
#   * the two the title is about in colour, the rest grey
#   * "edged out", not "beat": the title says what the data supports
