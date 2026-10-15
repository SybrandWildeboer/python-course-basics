"""LIVE EXERCISE: a chart makeover.

Run from the repository root:

    python sessions/session-07/exercises/makeover.py

It draws the bad chart and saves it to output/genre_chart_before.png. Open
it, then rebuild it below, one decision at a time:

    0. list everything that is wrong with it, and why
    1. write the question as one sentence: which genres grew from 2024 to
       2025, and which shrank?
    2. compute the number that answers it (the two years, or something
       you get from them?), plays or percent, and sort
    3. choose the kind of chart for that kind of question
    4. make the line the reader measures from visible
    5. give colour one job, with two colours that work for everyone
    6. label every bar, rounded with :.1f (try :+.1f)
    7. a title that gives the answer, computed in an f-string
    8. remove what says nothing, add units, and save to
       output/genre_change.png before anything else
    9. what does the chart not show? (what happened to all listening?)

The notebook version is notebooks/03-makeover-exercise.ipynb, and the
worked answer is solutions/makeover.py.
"""

import os

import matplotlib.pyplot as plt
import pandas as pd

plays = pd.read_csv("data/clean/plays.csv")
plays["year"] = plays["played_at"].str[:4].astype(int)
os.makedirs("output", exist_ok=True)

per_year = plays.pivot_table(index="genre", columns="year", values="play_id", aggfunc="count")
print(per_year)

# ------------------------------------------------- the chart you were given
fig, ax = plt.subplots(figsize=(8, 4.5))
per_year.plot(ax=ax, marker="s", linewidth=3, color=["red", "green"])
ax.set_ylim(55, 290)
ax.set_title("Genre data")
ax.grid(True, linewidth=1.5)
fig.savefig("output/genre_chart_before.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("saved output/genre_chart_before.png")

# ------------------------------------------------- your makeover
# TODO: steps 2 to 8 here.

# What this chart does not show:
#
