# Code review checklist

For reviewing a diff: somebody else's, or your own before you commit it. You will not need
every line every time. Go top to bottom; the first sections catch the expensive problems.

Read the diff with `git diff` (not yet staged), `git diff --staged` (staged), or
`git show <commit>` (already committed). VS Code's Source Control panel shows the same thing
side by side.

---

## 1. Before reading a single line

- [ ] **It runs.** From a fresh terminal at the repository root: `python project/pipeline.py`.
- [ ] **The tests pass.** From inside `project/`: `python -m pytest`.
- [ ] **The commit does one thing**, and its message says what and why. "Add awards and fix
      loading" is two commits.

## 2. Are the numbers right?

The mistakes that cost most produce no error at all.

- [ ] **Every merge or join is checked.** Row count before and after, or
      `merge(..., validate="many_to_one")`. If the count went up and nobody expected it to,
      that is fan-out (session 7).
- [ ] **Every cleaning decision is written down**, with how many rows it touched. Dropping,
      filling and coercing all change the answer (session 9).
- [ ] **Every division has a plan for zero.** Plain Python raises `ZeroDivisionError`;
      pandas quietly gives `NaN`.
- [ ] **One headline number is confirmed a second way**: the parts add up to the whole, or
      one cell recomputed with a filter instead of a `groupby` (session 11).
- [ ] **It survives the data changing slightly.** Imagine next month's file: an extra or
      renamed column, a new category, a missing month, twice the rows. Look for hardcoded
      column lists, assumed date ranges, a check that expects an exact number of rows, and a
      `groupby` or chart that silently drops a category it has not seen. Either it copes, or
      it stops with a clear message; it never carries on quietly wrong.

## 3. Errors

- [ ] **No bare `except:`**, and no `except Exception:` without a very good reason written
      next to it. Each `except` names the one error it expects.
- [ ] **A missing file is never turned into empty data.** `return pd.DataFrame()` or
      `return []` in an `except` is a lie that surfaces three functions later.
- [ ] **Each `try` block is small**: the one line that can fail, not the whole function.
- [ ] **Errors are handled in the outer layer** (`main()`), where there is a person to tell.

## 4. Shape and names

- [ ] **Functions that calculate return; only `main()` prints** (session 3). A `print` inside
      `clean()` or `analyse()` is a review comment.
- [ ] **Names say what things are.** `minutes_per_genre`, not `df2`, `temp` or `x`.
- [ ] **No paths that only exist on one laptop.** Paths are built from
      `Path(__file__).resolve().parent` (session 10). `C:/Users/...` in a diff is always a
      comment.
- [ ] **No unexplained numbers.** `summary[summary["minutes"] > 500]`: why 500? Give it a name
      in capitals at the top of the file and a comment saying where it came from.
- [ ] **Docstrings say what comes back**, and any decision the reader could not guess.

## 5. What goes into git

- [ ] **No private data.** Look at `git status` before every commit (session 11).
- [ ] **No `output/`, no `.venv/`, no `__pycache__/`.** If they show up, `.gitignore` is wrong.
- [ ] **`requirements.txt` lists everything that is imported**, including `pytest` once there
      are tests.

---

## Writing the comments

- **Point at a line**, and say what you see, not what you would have written: "line 18
  catches every error, including typos" rather than "I would not do it like this".
- **Ask when you are not sure.** "Is this merge meant to repeat each play once per award?"
  is a better comment than "this is wrong", and sometimes the answer is yes.
- **Say one thing to keep.** A review that only lists problems teaches the author to avoid
  reviews. Something in every diff was done well; say which.
- **Sort by cost.** A wrong number matters more than a variable name. If there are ten
  comments, say which two matter.
