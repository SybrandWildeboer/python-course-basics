# pandas cheatsheet

Sessions 8 and 9, on one page.

---

## Loading

```python
import pandas as pd

df = pd.read_csv(path, parse_dates=["played_at"])
df = pd.read_csv(path, encoding="utf-8")
df = pd.read_csv(path, keep_default_na=False)      # take "NA" literally
df = pd.read_csv(path, na_values=["", "n/a", "-"]) # say what counts as missing

import sqlite3
con = sqlite3.connect("data/music.db")
df = pd.read_sql("SELECT * FROM plays", con, parse_dates=["played_at"])
con.close()
```

`read_sql` takes **any** query, so everything you know about SQL still applies. Let the
database filter and join, then hand pandas a smaller tidier table.

## The first five minutes with any table

Make this a ritual, in this order.

```python
df.shape            # (rows, columns)
df.info()           # types, and how many non-empty. RUN THIS FIRST
df.head(3)          # and .tail(3)
df.describe()       # count, mean, std, min, quartiles, max
df.dtypes
df.columns
```

Text columns show as `str` in pandas 3 and `object` in pandas 2. Same thing; most tutorials
online say `object`.

## Selecting

```python
df["genre"]                       # one column: a Series
df[["genre", "minutes_played"]]   # several: a DataFrame, note the DOUBLE brackets

df.loc[0, "genre"]                # by label
df.loc[0:2, ["genre", "device"]]  # .loc INCLUDES row 2, unlike everything else
df.iloc[0:2]                      # purely positional, excludes the end
```

## Filtering

```python
df[df["minutes_played"] > 8]

df[(df["minutes_played"] > 8) & (df["played_at"] >= "2025-01-01")]
df[df["device"].isin(["car", "tablet"])]
df[df["genre"].isna()]
df[df["genre"].notna()]
df[df["track_name"].str.contains("Lines")]
```

**`&` and `|`, never `and` / `or`**, and **brackets around every condition**. Python's `and`
wants one true-or-false value; here each side is thousands of them, which is what
`ValueError: The truth value of a Series is ambiguous` means.

## Sorting and counting

```python
df.sort_values("minutes_played", ascending=False)
df.sort_values(["device", "minutes_played"], ascending=[True, False])

df["device"].value_counts()                    # the counting dictionary, in one call
df["device"].value_counts(normalize=True)      # proportions instead of counts
df["device"].value_counts(dropna=False)        # SHOW the missing ones
df["device"].unique()
df["device"].nunique()
```

`value_counts(dropna=False)` on every categorical column of a new dataset. It is how you
find three spellings of the same word.

## Grouping

```python
df.groupby("genre")["minutes_played"].sum()
df.groupby("genre")["minutes_played"].agg(["count", "sum", "mean"]).round(2)

# named, and the closest match to SQL's AS
df.groupby("device").agg(
    plays=("play_id", "count"),
    minutes=("minutes_played", "sum"),
    avg=("minutes_played", "mean"),
).round(2)

df.groupby(["genre", "device"])["minutes_played"].sum()      # two keys
```

**After a groupby the key becomes the index**, so anything treating it as a column fails:

```python
by_genre = df.groupby("genre")["minutes_played"].sum().reset_index()
```

`reset_index()` is the reflex whenever a groupby result is awkward.

A useful trick: `.mean()` on a column of 0s and 1s gives you the **rate** directly.

```python
df.groupby("device")["skipped"].mean() * 100     # percentage skipped
```

## Merging (joins)

```python
both = plays.merge(artists, on="artist_id")                  # inner, the default
left = artists.merge(plays, on="artist_id", how="left")
df.merge(other, on="id", how="outer")
df.merge(other, left_on="a_id", right_on="id")

# which rows had no match
left[left["play_id"].isna()]
```

`NaN` is pandas' `NULL`. `.isna()` is its `IS NULL`.

**Fan-out happens here too, with the same arithmetic and the same name.** pandas gives you a
seatbelt that SQL does not:

```python
plays.merge(awards, on="artist_id", validate="many_to_one")
# MergeError: Merge keys are not unique in right dataset
```

`validate=` makes you state the shape you expect: `"one_to_one"`, `"one_to_many"`,
`"many_to_one"`, `"many_to_many"`. It turns a silent wrong answer into an error message.
Check `df["key"].is_unique` if you are not sure which shape you have.

## Cleaning

```python
df = df.rename(columns={"minutes played ": "minutes_played"})
print([repr(c) for c in df.columns])            # catches invisible trailing spaces

for col in ["genre", "device"]:
    df[col] = df[col].str.strip()               # STRIP BEFORE YOU COMPARE
df["genre"] = df["genre"].str.title()
df["device"] = df["device"].str.lower()

df["minutes_played"] = pd.to_numeric(df["minutes_played"], errors="coerce")
df["count"] = df["count"].astype(int)
```

`errors="coerce"` turns anything unreadable into `NaN` instead of stopping the program, which
makes it countable. **Always check `.isna().sum()` after a conversion.**

### Dates: parse per format, not conveniently

```python
# CONVENIENT AND WRONG when the column has mixed formats:
pd.to_datetime(col, format="mixed", dayfirst=True)
# dayfirst applies to the ISO dates too, so 2025-09-06 becomes the 9th of June.
# Runs without complaint.

# right:
raw = df["played_at"].str.strip()
df["played_at"] = (
    pd.to_datetime(raw, format="%Y-%m-%d", errors="coerce")
    .fillna(pd.to_datetime(raw, format="%d/%m/%Y", errors="coerce"))
    .fillna(pd.to_datetime(raw, format="%d-%m-%Y", errors="coerce"))
)
```

```python
df["played_at"].dt.year, .dt.month, .dt.day_name()
df.set_index("played_at")["minutes_played"].resample("MS").sum()   # by month
```

### Duplicates and missing values

```python
df.duplicated().sum()
df[df.duplicated(keep=False)]           # ALL copies, so you can look first
df = df.drop_duplicates()
df.duplicated(subset=["play_id"]).sum()

df.isna().sum()
df = df.dropna(subset=["minutes_played"])     # drop, with a subset
df["device"] = df["device"].fillna("unknown") # label
df["x"] = df["x"].fillna(df["x"].mean())      # fill, and be ready to defend it
```

**A bare `dropna()` drops a row if ANY column is empty.** Almost never what you want.

**Every one of these is a decision, not a rule.** Drop when the missing value makes the row
useless for your question; label when the row is still useful; fill only when you can defend
the invented value out loud. Write down what you chose.

```python
print(before.shape, "->", after.shape)        # ALWAYS
```

## New columns

```python
df["hours"] = df["minutes_played"] / 60
df["long"] = df["minutes_played"] > 8
df["label"] = df["genre"].where(df["genre"].notna(), "Unknown")
df = df.assign(pct=lambda d: 100 * d["skips"] / d["plays"])
```

## Charts

```python
import matplotlib
matplotlib.use("Agg")          # in a SCRIPT: save files, never open a window
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(9, 4.5))

ax.plot(x, y, marker="o")      # line: change over time
ax.bar(names, values)          # bar: comparing categories
ax.scatter(x, y, alpha=0.75)   # scatter: relationship between two numbers
ax.hist(values, bins=30)       # histogram: distribution of one number

ax.set_title("Say the finding, not the column names")
ax.set_xlabel("Month")
ax.set_ylabel("Minutes played")
ax.set_ylim(bottom=0)          # BAR CHARTS START AT ZERO
ax.legend()                    # if there is more than one series
ax.grid(axis="y", alpha=0.3)

fig.tight_layout()             # stops labels being cut off
fig.savefig("output/chart.png", dpi=150)
plt.close(fig)
```

**A chart without labels is not finished.** Title that states the finding, both axes labelled
with units, and a legend if there is more than one series.

`plt.show()` in a script blocks, waiting for a window to be closed. In a notebook it is fine.

## The five irritations

| You wrote | You get | Fix |
|---|---|---|
| `df[a > 1 and b < 2]` | `truth value of a Series is ambiguous` | `df[(a > 1) & (b < 2)]` |
| `df[df.x > 1]["y"] = 0` | `SettingWithCopyWarning` | `df.loc[df.x > 1, "y"] = 0` |
| `grouped["genre"]` | `KeyError` | `.reset_index()` first |
| `df.sort_values("x", inplace=True)` | works, confuses you later | `df = df.sort_values("x")` |
| `df["n"] + df["text"]` | nonsense or a `TypeError` | check `df.dtypes` |

`SettingWithCopyWarning` means "you may have changed a copy and I cannot tell". Assign with
`.loc` and it never appears.

`inplace=True`: just do not. It saves five characters, is no faster, does not chain, and
makes half your lines change things invisibly.

## SQL to pandas

| Idea | SQL | pandas |
|---|---|---|
| pick columns | `SELECT a, b` | `df[["a", "b"]]` |
| pick rows | `WHERE x > 1` | `df[df["x"] > 1]` |
| two conditions | `AND` / `OR` | `&` / `\|`, with brackets |
| one of a set | `IN (...)` | `.isin([...])` |
| missing | `IS NULL` | `.isna()` |
| sort | `ORDER BY x DESC` | `.sort_values("x", ascending=False)` |
| first n | `LIMIT 5` | `.head(5)` or `.nlargest(5, "x")` |
| distinct | `SELECT DISTINCT x` | `df["x"].unique()` |
| count per value | `GROUP BY x` + `COUNT(*)` | `df["x"].value_counts()` |
| group and aggregate | `GROUP BY x` | `.groupby("x").agg(...)` |
| filter groups | `HAVING` | filter the result after `.groupby()` |
| join | `JOIN ... ON` | `.merge(other, on=...)` |
| left join | `LEFT JOIN` | `.merge(..., how="left")` |
| rename output | `AS name` | named `agg`, or `.rename()` |

The five verbs are the same everywhere: **filter, group, aggregate, join, sort.**
