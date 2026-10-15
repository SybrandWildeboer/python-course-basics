# Before session 8: scope your project

Session 8 is two hours of pair programming on your own project. Those two hours go to code
only if the thinking is done before: what the question is, what is in and out, and whether
your data can answer it. That is this worksheet. Budget about two hours, and fill it in, in
this file, before the session. Short answers are better than long ones: if a section takes
more than a few lines, the project is probably still too big.

A filled-in example on the music data is in [`worked-example.md`](worked-example.md). Read it
after you have had a go at sections 1 and 2, not before.

**Bring to session 8:** this file filled in, your data in `project/data/`, and your one
number from section 5.

---

## 1. The task you started from

In session 1 you named one repetitive thing you do in a spreadsheet. Write it down as it
actually happens: what you open, what you copy, what you work out, how often.

> ...

What is the *answer* you are after when you do that task? Not the steps: the thing you know
at the end that you did not know at the start.

> ...

## 2. The question

One sentence, ending in a question mark, answerable with a number, a short table, or one
chart.

> **Question:** ...

What would the answer look like? Write a made-up one, so it is clear what "done" means.

> *e.g. "Category X went up by N per month; category Y went down by M."*

**First ideas are three projects wearing a coat.** "A dashboard of my spending, with
predictions" is a data pipeline, a web app and a forecasting model, and any one of them is a
fortnight on its own. "Analyse my data and find interesting patterns" has no question, so it
has no "done". Count the projects inside your idea, keep the one that answers the task from
section 1, and put the others under *could* or *won't* below, where they are kept rather than
thrown away.

The test: **can you say what "done" means in one sentence?** If not, it is not a project
yet. It is an area of interest.

## 3. The data

| | |
|---|---|
| What file or files | |
| Where it comes from | |
| Roughly how many rows | |
| Is it on your laptop **today**? | yes / no, arrives on ... |
| Which columns the question needs | |
| Is any of it private? (names, amounts, IP addresses, anything about other people) | |

If it is not on your laptop today, the project is not ready. "Once I get the data" is the
most common way a project dies. Use data you do have, or the course's music data as a
stand-in, and swap your own in when it arrives.

**A CSV from Dutch Excel** often uses `;` between columns and a decimal comma. `read_csv`
then happily produces one column and no error. `pd.read_csv(path, sep=";", decimal=",")`
reads it properly. An `.xlsx` needs `pd.read_excel` and the extra package `openpyxl`; saving
the sheet as CSV avoids both.

### The Spotify route

If your project will use your own Spotify listening history, you requested the *Extended
streaming history* in session 7's homework. Spotify allows itself up to 30 days to send it
(reports range from a few hours to two weeks), so check your email now.

- **Not requested yet?** Do it today: spotify.com in a browser, **Account**, **Privacy
  settings**, **Download your data**, tick **Extended streaming history** only, confirm from
  the email. Then plan the project on other data, and swap the export in when it arrives.
- **Arrived?** Unzip it into `project/data/spotify/`. It is JSON, not CSV, and it has no
  genre field. `sessions/session-08/notebooks/08-spotify-exercise.ipynb` loads it, on a
  practice export first, so you can rehearse while you wait.

## 4. The output

One output: a file the pipeline writes into `project/output/`.

> **Must output:** ...

## 5. Must, should, could, won't

**Must** is the smallest thing that answers the question. If only this gets done, the
project still succeeded. **Should** is what makes it good (usually the chart). **Could** is
for if things go unexpectedly well. **Won't (this time)** is the list of good ideas you are
deliberately not doing, written down so they stop nagging.

| | What | Honest estimate |
|---|---|---|
| Must | | |
| Should | | |
| Could | | |
| Won't (this time) | | |
| Won't (this time) | | |

Add up must and should. If it is more than about six hours, move something down a row. Your
estimates will be optimistic; everybody's are.

## 6. The one-number test

Can you get a rough version of the must answer in about **fifteen lines**, today, in a
notebook? If yes, the plan is real. If you cannot even say what the number would be, the
question is not ready, and it is much better to find that out now than in session 8.

1. Put your file in `project/data/`, and point `INPUT` at the top of `project/pipeline.py`
   at it.
2. Open `project/notebooks/explore.ipynb` and run sections 1 and 2: rows, columns, types,
   missing values. Sections 3 and 4 will fail on your data; that is session 8's work.
3. In its scratch space, get your one number. `notebooks/01-one-number-test.ipynb` in this
   session's folder does all of this on the worked example, `first_look` function included.
4. Check it a second way: the parts add up to the whole, or one value worked out with a
   filter instead of a `groupby`.

> **My one number:** ...
>
> **Checked by:** ...

The first number usually shows a decision your question was quietly making. In the worked
example, total listening *fell*, so "which genre shrank most" depends on whether you mean
minutes or share. Neither is wrong. Write yours under section 8.

## 7. What the data looks like

From the first look.

- Rows and columns:
- Columns that are not the type you expected:
- Missing values in columns you need:
- Date range, and does it cover the question:
- Anything else that surprised you:

## 8. Decisions

Every choice that changes the answer (missing values, rows dropped, what counts as one
"play" or "sale", duplicates): what you did, how many rows it touched, and why. This list
keeps growing in session 8 and after.

1. ...

## 9. Private data

Everything in `project/data/` except its README is ignored by git, so a file kept there never
reaches GitHub. Check it before your first commit:

```
git check-ignore -v project/data/my_export.csv
git status
```

The first prints the `.gitignore` rule that hides the file; the second should not list it. A
data file anywhere else in the repository *will* be committed by `git add .`. A Spotify
export contains IP addresses; keep it in `project/data/`.

## 10. The scope check

- [ ] One question, one dataset, one output
- [ ] I can say what "done" means in one sentence
- [ ] My data is on my laptop, in `project/data/`
- [ ] The one-number test passed, and the number is checked a second way
- [ ] Must plus should is about six hours or less
- [ ] I know which parts of the data are private, and they stay in `project/data/`

If a box stays empty, send a message before session 8 rather than arriving with it. Scope
and data problems are cheap to fix by message and expensive to fix in the session.
