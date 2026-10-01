# Session 12: Presentation, review and what is next

**Goal:** they present their project and defend its numbers, review code by reading diffs,
handle the errors they can predict without hiding the ones they cannot, turn their `assert`
lines into tests, and leave with two first steps that have dates on them.

**Slides:** [`slides/session-12.html`](../../slides/session-12.html) (22 slides)

The first hour belongs to them. Protect it. If you run short of time, shorten the map, not
the presentation or the review.

---

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00–0:05 | The plan, and a check that the pipeline runs | Slide 2 |
| 0:05–0:30 | **They present**, ten minutes, then the four questions | Slides 4–5 |
| 0:30–0:55 | Code review: the practice diff, their own history, "what if the data changes?", then two or three fixes live | Slides 7–10 |
| 0:55–1:05 | Break | |
| 1:05–1:25 | `try` / `except`, then live exercise part 1 | Slides 12–15 |
| 1:25–1:45 | `pytest`, then live exercise part 2 | Slides 16–18 |
| 1:45–2:00 | The map, honest advice, two first steps written down, the close | Slides 20–22 |

## The blocks that matter

**The presentation (slides 4–5).** The structure is question, data, one chart, what
surprised them, what they would do next. Do not interrupt; write questions down. Afterwards,
say the one thing to keep before anything else, then ask the four questions on slide 5.
Question 3, "what is the smallest change to the data that would change your conclusion?",
is the hardest and the most useful. If the honest answer is "twelve plays in one month",
help them say the smaller, truer version of their finding.

**The practice diff (slide 7).** A realistic commit to a pipeline with five problems
planted: an absolute path, a bare `except` that returns an empty DataFrame, fan-out from a
merge, a `print` inside `analyse`, and two changes in one commit. Every number on the slide
was produced by running both versions: 2,183 rows become 3,391, total minutes go from
8,980.4 to 13,732.9, Rock climbs from last of eight to third, and Folk's 9 awards become
1,095. On a machine without Sam's file the "fixed" loader crashes anyway, one function later,
as `KeyError: 'artist_name'`. Let them find problems with the checklist before you say
anything. If they spot the fan-out unaided, session 7 worked.

**What if the data changes slightly? (slide 10).** Then their own code, with one question:
an extra or renamed column, a new category, a missing month, twice the rows. It finds more
real fragility than any other question: hardcoded column lists, assumed date ranges, a
check that expects exactly 24 months, a chart or a `groupby` that silently drops a category
it has not seen. Then **pick two or three things and fix them live**: one at a time, a commit
each, and a rerun with `project/output/` deleted first. A list of improvements they take
home is a list they will not do.

**Where to catch (slide 15).** The idea that holds both halves of the session together: a
missing file must not become empty data. It is the practice diff's bug, and it extends the
session 3 rule: functions that calculate return and let errors travel; the outer layer
prints and decides what to do about errors.

**The second failure (slide 17).** With `highest` starting at `best = 0`, two tests fail.
The negatives test is the one they expect. The empty-list test failing too, because
`highest([])` now quietly answers `0` instead of crashing, is the case for testing the
awkward cases on purpose. Let them say why before you do.

**The map (slide 20).** Six directions, each with a first task on their own project. Be
honest about machine learning if it comes up, because it will: it is mostly data work with a
model at the end, the pandas and SQL from this course are most of the job, and it is usually
the wrong next step. Point them at what they visibly enjoyed over the twelve weeks, not at
what sounds impressive.

**The close (slide 22).** Show their session 1 file, if you still have it, next to the
project: twelve weeks, a few hundred lines of their own code, a repo of real commits, and a
project they chose, scoped, built and presented. Then tell them the questions channel stays
open. It costs little, and the month after a course is when it matters most. End on time.

## What they use

| File | What it is |
|---|---|
| `worksheets/presentation.md` | The ten-minute structure, a prep checklist, the four questions |
| `worksheets/review-checklist.md` | The code review checklist, cheapest check first, and how to write comments |
| `worksheets/practice-review.diff` | The practice commit for slide 7 |
| `worksheets/practice-review-answers.md` | The five problems and two good things, with the fix verified |
| `worksheets/where-next.md` | The map, with resources, "first two hours" tasks, and the two first steps to fill in |
| `demos/try_except.py` | Walkthrough part one: the four errors, `try` / `except`, never bare, where to catch |
| `demos/statistics_functions.py` | The session 3 functions as an importable module, no prints, no asserts |
| `demos/test_statistics_functions.py` | Walkthrough part two: the session 3 asserts as nine tests |
| `exercises/robust.py`, `exercises/test_robust.py` | The live exercise starters. One test is written and fails until `safe_highest` works |
| `solutions/robust_solved.py`, `solutions/test_robust_solved.py` | Worked answers, twelve tests |
| `exercises/stretch.py`, `exercises/test_stretch.py` | Stretch starters |
| `solutions/stretch_solved.py`, `solutions/test_stretch_solved.py` | Stretch answers, twenty-three tests |
| `homework/README.md` | The week after the course: project in shape, then step 2 |
| `homework/test_pipeline_starter.py` | A starter for `project/test_pipeline.py` |
| `homework/solutions/test_pipeline_example.py` | Nine tests for `project/pipeline.py` as it comes out of the box |

Run tests one folder at a time from the repository root, for example
`python -m pytest sessions/session-12/solutions`. The exercise folder has one failing test by
design until the exercise is done.

## Notebooks

| Notebook | What it is |
|---|---|
| `notebooks/01-try-except.ipynb` | The empty list on real data, `try` / `except`, the bare-except typo, `if` versus `try`, `ValueError` on the messy minutes (2,033 numbers, 190 not), and catching `FileNotFoundError` in the outer layer |
| `notebooks/02-pytest.ipynb` | Tests as functions, a ten-line test runner, the `best = 0` bug caught twice, then real `pytest` on the demo files, and how to set it up in `project/` |
| `notebooks/03-robust-exercise.ipynb` | The live exercise: `safe_highest`, `to_minutes`, `summary_line`, then their tests |
| `notebooks/03-robust-solved.ipynb` | Worked version: `to_minutes` recovers 2,129 values and leaves the 94 empty ones missing |
| `notebooks/04-stretch-exercise.ipynb` | Optional stretch exercises |
| `notebooks/04-stretch-solved.ipynb` | Worked versions, with the reasoning written out |

**pytest is not part of Python.** Check with `python -m pytest --version`. If it is missing,
the learner installs it into the project's virtual environment with
`python -m pip install pytest` and adds it to `project/requirements.txt`. The notebooks check
for it before running it, and print that install line instead of failing, so every notebook
still runs top to bottom without it. With it, they show the real pytest output.

Notebook 02 writes a broken copy of the demo module to `output/session-12/broken/`, runs
pytest on it, and deletes it again, so a later `python -m pytest` never finds two modules with
the same name.

## If there is time left

There probably will not be, in this session. The stretch notebook is written to work on its
own in the week after. Six exercises, each adding one idea:

| # | Topic | What it adds |
|---|---|---|
| 1 | `else` and `finally` | Predict-then-run, and why `with` is why they rarely need `finally` |
| 2 | Raising your own error | `raise ValueError(...)` with a message that names the caller's mistake, and `pytest.raises(..., match=)` |
| 3 | Floats that are nearly equal | `celsius_to_fahrenheit(36.6)` is `97.88000000000001`; `math.isclose` and `pytest.approx` |
| 4 | One test, many cases | `@pytest.mark.parametrize`, and the decimal comma `"4,2"` that `float()` refuses |
| 5 | A test that needs a file | The `tmp_path` fixture, and a header-only file giving an empty list |
| 6 | pandas does not raise | The mean of an empty selection is `NaN`, not an error; `skip_rate` on a four-row DataFrame, and a fixture of their own |

Number 6 is the one to talk through. It closes the loop on session 9's divide-by-zero
promise: plain Python crashes, pandas quietly hands back `NaN`, and a test is the only thing
that notices. The car comes out at 10.6%, the same 19 out of 179 that came out as `0` under
integer division in session 6.

## Watch out for

- **A stale chart.** Have them run the pipeline before presenting. Presenting last week's PNG
  and then finding the numbers changed derails the ten minutes.
- **One giant commit.** Then there is no history to review. Review the current
  `pipeline.py` top to bottom with the checklist instead, and say once that small commits are
  what make review possible.
- **Reaching for a bare `except:` to make an error go away.** The single most likely habit to
  form after today. The typo demo on slide 14 is there to inoculate against it.
- **Wrapping everything in `try`.** A `try` around `clean()` or `analyse()` hides bugs. Only
  the load in `main()`, and text that may not be a number, need one in most projects.
- **`ModuleNotFoundError` when running pytest.** Either pytest is not installed in the active
  environment, or the test file is not next to the module it imports. `python -m pytest`
  rather than `pytest` avoids the first; the folder layout fixes the second.
- **Running `python -m pytest` with no folder from the repository root.** It collects every
  test file in the course, including the deliberately failing exercise starter. Name the
  folder.
- **A file called `statistics.py`.** It would hide Python's own `statistics` module. It is
  why the module here is called `statistics_functions.py`.

## Definition of done

They presented a question, its data, one chart and an honest limitation; they can read a
diff and say which problem in it matters most; they can catch one named error in the right
place and explain why a bare `except` is a lie; they have run `python -m pytest` on tests they
wrote; and step 2 is written down with a date.
