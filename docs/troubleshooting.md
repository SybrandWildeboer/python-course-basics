# When something breaks

The errors you will actually hit, roughly in the order the course hits them, with the fix.

**The habit that matters most: read the last line of the error first**, then look at the line
number. Everything above the last line is context.

---

## Setup and environment

### `python: command not found` or `'python' is not recognized`

The tool is installed; your terminal cannot find it.

1. **Close every terminal window and open a new one.** PATH is only read at startup, and this
   fixes it most of the time.
2. On **Windows**, re-run the Python installer, choose **Modify**, and tick **Add Python to
   PATH**.
3. On **macOS and Linux**, it is `python3` and `pip3`, not `python` and `pip`.

### `pip: command not found`

Use `python3 -m pip install ...` instead. It does the same thing and works whenever Python
itself does.

### `error: externally-managed-environment`

Your Linux distribution is protecting the system Python. Either use a virtual environment
(the right answer, and session 10 covers it):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas
```

or install for your user only: `python3 -m pip install --user pandas`.

### `ModuleNotFoundError: No module named 'pandas'`

Python cannot see the package. Almost always one of:

- **the venv is not activated.** Your prompt shows `(.venv)` when it is. Activating is per
  terminal, every time.
- **VS Code is using a different Python from your terminal.** Bottom right, or the kernel
  picker in a notebook: point it at the same one you installed into.
- it installed into a different Python. Check with `python3 -m pip list | grep pandas`.

### VS Code cannot find a kernel for a notebook

`pip install ipykernel`, then **Select Kernel** again. VS Code usually offers to do this for
you; say yes.

### `git clone` asks for a username and password

For a public repo it should not. An old credential helper is in the way. Do not debug it
mid-session: download the ZIP from GitHub and carry on, then fix it properly in session 5
when authentication is on the agenda anyway.

---

## Python errors

### `SyntaxError`

Python cannot even read the line. Missing colon, quote or bracket. **Look at the line above
it too**, because an unclosed bracket makes the *next* line look wrong.

If it makes no sense at all, you may have **smart quotes** from pasting out of a chat app:
`“like this”` instead of `"like this"`. Retype the quotes by hand.

### `IndentationError`

Spacing is wrong at the start of a line. Usually a mix of tabs and spaces, which looks fine
on screen. In VS Code: **Convert Indentation to Spaces** from the Command Palette.

### `NameError: name 'x' is not defined`

Python has never seen that name. A typo, a capitalisation difference, or a variable you
meant to create earlier.

**In a notebook**, it also means you did not run the cell that created it, or you ran cells
out of order. **Restart and Run All.**

### `TypeError: unsupported operand type(s) for -: 'int' and 'str'`

Text where a number belongs. `input()` and CSV files **always** give you text.

```python
year = int(input("Year: "))
total += float(row["minutes_played"])
```

### `TypeError` mentioning `NoneType`

Something returned `None`. Nearly always a function that **printed instead of returning**:

```python
def double(n):
    print(n * 2)      # dead end
    return n * 2      # usable
```

Also: `x = x.sort()` sets `x` to `None`, because `.sort()` sorts in place and returns
nothing. Use `sorted(x)`.

### `ValueError: invalid literal for int() with base 10`

The text is not a number. `int("forty one")`, or `int("21.5")` which needs `float()`.

On a whole column, `pd.to_numeric(col, errors="coerce")` turns the unreadable ones into
`NaN` instead of stopping.

### `ZeroDivisionError`

Usually dividing by a count that came out empty. Check the count before dividing.

### `IndexError: list index out of range`

You asked for a position that does not exist. Remember `len(x) - 1` is the last position, and
an empty list has none at all.

### `KeyError: 'genre'`

That key is not in the dictionary, or that column is not in the DataFrame.

```python
print(list(rows[0].keys()))          # what IS there
print([repr(c) for c in df.columns]) # catches invisible trailing spaces
```

A column called `"minutes played "` with a trailing space is a real thing that happens, and
`repr()` is how you see it.

### `FileNotFoundError`

The file is nearly always fine. Python is looking somewhere else.

```python
import os
print(os.getcwd())            # where am I actually?
```

Relative paths are counted from the folder your **terminal** is in, not the file you are
editing. Either run everything from the repo root, or use:

```python
from pathlib import Path
HERE = Path(__file__).resolve().parent
```

### `UnicodeDecodeError`

Pass `encoding="utf-8"` to `open` or `read_csv`. Without it, Python guesses, and the guess is
often wrong on Windows. The course data has `Salon Mécanique` in it, so this matters.

### The program runs forever

An infinite loop. `Ctrl` `C` in a terminal, the square **interrupt** button in a notebook.
Check that something inside the loop actually changes the condition.

---

## Notebook problems

### Results make no sense, or a variable that should exist does not

The **run-order trap**. Cells remember what you ran, not what is on screen. **Restart and Run
All.**

If a notebook cannot run cleanly from top to bottom, it is not finished, however good the
output looks.

### A cell says `[*]` forever

It is still running, or waiting for input. If you called `input()`, look for the prompt box
at the top of the window. Otherwise interrupt it.

### `plt.show()` does nothing, or the chart does not appear

In a notebook, charts usually appear by themselves. If not, `%matplotlib inline` in a cell.

In a **script**, `plt.show()` opens a window and waits; use `fig.savefig(...)` instead, with
`matplotlib.use("Agg")` at the top.

### Git diffs on notebooks are unreadable

Notebooks are JSON, including every cell's output. Strip the outputs before committing:

```bash
python3 tools/nbtool.py check
python3 tools/nbtool.py strip
```

---

## SQL problems

### `no such column: artist_id` after a join

Ambiguous or unqualified. Alias the tables and qualify the columns:
`p.artist_id`, `a.artist_name`.

### A query returns no rows and you expected some

- `= NULL` **never matches anything.** Use `IS NULL`.
- text comparisons are exact: `'phone'` is not `'Phone'`.
- single quotes for text; double quotes mean an identifier.
- if you joined, the keys may not match. Look at a few values from each side.

### `misuse of aggregate function COUNT()`

You used `COUNT(*)` in a `WHERE`. Aggregates are filtered with `HAVING`, because at `WHERE`
time no counting has happened yet.

### A percentage comes out as 0

Whole-number division. `19 / 179` is `0` in SQLite. Multiply by `100.0` first.

### The totals are bigger than they should be

**Fan-out.** A one-to-many join multiplied your rows. Count the rows before and after the
join. The fix is to aggregate first, then join, usually with a CTE. `SUM(DISTINCT x)` is
**not** the fix; it produces a different wrong answer.

---

## pandas problems

### `ValueError: The truth value of a Series is ambiguous`

Use `&` and `|` instead of `and` and `or`, and bracket every condition:

```python
df[(df["a"] > 1) & (df["b"] < 2)]
```

### `SettingWithCopyWarning`

"You may have changed a copy and I cannot tell." Assign with `.loc` and it never appears:

```python
df.loc[df["x"] > 1, "y"] = 0
```

### `KeyError` on a column that is definitely there

After a `groupby`, the key became the **index**, not a column. `.reset_index()`.

### The numbers in a column will not add up

Check `df.dtypes`. A column of numbers read as text will concatenate rather than add.

### Dates are wrong but nothing errored

If the column has **mixed formats**, `pd.to_datetime(..., dayfirst=True)` applies day-first
to the ISO dates too, so `2025-09-06` silently becomes the 9th of June. Parse each format
explicitly. Session 9 covers this, and it is the worst bug in the course because nothing
complains.

### Rows vanished after cleaning

A bare `dropna()` drops a row if **any** column is empty. Use `subset=[...]`. And print the
shape before and after, every time.

---

## Still stuck?

After twenty minutes, send:

1. **what you were trying to do**, in one sentence
2. **the exact error text**, copied and pasted, especially the last line
3. **the code**, or a link to the commit

That is not a hurdle. It is the habit that gets you useful answers from anybody, including
strangers on the internet, long after this course ends.
