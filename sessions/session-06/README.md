# Session 6: SQL foundations

**Goal:** they can ask a database questions and get answers back.

**Slides:** [`slides/session-06.html`](../../slides/session-06.html) (25 slides)

---

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00–0:15 | Homework review: their repo, their commit messages | Slide 2 |
| 0:15–0:30 | The relational idea, why a database, the three tables | Slides 4–6 |
| 0:30–0:35 | Open DB Browser and look around | Slide 7 |
| 0:35–0:50 | `SELECT`, `WHERE`, combining conditions | Slides 9–11 |
| 0:50–1:00 | Break | |
| 1:00–1:20 | `IN` / `BETWEEN` / `LIKE`, `NULL`, `ORDER BY`, `LIMIT`, `DISTINCT` | Slides 12–15 |
| 1:20–1:40 | Aggregates, `GROUP BY`, the grouping trap, `HAVING` | Slides 17–20 |
| 1:40–1:45 | Execution order, and SQL next to their session 4 Python | Slides 21–22 |
| 1:45–1:55 | The ladder of ten questions | Slide 23 |
| 1:55–2:00 | Homework, commit, push | Slides 24–25 |

That is a lot of keywords for one session, and it is fine: it is one idea with variations,
and they already have filtering, sorting and counting from session 4. Keep saying so.

## The three slides that matter

**Slide 13, `NULL`.** Three artists genuinely have missing values, so `= NULL` returning
nothing is a real demonstration and not a hypothetical. Silent empty results that look like
answers are the thing to fear.

**Slide 19, the `GROUP BY` trap.** Run the wrong version live. SQLite allows a column that is
neither grouped nor aggregated and picks a value at random, so the result table looks
plausible and is meaningless. Most other databases refuse outright.

**Slide 22, SQL next to their own Python.** Put their session 4 homework on screen beside the
one-line `GROUP BY`. Nothing else you can say will sell SQL as effectively.

## What they use

| File | What it is |
|---|---|
| `demos/walkthrough.sql` | Every query from the slides, with the real answers in comments |
| `exercises/queries.sql` | The ladder of ten, as comments to fill in |
| `solutions/queries.sql` | Worked answers, with row counts pinned |
| `solutions/stretch.sql` | The stretch queries, with row counts pinned so the stretch notebook's numbers stay true |
| `homework/README.md` | The ten homework questions, with two collapsible hints |
| `homework/answers.sql` | Where they write their answers |
| `homework/solutions/answers.sql` | Worked answers, plus two invented questions as examples |

Every query in these files is executed by `python3 tools/check_sql.py`, which also checks the
row counts pinned in `-- expect: N rows` comments. If you edit the dataset, run it.

## Notebooks

DB Browser is the main tool this session, because seeing the tables in a window is worth a lot
while the ideas are new. The notebooks are the same queries run from Python, which is how they
will actually use SQL in a project.

| Notebook | What it is |
|---|---|
| `notebooks/01-sql-from-python.ipynb` | Every query from the slides, via `sqlite3`, with a small `run()` helper that prints results as a table. Includes the Python counting dictionary and the `GROUP BY` next to each other |
| `notebooks/02-queries-exercise.ipynb` | The ladder of ten |
| `notebooks/02-queries-solved.ipynb` | Worked answers |
| `notebooks/03-stretch-exercise.ipynb` | Optional stretch questions, for when the ladder finishes early |
| `notebooks/03-stretch-solved.ipynb` | Worked versions, with the reasoning written out |

## If there is time left

The stretch notebook has six questions about the listening data that get harder as you go.
Use as many as the time allows; you don't need to finish it. No joins: everything stays on
one table at a time. Each one adds one idea:

| # | Question | What it adds |
|---|---|---|
| 1 | Which award is given most, and who won the same one twice? | The `awards` table, and `COUNT(*)` against `COUNT(DISTINCT ...)` in a `HAVING` |
| 2 | How many artists are still active? | **Trap:** `COUNT(still_active)` says 39, the answer is 34, and active plus inactive is 39, not 40 |
| 3 | In which decade were most artists formed? | Integer division as a tool, and `NULL` as its own group |
| 4 | Which tracks were played on all five devices? | **Trap:** `skipped = 0` in `WHERE` gives 30, in `HAVING` it gives a plausible, wrong 29 |
| 5 | Do I listen more at the weekend? | `strftime('%w', ...)` and `CASE`, then totals against rates |
| 6 | Which device lost listeners from 2024 to 2025? | `SUM(CASE ...)` to put two years side by side |

Numbers 2 and 4 are the ones to talk through rather than just check. Make him predict before
running: both queries run without complaint and give an answer that looks fine. Number 5 is
the same lesson in a different form: 1,573 weekday plays against 610 sounds like a finding,
and per day it is 3.19 against 3.23.

## Watch out for

- **`=` not `==`.** A Python habit. SQLite quietly accepts `==` as well, so nothing breaks,
  but most other databases reject it. Steer them to `=` now.
- **Double quotes around text.** SQL wants `'phone'`. Double quotes mean an identifier, and
  the resulting error is confusing.
- **`= NULL`.** Runs, returns nothing, warns nobody. Slide 13.
- **Selecting ungrouped columns.** SQLite permits it and gives nonsense. Slide 19.
- **`WHERE` versus `HAVING`.** Trying to filter on `COUNT(*)` in a `WHERE` is the error they
  will hit; the execution-order slide explains why in one picture.
- **Integer division.** In SQLite `19 / 179` is `0`. `100.0 * x / y` fixes it, and it comes up
  in homework question 9.
- **`LIMIT` without `ORDER BY`.** Gives arbitrary rows. SQLite happens to look stable, which
  teaches a habit that breaks on a real database.

## Definition of done

They can write a query with `WHERE`, `GROUP BY`, `HAVING` and `ORDER BY` in it, and they can
explain why `HAVING` exists.
