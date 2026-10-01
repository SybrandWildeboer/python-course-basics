# Your project

This folder is the starting point for your final project, from session 11. It already runs:
out of the box it answers one question about the course's music data, so you begin by
changing something that works rather than by staring at an empty file.

It was built in session 10 from `sessions/session-10/demos/genre_pipeline.py`: the same
stages and the same answer, with a shorter `clean` that is easier to rewrite, and the places
you will change marked `MAKE IT YOURS`.

```
project/
    README.md            this file: what it is, how to run it, how to make it yours
    requirements.txt     the packages it needs, with exact versions
    pipeline.py          load -> clean -> analyse -> save, and main()
    notebooks/
        explore.ipynb    where you look at the data before code moves into pipeline.py
    data/
        README.md        your input data goes in this folder; git ignores everything else in it
    output/              what the pipeline writes; git ignores it
```

## The question

> Which genre do I spend most of my listening time on?

*Replace this with your own question in session 11: one question, one dataset, one
output.*

## Run it

### The first time: a virtual environment

A virtual environment is a private set of packages for this project only, so what you
install here cannot break anything else, and the versions in `requirements.txt` are the
ones you actually run. You make it once.

It needs Python 3.10 to 3.12 (`python --version` tells you). The `matplotlib==3.9.0` in
`requirements.txt` has no ready-made installer for 3.13 or newer, so pip tries to build it
from source there and fails. Open a terminal in the repository root, then:

**Windows (PowerShell)**

```powershell
cd project
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS**

```bash
cd project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

When it is active, the prompt starts with `(.venv)`. Inside it, `python` and `pip` mean the
project's own copies on both systems.

If PowerShell says running scripts is disabled, run this once and try again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### Every time after that

```bash
cd project
.venv\Scripts\Activate.ps1        # Windows
source .venv/bin/activate         # macOS
python pipeline.py
```

You should see:

```
Which genre do I spend most of my listening time on?
  loaded    2223 rows from plays_messy.csv
  cleaned   2183 rows
  analysed     8 rows in the summary
  wrote    output/summary.csv
  wrote    output/chart.png
  checked  the summary adds up to the cleaned rows
```

One line per stage, printed as each one finishes. The stages themselves print nothing;
only `main()` talks. So if a run stops halfway, the last line tells you which stage it
reached, and if `cleaned` suddenly says 218 instead of 2183, you see it before the chart
hides it.

`deactivate` switches the environment off again. Closing the terminal does the same.

The paths in `pipeline.py` are built from the location of the file itself, so
`python project/pipeline.py` from the repository root works just as well.

### Why `.venv/` is not in git

The `.venv` folder holds a few hundred megabytes of installed packages, built for your
computer and your version of Python. It would be useless on anyone else's machine. So git
ignores it, and `requirements.txt` goes in git instead: a short list from which anyone can
rebuild the same environment with one `pip install -r requirements.txt`.

If you add a package, install it with `pip install` while the environment is active, then
add it to `requirements.txt` with its version. `pip freeze` lists exactly what is installed.

## Make it yours

Change one stage at a time, and run the whole pipeline after each change. A pipeline that
ran five minutes ago is easy to fix; one that has not run since this morning is not.

1. **Data.** Put your file in `data/`, and point `INPUT` at the top of `pipeline.py` at it.
   Nothing in `data/` is committed except its README: git ignores your input files by
   default, because they are often personal. Say in this README where the data comes from
   instead.
2. **Look.** Open `notebooks/explore.ipynb` and run it. It uses the pipeline's own `load`,
   so you are looking at exactly what the script sees. Write down every problem you find.
3. **Load.** If `load` fails, fix it first: a different separator, an Excel file, a
   different encoding. Nothing else matters until the data arrives. For Excel,
   `pd.read_excel` needs the `openpyxl` package, which is not in `requirements.txt`:
   `pip install openpyxl` with the environment active, and add it to the file. Saving the
   sheet as a CSV avoids the extra package altogether.
4. **Clean.** Rewrite `clean` for your problems, one at a time. Put each decision in its
   docstring, because each one changes the answer.
5. **Analyse.** Rewrite `analyse` to answer your question. It returns a table and prints
   nothing.
6. **Save.** Change the column names and title in `save_chart`. The title states the
   answer.
7. **Check.** Keep at least one check that compares a total in the written file with the
   same total worked out from the cleaned data.
8. **This README.** Your question, where the data came from, how to run it, and the three
   sections below.

Before you call it done, delete `output/` and run the pipeline again: everything should come
back the same. Then delete `.venv/` and rebuild it from `requirements.txt`. If both work, the
project runs on a machine that is not yours.

## What I found

*Two or three sentences: the answer to the question at the top, with the number. For the
music data: Electronic, with 2,753.2 of 8,608.0 minutes, 32.0% of my listening time.*

## What this does not show

*The most valuable paragraph in the file. What can this analysis not tell you? What would
somebody be wrong to conclude from it? How much data is each claim resting on? Every dataset
has gaps: say what yours are, and how big. For the music data: 94 plays lost their minutes in
the messy export, 372.4 minutes, about 4% of the total, so every genre's minutes are a little
low. And it is two years of one person's listening: it says nothing about anyone else.*

## Cleaning decisions

*What you dropped, filled or labelled, how many rows each decision touched, and what it did
to the answer. Copy them from the docstring of `clean`. For the music data: 40 exact
duplicate rows dropped (2,223 to 2,183); 34 missing genres and 48 missing
countries filled in from the same artist's other plays; 69 blank devices labelled
`unknown`; 94 blank minutes left missing rather than guessed.*
