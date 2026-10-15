# Session 12 homework: the week after the course

Budget: 2 to 4 hours, in the week after the last session. **When you are done:** send one
line, the link to your pushed project.

There is no session 13 to bring this to, which is exactly why it is worth doing. The course
ends; the habit of finishing things properly does not have to.

---

## Task 1: Put your project in shape

Everything here happens in `project/`, in your own repository.

1. **Tests.** Copy `homework/test_pipeline_starter.py` to `project/test_pipeline.py`, delete
   the two `sys.path` lines, and point the import at your own functions. Write at least five
   tests:
   - one for each cleaning decision written in your `clean()` docstring,
   - one for `analyse()`, on three or four rows you build by hand, where you know the right
     answer without a calculator,
   - one that checks an error **does** happen: `load()` on a file that is not there,
   - one on your real data, checking a number you have verified some other way.

   Install pytest into the project's virtual environment, add `pytest` to
   `project/requirements.txt`, and run `python -m pytest` from inside `project/`.

2. **One specific `except`.** In `main()`, catch `FileNotFoundError` around the load, and
   stop with a message that says which file it looked for and what to check:

   ```python
   try:
       raw = load(INPUT)
   except FileNotFoundError:
       raise SystemExit(f"No file at {INPUT}. Put your data in project/data/ first.")
   ```

   Nowhere else. Do not wrap `clean()` or `analyse()`: if they crash, that is a bug to fix,
   not a situation to handle.

3. **The README.** `project/README.md` should answer four things for a stranger: the
   question, the data (where it came from, and how to get it if it is not in the repo), how
   to run it, and what you found. Then fill in its last two headings, **What this does not
   show** and **Cleaning decisions**: the limits of the answer, and what you dropped, filled
   or labelled. Two or three sentences each.

4. **Review your own diff.** Before the last commit, run `git diff` and go through
   `worksheets/review-checklist.md` as if somebody else had written the change. Fix what you
   find. Then commit, and push.

## Task 2: Your two first steps

At the end of the session you wrote two concrete first steps into
`worksheets/where-next.md`. Do the first one. Not all of it: the first two hours of it.

If you get stuck, the most useful thing you can send is not "it does not work" but the
command you ran, the last line of the error, and what you expected instead. That habit
alone puts you ahead of most people who write code for a living.

---

## The one thing to check before you send the link

Clone your own repository into a new folder, make a fresh virtual environment, install from
`requirements.txt`, and run the pipeline and the tests. If it only works on the laptop it was
written on, it does not work yet.

If your data is private and not committed (session 11's homework), the pipeline will stop at
the load in the fresh clone. That is fine, and it is exactly what your new `except` is for:
check that the message it prints tells a stranger what to do.

```
git clone https://github.com/YOUR-NAME/python-course.git check-it
cd check-it
python -m venv .venv
.venv\Scripts\activate              (Windows)
source .venv/bin/activate           (macOS)
python -m pip install -r project/requirements.txt
python project/pipeline.py
cd project
python -m pytest
```
