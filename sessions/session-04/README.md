# Session 4: Lists, dictionaries, files, and git

**Goal:** hold a table's worth of data in memory, get data in and out of files, and meet the
dataset that carries the rest of the course. Then put four sessions of work under version
control and push it to their own GitHub repo, with enough understanding that git does not feel
frightening.

**Slides:** [`slides/session-04.html`](../../slides/session-04.html) (34 slides)

---

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00–0:10 | Homework review: the four functions and the menu | Slide 2 |
| 0:10–0:25 | Lists and dictionaries: indexing, slicing, `.get()`, `.items()` | Slides 3–10 |
| 0:25–0:30 | **A list of dicts is a table** | Slide 11 |
| 0:30–0:45 | Files, paths, `csv.DictReader`, text versus numbers, **the counting pattern**, writing a CSV | Slides 12–18 |
| 0:45–1:00 | Meet the listening log, then three questions about it, them driving | Slides 19–20 |
| 1:00–1:10 | Break | |
| 1:10–1:15 | Why version control, and the three places | Slides 21–23 |
| 1:15–1:30 | Configure git, status / add / commit / log, `.gitignore`, then commit sessions 1 to 4 | Slides 24–28 |
| 1:30–1:50 | **Authentication.** Budget the whole twenty minutes | Slide 29 |
| 1:50–1:55 | Their own repo: the remote rename, and the first push | Slide 30 |
| 1:55–2:00 | Branches for the homework, homework briefing, and DB Browser | Slides 31–34 |

The two halves meet at the break: the exercise they finish at 1:00 is the first thing they
commit at 1:15. Say so. Git is for the work they just did, not a separate subject.

## The slides that matter

**Slide 11, "a list of dictionaries is a table".** This is the hinge of the whole course.
`csv.DictReader` hands them this shape, a SQL query returns this shape, and a pandas
DataFrame is this shape with a faster engine underneath. Say that out loud.

**Slide 17, the counting pattern.** It is the accumulate pattern from session 2 with a
dictionary instead of one running total. In session 5 the same question is `GROUP BY genre`
and in session 6 it is `groupby("genre")`. Same idea, three notations. Making that link now
means SQL and pandas arrive as translations rather than as new subjects.

**Slide 29, authentication.** It reliably eats twenty minutes and it is miserable to debug
over chat, so **do it in the session**, never as homework. If the Python half overruns, take
the time from the Python exercise, not from this. Order of preference:

1. `gh auth login`. Least painful, and it configures the git credential helper too.
2. A personal access token pasted at the password prompt. Always works. Have them save it
   in a password manager, because it is not viewable again.
3. An SSH key. The grown-up answer, the fiddliest today.

## The remote rename, and why

They cloned this repo in session 1, so `origin` points at the course. Rather than starting a
fresh repo and losing four sessions of history, have them keep both remotes:

```bash
git remote rename origin course
git remote add origin https://github.com/THEIR-NAME/python-course.git
git push -u origin main
```

Now `git push` goes to their repo and `git pull course main` collects course updates. Say out
loud that a remote is just a nickname for a URL; that one sentence removes most of the
mystery.

## What they use

| File | What it is |
|---|---|
| `demos/lists_and_dicts.py` | Walkthrough part one, with the errors commented out |
| `demos/files_and_csv.py` | Walkthrough part two: paths, DictReader, counting, writing |
| `demos/git_commands.md` | Every git command from the session, with what each is for |
| `exercises/explore_plays.py` | Live exercise part one: three questions about the listening log |
| `solutions/explore_plays.py` | Worked version, with the expected output in a comment |
| `exercises/push_your_work.md` | Live exercise part two, in the terminal: commit and push |
| `homework/README.md` | All three homework tasks |
| `homework/filter_plays.py` | Homework 1 starter |
| `homework/questions.py` | Homework 2 starter |
| `homework/solutions/` | Both answers, including a note on the genuine tie in 2025, and `MY-NOTES-example.md` to show the level of detail for task 3 |

## Notebooks

| Notebook | What it is |
|---|---|
| `notebooks/01-lists-and-dicts.ipynb` | Lists, dictionaries, and the "a list of dicts is a table" idea |
| `notebooks/02-files-and-csv.ipynb` | Paths, `DictReader`, text-versus-number, the counting pattern, writing a CSV |
| `notebooks/03-explore-plays-exercise.ipynb` | Live exercise part one |
| `notebooks/03-explore-plays-solved.ipynb` | Worked version, with the expected output written out |
| `notebooks/04-notebooks-and-git.ipynb` | Why notebooks and git get along badly: JSON diffs, committed outputs, churning execution counts. Shows a real cell's JSON, and introduces `tools/nbtool.py check` and `strip` |
| `notebooks/05-questions-homework.ipynb` | Homework 2 |
| `notebooks/05-questions-solved.ipynb` | Worked version, showing the 2025 tie and the total-versus-average trap |
| `notebooks/06-stretch-exercise.ipynb` | Optional Python stretch, for when the live exercise finishes early |
| `notebooks/06-stretch-solved.ipynb` | Worked versions, with the reasoning written out |
| `notebooks/07-git-stretch-exercise.ipynb` | Optional git stretch, for when the repo is pushed early. Instructions only; the work happens in the terminal |
| `notebooks/07-git-stretch-solved.ipynb` | Worked versions, with the real output of each command and the reasoning written out |

Each data notebook starts with a short cell that walks up to the repository root, so it works
whichever folder VS Code opened it from.

Notebook 04 belongs to the commit block at 1:15: open it just before the first commit and
show one cell's JSON, then run `strip`. Committing notebooks full of saved output is the
single most common way a beginner's repo becomes unpleasant to work with. If time is short,
run the strip step and leave the notebook as reading.

## Before the session

- [ ] Check they have a **GitHub account** and can log in to it. If not, ask them to create one
      before the session; doing it live costs ten minutes and an email verification wait
- [ ] Check the dataset is generated: `python3 data/scripts/build_dataset.py`
- [ ] Open `data/clean/plays.csv` in VS Code so you can show the raw text, commas and all
- [ ] Check whether `gh` (the GitHub CLI) is installed on their machine: `gh --version`. If
      not, have them install it from <https://cli.github.com> before the session, or during
      the break

## If they want to use their own dataset

Slide 19's notes cover this. The requirements are: a few thousand rows at most, at least one
date column, one numeric column, a few categorical columns, and something that can become a
second related table for the joins in session 5. If theirs qualifies, let them use it;
caring about the data is worth more than the convenience of a prepared file. You will have to
translate the exercises, so decide before session 5, when the SQLite database appears.

## If there is time left

There are two stretch notebooks, one for each half. Use as many as the time allows; you
don't need to finish either.

**`06-stretch-exercise.ipynb`, Python**, for when the live exercise finishes early or for
homework. Six questions that get harder as you go. None of them repeat the live exercise or
the homework, and each one adds one idea:

| # | Function | What it adds |
|---|---|---|
| 1 | `plays_per_month` | Slicing text like a list (`played_at[:7]`), and why `YYYY-MM` sorts correctly as text |
| 2 | `tracks_by_artist` | A dictionary of lists, and 168 track names versus 229 actual tracks |
| 3 | `index_by`, `plays_by_decade` | A second file, a lookup dictionary, and blank `formed_year` values to decide about |
| 4 | `artist_stats`, `skip_rates` | A dictionary of dictionaries, and a minimum number of plays before a rate counts |
| 5 | `genre_by_year` | Building your own rows and writing them out: a pivot table by hand |
| 6 | read it back | Numbers come back from a CSV as text, and an `assert` that the file matches the log |

Numbers 3 and 4 are the ones to talk through rather than just check. In 3, what to do with
the 53 plays from artists with no `formed_year` (skip, guess, or label them `"unknown"`)
matters more than the code, and it sets up `IS NULL` in session 5. In 4, the most-skipped
artist is Circuit Sparrow at 28.6%, which is 2 skips out of 7 plays. Ask whether they believe
it before showing the `min_plays=30` version.

Stretch 3 is also a first, by-hand look at a `JOIN`: index one table by name, then look up
each play in it. Say so; it makes the join in session 5 a translation.

**`07-git-stretch-exercise.ipynb`, git**, for when the repo is pushed early. Seven tasks
that get harder as you go. Stretches 2 to 6 happen in a throwaway `git-playground` repo next
to the course folder (never inside it), so mistakes cost nothing. Only 1 and 7 touch the real
repo, and 1 only reads it.

| # | Stretch | What it adds |
|---|---|---|
| 1 | Read the history like a detective | `git log` with `--author`, `-- file`, `--stat`, `--grep` and `--graph --all` |
| 2 | Fix the last commit | `git commit --amend`, the hash changing, and why never after a push |
| 3 | `.gitignore`, and the trap in it | `git check-ignore -v`, and `git rm --cached` for a file committed by mistake |
| 4 | Put work aside | `git stash`, met through git refusing to switch branches |
| 5 | Undo a commit | `git revert` on a commit that is not the latest one |
| 6 | A merge conflict, on purpose | Reading the markers, `git merge --abort`, resolving and finishing the merge |
| 7 | A pull request on their own repo | Push a branch, open, review and merge on GitHub, then `git pull` and tidy up |

Number 5 is the one to talk through rather than just check. Why an opposite commit is safer
than `git reset --hard` (which they do not run) matters more than the command, and it ties
together the amend answer from 2 and the "committed work is hard to lose" message from the
session. Number 6 also turns the "merge conflicts are out of scope" line below into a
planned lesson instead of an unplanned one.

Every command that would otherwise open an editor is given with `--no-edit` or `-m`, but the
notebook tells them `:wq` gets them out of `vim` just in case.

## Watch out for

In the Python half:

- **`FileNotFoundError` from a relative path.** First move, every time: print
  `os.getcwd()`. The file is fine; Python is looking elsewhere. Agree the habit of running
  everything from the repo root.
- **Forgetting `list()` around `DictReader`.** You get a reader that can only be walked
  once, and the second loop silently does nothing. Genuinely worth demonstrating.
- **Everything arriving as text.** `total += row["minutes_played"]` fails with a `TypeError`.
  This is the same lesson as `input()` in session 1.
- **`KeyError` from a mistyped column name.** Show them `rows[0].keys()` as the fix.
- **`x = x.sort()`** throwing the list away. It connects straight back to functions that
  return `None`.
- **Missing `encoding="utf-8"`.** The dataset contains `Salon Mécanique`, so this bites.
- **Writing to `output/` before it exists.** `os.makedirs("output", exist_ok=True)`.

In the git half:

- **`user.name` and `user.email` not configured.** The most common first-commit failure.
  Do it before anything else.
- **Committing everything including junk.** Look at this repo's `.gitignore` together and
  point out that `output/` is why the CSVs they write there never appear in `git status`.
- **Committing notebooks with saved output.** `python tools/nbtool.py strip` before the
  first commit, and `check` before every commit after that.
- **Commit messages like "stuff".** Do not lecture. Homework task 3 has them read their own
  messages back, which teaches it better than you can.
- **Fear of breaking things.** Say out loud, more than once, that committed work is very hard
  to lose. Fear is what stops people committing often, and committing often is the benefit.
- **`git reset --hard`.** Deliberately not taught. If they find it online, explain that it
  genuinely destroys work and that `git restore` and `git revert` cover what they need.
- **Merge conflicts.** Out of scope today. If one happens, resolve it together calmly; it is
  a good unplanned lesson, and git stretch 6 covers it.

## Definition of done

They can load the CSV, count rows into a dictionary by any column, and total a numeric
column. `git status` is clean, `git log --oneline` shows several commits with real messages,
and their work is visible on github.com under their own account. From here every session
ends with a commit and a push.
