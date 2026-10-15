# Session 9: Cleaning and visualization

**Goal:** turn a deliberately messy file into a chart that answers a question, and a learner
who can say how much each cleaning decision moved the answer.

**Slides:** [`slides/session-09.html`](../../slides/session-09.html) (25 slides)

The session has two halves that feel different. The first is slow and forensic: one kind of
damage at a time, with a number checked after every fix. The second is quick and visual. If
you run short, shorten the chart half, never the ledger.

---

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00–0:10 | Homework review: session 6 answers in pandas, and the verdict | Slide 2 |
| 0:10–0:20 | Look before you touch, and the inventory of damage | Slides 4–5 |
| 0:20–0:50 | Names, text, numbers, dates, and `NA` | Slides 6–10 |
| 0:50–1:00 | Break | |
| 1:00–1:20 | Duplicates, missing values, **the ledger**, the zero count, the comparison | Slides 11–15 |
| 1:20–1:40 | One question, one chart: titles, bar or line, honest axes, histogram and scatter, saving | Slides 17–21 |
| 1:40–1:57 | Thirty cells become two functions; live exercise | Slides 22–23 |
| 1:57–2:00 | Homework briefing | Slides 24–25 |

The live exercise is short on purpose: it is mostly moving tested code from notebook 01 into
two functions. If it finishes early, the stretch notebook is ready.

## The slides that carry the session

**Slide 7, numbers as text.** `pd.to_numeric(errors="coerce")` straight away makes 190
missing values from a column with 94 empty cells, and the total drops from 8,769.9 to
8,333.2. Nothing warns you. The habit to install: count the missing values before and
after every `coerce`.

**Slide 8, the dates.** `format="mixed"` parses every row without a word and gets 159 dates
wrong. Work the arithmetic out loud: 430 European dates, 174 that fit either way round, 15 of
those harmless because day and month are equal. The plain `pd.to_datetime` call that fails
with a `ValueError` is the good outcome, and the error message itself suggests the bad fix.

**Slide 13, the ledger.** Total minutes and phone plays after each step. The total goes
8,333.2, 8,769.9, 8,608.0, against 8,980.4 in the clean file; phone plays go 799, 1,024,
1,004, against 1,039. Every row is a confident answer, and only the last one is checked.
This is the session.

**Slide 15, how close did we get.** Seven of the nine columns match the clean file in every
row. The two that do not are exactly the information destroyed before we got the file: 94
minutes and 69 devices. The 372.4-minute gap in the total is precisely those 94 plays.
"Cleaning recovers what the file still knows, labels what it does not, and never makes
things up."

**Slide 20, a histogram and a scatter.** The stacked histogram of skipped and kept plays
carries the one statistics lesson of the session: the same 190 plays give 73.6% or 84.4%
depending on what you divide by. Notebook 02 also draws plays against minutes per artist as a
scatter, and ends each new chart with a "what this does not show" sentence, which homework
task 2 now asks for.

## Promises this session keeps

- **Session 2:** "by session 9 you will divide by a count that happens to be zero." Slide 14.
  May 2024 has one tablet play, and it is one of the 94 with no minutes, so the session 3
  `average` hits `ZeroDivisionError` while pandas quietly returns `NaN`. It falls out of the
  data; nothing was planted.
- **Session 1:** `:.1f` "comes back in session 9 for chart labels". Slide 17, in the title
  f-string and in `ax.bar_label(bars, fmt="{:.1f}")`.
- **Session 6:** `phone` versus `PHONE` "is what session 9 is about". Slide 6.
- **Session 10:** the cleaning ends as `load_messy(path)` and `clean_plays(df)` in
  `solutions/cleaning.py`, which the session 10 pipeline reuses by name.

## What they use

| File | What it is |
|---|---|
| `demos/cleaning.py` | Walkthrough part one as a script, printing the ledger as it goes |
| `demos/charts.py` | Walkthrough part two: three charts saved to `output/` |
| `exercises/cleaning_functions.py` | The live exercise starter, with the checks commented out |
| `solutions/cleaning.py` | `load_messy` and `clean_plays`, verified against the clean file. **Session 10 builds on this file** |
| `homework/README.md` | The decision diary and the one-chart task |
| `homework/decisions.py`, `homework/my_chart.py` | Homework starters |
| `homework/solutions/` | Both answers, with the reasoning in comments |

Scripts save charts rather than showing them: `plt.show()` in a script opens a window and
stops until it is closed. Every PNG goes into `output/`, which git ignores.

### The two functions, for session 10

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
| `notebooks/01-cleaning.ipynb` | Every kind of damage found and fixed (`repr` to see the trailing space, `duplicated(keep=False)` to look before deleting), the ledger, the zero count, and the comparison with the clean file |
| `notebooks/02-charts.ipynb` | One question, one chart: answer titles, `:.1f` labels, bar or line, the misleading axis, a histogram and a stacked histogram, a scatter, a "which chart when" table, saving a PNG |
| `notebooks/03-cleaning-functions-exercise.ipynb` | The live exercise |
| `notebooks/03-cleaning-functions-solved.ipynb` | Worked version, with the usual wrong numbers and what causes each |
| `notebooks/04-decisions-homework.ipynb` | The homework: decision diary and one chart |
| `notebooks/04-decisions-solved.ipynb` | Worked version, including a chart whose honest title is "neck and neck" |
| `notebooks/05-stretch-exercise.ipynb` | Optional stretch exercises, for when the live exercise finishes early |
| `notebooks/05-stretch-solved.ipynb` | Worked versions, with the reasoning written out |

Notebook 02 starts from the clean file on purpose, so the charts never wait on the cleaning.
The exercise then redraws one chart from their own cleaned data, and three bar labels move by
0.1: a small, visible effect of leaving the missing minutes out.

The homework and stretch notebooks import `load_messy` and `clean_plays` from
`solutions/cleaning.py` with a `sys.path` line. If the learner's own functions passed every
check, they should paste theirs in instead.

## Before the session

- [ ] Check the dataset is generated: `python data/scripts/build_dataset.py`
- [ ] Open `data/messy/plays_messy.csv` in VS Code, so you can show the raw text: the capitals,
  the three date styles, the trailing space in the header
- [ ] Run `notebooks/02-charts.ipynb` once, so matplotlib has built its font cache before the
  learner watches it do so

## If there is time left

The stretch notebook has six exercises that get harder as you go. Use as many as the time
allows; you don't need to finish it. None of them repeat the walkthrough, the exercise or the
homework, and each one adds one idea:

| # | Exercise | What it adds |
|---|---|---|
| 1 | `damage_report` | A list of dicts turned into a DataFrame; why 2,183 spellings of `play_id` is not damage |
| 2 | Draw the wrong dates | Two lines on one `ax`, a `label` and a legend; the wrong line looks perfectly normal |
| 3 | What were the unknowns? | `merge` with `suffixes` and `validate="one_to_one"`; missing at random or for a reason |
| 4 | An honest skip-rate chart | `barh`, custom bar labels with `zip`, a grey bar for `"unknown"` |
| 5 | Two years, side by side | `plt.subplots(1, 2, sharey=True)` and `unstack`; why a shared axis matters |
| 6 | Guess the missing minutes | `groupby().transform("median")` to impute, marked against the truth |

Numbers 3 and 6 are the ones to talk through rather than just check. In 3, the 69 unknown
devices turn out to be spread across devices in about the same shares as the whole log (35
were phones), which is what makes labelling or dropping them safe. In 6, the artist median
is a worse guess than the plain average (27.0 minutes too many against 14.9), because the
missing plays were skipped more often than the rest, 16.0% against 11.8%. Adding `skipped`
to the group lands within 3.4 minutes of the truth. Ask which total they would report, and
what they would write next to it.

## Watch out for

- **Forgetting to assign back.** `df["device"].str.lower()` on its own changes nothing.
  Nearly every pandas method returns a new object. When "my fix did nothing", this is why.
- **Reaching for `errors="coerce"` first.** It hides failures by design. Count the missing
  values before and after, every time.
- **Trusting `format="mixed"`.** The error message suggests it, which makes it feel
  endorsed. It is the single most dangerous line in the session.
- **`value_counts()` hiding missing values.** Without `dropna=False`, 70 blank devices
  vanish from the table. `groupby` drops missing keys the same way.
- **`dropna()` with no arguments.** It throws away 159 rows when the question needed 94.
- **`fillna(0)` as a placeholder.** Zero is a claim. It drags the average from 4.121 to
  3.943.
- **The dtypes check failing on `played_at`.** The clean file stores dates as text; parsed
  dates need `.dt.strftime("%Y-%m-%d")` before the comparison.
- **`plt.savefig` after `plt.show()`.** Blank PNG in a script. Save first.
- **A percentage without its "out of what".** Slide 20. 190 plays are under a minute and
  skipped: 73.6% of the 258 skips, but 84.4% of the 225 short plays. Move the line for
  "short" to two minutes and it is 98.4% against 65.0%, the other way round. "Most skips are
  short" and "most short plays are skips" are different claims; ask which one the title
  makes.
- **Not knowing the clean file is a cheat.** Say it more than once: real work has no answer
  key, which is why every step has its own check.

## Definition of done

They can find each kind of damage with `info`, `value_counts` and `duplicated`, fix it, and
say how much the fix moved a headline number. They can draw one chart with a title that
gives the answer, and they have `load_messy` and `clean_plays` passing every check, ready for
session 10.
