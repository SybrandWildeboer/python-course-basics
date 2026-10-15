"""The session 7 walkthrough, part two: time, many charts, and the one that matters.

Run it from the repository root:

    python sessions/session-07/demos/time_and_panels.py

It writes four PNGs into output/: an annotated line with real dates, small
multiples, a highlighted line chart, and a four-panel figure ready to share.
"""

import os

import matplotlib.pyplot as plt
import pandas as pd

BLUE = "#4f6ddb"          # the data
GREY = "#b8bec9"          # context
HIGHLIGHT = "#d55e00"     # the one thing the title is about

plays = pd.read_csv("data/clean/plays.csv")
plays["date"] = pd.to_datetime(plays["played_at"])
os.makedirs("output", exist_ok=True)


# ------------------------------------------------- real dates, a reference line, annotations
monthly = plays.set_index("date").resample("MS").size()
average = monthly.mean()
peak_date, peak = monthly.idxmax(), monthly.max()
low_date, low = monthly.idxmin(), monthly.min()

fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(monthly.index, monthly.values, marker="o", color=BLUE)
ax.axhline(average, color=GREY, linestyle="--", linewidth=1)
ax.text(monthly.index[0], average + 3, f"average: {average:.1f} plays a month", color="#6b7280")
for year in [2024, 2025]:
    ax.axvspan(pd.Timestamp(f"{year}-06-01"), pd.Timestamp(f"{year}-08-01"),
               color=GREY, alpha=0.25, linewidth=0)
ax.annotate(f"{peak_date:%B %Y}: {peak}", xy=(peak_date, peak), xytext=(15, 8),
            textcoords="offset points", arrowprops={"arrowstyle": "->"})
ax.annotate(f"{low_date:%B %Y}: {low}", xy=(low_date, low), xytext=(15, -22),
            textcoords="offset points", arrowprops={"arrowstyle": "->"})
ax.set_title(f"Every summer falls below the average of {average:.1f} plays a month")
ax.set_ylabel("plays per month")
ax.set_ylim(0, 145)
ax.spines[["top", "right"]].set_visible(False)

fig.savefig("output/monthly_annotated.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("saved output/monthly_annotated.png")
assert round(average, 1) == 91.0
assert (f"{peak_date:%B %Y}", peak, f"{low_date:%B %Y}", low) == ("October 2024", 127, "August 2025", 57)


# ------------------------------------------------- small multiples, with a shared axis
plays["quarter"] = plays["date"].dt.to_period("Q").dt.start_time
quarterly = plays.pivot_table(index="quarter", columns="genre", values="play_id", aggfunc="count")

fig, axes = plt.subplots(2, 4, figsize=(13, 5.5), sharex=True, sharey=True)
for ax, genre in zip(axes.flat, quarterly.columns):
    ax.plot(quarterly.index, quarterly[genre], color=BLUE, linewidth=2)
    ax.set_title(genre)
    ax.set_xticks([pd.Timestamp("2024-01-01"), pd.Timestamp("2025-01-01")], ["2024", "2025"])
    ax.spines[["top", "right"]].set_visible(False)
for ax in axes[:, 0]:
    ax.set_ylabel("plays per quarter")
axes[0, 0].set_ylim(bottom=0)                     # shared, so this sets all eight
fig.suptitle("Electronic and Folk are the two biggest genres in every quarter")

fig.savefig("output/genres_small_multiples.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("saved output/genres_small_multiples.png")


# ------------------------------------------------- grey everything, colour the one that matters
per_year = plays.pivot_table(index="genre", columns=plays["date"].dt.year,
                             values="play_id", aggfunc="count")
loser = (per_year[2025] - per_year[2024]).idxmin()
last = quarterly.index[-1]

fig, ax = plt.subplots(figsize=(10, 4.5))
for genre in quarterly.columns:
    if genre != loser:
        ax.plot(quarterly.index, quarterly[genre], color=GREY, linewidth=1.5)
ax.plot(quarterly.index, quarterly[loser], color=HIGHLIGHT, linewidth=3)
ax.text(last + pd.Timedelta(days=20), quarterly.loc[last, loser], loser,
        color=HIGHLIGHT, va="center", fontweight="bold")
ax.set_title(f"{loser} lost the most plays: {per_year.loc[loser, 2024]} in 2024, "
             f"{per_year.loc[loser, 2025]} in 2025")
ax.set_ylabel("plays per quarter")
ax.set_ylim(bottom=0)
ax.spines[["top", "right"]].set_visible(False)

fig.savefig("output/folk_highlighted.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("saved output/folk_highlighted.png")       # Folk, 236 then 202
assert loser == "Folk"


# ------------------------------------------------- one figure, four panels, for sharing
blue, orange = "#0072b2", "#e69f00"               # Okabe-Ito: safe for colour-blind readers
by_genre = plays.groupby("genre")["minutes_played"].mean().sort_values()
per_artist = plays.groupby("artist_name").agg(plays=("play_id", "count"),
                                              minutes=("minutes_played", "sum"))
kept = plays.loc[plays["skipped"] == 0, "minutes_played"]
skips = plays.loc[plays["skipped"] == 1, "minutes_played"]

fig, axes = plt.subplots(2, 2, figsize=(13, 8), layout="constrained")
(time_ax, genre_ax), (spread_ax, artist_ax) = axes

time_ax.plot(monthly.index, monthly.values, marker="o", color=blue)
time_ax.axhline(average, color=GREY, linestyle="--", linewidth=1)
time_ax.set_title(f"Summers fall below the {average:.1f}-play average")
time_ax.set_ylabel("plays per month")
time_ax.set_ylim(bottom=0)

colours = [orange if genre == "Jazz" else blue for genre in by_genre.index]
bars = genre_ax.barh(by_genre.index, by_genre.values, color=colours)
genre_ax.bar_label(bars, fmt="{:.1f}", padding=3)
genre_ax.set_title(f"Jazz plays last longest: {by_genre['Jazz']:.1f} minutes")
genre_ax.set_xlabel("average minutes per play")

spread_ax.hist([kept, skips], bins=range(0, 13), stacked=True, color=[blue, orange],
               edgecolor="white", label=["played through", "skipped"])
spread_ax.set_title(f"{(skips < 1).mean():.1%} of skips last under a minute")
spread_ax.set_xlabel("minutes played")
spread_ax.set_ylabel("number of plays")
spread_ax.legend()

artist_ax.scatter(per_artist["plays"], per_artist["minutes"], color=blue, alpha=0.75)
artist_ax.set_title("More plays, more minutes, but not in step")
artist_ax.set_xlabel("plays per artist")
artist_ax.set_ylabel("total minutes")
artist_ax.set_ylim(bottom=0)

for ax in axes.flat:
    ax.spines[["top", "right"]].set_visible(False)
fig.suptitle(f"Two years of listening: {len(plays):,} plays, "
             f"{plays['minutes_played'].sum():,.0f} minutes", fontsize=16)

fig.savefig("output/listening_overview.png", dpi=200, bbox_inches="tight")
plt.close(fig)
print("saved output/listening_overview.png")     # 2,183 plays, 8,980 minutes
