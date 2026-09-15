# Watch out for

Every "watch out for" from all twelve sessions, in one place, for when a question arrives
mid-week and you want the likely cause fast.

The per-session versions with more context are in each `sessions/session-NN/README.md`.

---

## Setup and environment

- **Windows PATH.** "Add Python to PATH" is unticked by default. Fix: close every terminal,
  open a new one. Then re-run the installer, Modify, tick the box.
- **`python` versus `python3`.** Agree one spelling in session 1 and keep it for twelve
  sessions.
- **Not saving before running.** Python runs the file on disk. VS Code shows a dot on the
  tab.
- **Smart quotes** from pasting out of a chat app. `“like this”` is not `"like this"` and the
  difference is nearly invisible.
- **Opening a file instead of a folder** in VS Code. Opening the folder is what makes the
  terminal start in the right place.
- **VS Code and the terminal using different Pythons.** `pip install` succeeds and `import`
  still fails. Point both at the same one.
- **The venv not activated.** Per terminal, every time. The prompt shows `(.venv)`.

## Python

- **`=` versus `==`.** Constant in session 2. Python's message is good; let them read it.
- **`range(1, 10)` not including 10.** Say it, show it, let them be annoyed.
- **Missing colons** at the end of `if` and `for` lines.
- **Indentation.** Grammar, not decoration. Mixed tabs and spaces is the nasty version.
- **`total = 0` inside the loop.** Let them hit it, then ask what is resetting.
- **Deep nesting.** Let them finish, then flatten it together. Showing beats telling.
- **Printing instead of returning.** Ask for one line containing four numbers and let the
  requirement force the change.
- **Defining a function and never calling it.** No error, no output, total confusion.
- **Missing brackets on a call.** `greet` instead of `greet()`.
- **A `return` inside an `if` with no other path.** Returns `None` silently.
- **Reaching for `global`.** Say it exists, that it is almost always wrong, and steer back.
- **`x = x.sort()`** throwing the list away.

## Files and data

- **`FileNotFoundError` from a relative path.** First move, every time: print
  `os.getcwd()`.
- **Forgetting `list()` around `DictReader`.** Can only be walked once; the second loop
  silently does nothing.
- **Everything from a CSV being text.** `float()` before arithmetic.
- **`KeyError` from a mistyped column.** `print(list(rows[0].keys()))`.
- **Missing `encoding="utf-8"`.** The data has `Salon Mécanique` in it.
- **Writing to `output/` before it exists.** `os.makedirs("output", exist_ok=True)`.

## Notebooks

- **The run-order trap.** Cells remember what ran, not what is on screen. **Restart and Run
  All** is the fix and the standard.
- **Notebooks committed with saved output.** `tools/nbtool.py check` and `strip`.
- **`input()` in a notebook.** Technically works, awkward. Interactive things want to be
  scripts.
- **A cell stuck on `[*]`.** Still running, or waiting for input. Interrupt it.

## Git

- **`user.name` and `user.email` not configured.** The most common first-commit failure.
- **Committing everything including junk.** Look at `.gitignore` together.
- **Commit messages like "stuff".** Do not lecture; the homework has them read their own
  messages back.
- **Fear of breaking things.** Say out loud, more than once, that committed work is very hard
  to lose.
- **`git reset --hard`.** Deliberately not taught.

## SQL

- **`=` not `==`.** A Python habit.
- **Double quotes around text.** SQL wants `'phone'`.
- **`= NULL`.** Runs, returns nothing, warns nobody.
- **Selecting ungrouped columns.** SQLite permits it and returns nonsense.
- **`WHERE` versus `HAVING`.** The execution-order slide explains it in one picture.
- **Integer division.** `19 / 179` is `0`. `100.0 *` first.
- **`LIMIT` without `ORDER BY`.** Arbitrary rows, and SQLite looks stable enough to teach a
  bad habit.
- **Ambiguous column names** after a join. Alias everything.
- **`COUNT(*)` after a `LEFT JOIN`.** Reports 1 for a row with no matches, so "never played"
  becomes "played once".
- **Fan-out.** After any join, compare the row count with what it was before.
- **Reaching for `DISTINCT`** to fix fan-out. It produces a different wrong answer.

## pandas

- **`and` / `or` instead of `&` / `|`**, and missing brackets.
- **`SettingWithCopyWarning`.** Explain once, calmly, then give the `.loc` habit.
- **The index after `groupby`.** `reset_index()`.
- **`inplace=True`.** Tell them not to.
- **Types.** `df.dtypes` first when arithmetic misbehaves.
- **A bare `dropna()`.** Drops a row if any column is empty. On the messy file that is 238
  rows instead of 94.
- **Not checking `shape` before and after cleaning.**
- **Comparing unstripped text.** `" Pop "` is not `"Pop"`.
- **`pd.to_datetime(..., dayfirst=True)` on mixed formats.** Silently corrupts every ISO
  date. The worst bug in the course, because nothing complains.

## Charts

- **`plt.show()` blocking** in a script. `matplotlib.use("Agg")`.
- **Charts with no labels.** Hold the line from the first one.
- **Forgetting `fig, ax`** and stacking everything on one plot.
- **A cropped y-axis on a bar chart.** Happens by accident as often as on purpose.
- **A title that claims more than the data shows.** The most common way to over-claim, and
  the hardest thing to catch in your own work.

## Projects

- **A project that needs data they do not have.** The most common way these fail.
- **Scope creep disguised as ambition.**
- **Planning for two weeks and coding for zero.** Hard stop the planning block.
- **A question with no answer.** "Find interesting patterns" has no "done".
- **Hardcoded absolute paths.** The reason a project runs on one machine only.
- **Functions that do four things.** If you cannot name it after one thing, it is more than
  one.
- **Committing the venv or large data files.**
