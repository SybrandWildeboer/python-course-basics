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
| `homework/README.md` | The ten homework questions, with two collapsible hints |
| `homework/answers.sql` | Where they write their answers |
| `homework/solutions/answers.sql` | Worked answers, plus two invented questions as examples |

Every query in these files is executed by `python3 tools/check_sql.py`, which also checks the
row counts pinned in `-- expect: N rows` comments. If you edit the dataset, run it.

## Watch out for

- **`=` not `==`.** A Python habit, and the error message is not always obvious.
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
