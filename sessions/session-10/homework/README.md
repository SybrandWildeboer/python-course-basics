# Session 10 homework

Budget: 2 to 4 hours. **Saturday:** one line, `Homework done` or `Homework not done`.

Do task 3 first. It takes five minutes, and the waiting starts when you do it.

---

## Task 1: Give the pipeline a second question

`pipeline.py` in this folder is today's genre pipeline. Add a second question to it:
**how did my listening change, month by month?**

```
python sessions/session-10/homework/pipeline.py
```

The rule: **do not touch `load_messy` or `clean_plays`.** If the pipeline is built well, a
new question needs only:

1. `minutes_by_month(plays)`, which returns one row per month (`"2024-01"` to `"2025-12"`)
   with the plays and the minutes,
2. `save_month_chart(months, path)`, which draws it as a **line** chart titled with the
   busiest month, and saves a PNG,
3. `check_months(path, plays)`, which reads the CSV back and checks there are 24 rows and
   that the plays add up to every cleaned play,
4. a few lines in `main()` that call them. Save the table with the `save_csv` you already
   have.

The `TODO` markers in the file show where each piece goes. If you would rather work it out
in a notebook first, `notebooks/03-monthly-homework.ipynb` imports today's pipeline and has
the checks ready.

When it runs, look at the chart and write one sentence about what it shows, as a comment at
the bottom of the file.

## Task 2: Your project, in its own environment

The `project/` folder at the repository root is the scaffold for your final project. Make
it run in its own virtual environment, following `project/README.md`:

1. create `.venv` inside `project/`, activate it, and `pip install -r requirements.txt`,
2. run `python pipeline.py` and open the chart it writes in `project/output/`,
3. run `git status` and check that neither `.venv/` nor `output/` appears. If either does,
   stop and ask.

Then bring one real file of your own. In session 1 you named a repetitive spreadsheet task
from your own week. Export that spreadsheet as a CSV, put it in `project/data/`, and point
`INPUT` in `pipeline.py` at it. Files in `project/data/` are not committed (git ignores
everything there except the README), so private data stays on your laptop. If it is an
Excel file, saving it as CSV is simplest: `pd.read_excel` needs an extra package,
`openpyxl`, which is not in `requirements.txt`.

Do not rewrite the pipeline yet. Get as far as this:

- run sections 1 and 2 of `project/notebooks/explore.ipynb` on your file, so `load` works
  and you can see the columns,
- write down, in the markdown cell there, every problem you can see in the data.

The pipeline itself will fail at `clean`, because that is still written for the music data.
That is expected, and it is where session 11 starts.

## Task 3: Request your Spotify data (five minutes, do it first)

If you use Spotify, your own listening history is a strong candidate for your project
dataset: the same kind of data as the course's log, but yours. It has to be requested, and
it does not arrive straight away. Spotify says the extended history can take up to 30 days,
so request it today even if you are not sure you will use it.

1. Log in at spotify.com in a browser (not the app) and open your **Account** page.
2. Go to **Privacy settings**, then **Download your data**.
3. Tick **Extended streaming history** only. The basic account data is much thinner, so
   make sure it is the extended one.
4. Confirm the request from the email Spotify sends.

The menus move around from time to time; if these names do not match exactly, look for
"Download your data". When the email with the files arrives, put them in `project/data/`.
Git ignores everything in that folder except its README, so your listening history stays
off GitHub. Session 11 offers it as an optional project dataset and covers what is inside.

If you do not use Spotify, skip this task. Your spreadsheet from task 2 is a perfectly good
project.

---

## Stretch, if you want it

Which **year** had more listening, and by how much? Answer it from the monthly table alone,
without going back to the plays. (The first four characters of `month`.)
