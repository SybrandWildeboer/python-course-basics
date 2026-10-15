# Session 5: SQL, foundations and joins

**Goal:** they can ask a database questions and get answers back, across more than one
table. And they can spot fan-out and explain it.

**Slides:** [`slides/session-05.html`](../../slides/session-05.html) (40 slides)

---

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00–0:10 | Homework review: the genre averages, the 2025 tie, his repo on GitHub | Slide 2 |
| 0:10–0:20 | The relational idea, the three tables, open DB Browser | Slides 3–6 |
| 0:20–0:35 | `SELECT`, `WHERE`, `IN` / `BETWEEN` / `LIKE`, `NULL`, `ORDER BY`, `LIMIT`, `DISTINCT` | Slides 7–14 |
| 0:35–0:50 | Aggregates, `GROUP BY`, the grouping trap, `HAVING`, execution order, SQL next to his Python | Slides 15–21 |
| 0:50–1:00 | The ladder of ten, as a sprint | Slide 22 |
| 1:00–1:10 | Break | |
| 1:10–1:25 | Why data is split, keys, first join, `LEFT JOIN`, join then aggregate | Slides 23–31 |
| 1:25–1:45 | **Fan-out.** The wrong total, why, the fake fix, the real fix, the diagnosis table | Slides 32–37 |
| 1:45–1:55 | Live exercise: break it on purpose, explain it in a comment | Slide 38 |
| 1:55–2:00 | Homework, commit, push | Slides 39–40 |

Two sessions' worth of SQL in one, and it fits because the first half is one idea with
variations: he already has filtering, sorting and counting from session 4. Keep saying so,
and keep the first half moving.

**If you run short of time, take it from the first half.** `IN` / `BETWEEN` / `LIKE` and
`DISTINCT` can be pointed at rather than taught, and the ladder can shrink to rungs 8 to 10.
**Never cut the fan-out block.** It is the one idea from this session he will still be using
in ten years. If the earlier blocks run fast, spend the time there, not on the stretch.

## The slides that matter

**Slide 12, `NULL`.** Three artists genuinely have missing values, so `= NULL` returning
nothing is a real demonstration and not a hypothetical. Silent empty results that look like
answers are the thing to fear.

**Slide 18, the `GROUP BY` trap.** Run the wrong version live. SQLite allows a column that is
neither grouped nor aggregated and picks a value at random, so the result table looks
plausible and is meaningless. Most other databases refuse outright.

**Slide 21, SQL next to his own Python.** The left side is his session 4 homework question,
average minutes per genre. Put his own version on screen beside the `GROUP BY` if he has it.
Nothing else you can say will sell SQL as effectively.

**Slides 33 to 36, the fan-out block.**

- **33, the wrong total.** 8,980.4 minutes becomes 9,732.1 because a table was joined on. Let
  it sit for a moment before explaining. The discomfort is the point.
- **34, why.** Fjord & Flint has 237 plays and 3 awards, and after the join has 711 rows.
  Work the arithmetic out loud with him.
- **35, the fake fix.** `SUM(DISTINCT)` gives 680.6 when the truth is 846.2. Two wrong
  answers sit either side of the right one, and both look like fixes. Nearly every beginner
  reaches for `DISTINCT` here, and almost nobody checks whether it is the right tool.
- **36, the real fix.** Aggregate first in a CTE, then join. The verification matters as much
  as the fix: 846.2 matches the standalone query exactly, so it is confirmed by an
  independent calculation rather than by looking plausible.

Slide 37, the diagnosis table, is the practical residue of the whole session. Leave it up
while he does the live exercise.

## What they use

| File | What it is |
|---|---|
| `demos/foundations.sql` | Every query from the first half of the slides, with the real answers in comments |
| `demos/joins.sql` | Every query from the second half: joins, the full fan-out demonstration and the CTE fix |
| `exercises/queries.sql` | The ladder of ten, as comments to fill in |
| `solutions/queries.sql` | Worked answers, with row counts pinned |
| `exercises/joins.sql` | The joins live exercise, as comments to fill in |
| `solutions/joins.sql` | Worked answers, with the fan-out explanation written out in full |
| `solutions/stretch.sql` | The stretch queries, with row counts pinned so the stretch notebook's numbers stay true |
| `homework/README.md` | The fifteen homework questions and the join-type task, with collapsible hints |
| `homework/answers.sql` | Where they write their answers |
| `homework/solutions/answers.sql` | Worked answers, including the wrong versions of 13 and 15 |

Every query in these files is executed by `python tools/check_sql.py`, which also checks the
row counts pinned in `-- expect: N rows` comments. If you edit the dataset, run it.

## Notebooks

DB Browser is the main tool this session, because seeing the tables in a window is worth a lot
while the ideas are new. The notebooks are the same queries run from Python, which is how he
will actually use SQL in a project. For the fan-out block the notebook is the better tool:
having the wrong number and the right number on screen together is most of the lesson.

| Notebook | What it is |
|---|---|
| `notebooks/01-sql-from-python.ipynb` | The first half of the slides via `sqlite3`, with a small `run()` helper that prints results as a table. The Python counting dictionary and the `GROUP BY` side by side, checked equal with an `assert` |
| `notebooks/02-queries-exercise.ipynb` | The ladder of ten |
| `notebooks/02-queries-solved.ipynb` | Worked answers, with rungs 3, 4, 6 and 10 pinned by `assert` |
| `notebooks/03-joins-from-python.ipynb` | Joins, then the full fan-out demonstration: the wrong total, the row count that reveals it, the `SUM(DISTINCT)` that makes it worse, and the CTE that fixes it, checked against the standalone query |
| `notebooks/04-joins-exercise.ipynb` | The joins live exercise, including the written explanation |
| `notebooks/04-joins-solved.ipynb` | Worked answers, and the second bug in the broken query: eleven countries silently disappear |
| `notebooks/05-questions-homework.ipynb` | The homework, for working in a notebook instead of DB Browser |
| `notebooks/05-questions-solved.ipynb` | Worked answers, every one pinned with an `assert` |
| `notebooks/06-stretch-exercise.ipynb` | Optional stretch questions, for when an exercise finishes early |
| `notebooks/06-stretch-solved.ipynb` | Worked versions, with the reasoning written out |

## Before the session

- [ ] Check DB Browser for SQLite is installed on his machine (he installs it after session 4)
- [ ] Check the database is generated: `python data/scripts/build_dataset.py`
- [ ] Have his session 4 genre script ready to put next to slide 21
- [ ] Open `notebooks/03-joins-from-python.ipynb` and run it once, so the fan-out numbers are
  on screen if DB Browser misbehaves

## If there is time left

The stretch notebook has eight questions about the listening data that get harder as you go.
Use as many as the time allows; you don't need to finish it. 1 to 3 stay on one table, so
they fit after the ladder; 4 to 8 need joins. Each one adds one idea:

| # | Question | What it adds |
|---|---|---|
| 1 | How many artists are still active? | **Trap:** `COUNT(still_active)` says 39, the answer is 34, and active plus inactive is 39, not 40 |
| 2 | Which tracks were played on all five devices? | **Trap:** `skipped = 0` in `WHERE` gives 30, in `HAVING` it gives a plausible, wrong 29 |
| 3 | Do I listen more at the weekend? | `strftime('%w', ...)` and `CASE`, then totals against rates |
| 4 | Who did I not play in 2025? | A `WHERE` that silently turns a left join into an inner one, the fix in the `ON`, and `IS NULL` to find rows with no match |
| 5 | Spot the bug | A fan-out where both counts multiply each other, and why `COUNT(DISTINCT key)` is a safe repair when `SUM(DISTINCT value)` was not |
| 6 | 2024 against 2025 | Three chained CTEs, starting from the right table so the artists who dropped to zero stay in |
| 7 | The same fix, three ways | The CTE fix as a nested subquery, a subquery after `IN`, and a `TEMP VIEW` |
| 8 | The top artist in every genre | A first window function: `RANK() OVER (PARTITION BY ...)` |

Numbers 1, 2 and 5 are the ones to talk through rather than just check. Make him predict
before running: each query runs without complaint and gives an answer that looks fine.
Number 3 is the same lesson in a different form: 1,573 weekday plays against 610 sounds like
a finding, and per day it is 3.19 against 3.23. Number 5 is fan-out from the other side: the
difference between a key and a value is what decides whether `DISTINCT` can help.

Number 8 is not needed for the rest of the course. If he gets that far, the point to land is
why the rank needs its own CTE before it can be filtered, which ties straight back to the
execution order slide.

## Watch out for

- **`=` not `==`.** A Python habit. SQLite quietly accepts `==` as well, so nothing breaks,
  but most other databases reject it. Steer him to `=` now.
- **Double quotes around text.** SQL wants `'phone'`. Double quotes mean an identifier, and
  the resulting error is confusing.
- **`= NULL`.** Runs, returns nothing, warns nobody. Slide 12.
- **Selecting ungrouped columns.** SQLite permits it and gives nonsense. Slide 18.
- **`WHERE` versus `HAVING`.** Trying to filter on `COUNT(*)` in a `WHERE` is the error he
  will hit, probably on rung 10; the execution-order slide explains why in one picture.
- **`LIMIT` without `ORDER BY`.** Gives arbitrary rows. SQLite happens to look stable, which
  teaches a habit that breaks on a real database.
- **Ambiguous column names.** The error is clear once seen once, which is why it is on a
  slide and demonstrated in the notebook.
- **`COUNT(*)` after a `LEFT JOIN`.** Reports 1 for a row with no matches. This is how "never
  played" silently becomes "played once".
- **Fan-out, and reaching for `DISTINCT`.** The habit to install: after any join, compare the
  row count with what it was before. Slide 35 exists for the `DISTINCT` reflex.
- **Assuming the keys match.** Not a problem in this dataset, and a huge one in real work.
  Worth a sentence: if a join returns nothing, compare a few key values from each side by eye.
- **Integer division.** In SQLite `19 / 179` is `0`. `100.0 * x / y` fixes it, and it comes
  up in homework question 9.

## Definition of done

He can write a query with `WHERE`, `GROUP BY`, `HAVING` and `ORDER BY` in it and say why
`HAVING` exists; he can write a join with an aggregate and choose the join type deliberately;
and he can explain fan-out in his own words. The explanation matters more than the SQL.
