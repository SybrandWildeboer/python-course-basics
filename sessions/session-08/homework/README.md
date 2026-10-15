# Session 8 homework: finish the must answer

Budget: 2 to 4 hours, in the week after the last session. **When you are done:** send one
line, the link to your pushed project. If something stops you, send the command you ran, the
last line of the error, and what you expected instead.

Session 8 ended with `project/pipeline.py` running from one command, on your data, with a
rough must answer. This week makes the answer finished and trustworthy. There is no session
9 to bring it to, which is exactly why it is worth doing: the course ends, the habit of
finishing things properly does not have to.

Everything happens in `project/`, in your own repository, with the project's virtual
environment active.

---

## Task 1: The must answer, honest

Work it out in `notebooks/06-finish-the-must-homework.ipynb` (or `finish_the_must.py`, the
script version), then move it into `project/pipeline.py`. It is done when:

1. **Cleaning is logged.** Each cleaning step is its own small function that returns a
   DataFrame, and the pipeline prints one line per step with the rows before and after.
2. **`find_problems` finds nothing.** A function that returns a list of everything wrong with
   the cleaned data, as sentences, and the pipeline stops with that list if it is not empty:

   ```python
   problems = find_problems(data)
   assert not problems, problems
   ```

3. **The must answer is checked two ways.** One number in it is confirmed by a different
   route: the parts add up to the whole, or one cell worked out with a filter instead of a
   `groupby`. `check()` reads the written file back and compares.
4. **Your decisions are written down**: in `clean()`'s docstring, and in section 8 of your
   scoping worksheet, with how many rows each one touched.

`notebooks/06-finish-the-must-solved.ipynb` does all four on the worked example.

## Task 2: The project README

`project/README.md` should answer four things for a stranger: the question, the data (where
it came from, and how to get it if it is not in the repository), how to run it, and what you
found, with the number. Then fill in its last two headings, **What this does not show** and
**Cleaning decisions**: two or three sentences each. The first is the most valuable
paragraph in the project.

## Task 3: Review, run fresh, push

1. **Review your own diff.** Before the last commit, run `git diff` and go through
   `worksheets/review-checklist.md` as if somebody else had written the change. Fix what you
   find. Then commit, and push.
2. **Run it on a machine that is not quite yours.** Clone your repository into a new folder,
   make a fresh virtual environment, install from `requirements.txt`, and run the pipeline:

   ```
   git clone https://github.com/YOUR-NAME/python-course.git check-it
   cd check-it
   python -m venv .venv
   .venv\Scripts\Activate.ps1          (Windows PowerShell)
   source .venv/bin/activate           (macOS)
   python -m pip install -r project/requirements.txt
   python project/pipeline.py
   ```

   If your data is private and not committed, the fresh clone stops at the load, with the
   message from the `except FileNotFoundError` in `main()`. That is fine: check that the
   message tells a stranger what to do. If anything else breaks, the project depends on
   something that is only on your laptop. Find out what, and fix it.

---

## Optional, after the course

None of this is required. Pick what serves your project.

- **The should item**, usually the chart: one question, the answer in the title, saved by
  the pipeline into `project/output/`. Session 7 has all the pieces.
- **Tests.** Copy `test_pipeline_starter.py` to `project/test_pipeline.py`, follow the
  instructions at its top, and write at least five tests. `solutions/test_pipeline_example.py`
  has nine for the pipeline as it comes out of the box. Read `notebooks/04-pytest.ipynb` first.
- **The optional notebooks**, in order: `02-notebook-to-script` (the whole notebook-to-pipeline
  story on the music data), `03-try-except`, `04-pytest`, then `05-robust-exercise` to
  practise both. `07-stretch-exercise` adds six things a real pipeline needs.
- **The practice review.** `worksheets/practice-review.diff` is a commit with five problems
  planted in it. Find them with the checklist, then read `practice-review-answers.md`.
- **Your step 2.** `worksheets/where-next.md` is a map of where to go next. Pick one
  direction, write the first thing and a date at the bottom, and do the first two hours of it
  within two weeks.
