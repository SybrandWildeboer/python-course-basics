# Session 4: Lists, dictionaries and files

**Goal:** hold a table's worth of data in memory, and get data in and out of files. And meet
the dataset that carries the rest of the course.

**Slides:** [`slides/session-04.html`](../../slides/session-04.html) (23 slides)

---

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00–0:15 | Homework review: the four functions and the menu | Slide 2 |
| 0:15–0:35 | Lists: indexing, slicing, changing, looping | Slides 4–7 |
| 0:35–0:50 | Dictionaries, and **a list of dicts is a table** | Slides 9–12 |
| 0:50–1:00 | Break | |
| 1:00–1:30 | Files, paths, `csv.DictReader`, the counting pattern | Slides 14–19 |
| 1:30–1:35 | Meet the listening log | Slide 20 |
| 1:35–1:55 | Three questions about the data, them driving | Slide 21 |
| 1:55–2:00 | Homework briefing, and a reminder about GitHub | Slides 22–23 |

## The two slides that matter

**Slide 12, "a list of dictionaries is a table".** This is the hinge of the whole course.
`csv.DictReader` hands them this shape, a SQL query returns this shape, and a pandas
DataFrame is this shape with a faster engine underneath. Say that out loud.

**Slide 19, the counting pattern.** It is the accumulate pattern from session 2 with a
dictionary instead of one running total. In session 6 the same question is `GROUP BY genre`
and in session 8 it is `groupby("genre")`. Same idea, three notations. Making that link now
means SQL and pandas arrive as translations rather than as new subjects.

## What they type

| File | What it is |
|---|---|
| `demos/lists_and_dicts.py` | Walkthrough part one, with the errors commented out |
| `demos/files_and_csv.py` | Walkthrough part two: paths, DictReader, counting, writing |
| `exercises/explore_plays.py` | The live exercise starter |
| `solutions/explore_plays.py` | Worked version, with the expected output in a comment |
| `homework/filter_plays.py` | Homework 1 starter |
| `homework/questions.py` | Homework 2 starter |
| `homework/solutions/` | Both answers, including a note on the genuine tie in 2025 |

## Before the session

- [ ] Check the dataset is generated: `python3 data/scripts/build_dataset.py`
- [ ] Open `data/clean/plays.csv` in VS Code so you can show the raw text, commas and all
- [ ] Remind them to create a GitHub account before session 5

## If they want to use their own dataset

Session 20's slide notes cover this. The requirements are: a few thousand rows at most, at
least one date column, one numeric column, a few categorical columns, and something that can
become a second related table for session 7. If theirs qualifies, let them use it; caring
about the data is worth more than the convenience of a prepared file. You will have to
translate the exercises, so decide before session 6 when the SQLite database appears.

## Watch out for

- **`FileNotFoundError` from a relative path.** First move, every time: print
  `os.getcwd()`. The file is fine; Python is looking elsewhere. Agree the habit of running
  everything from the repo root.
- **Forgetting `list()` around `DictReader`.** You get a reader that can only be walked
  once, and the second loop silently does nothing. Genuinely worth demonstrating.
- **Everything arriving as text.** `total += row["minutes_played"]` fails with a `TypeError`.
  This is the same lesson as `input()` in session 1.
- **`KeyError` from a mistyped column name.** Show them `rows[0].keys()` as the fix.
- **`x = x.sort()`** throwing the list away. It connects straight back to functions that
  return `None`.
- **Missing `encoding="utf-8"`.** The dataset contains `Salon Mécanique`, so this bites.
- **Writing to `output/` before it exists.** `os.makedirs("output", exist_ok=True)`.

## Definition of done

They can load the CSV, count rows into a dictionary by any column, total a numeric column,
and write a filtered file back out.
