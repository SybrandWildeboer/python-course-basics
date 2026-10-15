"""HOMEWORK 1: a decision diary, worked solution.

    python sessions/session-09/homework/solutions/decisions.py
"""

import sys

import pandas as pd

sys.path.insert(0, "sessions/session-09/solutions")
from cleaning import clean_plays, load_messy


def skip_rates(df):
    """Return one row per device: number of plays, and percentage skipped, highest first."""
    rates = df.groupby("device")["skipped"].agg(plays="size", rate="mean")
    rates["rate"] = rates["rate"] * 100
    return rates.sort_values("rate", ascending=False)


def winner(rates):
    """Return a one-line summary of the top row of a skip_rates table.

    {device!r} prints the value with quotes, so "CAR" and "phone " show
    exactly how they are spelled.
    """
    device = rates.index[0]
    return f"{device!r}: {rates['rate'].iloc[0]:.1f}% of {rates['plays'].iloc[0]} plays"


raw = load_messy("data/messy/plays_messy.csv")
plays = clean_plays(raw)
clean = pd.read_csv("data/clean/plays.csv")

text_cleaned = raw.copy()
text_cleaned["device"] = text_cleaned["device"].str.strip().str.lower()
text_cleaned = text_cleaned[text_cleaned["device"] != ""]

steps = {
    "1. as loaded": skip_rates(raw),
    "2. text cleaned": skip_rates(text_cleaned),
    "3. duplicates dropped": skip_rates(text_cleaned.drop_duplicates()),
    "4. full clean, with unknown": skip_rates(plays),
    "5. the clean file": skip_rates(clean),
}

print("Which device gets skipped most?\n")
for step, rates in steps.items():
    print(f"  {step:30} {winner(rates)}")

big_enough = steps["1. as loaded"][steps["1. as loaded"]["plays"] >= 30]
print(f"\n  step 1 with at least 30 plays:  {winner(big_enough)}")

assert steps["1. as loaded"].index[0] == "CAR"
assert steps["2. text cleaned"].index[0] == "speaker"
assert steps["4. full clean, with unknown"].index[0] == "unknown"
assert steps["5. the clean file"].index[0] == "speaker"
assert big_enough.index[0] == "LAPTOP"


# ---------------------------------------------------------------------------
# The output:
#
#   1. as loaded                   'CAR': 17.2% of 29 plays
#   2. text cleaned                'speaker': 14.1% of 333 plays
#   3. duplicates dropped          'speaker': 14.1% of 326 plays
#   4. full clean, with unknown    'unknown': 15.9% of 69 plays
#   5. the clean file              'speaker': 14.0% of 336 plays
#
#   step 1 with at least 30 plays:  'LAPTOP': 16.2% of 74 plays
#
# Which decision changed the answer most? Cleaning the text. Before it, you
# are ranking twenty spellings, not five devices, and the winner is whichever
# small group happened to collect a few skips. After it, every step agrees
# with the clean file on the winner, as long as "unknown" is kept out.
#
# Dropping duplicates moved the counts (333 speaker plays became 326) and
# barely moved the rates. Duplicates change totals far more than percentages.
#
# What to do about "unknown"? Keep it in the table and out of the ranking.
# It is not a device; it is 69 plays on some mix of devices, so "the most
# skipped device is unknown" means nothing. The honest sentence is: "speaker
# is skipped most, at 14.1%; 69 plays (3%) had no device recorded."
#
# Would min_plays have rescued step 1? No. It removes "CAR" (29 plays) and
# "tablet" (6), and then "LAPTOP" in capitals wins at 16.2%, where the clean
# file says laptop is 11.5%. A minimum protects you from small groups. It
# cannot protect you from asking about spellings instead of devices. Only
# cleaning does that.
