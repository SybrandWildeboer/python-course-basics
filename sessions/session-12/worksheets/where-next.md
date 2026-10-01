# Where to go next

A map, not a syllabus. Twelve sessions got you from nothing to a pipeline with tests that
answers a question you care about. There is no correct next step, only the next step that
serves a question you actually have.

**The rule that has worked all course:** pick a question first, then learn exactly as much of a
tool as the question needs. Learning a tool in the abstract, "I should learn APIs", is how
people spend six months on tutorials and build nothing.

---

## The map

### More pandas

**When you want it:** your questions are about one or two tables, and the hard part is
reshaping, time, or many steps of cleaning.

**What is next:** time series (`resample`, rolling averages), `pivot_table`, `melt`, and
method chaining so a long cleaning step reads top to bottom.

**Where to learn it:**
- *Python for Data Analysis*, 3rd edition, by Wes McKinney, who wrote pandas. Free to read
  online at <https://wesmckinney.com/book/>. The chapters on data cleaning and on group
  operations are the ones to read first.
- The pandas user guide, <https://pandas.pydata.org/docs/user_guide/>. Dry, complete, and the
  thing to search when you know what you want to do but not what it is called.

**First two hours:** take the date column of your project and plot one number per week
instead of per day. `resample("W")` is the tool; finding out how it works is the exercise.

### SQL in the real world

**When you want it:** the data lives in a company database, or is too big to load into
pandas comfortably.

**What is next:** a "real" database (PostgreSQL is the usual free one), window functions
(`ROW_NUMBER() OVER (...)`, running totals), and reading other people's long queries.

**Where to learn it:**
- *Select Star SQL*, <https://selectstarsql.com/>. Free, interactive, built around one real
  dataset the way this course was, and it goes further than session 7 did.
- DuckDB, <https://duckdb.org/>. A database that runs inside Python with nothing to set up,
  and can query a CSV directly. This runs as written on the course data:

  ```python
  import duckdb

  duckdb.sql("""
      SELECT genre, ROUND(SUM(minutes_played), 1) AS minutes
      FROM 'data/clean/plays.csv'
      GROUP BY genre ORDER BY minutes DESC LIMIT 3
  """).df()
  ```

  Electronic 2,874.5, Folk 1,562.2, Jazz 1,012.3: the same answer as session 6, without a
  database file. Install it with `python -m pip install duckdb`.

**First two hours:** redo two of your session 6 and 7 answers in DuckDB against the CSVs, and
check you get the same numbers.

### APIs and `requests`

**When you want it:** the data you need is on a website that offers it to programs, not as a
download: weather, exchange rates, public transport, your own accounts.

**What is next:** `requests.get(url, params=...)`, reading JSON (a dictionary of lists of
dictionaries: session 4 again), API keys kept out of git, and being polite about how often you
ask.

**Where to learn it:**
- The `requests` quickstart, <https://requests.readthedocs.io/en/latest/user/quickstart/>.
  Short, and enough for most of what you will do.
- Open-Meteo, <https://open-meteo.com/>. Free weather data, historical too, with no key and no
  sign-up, which makes it the best first API there is.
- The Spotify Web API exists, but you have to register an app and handle logins before it
  will answer. Not a first API; a fine third one.

**First two hours:** fetch the daily temperature for your city for the dates in your project,
and merge it onto your data by date. Then the obvious question: does the weather change what
you do? (Check the row count after that merge.)

### Automation and scheduling

**When you want it:** the repetitive task from session 1 should now happen without you.

**What is next:** a pipeline that takes its input path as an argument, logs to a file
instead of printing, and runs on a schedule: Task Scheduler on Windows, `cron` on macOS and
Linux, or a scheduled GitHub Actions workflow in the cloud.

**Where to learn it:**
- *Automate the Boring Stuff with Python*, by Al Sweigart, free online at
  <https://automatetheboringstuff.com/>. Spreadsheets, PDFs, email, files and folders. Exactly
  the "my own week" tasks.

**First two hours:** make your pipeline run once by double-clicking (or one command), from
any folder, and write the output with today's date in the file name. Scheduling it is then a
small step.

### Collaborating with git

**When you want it:** anybody else will ever touch your code, or you want somebody to review
it.

**What is next:** branches for every change, pull requests on GitHub, review comments, and
merge conflicts (unpleasant, survivable, and much rarer with small commits).

**Where to learn it:**
- GitHub Skills, <https://skills.github.com/>. Short guided courses that run inside a real
  repository. "Introduction to GitHub" and "Review pull requests" are the two to do.
- *Pro Git*, free at <https://git-scm.com/book/en/v2>. Chapters 2 and 3 cover everything you
  have used and branches properly.

**First two hours:** make your next project change on a branch, push it, open a pull request
on your own repository, and review it yourself with `review-checklist.md` before merging.

### Dashboards

**When you want it:** other people need to look at the answer, and change one thing (a year,
a genre) without asking you to rerun the script.

**What is next:** Streamlit, which turns a Python script into a web page with a few extra
lines. Your `analyse()` function does not change at all, which is the session 3 rule paying
out one last time.

**Where to learn it:**
- The Streamlit docs, <https://docs.streamlit.io/>. The "Get started" tutorial builds a small
  app in under an hour.

**First two hours:** a page that shows your project chart, with one dropdown that filters
the data before `analyse()` runs.

---

## Honest notes on learning resources

- **Typing beats watching.** Videos feel productive and teach less than the same hour spent
  breaking something of your own. If you watch, type along, and then change something.
- **Free is usually enough.** Everything above is free. Real Python
  (<https://realpython.com/>) has many good free articles and a paid tier; Exercism
  (<https://exercism.org/tracks/python>) has free practice problems with human mentors.
  Neither is needed before you have a question.
- **AI assistants** are good at explaining an error message and drafting code you already know
  how to check. They are confidently wrong often enough that their code needs reviewing like
  anybody else's diff: run it, read it, and go through the checklist. If you could not have
  reviewed it, you should not commit it.
- **The official documentation becomes readable** around now. The Python tutorial's chapter
  on errors and exceptions, <https://docs.python.org/3/tutorial/errors.html>, and the pytest
  getting started page, <https://docs.pytest.org/en/stable/getting-started.html>, are both
  good examples, and both cover today's material.

---

## Your two first steps

Concrete enough that you will know when each one is done. Write a date next to each.

**Step 1, this week.** Finish the homework: tests, one specific `except`, the README, a review
of your own diff, pushed. *(This one is the same for everybody.)*

Date:

**Step 2, within two weeks.** One direction from the map, applied to your own project, for
the first two hours. Write the direction and the first thing you will do:

Direction:

First thing:

Date:
