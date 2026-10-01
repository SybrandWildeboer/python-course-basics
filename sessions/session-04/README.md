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

## Notebooks

| Notebook | What it is |
|---|---|
| `notebooks/01-lists-and-dicts.ipynb` | Lists, dictionaries, and the "a list of dicts is a table" idea |
| `notebooks/02-files-and-csv.ipynb` | Paths, `DictReader`, text-versus-number, the counting pattern, writing a CSV |
| `notebooks/03-explore-plays-exercise.ipynb` | The live exercise |
| `notebooks/03-explore-plays-solved.ipynb` | Worked version, with the expected output written out |
| `notebooks/04-questions-homework.ipynb` | Homework 2 |
| `notebooks/04-questions-solved.ipynb` | Worked version, showing the 2025 tie and the total-versus-average trap |
| `notebooks/05-stretch-exercise.ipynb` | Optional stretch exercises, for when the live exercise finishes early |
| `notebooks/05-stretch-solved.ipynb` | Worked versions, with the reasoning written out |

Each data notebook starts with a short cell that walks up to the repository root, so it works
whichever folder VS Code opened it from.

## If there is time left

The stretch notebook has six questions that get harder as you go. Use as many as the time
allows; you don't need to finish it. None of them repeat the live exercise or the homework,
and each one adds one idea:

| # | Function | What it adds |
|---|---|---|
| 1 | `plays_per_month` | Slicing text like a list (`played_at[:7]`), and why `YYYY-MM` sorts correctly as text |
| 2 | `tracks_by_artist` | A dictionary of lists, and 168 track names versus 229 actual tracks |
| 3 | `index_by`, `plays_by_decade` | A second file, a lookup dictionary, and blank `formed_year` values to decide about |
| 4 | `artist_stats`, `skip_rates` | A dictionary of dictionaries, and a minimum number of plays before a rate counts |
| 5 | `genre_by_year` | Building your own rows and writing them out: a pivot table by hand |
| 6 | read it back | Numbers come back from a CSV as text, and an `assert` that the file matches the log |

Numbers 3 and 4 are the ones to talk through rather than just check. In 3, what to do with
the 53 plays from artists with no `formed_year` (skip, guess, or label them `"unknown"`)
matters more than the code, and it sets up `IS NULL` in session 6. In 4, the most-skipped
artist is Circuit Sparrow at 28.6%, which is 2 skips out of 7 plays. Ask whether they believe
it before showing the `min_plays=30` version.

Stretch 3 is also a first, by-hand look at a `JOIN`: index one table by name, then look up
each play in it. Say so; it makes session 7 a translation.

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
