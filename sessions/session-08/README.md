# Session 8: pandas

**Goal:** the questions from sessions 6 and 7, answered in Python. They leave able to read a
SQL query and write its pandas twin, and to say when they would reach for which.

**Slides:** [`slides/session-08.html`](../../slides/session-08.html) (23 slides)

Nothing in this session is a new idea, and that is the way to teach it. Every question has
already been answered with a loop in session 4 and with SQL in sessions 6 and 7. Keep saying
"you already know this one". It is true, and it is what makes a library with hundreds of
methods feel small.

---

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00–0:10 | Homework review: the CTE questions, inner versus left | Slide 2 |
| 0:10–0:25 | A DataFrame is the session 4 table; `read_csv`, the first looks, `read_sql` | Slides 4–6 |
| 0:25–0:40 | Columns, masks, and **the `&` and `|` trap** | Slides 7–9 |
| 0:40–0:55 | `value_counts`, `groupby` and `agg`, `sort_values`, `merge` | Slides 11–13 |
| 0:55–1:05 | Break | |
| 1:05–1:30 | **Four queries side by side**, ending with fan-out and `validate` | Slides 15–19 |
| 1:30–1:35 | When SQL, when pandas | Slide 20 |
| 1:35–1:55 | Live exercise: session 7's exercise, in pandas | Slide 21 |
| 1:55–2:00 | Homework, commit and push | Slides 22–23 |

Part one is fast for anyone who did the session 4 homework, and that is fine: if it runs
early, spend the time in part three rather than the stretch. The side-by-side block is the
session. If anything has to be cut, cut slide 7 (columns) to a one-minute demo, never slides
18 and 19.

## The slides that carry the session

**Slide 9, `&`, `|` and brackets.** Promised in session 2 as the thing that "trips everybody
up in session 8". Two of the four examples crash, which is the friendly outcome, and one is
the right way. The fourth runs and is wrong: long plays on the phone or laptop is 523 with the right brackets and 871 without,
because `&` is worked out before `|`. Let him hit the `ValueError` for real before showing the
fix; the message makes sense once he has seen a mask printed.

**Slide 11, same idea, three notations.** The line from session 4, slide 19, kept: the
counting dictionary, `GROUP BY genre`, and `groupby("genre")`, with identical numbers. Point
at the numbers.

**Slides 15 to 19, four queries side by side.** Each pair is run in
`02-sql-and-pandas.ipynb`, the SQL through `pd.read_sql`, with an `assert` that both give the
same answer. The four, chosen from the real session 6 and 7 material:

| # | From | What it shows |
|---|---|---|
| 1 | Session 6 ladder, rungs 4 and 5 | Filter and sort. 174 rows both ways. pandas writes the steps in the order they happen |
| 2 | Session 6 ladder, rung 10 | `HAVING` does not exist in pandas, and nothing is missing: filter the counts on the next line |
| 3 | Session 7, the artists the inner join hides | The `COUNT(*)` bug survives translation: `.size()` says Iron Fernway has 1 play, `.count()` says 0 |
| 4 | Session 7, the wrong total | Fan-out: 8,980.4 becomes 9,732.1 in pandas too, 2,183 rows become 2,371 |

**Slide 18, fan-out in pandas.** Session 7 closed with "fan-out exists there too, and it is
called the same thing". The pandas fake fixes fail differently from `SUM(DISTINCT)`:
`drop_duplicates()` removes nothing at all, because each fanned-out row carries a different
award; de-duplicating the minutes gives 680.6 for Fjord & Flint, exactly the `SUM(DISTINCT)`
answer.

**Slide 19, `validate=`.** A CTE becomes a variable with a good name, and the fix is the same:
aggregate first, then merge, and Fjord & Flint is back to 846.2. Then
`validate="many_to_one"` turns the silent fan-out into a `MergeError`. SQL has no
equivalent switch. Of everything today, it is the habit most worth taking away.

## What they use

| File | What it is |
|---|---|
| `demos/dataframes.py` | Walkthrough part one: loading, looking, columns, filtering, grouping, merging |
| `demos/sql_and_pandas.py` | The four queries both ways, each pair checked with an `assert` |
| `exercises/joins_in_pandas.py` | The live exercise starter |
| `solutions/joins_in_pandas.py` | Worked version, every number in the comments pinned with an `assert` |
| `homework/README.md` | The two tasks, with three collapsible hints |
| `homework/answers_in_pandas.py` | Homework starter, the ten session 6 questions as comments |
| `homework/solutions/answers_in_pandas.py` | Worked answers, each checked against the session 6 figures |

The scripts print everything, because a script shows nothing unless you ask. That difference
from a notebook is worth a sentence: in a notebook the last line of a cell displays itself.

## Notebooks

| Notebook | What it is |
|---|---|
| `notebooks/01-dataframes.ipynb` | From a list of dicts to a DataFrame, the first looks, columns, masks and the brackets trap, sorting, `value_counts`, `groupby`, `read_sql`, `merge`. Ends with a SQL-to-pandas table |
| `notebooks/02-sql-and-pandas.ipynb` | The four queries side by side with `assert`s, the fan-out diagnosis, the fake fixes, the real fix, `validate`, and when SQL versus pandas |
| `notebooks/03-joins-in-pandas-exercise.ipynb` | The live exercise |
| `notebooks/03-joins-in-pandas-solved.ipynb` | Worked answers, including the second bug: 25 countries become 14 |
| `notebooks/04-answers-in-pandas-homework.ipynb` | Homework: the ten session 6 questions |
| `notebooks/04-answers-in-pandas-solved.ipynb` | Worked answers, the traps marked, and a verdict on which was easier |
| `notebooks/05-stretch-exercise.ipynb` | Optional stretch exercises, for when the live exercise finishes early |
| `notebooks/05-stretch-solved.ipynb` | Worked versions, with the reasoning written out |

Each notebook starts with a short cell that walks up to the repository root, so it works
whichever folder VS Code opened it from. The notebooks are the main tool this session; having
the SQL answer and the pandas answer on screen together, with an `assert` between them, is
most of the lesson.

## If there is time left

The stretch notebook has six questions that get harder as you go. Use as many as the time
allows; you don't need to finish it. None of them repeat the live exercise or the homework,
and each one adds one idea:

| # | Question | What it adds |
|---|---|---|
| 1 | Genre by year as a table | `pd.crosstab` and `to_csv`: the session 4 stretch's hand-built pivot table, in one line, as promised there |
| 2 | Which artists get skipped most? | The `mean` of a 0/1 column is a rate, and a minimum number of plays as a filter after `groupby` |
| 3 | Merge `artists.csv` on by name | `_x` and `_y` suffixes from clashing columns, selecting columns before a merge, `validate` on a name key |
| 4 | Plays per decade the artist was formed | **Trap:** `groupby` silently drops `NaN` keys, so 53 plays vanish and the total is 2,130; `dropna=False` |
| 5 | Who is in one table and not the other? | `~` and `isin`, then `merge(indicator=True)`, and a small fan-out in a yes-or-no merge |
| 6 | The top artist in each genre | `sort_values` then `groupby().head(1)`, and second place: Electronic is won by 5.8 minutes |

Number 4 is the one to talk through rather than just check. Ask him to add the decade counts
up before showing the fix. Nothing errors; 53 plays from Rosewood Lane and Cassette Revival
simply are not in any group. It is the session 4 stretch decision (skip, pretend, or label)
made silently on his behalf, and the habit it installs, checking that the groups add up to
the total, is the `groupby` version of checking the row count after a merge.

Number 6 ends where the session 4 homework did: a ranking always produces a winner, whether or
not there is one. By plays, Rock is 64 against 63.

## Watch out for

- **`and` and `or` in a filter.** The `ValueError` about "the truth value of a Series" is the
  error of the day. Slide 9.
- **Missing brackets around an `|` inside an `&`.** No error, wrong number. The defence is to
  name each condition on its own line first.
- **`=` instead of `==` inside a mask.** `plays[plays["device"] = "car"]` is a `SyntaxError`,
  which at least is loud.
- **Single versus double brackets.** `plays["genre"]` is a column, `plays[["genre"]]` is a
  one-column table. Ask "do you want a column, or a table?"
- **`sort_values` without assigning the result.** It returns a new table; the old one is
  unchanged. The mirror image of `x = x.sort()` from session 4, and just as confusing the
  first time.
- **`plays.shape()`.** `shape` is not a method. `TypeError: 'tuple' object is not callable`.
- **Nothing printing in a script.** The notebook displays the last line of a cell; a script
  shows nothing without `print()`.
- **`merge` is an inner join by default.** It is why eleven countries vanish in part 2 of the
  exercise. Ask how many countries there are before and after.
- **`size` versus `count`.** `COUNT(*)` versus `COUNT(column)` with new names. Slide 17.
- **Decimals where they expected whole numbers.** `formed_year` is `2014.0` because a column
  with a `NaN` in it is stored as decimals. Not a bug; a sign there are missing values.
- **`SettingWithCopyWarning`.** If they filter a DataFrame and then add a column to the
  result, pandas may warn. None of today's material triggers it, but their own experiments
  might. The short explanation: pandas cannot tell whether you meant to change the filtered
  table or the original. Adding `.copy()` after the filter says "a new table", and the warning
  goes away for the right reason.

## Definition of done

They can load a DataFrame from a CSV and from SQL, filter it with `&` and `|` correctly, group
and merge it, and check a merge with the row count and `validate=`. And they can take a query
from their own session 6 or 7 file and write the pandas version without looking anything up
beyond the method names.
