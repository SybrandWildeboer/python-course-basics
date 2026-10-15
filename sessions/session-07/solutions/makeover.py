"""LIVE EXERCISE: a chart makeover, worked version.

    python sessions/session-07/solutions/makeover.py

Writes output/genre_change.png and, with the reference line from step 10,
output/genre_change_with_reference.png.
"""

import os

import matplotlib.pyplot as plt
import pandas as pd

UP, DOWN = "#0072b2", "#e69f00"           # Okabe-Ito blue and orange, not green and red

plays = pd.read_csv("data/clean/plays.csv")
plays["year"] = plays["played_at"].str[:4].astype(int)
os.makedirs("output", exist_ok=True)

# Step 1, the question: which genres grew from 2024 to 2025, and which shrank?

# Step 2: the question is about change, so compute the change. As a percent
# of each genre's own 2024, because Electronic and Latin both lost 11 plays,
# and that is 3.9% of one and 11.2% of the other.
per_year = plays.pivot_table(index="genre", columns="year", values="play_id", aggfunc="count")
per_year["change"] = per_year[2025] - per_year[2024]
per_year["percent"] = per_year["change"] / per_year[2024] * 100
per_year = per_year.sort_values("percent")      # barh draws from the bottom up
print(per_year.round(1))

# Steps 5 to 7: colour for up or down, labels with a sign, a computed title.
colours = [UP if change > 0 else DOWN for change in per_year["change"]]
labels = [f"{percent:+.1f}% ({change:+d})"
          for percent, change in zip(per_year["percent"], per_year["change"])]
grew = per_year[per_year["change"] > 0].index.tolist()
fell_most = per_year.index[0]
title = (f"Only {grew[1]} and {grew[0]} grew in 2025; "
         f"{fell_most} fell most, {per_year.loc[fell_most, 'percent']:.1f}%")


def draw(path, title, overall=None):
    """Draw the made-over chart, with the overall change as a reference line if given."""
    fig, ax = plt.subplots(figsize=(9, 4.5))
    bars = ax.barh(per_year.index, per_year["percent"], color=colours)   # step 3: bars
    ax.bar_label(bars, labels=labels, padding=4)
    ax.axvline(0, color="black", linewidth=1)                            # step 4: zero
    if overall is not None:
        ax.axvline(overall, color="#6b7280", linestyle="--", linewidth=1)
        ax.annotate(f"all listening: {overall:.1f}%", xy=(overall, 7.4), xytext=(-6, 0),
                    textcoords="offset points", ha="right", color="#6b7280")
    ax.set_title(title)
    ax.set_xlabel("change in plays from 2024 to 2025 (%)")              # step 8: units
    ax.set_xlim(-24, 26)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("saved", path)


draw("output/genre_change.png", title)

# Step 9: what the chart does not show. All listening fell too.
total_2024, total_2025 = per_year[2024].sum(), per_year[2025].sum()
overall = (total_2025 - total_2024) / total_2024 * 100
gained_share = per_year[per_year["percent"] > overall].index.tolist()
print(f"all plays: {total_2024} in 2024, {total_2025} in 2025, {overall:.1f}%")

# Step 10: the overall change as a reference line, and the title it earns.
draw("output/genre_change_with_reference.png",
     f"{len(gained_share)} of 8 genres fell less than listening as a whole", overall)

assert labels[0] == "-14.4% (-34)" and labels[-1] == "+16.9% (+14)"
assert grew == ["Jazz", "Afrobeat"] and fell_most == "Folk"
assert (total_2024, total_2025) == (1122, 1061)
assert round(overall, 1) == -5.4
assert gained_share == ["Indie", "Electronic", "Jazz", "Afrobeat"]

# What this chart does not show:
#
#   That all listening fell by 5.4%. Electronic (-3.9%) and Indie (-4.0%)
#   fell less than that, so their share of the log went up. "Shrank" in
#   plays and "shrank" in share are different claims, and the first chart
#   only supports the first one.
