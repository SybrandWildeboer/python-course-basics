# Virtual environments and project setup

The commands from session 10, with what each one is for.

---

## Creating and using a virtual environment

A virtual environment is a folder holding its own copy of Python and its own packages, just
for this project. Nothing in it can affect anything else on your machine.

```bash
python3 -m venv .venv                 # 1. create it, once per project
```

```bash
source .venv/bin/activate             # 2. macOS and Linux
.venv\Scripts\activate                # 2. Windows
```

```bash
pip install pandas matplotlib         # 3. installs into the venv, not your machine
pip freeze > requirements.txt         # 4. write down exactly what you installed
```

```bash
deactivate                            # when you are finished for the day
```

**Step 2 is the one everybody forgets.** Activating is per terminal, every time. Forget it
and `pip install` goes to your machine again, or your script cannot find pandas. The tell is
your prompt: it shows `(.venv)` when the environment is active.

### Rebuilding it somewhere else

This is the whole point of `requirements.txt`. On a new machine, or after deleting `.venv/`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Try it. Delete `.venv/`, rebuild it from the file, run your pipeline. That is the moment
`requirements.txt` stops being a ritual and becomes obviously useful.

### In VS Code

Once `.venv` exists, VS Code usually offers to use it, and it appears in the notebook kernel
picker. Pick it. Otherwise your notebook and your terminal end up using different Pythons,
which is maddening to debug: `pip install` succeeds and `import` still fails.

---

## Project layout

```
my-project/
    README.md            what this is, and how to run it
    requirements.txt     what it needs
    .gitignore           what not to commit
    .venv/               the environment (ignored)

    data/                inputs. read only, never edited by hand
        music.db

    notebooks/           exploring, thinking, trying things
        01-explore.ipynb

    src/                 the code that does the work
        pipeline.py

    output/              everything generated (ignored)
        minutes_by_genre.csv
        minutes_by_month.png
```

The idea:

- **`data/`** is input, and you never edit it by hand
- **`src/`** is what you wrote
- **`output/`** is what the code made, and can always be deleted and remade
- **`notebooks/`** is where you worked it out

### The test that the layout is honest

**Delete `output/` and run the script. If everything comes back, you are fine.**

If something does not come back, you had a file you could not regenerate and did not know
it. That usually means a notebook quietly wrote something the script depends on.

---

## What goes in .gitignore

```
.venv/
__pycache__/
*.pyc
output/
.ipynb_checkpoints/
.DS_Store
```

`.venv/` is hundreds of files of somebody else's code, specific to your operating system.
Commit `requirements.txt` instead: one small text file that rebuilds it exactly.

`output/` is generated. Commit the code that makes the chart, not the chart.

---

## Running your own code from a notebook

Once the logic lives in `src/pipeline.py`, borrow it rather than copying it:

```python
import sys
sys.path.append("src")

from pipeline import load, clean, minutes_by_genre

plays = clean(load())
minutes_by_genre(plays)
```

Nothing is written, because `main()` did not run. That is what
`if __name__ == "__main__":` is for: the file can be **run** as a program or **imported** as
a toolbox, and it behaves sensibly either way.

This is also how you debug a script. Import the failing function, call it with real data, and
poke at the result interactively instead of adding print statements.
