# Session 8: pandas

**Goal:** the same questions as sessions 6 and 7, answered in Python, and an honest sense of
when to reach for which tool.

**Slides:** [`slides/session-08.html`](../../slides/session-08.html) (21 slides)

---

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00–0:15 | Homework review: the join questions, and row counts | Slide 2 |
| 0:15–0:25 | `pip install`, and what a DataFrame is | Slides 4–5 |
| 0:25–0:45 | Loading data, the first-five-minutes ritual, selecting | Slides 6–8 |
| 0:45–0:50 | Filtering, and the two mistakes everybody makes | Slide 9 |
| 0:50–1:00 | Break | |
| 1:00–1:20 | `value_counts`, `groupby`, the index surprise | Slides 10–12 |
| 1:20–1:30 | `merge`, and fan-out again | Slides 13–14 |
| 1:30–1:40 | Side by side, and when to use which | Slides 16–17 |
| 1:40–1:55 | Translate four of their own queries | Slide 19 |
| 1:55–2:00 | Homework, commit, push | Slides 20–21 |

Today should feel easy, and it is worth saying so out loud. Every idea is one they already
have from sessions 4, 6 and 7. Only the notation is new.

## The three slides that matter

**Slide 9, filtering.** `and` instead of `&`, and missing brackets, account for a good half of
pandas frustration in the first month. Have them make both errors on purpose and read the
messages.

**Slide 12, the index surprise.** After a `groupby` the key becomes the index, and then
everything that treats it as a column fails. Show the `KeyError`, then `reset_index()`, and
tell them it is the reflex.

**Slide 14, fan-out in pandas.** Identical numbers to session 7, because it is the same
arithmetic. The point is that fan-out was never a SQL quirk. `validate="many_to_one"` is the
one real advantage pandas has here, and hardly anybody uses it.

## Notebooks

| Notebook | What it is |
|---|---|
| `notebooks/01-pandas-basics.ipynb` | The walkthrough: loading, orienting, selecting, filtering, grouping, merging, fan-out |
| `notebooks/02-sql-and-pandas.ipynb` | Four questions answered both ways, with `.equals()` proving they agree, plus a translation table |
| `notebooks/03-sql-to-pandas-exercise.ipynb` | The live exercise: translate four of **their own** queries |
| `notebooks/04-five-questions-homework.ipynb` | Homework task 1 and 2 |
| `notebooks/04-five-questions-solved.ipynb` | Worked answers, including the "awkward in SQL" question done both ways |

`demos/pandas_basics.py` is the same material as a script. Its docstring lists what changes
in that shape: every result needs an explicit `print`, tables are harder to read, you cannot
poke at an intermediate value, and it runs unattended in one command. Worth two minutes at
the end of the session, because session 10 is about making that move deliberately.

## The live exercise

They translate **their own** queries, not mine. Insist on checking that the two answers
match: it is how they discover for themselves that a merge changed the row count.

## Watch out for

- **`and` / `or` instead of `&` / `|`**, and missing brackets. Slide 9.
- **`SettingWithCopyWarning`.** Explain it once, calmly: "you may have changed a copy and I
  cannot tell". Then give them the habit that prevents it entirely, which is assigning with
  `.loc`. Do not go into views and copies.
- **The index after `groupby`.** `reset_index()`.
- **`inplace=True`.** Tell them not to. It saves five characters, is no faster, does not
  chain, and makes half their lines change things invisibly.
- **Types.** `df.dtypes` is the first thing to check when arithmetic behaves oddly. A column
  of numbers read as text will concatenate rather than add.
- **Version differences.** Text columns show as `str` in pandas 3 and `object` in pandas 2.
  The notebook says so, because most tutorials online say `object`.
- **`pip install` failing** with a permissions or "externally managed environment" error.
  `python3 -m pip install --user pandas` is the usual way through, and it previews why
  session 10 has virtual environments in it.

## Definition of done

They can load a CSV or a query into a DataFrame, filter it, group it, merge it, and translate
a query they wrote in session 6 or 7 into pandas without help.
