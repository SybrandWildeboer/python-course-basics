# Session 10: Putting it together

**Goal:** one script that goes from the database to a finished chart and CSV. It becomes the
template for their project.

**Slides:** [`slides/session-10.html`](../../slides/session-10.html) (19 slides)

---

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00–0:15 | Homework review: three charts and `findings.md` | Slide 2 |
| 0:15–0:35 | Why a venv, the four commands, project layout | Slides 4–6 |
| 0:35–0:45 | The project README, and why the question goes at the top | Slide 8 |
| 0:45–0:55 | Notebook to script, and the four steps | Slides 9–10 |
| 0:55–1:05 | Break | |
| 1:05–1:20 | Paths at the top, `__main__`, printing progress, the finished shape | Slides 11–14 |
| 1:20–1:50 | **They build the whole pipeline.** This is the session | Slide 16 |
| 1:50–1:55 | The delete-and-rerun test, and the project checklist | Slide 17 |
| 1:55–2:00 | Homework, commit, push | Slides 18–19 |

Protect the 30 minutes of building. If the earlier blocks overrun, cut the debugging slide
and the finished-shape slide; both are in the materials for them to read.

## What they type

| File | What it is |
|---|---|
| `exercises/pipeline.py` | The skeleton: constants, docstrings and TODOs, no bodies |
| `solutions/pipeline.py` | The finished pipeline, runnable, about 170 lines with comments |
| `demos/venv_commands.md` | Every command from the session, with what each is for |
| `notebooks/01-notebook-and-script.ipynb` | Imports the finished pipeline and uses its four functions, which is the pairing the session is about |

`project/` in the repository root is the template they copy in session 11: README with the
question at the top, `requirements.txt`, `.gitignore`, and a `src/pipeline.py` with the four
steps stubbed out.

## The two moments that land

**The delete-and-rerun test.** `rm -rf output/ && python3 src/pipeline.py`, and everything
comes back. It is a genuinely good feeling, and it is the test that catches a project
depending on a file nobody can regenerate.

**Importing their own script into a notebook.** Nothing prints, nothing is written, and the
four functions are just available. That is the payoff for every "return, do not print"
instruction since session 3, and it is how they will debug their project.

## Watch out for

- **Forgetting to activate the venv.** Per terminal, every time. The prompt shows `(.venv)`.
  Symptom: `pip install` works and `import pandas` still fails, or vice versa.
- **VS Code using a different Python from the terminal.** Once `.venv` exists, point both at
  it. This one wastes a lot of time when it goes unnoticed.
- **Hardcoded absolute paths.** The single most common reason a beginner's project does not
  run on anybody else's machine. `Path(__file__).resolve().parent` is the fix.
- **All the code at module level** instead of in functions. Then nothing can be imported or
  tested, and the file has to run top to bottom every time.
- **Functions that do four things.** If you cannot name it after one thing, it is more than
  one thing. Watch for load-and-clean-and-save.
- **Committing the venv or large data files.** Both belong in `.gitignore`.
- **`plt.show()` in a script**, which blocks waiting for a window to be closed.
  `matplotlib.use("Agg")` at the top prevents it entirely.

## Definition of done

One command produces both output files, from scratch, with `output/` deleted first. And they
can explain what `if __name__ == "__main__":` is for in their own words.

## Before session 11

Remind them to bring **one or two project ideas and data they can actually get hold of**.
Warn them, warmly, that you are going to scope it down hard. It is much easier to hear that
in advance.
