"""LIVE EXERCISE: turn a notebook-shaped script into a pipeline.

Below is code the way it comes out of a notebook: correct, top to bottom, no
functions. It answers one question: which device do I skip most on?

Step 0. Run it from the repository root. It works:

    python sessions/session-10/exercises/device_pipeline.py

    Now go into another folder and run the same file again:

    cd sessions/session-10
    python exercises/device_pipeline.py

    Read the error. The file is fine. Python is looking in the wrong place.

Then rebuild it, in this file, as a pipeline:

    1. load_messy(path)            returns the raw DataFrame
    2. clean_plays(df)             returns the cleaned DataFrame (this is your
                                   session 9 function: copy it from
                                   sessions/session-09/solutions/cleaning.py
                                   if yours is not to hand)
    3. skip_rate_by_device(plays)  returns the table of rates
    4. save_csv(table, path) and save_chart(rates, path)   write the files
    5. main()                      calls them in order, and is the ONLY place
                                   that prints
    6. if __name__ == "__main__": main()

Then:

    7. build the paths from __file__ with pathlib, so it runs from any folder
    8. add check_rates(path, plays): read the CSV back and assert that the
       plays and the skips add up to what is in the cleaned data

Every function gets a one-line docstring saying what it returns. When you are
done, run it from two different folders and get the same output both times.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------------------------------------------- the notebook way

raw = pd.read_csv("data/messy/plays_messy.csv", keep_default_na=False)
print(len(raw), "rows in")

# the session 9 cleaning, one step after another
df = raw.rename(columns={"minutes played ": "minutes_played"})
df = df.drop_duplicates().copy()

df["genre"] = df["genre"].str.strip().str.title().replace("", pd.NA)
df["device"] = df["device"].str.strip().str.lower().replace("", "unknown")
df["country"] = df["country"].str.strip().replace(["NA", ""], pd.NA)
for column in ["genre", "country"]:
    lookup = df.dropna(subset=[column]).groupby("artist_name")[column].first()
    df[column] = df[column].fillna(df["artist_name"].map(lookup))

dates = pd.to_datetime(df["played_at"], format="%Y-%m-%d", errors="coerce")
dates = dates.fillna(pd.to_datetime(df["played_at"], format="%d/%m/%Y", errors="coerce"))
dates = dates.fillna(pd.to_datetime(df["played_at"], format="%d-%m-%Y", errors="coerce"))
df["played_at"] = dates.dt.strftime("%Y-%m-%d")

minutes = df["minutes_played"].str.replace("min", "").str.replace(" ", "")
df["minutes_played"] = pd.to_numeric(minutes, errors="coerce")
print(len(df), "after cleaning")

rates = df.groupby("device").agg(plays=("play_id", "count"), skipped=("skipped", "sum"))
rates = rates.reset_index()
rates["skip_rate"] = (rates["skipped"] / rates["plays"] * 100).round(1)
rates = rates.sort_values("skip_rate", ascending=False).reset_index(drop=True)
print(rates)

Path("output").mkdir(exist_ok=True)
rates.to_csv("output/device_skip_rate.csv", index=False)

known = rates[rates["device"] != "unknown"]
fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.barh(known["device"], known["skip_rate"])
ax.invert_yaxis()
ax.bar_label(bars, labels=[f"{r:.1f}%" for r in known["skip_rate"]], padding=3)
ax.set_title(f"The {known.iloc[0]['device']} gets skipped most: "
             f"{known.iloc[0]['skip_rate']:.1f}% of plays")
fig.tight_layout()
fig.savefig("output/device_skip_rate.png", dpi=150)
print("wrote output/device_skip_rate.csv and output/device_skip_rate.png")


# ---------------------------------------------------------------- the pipeline
# TODO: rebuild everything above as functions, then delete the notebook way.
#
# ROOT = Path(__file__).resolve().parents[?]     # how many folders up is the repo?
#
# def load_messy(path):
# def clean_plays(df):
# def skip_rate_by_device(plays):
# def save_csv(table, path):
# def save_chart(rates, path):
# def check_rates(path, plays):
# def main():      # prints a line after each stage; first line: matplotlib.use("Agg")
#
# if __name__ == "__main__":
#     main()
