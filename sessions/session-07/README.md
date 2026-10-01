# Session 7: Joins and shaping

**Goal:** questions that span two tables, and a learner who can spot fan-out and explain it.

**Slides:** [`slides/session-07.html`](../../slides/session-07.html) (23 slides)

This session needs the most practice of any in the course. If you run short of time, cut
views and the subquery variations. Never cut the fan-out block.

---

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00–0:15 | Homework review: which two questions needed something new | Slide 2 |
| 0:15–0:25 | Why data is split, primary and foreign keys | Slides 4–5 |
| 0:25–0:50 | First join, how matching works, aliases, `USING` | Slides 7–9 |
| 0:50–1:00 | Break | |
| 1:00–1:20 | `LEFT JOIN`, when it matters, join then aggregate | Slides 10–12 |
| 1:20–1:45 | **Fan-out.** The wrong total, why, the fake fix, the real fix | Slides 14–18 |
| 1:45–1:50 | The diagnosis table | Slide 20 |
| 1:50–2:00 | Exercise brief, homework, commit and push | Slides 21–23 |

If the earlier blocks run fast, spend the time on fan-out rather than on views. It is the one
idea from this session they will still be using in ten years.

## The four slides that carry the session

**Slide 15, the wrong total.** Two queries side by side: 8,980.4 minutes becomes 9,732.1
because a table was joined on. Let it sit for a moment before explaining. The discomfort is
the point.

**Slide 16, why.** Fjord & Flint has 237 plays and 3 awards, and after the join has 711 rows.
Work the arithmetic out loud with them.

**Slide 17, the fake fix.** `SUM(DISTINCT)` gives 680.6 when the truth is 846.2. Two wrong
answers sitting either side of the right one, and both look like fixes. Nearly every beginner
reaches for `DISTINCT` here, and almost nobody checks whether it is the right tool.

**Slide 18, the real fix.** Aggregate first, then join. The verification matters as much as
the fix: 846.2 matches the standalone query exactly, so it is confirmed by an independent
calculation rather than by looking plausible.

## What they use

| File | What it is |
|---|---|
| `demos/walkthrough.sql` | Every query from the slides, with the real answers in comments |
| `exercises/joins.sql` | The live exercise, as comments to fill in |
| `solutions/joins.sql` | Worked answers, with the fan-out explanation written out in full |
| `solutions/stretch.sql` | The stretch queries, with row counts pinned so the stretch notebook's numbers stay true |
| `homework/README.md` | The five questions, plus the join-type task |
| `homework/answers.sql` | Where they write their answers |
| `homework/solutions/answers.sql` | Worked answers |

Everything is executed by `python3 tools/check_sql.py`, which also verifies the row counts
pinned in `-- expect: N rows` comments.

## Notebooks

| Notebook | What it is |
|---|---|
| `notebooks/01-joins-from-python.ipynb` | Joins, then the full fan-out demonstration: the wrong total, the row count that reveals it, the `SUM(DISTINCT)` that makes it worse, and the CTE that fixes it |
| `notebooks/02-joins-exercise.ipynb` | The live exercise, including the written explanation |
| `notebooks/02-joins-solved.ipynb` | Worked answers, and the second bug in the broken query: eleven countries silently disappear |
| `notebooks/03-stretch-exercise.ipynb` | Optional stretch questions, for when the live exercise finishes early |
| `notebooks/03-stretch-solved.ipynb` | Worked versions, with the reasoning written out |

The notebook is the better tool for the fan-out block, because having the wrong number and
the right number on screen together is most of the lesson.

## If there is time left

The stretch notebook has six questions about the listening data that get harder as you go.
Use as many as the time allows; you don't need to finish it. Each one adds one idea:

| # | Question | What it adds |
|---|---|---|
| 1 | Who did I not play in 2025? | A `WHERE` that silently turns a left join into an inner one, the fix in the `ON`, and `IS NULL` to find rows with no match |
| 2 | Artists from the same country | A self-join, and why `>` gives 22 pairs where `<>` gives 44 |
| 3 | 2024 against 2025 | Three chained CTEs, starting from the right table so the artists who dropped to zero stay in |
| 4 | Spot the bug | A fan-out where both counts multiply each other, and why `COUNT(DISTINCT key)` is a safe repair when `SUM(DISTINCT value)` was not |
| 5 | The top artist in every genre | A first window function: `RANK() OVER (PARTITION BY ...)` |
| 6 | When was I halfway? | A running total with `SUM() OVER`, and why you round at the end |

Number 4 is the one to talk through rather than just check. It is fan-out again, from the
other side: the difference between a key and a value is what decides whether `DISTINCT` can
help, and that is the understanding the session is really after.

Numbers 5 and 6 introduce window functions in a few lines each. They are not needed for the
rest of the course. If he gets that far, the point to land is why the rank needs its own CTE
before it can be filtered, which ties straight back to the execution order from session 6.

## Watch out for

- **Ambiguous column names.** The error is clear once seen once, which is why it is on a
  slide and demonstrated in the notebook.
- **`COUNT(*)` after a `LEFT JOIN`.** Reports 1 for a row with no matches. This is how "never
  played" silently becomes "played once".
- **Fan-out.** The whole middle of the session. The habit to install: after any join, compare
  the row count with what it was before.
- **Reaching for `DISTINCT`.** Slide 17 exists for this.
- **Assuming the keys match.** Not a problem in this dataset, and a huge one in real work.
  Worth a sentence: if a join returns nothing, compare a few key values from each side by eye.
- **Ending up with a query nobody can read.** Push CTEs hard. Beginners can adopt them
  immediately and then never write a deeply nested subquery at all.

## Definition of done

They can write a join with an aggregate, choose the join type deliberately, and explain
fan-out in their own words. The explanation matters more than the SQL.
