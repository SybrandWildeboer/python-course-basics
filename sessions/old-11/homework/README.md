# Session 11 homework: milestone 1

Budget: 2 to 4 hours. **Saturday:** one line, `Milestone 1 done` or `Milestone 1 not done`,
and if not, which part stopped you.

Today ended with a rough first run of `project/pipeline.py` on your own data. Milestone 1
makes the first two stages of that pipeline honest: you know which rows went in, which came
out and why, and a set of checks says so every time it runs.

Work it out in `notebooks/03-milestone-1-homework.ipynb` (or `milestone_1.py`, the script
version), then move it into `project/pipeline.py`. Run everything from the repository root,
with the project's virtual environment active:

```
python project/pipeline.py
```

---

## Milestone 1 is done when

1. **Cleaning is logged.** Each cleaning step is its own small function that returns a
   DataFrame, and the pipeline prints one line per step with the rows before and after.
2. **`find_problems` finds nothing.** A function that returns a list of everything wrong with
   the cleaned data, as sentences. The pipeline stops, with that list, if it is not empty:

   ```python
   problems = find_problems(cleaned)
   assert not problems, problems
   ```

3. **The must output is checked two ways.** `analyse` returns the must output from your
   worksheet, and one number in it is confirmed by a different route: the parts add up to the
   whole, or one cell worked out with a filter instead of a `groupby`.
4. **It runs start to finish.** `python project/pipeline.py` prints the log, passes the
   checks, and writes the output into `project/output/`.
5. **Your decisions are written down.** Section 7 of your scoping worksheet lists each cleaning
   decision, how many rows it touched, and why.
6. **It is committed and pushed.** Your code and worksheet, not your data (see below).

## Before you `git add`

Look at `git status` before every commit this week. Everything in `project/data/` except its
README is gitignored, so a data file kept there will not appear. A data file anywhere else
will.

- If the data is **private** (anything about money, other people, or an export like Spotify's,
  which contains IP addresses), keep it in `project/data/` and do not commit it. Check with:

  ```
  git check-ignore -v project/data/my_export.csv
  ```

  which prints the `.gitignore` rule that hides it.
- If it is **not private** and small (a few MB at most), committing it is fine, and it means
  the project runs for anyone who clones it. Add it on purpose with
  `git add -f project/data/my_export.csv`.
- If you are unsure, do not commit it. Adding a file later is easy. Removing one from the
  history once it has been pushed is not.

## Watch out for

- **Cleaning that quietly drops half the data.** That is what the log is for. Read it every
  run, and if a step drops more than you expected, stop and find out why before going on.
- **Checks that cannot fail.** Run `find_problems` on the *raw* data once. If it finds nothing
  there either, it is not looking hard enough.
- **Scope creep.** You will have a good new idea this week. Write it on the *could* or *won't*
  list and carry on with the must. The idea will still be there in session 12.

---

## If you have time left

Start milestone 2, the **should** item on your worksheet. For most projects that is the chart:
one chart, one question, the answer in the title, labels with `:.1f`, saved as a PNG into
`project/output/` by the pipeline. Session 9 has all the pieces.

If your project is the Spotify route and the export has arrived, work through
`notebooks/04-stretch-exercise.ipynb` first: it turns the export into the shape the pipeline
already understands.
