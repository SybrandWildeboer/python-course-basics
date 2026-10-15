"""HOMEWORK 2: a makeover.

Run from the repository root:

    python sessions/session-07/homework/makeover.py

Someone wanted to know whether the phone is losing ground to other devices,
and made two pie charts. This script draws them and saves them to
output/device_pies_before.png. Open the file and look at it.

Rebuild it the way you rebuilt the genre chart in the live exercise:

    1. list what is wrong with it, and why
    2. write the question as one sentence
    3. decide what number answers it, and what kind of chart shows it
    4. draw it, with a title that gives the answer, and save it to
       output/device_share_makeover.png
    5. one sentence on what your chart does not show. (Hint: a share can
       go up while the count goes down. Does that happen here?)

There is more than one good answer. A pie is not one of them.
"""

import os

import matplotlib.pyplot as plt
import pandas as pd

plays = pd.read_csv("data/clean/plays.csv")
plays["year"] = plays["played_at"].str[:4].astype(int)
os.makedirs("output", exist_ok=True)

shares = plays.pivot_table(index="device", columns="year", values="play_id", aggfunc="count")
shares = shares / shares.sum() * 100

# ------------------------------------------------- the chart you were given
fig, (left, right) = plt.subplots(1, 2, figsize=(10, 4.5))
left.pie(shares[2024], labels=shares.index, startangle=90, shadow=True)
right.pie(shares[2025], labels=shares.index, startangle=0, shadow=True)
left.set_title("2024")
right.set_title("2025")
fig.suptitle("Devices")
fig.savefig("output/device_pies_before.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("saved output/device_pies_before.png")

# What is wrong with it:
#

# My question:
#

# TODO: your makeover


# What this chart does not show:
#
