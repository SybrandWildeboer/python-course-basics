# Session 8: The end project, pair programming

**Goal:** his own question, answered by `project/pipeline.py` from one command, in a fresh
terminal, inside its own virtual environment, with `project/output/` regenerated from
nothing, committed and pushed. Built by him at the keyboard, with you navigating.

**Slides:** [`slides/session-08.html`](../../slides/session-08.html) (16 slides)

This session replaces three: putting it together, project scoping and the presentation.
The scoping happens before it, as pre-work. The structure (scripts versus notebooks,
`main()` and `__name__`, paths from `__file__`, virtual environments, the project layout)
and the review material (`try` / `except` and where to catch, an `assert` turned into a
test, reading a diff) are taught **when they come up in his code**, not as blocks. The deck
is eight slides that frame the session and a "teach it when it comes up" set (slides 9–15)
to jump to. Everything else from the old sessions is optional material for after the course.

---

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00–0:15 | His worksheet: cut the scope, run the one-number test on his laptop | Slides 2–3. This is the homework review |
| 0:15–0:30 | `project/` and a virtual environment on his machine; the template runs | Slide 4 (slide 12 if it fights back) |
| 0:30–1:00 | Pair programming 1: `INPUT`, `QUESTION`, `load`, `clean`, from his notebook | Slides 5–6, teach-it slides as needed |
| 1:00–1:10 | Break | At a moment when the pipeline runs |
| 1:10–1:40 | Pair programming 2: `analyse`, the chart, `save`, `check`, `main()` | Slide 6, teach-it slides as needed |
| 1:40–1:55 | **Fresh terminal, `output/` deleted, his diff reviewed, commit, push.** Never cut | Slide 7, slide 15 |
| 1:55–2:00 | Where next, two first steps with dates, homework | Slides 8 and 16 |

Swap driver and navigator about every twenty minutes: around 0:50, 1:20 and 1:40. He drives
most of the time; your turns are short.

If it runs slow, cut features (the chart can be the should item in the homework), never the
last fifteen minutes. A pipeline that runs from a fresh terminal and is pushed is the one
thing he cannot easily get to alone.

## The blocks that matter

**The first fifteen minutes (slide 3).** Read his worksheet with him. Count the projects in
his idea out loud ("three projects wearing a coat"), keep the one that answers his session 1
task, and move every "and also" to *could* or *won't* while he watches. Then he runs his
one-number test on his laptop and checks it a second way. Ask what decision the first number
found; in the worked example, total listening fell, so "shrank most" depends on minutes or
share.

**The virtual environment on his machine (slide 4).** He types it, in `project/`, on his
laptop. The Windows execution-policy error is the usual trap, and meeting it here costs two
minutes; meeting it alone costs an evening. The template must run before any of his code
goes in: 2,223 rows loaded, 2,183 cleaned, Electronic 2,753.2 of 8,608.0 minutes.

**Pair programming (slides 5–6).** His explore notebook becomes stages in
`project/pipeline.py`, one at a time, a run after each, a commit when it runs. Work down the
`MAKE IT YOURS` markers. The stages return and print nothing; only `main()` prints, one line
per stage, so a run that stops or loses rows says where.

**The finish line (slide 7).** A new terminal, the venv activated, `project/output/` deleted,
`python pipeline.py`, `git status`, `git diff` read together with slide 15's questions, then
commit and push. He runs every line.

## Instructor checklist

### What must be true by the end

- [ ] `python pipeline.py` in `project/` (or `python project/pipeline.py` from the root) runs
      start to finish in a **fresh terminal**
- [ ] It runs **inside `project/.venv`**, built from `requirements.txt`, with `(.venv)` in
      the prompt
- [ ] `project/output/` was **deleted and regenerated** by that run
- [ ] It writes a rough **must answer** for his question, not the music question
- [ ] `git status` shows no data file, no `output/`, no `.venv/`
- [ ] **Committed and pushed**, after reading the diff together
- [ ] Step 2 from `worksheets/where-next.md` has a direction and a date

### Pairing with a fast learner

- **He drives most of the time.** Your driving turns are short demonstrations, two or three
  minutes, after which the keyboard goes back.
- **Never take his keyboard.** Say the line number and the idea ("line 40 still prints"),
  not the keys. If you need to show something, show it on your own screen.
- **Ask before you tell.** "What does `clean` return?" finds the bug and leaves it his.
  Wait longer than is comfortable before giving the answer.
- **Navigate the scope, not the syntax.** He will race ahead; your job is "is this the must?",
  "did we run it?", "commit now?". Every new idea goes on the *could* list.
- **Let small mistakes run.** A `NameError` he reads himself teaches more than one you
  prevented. Step in when he has been stuck for about five minutes, or when he is about to
  commit private data.
- **Use the teach-it slides only when the moment comes.** Two minutes, then back to his code.
  If a moment never comes (no import, no missing file), skip the slide: the optional
  notebooks cover it.

### If the data or the scope fails in the first fifteen minutes

- **No data on his laptop, or it will not load:** do not spend the session on it. Point
  `INPUT` at the music data (`data/messy/plays_messy.csv`, the template's default), scope a
  stand-in question with the same shape as his (the worked example in
  `prework/worked-example.md` is ready), build the pipeline on that, and swap his file in
  as homework. Write in the README which data it is.
- **The Spotify export has not arrived:** the same. Build on the music data; notebook
  `08-spotify-exercise.ipynb` rehearses loading the export, and `load` is the only stage that
  changes when it arrives.
- **A file that loads as one column:** Dutch Excel. `pd.read_csv(path, sep=";",
  decimal=",")`. An `.xlsx`: save it as CSV for today.
- **The one-number test does not pass** (he cannot say what the number would be, or it needs
  data he does not have): the question is too big or too vague. Pick the smallest piece of it
  that has a number, write the rest on the *won't* list, and go. Five minutes, not fifteen.
- **The scope is still three projects:** choose for him if he cannot, and say so: "today we
  build this one; the others are on the list".
- **pip cannot install** (no internet, a blocked work laptop, Python 3.13 or newer): run the
  session on the Python he has, with pandas and matplotlib already installed, and make the
  venv part of the homework, by message.

## What they use

| File | What it is |
|---|---|
| `prework/scoping-worksheet.md` | The pre-work, assigned in session 7's homework: the question, must / should / could / won't, the data, the one-number test, private data, the Spotify route |
| `prework/worked-example.md` | The worksheet filled in on the music data, from an unscoped first draft |
| `project/` (repo root) | The template he builds in: `pipeline.py`, `README.md`, `requirements.txt`, `notebooks/explore.ipynb`, `data/` |
| `demos/genre_pipeline.py` | The finished pipeline on the music data: load, clean, analyse, save, check, `main()` |
| `demos/where_am_i.py` | The working folder versus the script's folder (slide 10) |
| `demos/name_main.py`, `demos/import_name_main.py` | What `__name__` is, run and imported (slide 11) |
| `demos/one_number_test.py` | Notebook 01 as a script: first look, the table, the checks, a rough chart |
| `demos/try_except.py` | The four errors you expect, `try` / `except`, never bare, where to catch |
| `demos/statistics_functions.py`, `demos/test_statistics_functions.py` | The session 3 functions as a module, and their asserts as nine tests |
| `exercises/robust.py`, `exercises/test_robust.py` | Optional exercise. One test is written and fails until `safe_highest` works |
| `solutions/robust_solved.py`, `solutions/test_robust_solved.py` | Worked answers, twelve tests |
| `worksheets/review-checklist.md` | The code review checklist, cheapest check first (slide 15) |
| `worksheets/practice-review.diff`, `practice-review-answers.md` | A practice commit with five planted problems, and the answers |
| `worksheets/where-next.md` | The map, with resources and "first two hours" tasks, and the two first steps |
| `homework/README.md` | Finish the must answer; optional work after the course |
| `homework/finish_the_must.py`, `homework/solutions/finish_the_must.py` | Script versions of notebook 06 |
| `homework/test_pipeline_starter.py`, `homework/solutions/test_pipeline_example.py` | A starter for `project/test_pipeline.py`, and nine tests for the template |

`load_messy` and `clean_plays` in `demos/genre_pipeline.py` are the session 6 functions from
`sessions/session-06/solutions/cleaning.py`, copied in so the script stands on its own. The
template's `clean` is shorter; the session 6 version is the one to borrow from when his data
needs more.

Run tests one folder at a time from the repository root, for example
`python -m pytest sessions/session-08/solutions`. The exercises folder has one failing test by
design until the exercise is done.

## Notebooks

| Notebook | What it is |
|---|---|
| `notebooks/01-one-number-test.ipynb` | Pre-work walkthrough: the five-minute first look, the one-number test on the worked example, the check that it adds up, the minutes-versus-share decision, and the same code shaped as load / clean / analyse / save |
| `notebooks/02-notebook-to-script.ipynb` | Optional: the whole notebook-to-pipeline story on the music data, one checked function at a time, `__name__` by importing, three folders, and the total against `music.db` |
| `notebooks/03-try-except.ipynb` | Optional: the empty list on real data, `try` / `except`, the bare-except typo, `if` versus `try`, and catching `FileNotFoundError` in the outer layer |
| `notebooks/04-pytest.ipynb` | Optional: tests as functions, a ten-line test runner, the `best = 0` bug caught twice, real `pytest`, and tests in `project/` |
| `notebooks/05-robust-exercise.ipynb` | Optional exercise: `safe_highest`, `to_minutes`, `summary_line`, then tests |
| `notebooks/05-robust-solved.ipynb` | Worked version |
| `notebooks/06-finish-the-must-homework.ipynb` | Homework: logged cleaning, `find_problems`, the must answer checked two ways, into the pipeline |
| `notebooks/06-finish-the-must-solved.ipynb` | Worked version on the worked example, including `find_problems` failing properly on the messy file |
| `notebooks/07-stretch-exercise.ipynb` | Optional stretch exercises, for when his pipeline runs early |
| `notebooks/07-stretch-solved.ipynb` | Worked versions, with the reasoning written out |
| `notebooks/08-spotify-exercise.ipynb` | Optional: the Spotify route, on a practice export it writes itself |
| `notebooks/08-spotify-solved.ipynb` | Worked version |

Virtual environments are terminal work and are not in a notebook: slide 4 and
`project/README.md` have the steps. pytest is not part of Python; the notebooks check for it
and print the install line instead of failing.

## The numbers worth knowing

All from running the code, and pinned with `assert` in the notebooks.

- The template out of the box: 2,223 messy rows, 2,183 after cleaning, eight genres;
  Electronic 2,753.2 of 8,608.0 minutes, 32.0%. The database says 8,980.4 in total; the gap of
  372.4 minutes is exactly the 94 plays with blank minutes.
- The worked example: Jazz grew most (+54.0 minutes), Electronic shrank most (−106.1); by
  share, Folk shrank most (−1.5 points). Total listening fell from 4,596.6 to 4,383.8.
- The demo tests: nine pass in `demos`, twelve in `solutions`, nine in
  `homework/solutions`.

## Before the session

- [ ] Ask him to send the filled-in `prework/scoping-worksheet.md` the day before, and read
      it. If a scope-check box is empty, sort it out by message now
- [ ] Check his Python version: `python --version` (Windows) or `python3 --version` (Mac).
      `project/requirements.txt` pins `pandas==2.3.1` and `matplotlib==3.9.0`, which need
      Python 3.12 or lower (3.10 to 3.12): matplotlib 3.9.0 has no ready-made installer for
      3.13 or newer, so pip would try to build it from source and fail. If he has 3.13+,
      install 3.12 before the session
- [ ] Check he can `pip install` from PyPI on his network; some work laptops block it
- [ ] Ask whether the Spotify export has arrived, if that is his route
- [ ] Run `python project/pipeline.py` from a clean checkout, and have
      `prework/worked-example.md` open as the fallback
- [ ] Have his session 1 file ready, for the close

## If there is time left

He finishes things fast, so his pipeline may run with time to spare. First move his should
item (usually the chart) into the pipeline; it is the best use of the time. After that, the
stretch notebook: six exercises that get harder, each adding one thing a real pipeline
needs. Use as many as the time allows.

| # | Function | What it adds |
|---|---|---|
| 1 | `load_from_db` | Swapping one stage: the database through a join, no cleaning, the rest unchanged |
| 2 | `cleaning_report` | A run that says what cleaning did: 40 duplicates, 94 minutes missing, 69 devices unknown |
| 3 | `check_columns` | `raise ValueError` with a message, so the wrong file fails early and clearly |
| 4 | `parse_year`, `plays_in_year` | `sys.argv`, and why a function should take the list rather than read it |
| 5 | `fill_minutes` | A cleaning decision as a parameter: keep, drop or median, side by side with the truth |
| 6 | `log_run` | Appending with `"a"`, and a history of every run |

Number 5 is the one to talk through rather than just check. The median version gets the
total closest to the truth (8,993.4 against 8,980.4), and that is exactly why it deserves
suspicion: 94 of its numbers are invented. Number 1 shows the point of the whole structure in
one move: the source changes, and the analysis never knows.

## Watch out for

- **Building features before it runs end to end.** A running rough pipeline at 1:00 beats a
  perfect `clean` at 1:40. Get every stage in, crude, then improve.
- **`python3` versus `python`.** On Windows it is `python` (`python3` may open the Microsoft
  Store). On a Mac it is `python3` until the venv is active.
- **Forgetting to activate.** `No module named 'pandas'` in a new terminal means the venv is
  not active, not that pandas is missing. Look for `(.venv)`.
- **VS Code using a different Python.** The notebook kernel and the terminal can each pick a
  different interpreter; pick the `.venv` one for `project/`.
- **Printing inside the stages.** The session 3 habit slips under pressure. Ask for one more
  output (the CSV, or a test) and let the requirement force the return.
- **A bare `except:` to make an error go away.** Slide 13. Catch the one error by name, in
  `main()`; never wrap `clean()` or `analyse()`.
- **`check` and `save_chart` still expecting the music columns.** They fail on his table.
  Rename the columns they use; do not delete the check.
- **`save_csv` dropping the labels.** It writes with `index=False`, so an `analyse` that ends
  with the labels in the index loses them silently. `.reset_index()` at the end.
- **`git add .` with data outside `project/data/`.** Look at `git status` before every
  commit. `git check-ignore -v project/data/<file>` shows the rule that hides it.
- **`__file__` in a notebook.** `NameError`. Notebooks walk up from the working folder
  instead; `explore.ipynb` already does.

## Definition of done

His pipeline answers his must question roughly, from one command in a fresh terminal, inside
`project/.venv`, with `project/output/` regenerated; it is committed and pushed with no
private data; and he can say why the paths use `__file__`, what the two lines at the bottom
are for, and why `.venv/` is not in git. Step 2 is written down with a date.

The homework finishes the must answer properly: logged cleaning, checks, the README, and a
run from a fresh clone.
