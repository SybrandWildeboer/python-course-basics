# Project scoping worksheet

Fill this in during session 11, in this file, and commit it. It is the plan for your project,
and it is also where your decisions get written down as you go, so you can explain every one
of them in session 12.

Short answers are better than long ones. If a section takes more than a few lines, the
project is probably still too big.

A filled-in example, scoped on the music data, is in
[`../solutions/worked-example-scope.md`](../solutions/worked-example-scope.md). Read it after
you have had a go at sections 1 and 2, not before.

---

## 1. The task you started from

In session 1 you named one repetitive thing you do in a spreadsheet. Write it down here, as it
actually happens: what you open, what you copy, what you work out, how often.

> ...

What is the *answer* you are after when you do that task? Not the steps: the thing you know
at the end that you did not know at the start.

> ...

## 2. The question

One sentence, ending in a question mark. It should be answerable with a number, a short
table, or one chart.

> **Question:** ...

What would the answer look like? Write a made-up example, so it is clear what "done" means.

> *e.g. "Category X went up by N per month; category Y went down by M."*

Why do you care about the answer? One line. (If you do not, pick another question. You will
spend four or five evenings with this one.)

> ...

## 3. The data

| | |
|---|---|
| What file or files | |
| Where it comes from | |
| Roughly how many rows | |
| Do you have it **today**? | yes / no, arrives on ... |
| Which columns the question needs | |
| Is any of it private? (names, amounts, IP addresses, anything about other people) | |

If the answer to "do you have it today" is no, the project is not ready. Either use data you
do have, or use the music data for the first run and swap your own in when it arrives.

## 4. The output

One output. A file the pipeline writes into `project/output/`.

> **Must output:** ...

## 5. Must, should, could, won't

**Must** is the smallest thing that answers the question. If only this is done in session 12,
the project still succeeded. **Should** is what makes it good. **Could** is for if things go
unexpectedly well. **Won't (this time)** is the list of good ideas you are deliberately not
doing, written down so they stop nagging.

| | What | Honest estimate |
|---|---|---|
| Must | | |
| Should | | |
| Could | | |
| Could | | |
| Won't (this time) | | |
| Won't (this time) | | |

Add up the must and should estimates. If it is more than about six hours, move something
down a row.

## 6. What the data looks like

Fill this in after the five-minute first look (notebook 02, part 1).

- Rows and columns:
- Columns that are not the type you expected:
- Missing values in columns you need:
- Date range, and does it cover the question:
- Anything else that surprised you:

## 7. Decisions

Every time you make a choice that changes the answer (what to do with missing values, which
rows to drop, what counts as one "play" or one "sale", how to treat a duplicate), write it
here: what you did, how many rows it touched, and why. Notebook 03 adds to this.

1. ...

## 8. Milestones

Agree the date of session 12 first, then fill in the dates backwards from it.

| Milestone | Done when | Date |
|---|---|---|
| 0. First run | `python project/pipeline.py` writes a rough version of the must output from your data | today |
| 1. It loads, it cleans, you can prove it | logged cleaning steps, `find_problems` finds nothing, the must output checked two ways, committed and pushed | |
| 2. The should item | usually the chart: one question, the answer in the title, saved by the pipeline | |
| 3. Ready to present | `project/README.md` says what it is and how to run it; a clean run from a fresh terminal; the ten-minute story rehearsed once out loud | the day before session 12 |

## 9. The scope check

Tick these before you leave the session.

- [ ] One question, one dataset, one output
- [ ] I have the data today, in `project/data/`
- [ ] The one-number test passed: a rough answer in about fifteen lines (notebook 02, part 2)
- [ ] Must plus should is about six hours or less, honestly estimated
- [ ] I know which parts of the data are private, and they will not be pushed
- [ ] `python project/pipeline.py` ran on my data, and the output file holds my rough number
