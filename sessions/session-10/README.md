# Session 10: Putting it together

**Goal:** turn notebook work into a script that runs from one command, from any folder, in
its own environment. And leave with the `project/` scaffold that sessions 11 and 12 build on.

**Slides:** [`slides/session-10.html`](../../slides/session-10.html) (22 slides)

This is the session where nothing new about data gets taught. Everything is structure:
where code lives, how it is run, and what it needs installed. That can feel like a step
down after two sessions of pandas, so sell it early: the session 1 task from his own week is
something he could now automate, and today is the difference between "I did it once in a
notebook" and "I run it every Monday".

---

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00–0:10 | Homework review: the cleaning functions, and the chart | Slide 2 |
| 0:10–0:20 | Why a script, and the pipeline shape | Slides 4–5 |
| 0:20–0:45 | Stages as functions, the session 3 shape, `main()`, `__name__` | Slides 6–9 |
| 0:45–0:55 | Paths from `__file__`, running it, the read-back check | Slides 10–11 |
| 0:55–1:05 | Break | |
| 1:05–1:35 | Live exercise: the device pipeline, them driving | Slide 20 |
| 1:35–1:50 | Virtual environments, done for real on `project/` | Slides 13–15 |
| 1:50–1:55 | The project layout, notebook versus pipeline | Slides 17–18 |
| 1:55–2:00 | Homework, and the Spotify request | Slides 21–22 |

Slide 19, the mistakes table, is reference: point at it when one of them happens rather than
teaching it as a block.

If the morning runs fast, which with him it may, the stretch notebook is the place to go.
If it runs slow, shorten the exercise rather than the virtual environment block: the venv has
to be working on his machine before session 11, and it is much easier to fix together than
over chat.

## The three slides that carry the session

**Slide 7, the session 3 shape.** Put session 3's `total` next to `summarise_by_genre`. Same
shape: takes data, returns an answer, prints nothing. Session 3 promised "these exact shapes
get called by a pipeline that writes a CSV instead of printing", and this is that moment.
Say it, because it turns a rule he was asked to take on trust into something that paid off.

**Slide 10, paths from `__file__`.** Session 4 said `Path(__file__)` would be used properly
in session 10. Do it live: run the exercise starter from the repo root (works), `cd
sessions/session-10`, run it again (`FileNotFoundError`). Then run the demo pipeline from the
same folder (works). The difference sinks in when he sees it break, not when he hears why.

**Slide 14, the venv on his machine.** Actually do it, in `project/`, on his laptop, during
the session. Activation on Windows is where it goes wrong (execution policy), and that error
is miserable to meet alone at home.

## What they use

| File | What it is |
|---|---|
| `demos/genre_pipeline.py` | The walkthrough pipeline: load, clean, analyse, save, check, `main()` |
| `demos/where_am_i.py` | The working folder versus the script's folder, and a short tour of `Path` |
| `demos/name_main.py` | What `__name__` is, run directly |
| `demos/import_name_main.py` | The same file imported: the top-level print runs, `main()` does not |
| `exercises/device_pipeline.py` | The live exercise starter: working notebook-shaped code to restructure |
| `solutions/device_pipeline.py` | Worked version, with the expected output and the `unknown` discussion |
| `homework/README.md` | The three tasks |
| `homework/pipeline.py` | Homework 1 starter: the genre pipeline with `TODO` markers |
| `homework/solutions/pipeline.py` | Worked version, with the monthly question added |
| `project/` (repo root) | The scaffold for sessions 11 and 12, built from the genre pipeline |

`load_messy` and `clean_plays` in every session 10 script are the session 9 functions from
`sessions/session-09/solutions/cleaning.py`, copied in unchanged so each script stands on its
own. If he brings his own session 9 versions, use those; the exercise only needs them to
return the cleaned plays.

Every script runs from any folder. They write to `output/` at the repository root, except
`project/pipeline.py`, which writes to `project/output/`. Both are gitignored.

## Notebooks

| Notebook | What it is |
|---|---|
| `notebooks/01-notebook-to-script.ipynb` | The walkthrough. Builds the genre pipeline one checked function at a time, imports it to show `__name__`, runs it from three folders, and checks the total against `music.db` |
| `notebooks/02-device-pipeline-exercise.ipynb` | The live exercise: the same restructuring, function by function, with the checks ready |
| `notebooks/02-device-pipeline-solved.ipynb` | Worked version, including why the top row is not a device, and the tablet that goes from last to first |
| `notebooks/03-monthly-homework.ipynb` | Homework 1, importing today's pipeline instead of copying it |
| `notebooks/03-monthly-solved.ipynb` | Worked version: the summer dip, line versus bar, and why the axis starts at zero |
| `notebooks/04-stretch-exercise.ipynb` | Optional stretch exercises, for when the live exercise finishes early |
| `notebooks/04-stretch-solved.ipynb` | Worked versions, with the reasoning written out |

Virtual environments are terminal work and are not in a notebook. The slides and
`project/README.md` have the steps for Windows and macOS.

## The numbers worth knowing

All from running the code, and pinned with `assert` in the solved notebooks.

- The messy file has 2,223 rows; cleaning leaves 2,183, which is the clean file's count.
  Genre, country and every date then match `data/clean/plays.csv` exactly.
- What cleaning cannot recover: 69 blank devices (labelled `unknown`) and 94 blank minutes
  (left missing).
- Electronic: 2,753.2 minutes from the messy file, 32.0% of the 8,608.0 total. The database
  says 2,874.5 and 8,980.4. The gap of 372.4 minutes is exactly the 94 blank plays, which
  notebook 01 proves against `music.db`.
- Device skip rates: `unknown` 15.9% (11 of 69) comes top, then speaker 14.1%, tablet 13.9%,
  laptop 11.4%, phone 11.1%, car 10.4%.
- Busiest month October 2024 (531.2 minutes), quietest July 2025 (219.6).

## Before the session

- [ ] Run `python sessions/session-10/demos/genre_pipeline.py` from the repo root and from
      `sessions/session-10`, so you have seen both work
- [ ] Check what Python he has on his laptop: `python --version` on Windows, `python3
      --version` on a Mac. It needs to be 3.10 to 3.12: `project/requirements.txt` pins
      `matplotlib==3.9.0`, which has no ready-made installer for 3.13 or newer, so pip would
      try to build it from source and fail (`slides/install.html` recommends 3.12)
- [ ] Check he can install from PyPI on his network: `pip install` needs internet, and some
      work laptops block it. Better to find out before the venv block than during it
- [ ] Look at the `project/` folder, so the tree on slide 17 is familiar

## If there is time left

The stretch notebook has six exercises that get harder as you go. Use as many as the time
allows; you don't need to finish it. Each one adds one thing a real pipeline needs:

| # | Function | What it adds |
|---|---|---|
| 1 | `load_from_db` | Swapping one stage: the database through a join, no cleaning, and the rest unchanged |
| 2 | `cleaning_report` | A run that says what cleaning did, worked out rather than typed in |
| 3 | `check_columns` | `raise ValueError` with a message, so the wrong file fails early and clearly |
| 4 | `parse_year`, `plays_in_year` | `sys.argv`, and why a function should take the list rather than read it |
| 5 | `fill_minutes` | A cleaning decision as a parameter: keep, drop or median, side by side with the truth |
| 6 | `log_run` | Appending with `"a"`, and a history of every run |

Number 5 is the one to talk through rather than just check. The median version gets the
overall total closest to the truth (8,993.4 against 8,980.4), and that is exactly why it is
tempting and why it deserves suspicion: 94 of its numbers are invented. It is the session 9
lesson, now living in a pipeline as a choice with a default.

Number 1 is worth doing even if nothing else is, because it shows the point of the whole
structure in one move: the source changes, and `summarise_by_genre` never knows.

Numbers 3 and 6 use `try`/`except` in the solved notebook only to show an error without
stopping the notebook. Say that it is session 12 material, and leave it there.

## Watch out for

- **`python3` versus `python`.** On Windows it is `python` (and `python3` may open the
  Microsoft Store). On a Mac it is `python3` until a venv is active, after which `python`
  works too. Agree which one he types before the venv block.
- **PowerShell refusing to activate.** "Running scripts is disabled on this system". The fix
  is `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, once. Command Prompt uses
  `.venv\Scripts\activate.bat` instead, and Git Bash `source .venv/Scripts/activate`.
- **Forgetting to activate.** `ModuleNotFoundError: No module named 'pandas'` in a fresh
  terminal means the venv is not active, not that pandas is missing. The `(.venv)` at the
  start of the prompt is the thing to look at.
- **VS Code using a different Python.** The notebook kernel and the terminal can each pick a
  different interpreter. Bottom right in VS Code shows which one; pick the `.venv` one for
  `project/`.
- **Committing `.venv/`.** The root `.gitignore` already covers it. Have him run
  `git status` after creating it and see that it does not appear; that is the proof.
- **`parents[3]` off by one.** Counting from zero confuses everybody once. `parents[0]` is
  the folder the file is in. If the script cannot find `data/`, print `ROOT` first.
- **Printing inside the stages.** The session 3 habit slips under pressure. Same move as then:
  ask for one more output (the CSV) and let the requirement force the return.
- **"My data file is not in `git status`."** Deliberate: the root `.gitignore` ignores
  everything in `project/data/` except its README, so personal exports never reach GitHub.
  The project README says where the data comes from instead.
- **`__file__` in a notebook.** `NameError`. Notebooks have no file being run; that is why
  every notebook here starts with the walk-up cell instead.

## Definition of done

The device pipeline runs from two different folders with the same output, only `main()`
prints, and `project/pipeline.py` runs inside its own activated `.venv` on his machine. He
can say in his own words why `.venv/` is not committed and what the two lines at the bottom
of the script are for.

By session 11, the homework's two rebuilds have worked on his machine: `output/` deleted and
the same summary back, and `.venv/` deleted and rebuilt from `requirements.txt`.
