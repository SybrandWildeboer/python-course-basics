# Jupyter cheatsheet

Notebooks are the main way you work on this course. This is everything you need to know
about the tool itself.

---

## Running cells

| Keys | What it does |
|---|---|
| `Shift` `Enter` | Run this cell and move to the next |
| `Ctrl`/`Cmd` `Enter` | Run this cell and stay here |
| `Alt`/`Option` `Enter` | Run this cell and insert a new one below |
| `Esc` then `A` | Insert a cell above |
| `Esc` then `B` | Insert a cell below |
| `Esc` then `D` `D` | Delete this cell |
| `Esc` then `M` | Turn it into a markdown cell |
| `Esc` then `Y` | Turn it back into code |
| `Ctrl`/`Cmd` `/` | Comment or uncomment the selected lines |

`Esc` leaves the cell so the next key is a command rather than typing. `Enter` gets you back
in.

## The one trap

**Cells remember what you ran, not what is on screen.**

Scroll up, change a cell, run it, and everything below it is now out of date. The notebook
will happily disagree with itself and it looks completely normal. The number beside a cell,
`[1]`, `[2]`, tells you the order things actually ran in.

Worse: a cell can pass because of a variable you created ten minutes ago and have since
deleted.

**The fix, and it is the whole fix: Restart and Run All.** It clears everything and runs from
the top, in order.

> **If a notebook cannot run cleanly from top to bottom, it is not finished, however good
> the output looks on screen.**

## Stopping a runaway cell

The square **interrupt** button in the toolbar, or **Kernel, Interrupt**. It is the notebook
equivalent of `Ctrl` `C`.

If that does not work, **Kernel, Restart**, which throws away every variable but always
works.

## Showing values

The last line of a cell displays its value without needing `print`:

```python
df.head()          # shows the table
```

Only the **last** line, though. Use `print()` when you want several things from one cell.

```python
df.head()          # this one is not shown
df.tail()          # only this one
```

## Markdown cells

Double-click one to edit it, `Shift` `Enter` to render it.

```markdown
# Heading
## Smaller heading

**bold**, *italic*, `code`

- a list
- another item

1. numbered
2. another

| a | b |
|---|---|
| 1 | 2 |

> a quote

```python
a fenced code block, not run
```
```

Use them. A notebook with prose between the cells is a document; one without is a pile of
code with output in it.

## Useful magics

```python
%whos                  # every variable currently defined, with its type
%time expression       # how long one line took
%%time                 # how long this whole cell took (first line of the cell)
!ls                    # run a shell command
!pip install pandas    # install without leaving the notebook
%matplotlib inline     # charts appear in the notebook (usually the default)
```

## In VS Code

- open any `.ipynb` and it just works
- top right, **Select Kernel**, choose your Python or your `.venv`
- if it cannot find a kernel, the fix is almost always `pip install ipykernel`, and VS Code
  usually offers to do it for you
- the variables panel shows everything currently defined, which is handy when the run-order
  trap bites

## In the browser

```bash
pip install jupyterlab
jupyter lab                    # from your project folder
```

Same notebooks, same everything. Stop the server with `Ctrl` `C` in the terminal.

## Notebooks and git

A `.ipynb` is JSON: your code, your prose, and the **output of every cell**. So:

1. diffs are hard to read
2. outputs get committed, so files bloat and every run makes a diff
3. execution counts churn even when nothing changed

```bash
python3 tools/nbtool.py check    # valid, and free of saved output?
python3 tools/nbtool.py strip    # remove saved output
python3 tools/nbtool.py run      # do they all still run?
```

Strip outputs before committing, and `.ipynb_checkpoints/` goes in `.gitignore`.

## Notebook or script?

| A notebook is right when | A script is right when |
|---|---|
| exploring, in small steps | somebody needs to *run* the thing |
| you want the answer next to the code | it asks questions, with `input()` |
| learning something new | it runs start to finish, unattended |
| you will write it up with prose | it gets scheduled, or shared as a tool |
| you will read it more than run it | you have run the same cells three times |

It is not either/or. Explore in the notebook, move the settled parts into a script, and
import them back:

```python
import sys
sys.path.append("src")

from pipeline import load, clean
plays = clean(load())
```

Nothing runs that you did not ask for, because everything in the script that does work sits
behind `if __name__ == "__main__":`. That is also how you debug a script: import the failing
function, call it with real data, and poke at the result.
