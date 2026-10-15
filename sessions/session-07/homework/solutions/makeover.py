"""HOMEWORK 2: a makeover, worked version.

    python sessions/session-07/homework/solutions/makeover.py

What was wrong with the two pies: comparing angles that start in different
places (the second pie is turned a quarter), on two separate circles; the
shadows add nothing; there are no numbers; and "Devices" is a topic, not an
answer. You cannot tell from them whether the phone went up or down.

My question: is the phone losing ground to other devices?

That is a part-of-a-whole question across two years. The thing to show is
how each share moved, so: a dumbbell chart, one row per device, a grey dot
for 2024, a coloured dot for 2025, and a line between them.
"""

import os

import matplotlib.pyplot as plt
import pandas as pd

plays = pd.read_csv("data/clean/plays.csv")
plays["year"] = plays["played_at"].str[:4].astype(int)
os.makedirs("output", exist_ok=True)

counts = plays.pivot_table(index="device", columns="year", values="play_id", aggfunc="count")
shares = counts / counts.sum() * 100
shares["change"] = shares[2025] - shares[2024]
shares = shares.sort_values(2025)
print(shares.round(1))

phone_2024, phone_2025 = shares.loc["phone", 2024], shares.loc["phone", 2025]
others_gained = (shares.drop("phone")["change"] > 0).all()

fig, ax = plt.subplots(figsize=(9, 4))
ax.hlines(shares.index, shares[2024], shares[2025], color="#b8bec9", linewidth=3)
ax.scatter(shares[2024], shares.index, color="#b8bec9", s=80, label="2024", zorder=3)
ax.scatter(shares[2025], shares.index, color="#0072b2", s=80, label="2025", zorder=3)
for device, row in shares.iterrows():
    ax.annotate(f"{row[2025]:.1f}%", (row[2025], device), xytext=(0, 9),
                textcoords="offset points", ha="center", color="#0072b2")

ax.set_title(f"The phone's share fell from {phone_2024:.1f}% to {phone_2025:.1f}%; "
             "every other device gained")
ax.set_xlabel("share of the year's plays (%)")
ax.set_xlim(0, 55)
ax.margins(y=0.15)
ax.legend(loc="lower right", frameon=False)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.tick_params(axis="y", length=0)

fig.savefig("output/device_share_makeover.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("saved output/device_share_makeover.png")

print(counts)

assert (round(phone_2024, 1), round(phone_2025, 1)) == (49.9, 45.1)
assert others_gained
assert (counts.loc["phone", 2024], counts.loc["phone", 2025]) == (560, 479)
assert (counts.loc["laptop", 2024], counts.loc["laptop", 2025]) == (263, 261)

# ---------------------------------------------------------------------------
# What this chart does not show:
#
#   Whether anything was played less. Shares only say how each year was
#   split. Phone plays fell from 560 to 479, and the laptop's share went up,
#   from 23.4% to 24.6%, while its plays went down, from 263 to 261, because
#   listening as a whole fell by more. "Every other device gained" is true
#   of shares and false of plays, so the title says "share".
#
# A grouped bar chart, 2024 and 2025 side by side per device, would also be
# a good answer. What matters is one shared axis starting at zero, and a
# reader comparing lengths or positions instead of angles.
