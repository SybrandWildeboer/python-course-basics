"""The session 9 walkthrough, part two: one question, one chart.

Run it from the repository root:

    python sessions/session-09/demos/charts.py

It writes three PNGs into output/, which git ignores. A script saves its
charts rather than showing them: plt.show() would open a window and stop
the script until you closed it.
"""

import os

import matplotlib.pyplot as plt
import pandas as pd

plays = pd.read_csv("data/clean/plays.csv")
os.makedirs("output", exist_ok=True)


# ------------------------------------------------- a bar chart, for categories
# Question: which genre do I listen to longest, per play?
by_genre = plays.groupby("genre")["minutes_played"].mean().sort_values(ascending=False)
top_genre = by_genre.index[0]

fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.bar(by_genre.index, by_genre.values, color="#4f6ddb")

ax.set_title(f"{top_genre} plays last longest: {by_genre.iloc[0]:.1f} minutes on average")
ax.set_ylabel("average minutes per play")        # units on the axis
ax.bar_label(bars, fmt="{:.1f}")                 # the :.1f from session 1
ax.spines[["top", "right"]].set_visible(False)   # borders that say nothing

fig.savefig("output/minutes_by_genre.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("saved output/minutes_by_genre.png")       # Jazz, 6.6 minutes


# ------------------------------------------------- a line chart, for time
# Question: does my listening change through the year?
per_month = plays.groupby(plays["played_at"].str[:7]).size()

fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(per_month.index, per_month.values, marker="o", color="#4f6ddb")

ax.set_title("Listening dips every summer, in both years")
ax.set_ylabel("plays per month")
ax.set_ylim(bottom=0)                            # start at zero, so a dip is not a cliff
ax.tick_params(axis="x", labelrotation=90)
ax.spines[["top", "right"]].set_visible(False)

fig.savefig("output/plays_per_month.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("saved output/plays_per_month.png")        # lowest: 2025-08, 57 plays


# ------------------------------------------------- the same numbers, two stories
# Every number is right in both charts. Only the axis differs.
skip_rate = plays.groupby("device")["skipped"].mean().sort_values(ascending=False) * 100

fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4))

left.bar(skip_rate.index, skip_rate.values, color="#c0392b")
left.set_ylim(10, 14.5)
left.set_title("Zoomed in: speaker looks terrible")

right.bar(skip_rate.index, skip_rate.values, color="#4f6ddb")
right.set_ylim(0, 15)
right.set_title("From zero: they are all much the same")
right.bar_label(right.containers[0], fmt="{:.1f}%")

fig.savefig("output/skip_rate_two_ways.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("saved output/skip_rate_two_ways.png")     # speaker 14.0%, car 10.6%

# Bars always start at zero: the length of a bar is the number.
# Save before plt.show(). After show(), plt.savefig() writes a blank picture.
