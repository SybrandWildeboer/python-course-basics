"""The session 9 walkthrough, part one: cleaning the messy listening log.

Run it from the repository root, or the relative paths will not find the data:

    python sessions/session-09/demos/cleaning.py

Every kind of damage is found first and fixed second, and the headline numbers
are printed after each fix, because the lesson of the day is that every
cleaning decision changes the answer.
"""

import pandas as pd

MESSY = "data/messy/plays_messy.csv"
CLEAN = "data/clean/plays.csv"


def headline(df, label):
    """Print rows, total minutes (if they are numbers yet) and phone plays."""
    minutes = df["minutes_played"]
    total = f"{minutes.sum():,.1f}" if minutes.dtype == "float64" else "text, cannot add up"
    phone = (df["device"] == "phone").sum()
    print(f"  {label:28} rows {len(df):>5,}   minutes {total:>20}   phone {phone:>5,}")


# ------------------------------------------------------------ look first
df = pd.read_csv(MESSY)
print(df.shape)                          # (2223, 9): the clean log has 2183
print(df.columns.tolist())               # 'minutes played ' with two spaces
print(df.dtypes["minutes played "])      # object, which means text

# df["minutes played "].sum()
# TypeError: can only concatenate str (not "int") to str


# ------------------------------------------------------------ column names
df = df.rename(columns={"minutes played ": "minutes_played"})

print("\nthe headline numbers after each step:")
headline(df, "as loaded")


# ------------------------------------------------------------ numbers as text
# Converting straight away throws away every "4.4 min" as well as the blanks.
straight = pd.to_numeric(df["minutes_played"], errors="coerce")
print(f"  {'to_numeric straight away':28} missing {straight.isna().sum()}, "
      f"total {straight.sum():,.1f}")                       # 190 missing, 8,333.2

# Clean the text first, then convert. Now only the real blanks are missing.
fixed = pd.to_numeric(df["minutes_played"].str.replace(" min", ""), errors="coerce")
assert fixed.isna().sum() == df["minutes_played"].isna().sum() == 94
df["minutes_played"] = fixed
headline(df, "strip ' min' first")                          # 8,769.9


# ------------------------------------------------------------ text: phone, PHONE, "phone "
# value_counts() is SELECT DISTINCT from session 6. Twenty spellings of five devices.
df["device"] = df["device"].str.strip().str.lower()
df["genre"] = df["genre"].str.strip().str.title()
headline(df, "strip and lower device")                      # phone 799 -> 1,024


# ------------------------------------------------------------ dates written three ways
dates = df["played_at"]

# pd.to_datetime(dates)               ValueError: a GOOD error, it refuses to guess
guessed = pd.to_datetime(dates, format="mixed")       # no error, and silently wrong

parsed = pd.to_datetime(dates, format="%Y-%m-%d", errors="coerce")
parsed = parsed.fillna(pd.to_datetime(dates, format="%d/%m/%Y", errors="coerce"))
parsed = parsed.fillna(pd.to_datetime(dates, format="%d-%m-%Y", errors="coerce"))
assert parsed.isna().sum() == 0

print(f"\n  format='mixed' got {(guessed != parsed).sum()} dates wrong")     # 159
# 03/09/2025 is the 3rd of September. The guess says the 9th of March.
df["played_at"] = parsed


# ------------------------------------------------------------ NA: Namibia, or missing?
as_written = pd.read_csv(MESSY, keep_default_na=False)
print(f"  rows where country is the text 'NA': {(as_written['country'] == 'NA').sum()}")  # 49
# No artist is from Namibia, so here "NA" means missing. Fill it, and blank
# genres, from the same artist's other plays: every artist has one of each.
for column in ["country", "genre"]:
    lookup = df.dropna(subset=[column]).groupby("artist_name")[column].first()
    df[column] = df[column].fillna(df["artist_name"].map(lookup))
    assert df[column].isna().sum() == 0


# ------------------------------------------------------------ duplicates
print(f"  exact duplicate rows: {df.duplicated().sum()}")                 # 40
df = df.drop_duplicates()
headline(df, "drop duplicates")                             # 2,183 rows, 8,608.0


# ------------------------------------------------------------ what is still missing
print("\nstill missing:")
missing = df.isna().sum()
print(missing[missing > 0])                                 # device 69, minutes 94

minutes = df["minutes_played"]
print(f"  average, leave missing: {minutes.mean():.3f}")             # 4.121
print(f"  average, drop rows:     {minutes.dropna().mean():.3f}")    # 4.121, the same
print(f"  average, fill with 0:   {minutes.fillna(0).mean():.3f}")   # 3.943, a false claim
print(f"  dropna() on everything throws away {len(df) - len(df.dropna())} rows")  # 159

df["device"] = df["device"].fillna("unknown")      # still counted, still visible


# ------------------------------------------------------------ a count that is zero
def average(numbers):
    """Return the mean of a list of numbers, the session 3 way."""
    return sum(numbers) / len(numbers)


tablet = df[df["device"] == "tablet"]
months = tablet["played_at"].dt.strftime("%Y-%m")
may = list(tablet.loc[months == "2024-05", "minutes_played"].dropna())
print(f"\ntablet plays with minutes in May 2024: {len(may)}")         # 0
# average(may)                      ZeroDivisionError: division by zero
print(tablet.groupby(months)["minutes_played"].mean().loc["2024-05"])  # nan: pandas carries on


# ------------------------------------------------------------ how close did we get?
clean = pd.read_csv(CLEAN)
ours = df.sort_values("play_id").reset_index(drop=True)
ours["played_at"] = ours["played_at"].dt.strftime("%Y-%m-%d")

print("\ncells matching the clean file:")
for column in clean.columns:
    print(f"  {column:15} {(ours[column] == clean[column]).sum():>5} of {len(clean)}")

headline(clean, "the clean file")                           # 8,980.4
print(f"  the 94 unknown plays, in the clean file: "
      f"{clean.loc[ours['minutes_played'].isna(), 'minutes_played'].sum():.1f}")  # 372.4

# Cleaning recovers what the file still knows, labels what it does not, and
# never makes things up.
