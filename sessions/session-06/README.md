# Session 6: pandas

**Goal:** the questions from session 5, answered in Python, and a deliberately messy file
turned into data you can trust. They leave able to write the pandas twin of a SQL query, to
spot fan-out in either language, to say how much each cleaning decision moved the answer,
and with the dates and table shapes that session 7 will chart.

**Slides:** [`slides/session-06.html`](../../slides/session-06.html) (33 slides)

The session has two halves that feel different. The first is fast: nothing in it is a new
idea, because every question has already been answered with a loop in session 4 and with SQL
in session 5. Keep saying "you already know this one"; it is what makes a library with
hundreds of methods feel small. The second half is slow and forensic: one kind of damage at a
time, with a number checked after every fix.

---

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00–0:10 | Homework review: questions 11 to 15, inner versus left | Slide 2 |
| 0:10–0:25 | A DataFrame, first looks, `read_sql`, masks and **the `&` and `\|` trap** | Slides 3–8 |
| 0:25–0:40 | `groupby` and `agg`, `merge`, **fan-out and `validate=`** | Slides 9–13 |
| 0:40–0:50 | Live exercise: break a merge, explain it, fix it, guard it | Slide 14 |
| 0:50–1:00 | Break | |
| 1:00–1:20 | The messy file: look first, the inventory, text, numbers as text, dates, `NA` | Slides 15–22 |
| 1:20–1:35 | Duplicates, missing values, **the ledger**, the zero count, how close | Slides 23–27 |
| 1:35–1:45 | Dates as dates, totals per month, long to wide: the tables session 7 draws | Slides 28–30 |
| 1:45–1:55 | Live exercise: the cleaning as two functions | Slide 31 |
| 1:55–2:00 | Homework briefing, commit and push | Slides 32–33 |

This is two old sessions in one, so the slides carry only what is needed live and the
notebooks carry the rest. The four SQL-and-pandas queries side by side, "when SQL, when
pandas", and the five irritations (`SettingWithCopyWarning`, `inplace=True`, the index after a
`groupby`) are in notebooks 01 and 02, not on slides. Point at them; do not walk through them.

If something has to be cut, in this order: shorten the first half to a demo of slides 7, 8
and 10 (he has SQL fresh); shorten part three to the genre-by-year table; let the second live
exercise run into the homework. **Never cut slides 12 and 13 (fan-out and `validate=`), and
never cut the ledger (slide 25).**

## The slides that carry the session

**Slide 8, `&`, `|` and brackets.** Promised in session 2 as the thing that "trips everybody
up". Two of the four examples crash, which is the friendly outcome, and one is the right way.
The fourth runs and is wrong: long plays on the phone or laptop is 523 with the right brackets
and 871 without, because `&` is worked out before `|`. Let him hit the `ValueError` for real
before showing the fix; the message makes sense once he has seen a mask printed.

**Slide 12, fan-out in pandas.** Session 5 ended with "fan-out exists there too, and it is
called the same thing". 8,980.4 becomes 9,732.1 in pandas too, 2,183 rows become 2,371. The
pandas fake fixes fail differently from `SUM(DISTINCT)`: `drop_duplicates()` removes nothing at
all, because each fanned-out row carries a different award; de-duplicating the minutes gives
680.6 for Fjord & Flint, exactly the `SUM(DISTINCT)` answer.

**Slide 13, `validate=`.** A CTE becomes a variable with a good name, and the fix is the same:
aggregate first, then merge, and Fjord & Flint is back to 846.2. Then `validate="many_to_one"`
turns the silent fan-out into a `MergeError`. SQL has no equivalent switch. Of the first half,
it is the habit most worth taking away.

**Slide 19, numbers as text.** `pd.to_numeric(errors="coerce")` straight away makes 190
missing values from a column with 94 empty cells, and the total drops from 8,769.9 to
8,333.2. Nothing warns you. The habit: count the missing values before and after every
`coerce`.

**Slide 20, the dates.** `format="mixed"` parses every row without a word and gets 159 dates
wrong. Work the arithmetic out loud: 430 European dates, 174 that fit either way round, 15 of
those harmless because day and month are equal. The plain `pd.to_datetime` call that fails
with a `ValueError` is the good outcome, and the error message itself suggests the bad fix.

**Slide 25, the ledger.** Total minutes and phone plays after each step. The total goes
8,333.2, 8,769.9, 8,608.0, against 8,980.4 in the clean file; phone plays go 799, 1,024,
1,004, against 1,039. Every row is a confident answer, and only the last one is checked.
This is the session.

**Slide 27, how close did we get.** Seven of the nine columns match the clean file in every
row. The two that do not are exactly the information destroyed before we got the file: 94
minutes and 69 devices. The 372.4-minute gap in the total is precisely those 94 plays.
"Cleaning recovers what the file still knows, labels what it does not, and never makes
things up."

**Slides 29 and 30, dates and shapes.** Short and new, and they set up session 7. `.dt` on a
real date, plays per month with `groupby(... .dt.to_period("M"))` (24 months, 57 to 127
plays), minutes per month with `resample("MS")` (October 2024 554.6, June 2025 231.1), and
long to wide with `unstack` and `pivot_table`. The zero count comes back in a new costume: the
tablet's May 2024 **sum** is 0.0, a claim nobody made, while the mean is `NaN`;
`sum(min_count=1)` keeps it unknown. The genre-by-year table is the session 4 stretch's
hand-built pivot table, in one line: Folk 236 to 202, down 34.

## Promises this session keeps

- **Session 2:** the `&` and `|` brackets that "trip everybody up". Slide 8.
- **Session 2:** "you will divide by a count that happens to be zero". Slide 26. May 2024 has
  one tablet play, and it is one of the 94 with no minutes, so the session 3 `average` hits
  `ZeroDivisionError` while pandas quietly returns `NaN`. It falls out of the data; nothing
  was planted.
- **Session 4:** a DataFrame is the list-of-dicts table (slide 4), and the stretch's pivot
  table in one line of pandas (slide 30).
- **Session 5:** `phone` versus `PHONE` "is what session 6 is about". Slide 18. And fan-out
  "exists in pandas too, and it is called the same thing". Slide 12.
- **Session 8:** the cleaning ends as `load_messy(path)` and `clean_plays(df)` in
  `solutions/cleaning.py`, which the session 8 project reuses by name.

Session 1's `:.1f` "for chart labels" is session 7's to keep.

## What they use

| File | What it is |
|---|---|
| `demos/dataframes.py` | Walkthrough part one: loading, looking, columns, filtering, grouping, merging |
| `demos/sql_and_pandas.py` | Four session 5 queries both ways, each pair checked with an `assert`, ending in fan-out and `validate` |
| `demos/cleaning.py` | Walkthrough part two as a script, printing the ledger as it goes |
| `demos/dates_and_shapes.py` | Walkthrough part three: `.dt`, per month, the sum of nothing, long and wide |
| `exercises/joins_in_pandas.py` | Live exercise 1 starter |
| `solutions/joins_in_pandas.py` | Worked version, every number in the comments pinned with an `assert` |
| `exercises/cleaning_functions.py` | Live exercise 2 starter, with the checks commented out |
| `solutions/cleaning.py` | `load_messy` and `clean_plays`, verified against the clean file. **Session 8 builds on this file** |
| `homework/README.md` | The two tasks, with four collapsible hints |
| `homework/answers_in_pandas.py`, `homework/decisions.py` | Homework starters |
| `homework/solutions/` | Both answers, with the reasoning in comments |

The scripts print everything, because a script shows nothing unless you ask. That difference
from a notebook is worth a sentence: in a notebook the last line of a cell displays itself.

### The two functions, for session 8

```python
load_messy(path)   # pd.read_csv(path, keep_default_na=False): nothing guessed
clean_plays(df)    # returns a new DataFrame; the input is not changed
```

`clean_plays` returns the same nine columns, in the same order and with the same dtypes, as
`pd.read_csv("data/clean/plays.csv")`: `played_at` as `YYYY-MM-DD` text, `minutes_played`
as float with `NaN` for the 94 unknown lengths, `device` with `"unknown"` for the 69 blanks,
2,183 rows sorted by `play_id` with a fresh index.

## Notebooks

| Notebook | What it is |
|---|---|
| `notebooks/01-dataframes.ipynb` | From a list of dicts to a DataFrame, where pandas comes from (pip and PyPI), the first looks, columns, `.loc` and its inclusive slice, masks and the brackets trap, sorting, `value_counts`, `groupby`, `read_sql`, `merge`, the five irritations. Ends with a SQL-to-pandas table |
| `notebooks/02-sql-and-pandas.ipynb` | Four session 5 queries side by side with `assert`s, the fan-out diagnosis, the fake fixes, the real fix, `validate`, and when SQL versus pandas |
| `notebooks/03-joins-in-pandas-exercise.ipynb` | Live exercise 1 |
| `notebooks/03-joins-in-pandas-solved.ipynb` | Worked answers, including the second bug: 25 countries become 14 |
| `notebooks/04-cleaning.ipynb` | Every kind of damage found and fixed (`repr` to see the trailing space, `duplicated(keep=False)` to look before deleting), the ledger, the zero count, and the comparison with the clean file |
| `notebooks/05-dates-and-shapes.ipynb` | `.dt`, plays and minutes per month, the sum of nothing, long and wide, `pivot_table`, `fill_value=0`, and one `.plot()` glance |
| `notebooks/06-cleaning-functions-exercise.ipynb` | Live exercise 2 |
| `notebooks/06-cleaning-functions-solved.ipynb` | Worked version, with the usual wrong numbers and what causes each |
| `notebooks/07-answers-and-decisions-homework.ipynb` | The homework: the ten session 5 questions, the join-type question, the decision diary |
| `notebooks/07-answers-and-decisions-solved.ipynb` | Worked version, the traps marked, a verdict, and the diary |
| `notebooks/08-stretch-exercise.ipynb` | Optional stretch exercises, for when a live exercise finishes early |
| `notebooks/08-stretch-solved.ipynb` | Worked versions, with the reasoning written out |

Each notebook starts with a short cell that walks up to the repository root, so it works
whichever folder VS Code opened it from. Notebooks 05, 07 and 08 import `load_messy` and
`clean_plays` from `solutions/cleaning.py` with a `sys.path` line. If the learner's own
functions passed every check, they should paste theirs in instead.

## Before the session

- [ ] Check the dataset is generated: `python data/scripts/build_dataset.py`
- [ ] Open `data/messy/plays_messy.csv` in VS Code, so you can show the raw text: the capitals,
  the three date styles, the trailing space in the header
- [ ] Have their session 5 `answers.sql` and the session 5 joins exercise to hand: they are the
  answer key for live exercise 1 and the homework
- [ ] Run `notebooks/05-dates-and-shapes.ipynb` once, so matplotlib has built its font cache
  before the `.plot()` glance

## If there is time left

The stretch notebook has seven exercises that get harder as you go. Use as many as the time
allows; you don't need to finish it. Numbers 1 to 4 build on the first half, 5 to 7 on the
cleaning. None of them repeat the walkthrough, the exercises or the homework, and each one
adds one idea:

| # | Exercise | What it adds |
|---|---|---|
| 1 | Merge `artists.csv` on by name | `_x` and `_y` suffixes from clashing columns, selecting columns before a merge, `validate` on a name key |
| 2 | Plays per decade the artist was formed | **Trap:** `groupby` silently drops `NaN` keys, so 53 plays vanish and the total is 2,130; `dropna=False` |
| 3 | Who is in one table and not the other? | `~` and `isin`, then `merge(indicator=True)`, and a small fan-out in a yes-or-no merge |
| 4 | The top artist in each genre | `sort_values` then `groupby().head(1)`, and second place: Electronic is won by 5.8 minutes |
| 5 | `damage_report` | A list of dicts turned into a DataFrame; why 2,183 spellings of `play_id` is not damage |
| 6 | What were the unknowns? | `merge` with `suffixes` and `validate="one_to_one"`; missing at random or for a reason |
| 7 | Guess the missing minutes | `groupby().transform("median")` to impute, marked against the truth |

Numbers 2 and 7 are the ones to talk through rather than just check. In 2, ask him to add the
decade counts up before showing the fix. Nothing errors; 53 plays from Rosewood Lane and
Cassette Revival simply are not in any group. The habit it installs, checking that the groups
add up to the total, is the `groupby` version of checking the row count after a merge. In 7,
the artist median is a worse guess than the plain average (27.0 minutes too many against
14.9), because the missing plays were skipped more often than the rest, 16.0% against 11.8%.
Adding `skipped` to the group lands within 3.4 minutes of the truth. Ask which total they
would report, and what they would write next to it.

## Watch out for

- **`and` and `or` in a filter.** The `ValueError` about "the truth value of a Series" is the
  error of the first half. Slide 8.
- **Missing brackets around an `|` inside an `&`.** No error, wrong number. The defence is to
  name each condition on its own line first.
- **Single versus double brackets.** `plays["genre"]` is a column, `plays[["genre"]]` is a
  one-column table. Ask "do you want a column, or a table?"
- **Forgetting to assign back.** `sort_values`, `rename` and `df["device"].str.lower()` all
  return something new and change nothing. When "my fix did nothing", this is why. The mirror
  image of `x = x.sort()` from session 4.
- **`merge` is an inner join by default.** It is why eleven countries vanish in live exercise
  1. Ask how many countries there are before and after.
- **`size` versus `count`.** `COUNT(*)` versus `COUNT(column)` with new names. Slide 11.
- **`SettingWithCopyWarning`.** Notebook 01 triggers it on purpose, on a copy: the chained
  `demo[long_ones]["device"] = "LONG"` warns and changes 0 rows, and the `.loc` line changes
  all 32. `.loc` for changing the original, `.copy()` after a filter for "a new table".
- **`inplace=True`.** Many tutorials use it. Tell them not to: it returns `None`, so nothing
  chains after it.
- **Reaching for `errors="coerce"` first.** It hides failures by design. Count the missing
  values before and after, every time.
- **Trusting `format="mixed"`.** The error message suggests it, which makes it feel
  endorsed. It is the single most dangerous line in the session.
- **`value_counts()` hiding missing values.** Without `dropna=False`, 70 blank devices
  vanish from the table. `groupby` drops missing keys the same way.
- **`dropna()` with no arguments.** It throws away 159 rows when the question needed 94.
- **`fillna(0)` as a placeholder.** Zero is a claim. It drags the average from 4.121 to
  3.943. `resample(...).sum()` makes the same claim for an empty month without being asked.
- **The dtypes check failing on `played_at`.** The clean file stores dates as text; parsed
  dates need `.dt.strftime("%Y-%m-%d")` before the comparison.
- **Decimals where they expected whole numbers.** `formed_year` is `2014.0` because a column
  with a `NaN` in it is stored as decimals. Not a bug; a sign there are missing values.
- **`No module named 'pandas'`.** The kernel's Python is not the one pandas went into. Step 8
  of `slides/install.html` has the commands; session 8 fixes the underlying problem with a
  virtual environment.
- **Not knowing the clean file is a cheat.** Say it more than once: real work has no answer
  key, which is why every step has its own check.

## Definition of done

They can load a DataFrame from a CSV and from SQL, filter it with `&` and `|` correctly, group
and merge it, and check a merge with the row count and `validate=`. They can find each kind of
damage with `info`, `value_counts` and `duplicated`, fix it, and say how much the fix moved a
headline number. They can turn a date column into real dates and a long table into a wide
one, and they have `load_messy` and `clean_plays` passing every check, ready for session 8.
