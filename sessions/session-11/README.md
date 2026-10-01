# Session 11: Project scoping and setup

**Goal:** a question small enough to finish, written down with its must, should and could,
and their own data running through `project/pipeline.py` before they leave. Rough is fine.
Running is not optional.

**Slides:** [`slides/session-11.html`](../../slides/session-11.html) (20 slides)

> **Tell him about Spotify in session 10, not in this one.** If there is any chance the
> project will use his own Spotify listening history, the *Extended streaming history* has to
> be requested a week or more ahead: Spotify allows itself up to 30 days, and reports range
> from a few hours to two weeks. Mention it at the end of session 10 (or by message straight
> after it). If he requests it today instead, the first run uses other data and the export is
> swapped in when it arrives. Details under [The Spotify route](#the-spotify-route).

---

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00–0:10 | Homework review: the month question, and the fresh-terminal run | Slide 2 |
| 0:10–0:20 | From the session 1 task to a question, and what a good one looks like | Slides 4–5 |
| 0:20–0:45 | One, one, one; must / should / could / won't; the worked example; **the one-number test and the decision it finds** | Slides 6–10 |
| 0:45–1:05 | Live exercise part 1: the worksheet, sections 1 to 5 | Slide 11 |
| 1:05–1:15 | Break | |
| 1:15–1:30 | Milestones, the first run, the Spotify route, private data | Slides 13–17 |
| 1:30–1:55 | **Live exercise part 2: the first run.** Protect this | Slide 18 |
| 1:55–2:00 | Homework (milestone 1), agree the date of session 12 | Slides 19–20 |

If anything runs long, cut the Spotify slides (16 is in the stretch notebook anyway) and keep
the first run. A learner who leaves with a plan but no run has to start the hardest part
alone; a learner who leaves with a rough run only has to improve it.

## The slides that carry the session

**Slide 4, from task to question.** The step that matters is the second card: the *answer*
the task is after, not its steps. Describing steps produces a script that copies cells around;
describing the answer produces a question with a natural "done". You wrote his task down in
session 1. Read it back to him.

**Slide 9, the one-number test.** Can he get a rough version of the must answer in about
fifteen lines, today? It decides whether the plan is real. On the worked example it is five
lines of `groupby` and `unstack`.

**Slide 10, the hidden decision.** The one-number test found that total listening *fell*
(4,596.6 to 4,383.8 minutes), so "which genre shrank most" depends on whether you mean
minutes (Electronic, −106.1) or share of the year (Folk, −1.5 points). Neither is wrong. It
goes in the worksheet under *decisions*. Slow down here: nobody would have found it from the
plan alone, and that is the whole argument for looking at the data before the plan is final.
It is session 9's lesson ("every cleaning decision changes the answer") applied to scoping.

**Slide 17, private data.** Everything in `project/data/` except its README is gitignored, so
his data stays off GitHub as long as it lives there. Check it together with
`git check-ignore -v` and `git status` before the first commit of the day. A Spotify export
contains IP addresses.

## What they use

| File | What it is |
|---|---|
| `exercises/scoping-worksheet.md` | The worksheet: task, question, data, output, must/should/could/won't, first-look notes, decisions, milestones, scope check |
| `solutions/worked-example-scope.md` | The worksheet filled in for the music data, starting from an unscoped first draft |
| `demos/one_number_test.py` | Notebook 01 as a script: first look, the table, the checks, the share decision, a chart saved to `output/session-11/` |
| `exercises/first_run.py` | Script version of the live exercise, part 2 |
| `solutions/first_run.py` | Worked version on the music data, with the expected output in a comment |
| `homework/README.md` | Milestone 1, what "done" means, and what not to commit |
| `homework/milestone_1.py` | Script version of the homework starter |
| `homework/solutions/milestone_1.py` | Worked version: logged cleaning, `find_problems`, two routes to one number |

The project itself lives in `project/` (built in session 10): `project/pipeline.py`,
`project/data/`, `project/output/`, `project/notebooks/explore.ipynb`, `project/README.md`.
Nothing in this session folder changes it. He does, today.

## Notebooks

| Notebook | What it is |
|---|---|
| `notebooks/01-scoping-a-question.ipynb` | The walkthrough: the five-minute first look, the one-number test on the worked example, the check that the table adds up, the minutes-versus-share decision, a rough chart, and the same code shaped as load / clean / analyse / save |
| `notebooks/02-first-run-exercise.ipynb` | The live exercise, part 2: read your own file (with the semicolon / decimal comma / encoding traps from Dutch Excel), first look, one number, one assert, then the six steps into `project/pipeline.py` |
| `notebooks/02-first-run-solved.ipynb` | The same done on the worked example, with the first-look notes and the pipeline steps as they actually went |
| `notebooks/03-milestone-1-homework.ipynb` | Homework: logged cleaning steps, a `find_problems` function that returns a list, the must output checked two ways, and how to move it all into the pipeline |
| `notebooks/03-milestone-1-solved.ipynb` | Worked version, including `find_problems` run on the session 9 messy file to show it failing properly (five problems, each with a count) |
| `notebooks/04-stretch-exercise.ipynb` | Optional stretch: the Spotify route, on a practice export |
| `notebooks/04-stretch-solved.ipynb` | Worked versions, with the reasoning written out |

Every notebook starts with the cell that walks up to the repository root. Notebooks 01 to 03
use the music data as a stand-in for "my own file"; the exercise versions point at
`project/data/`.

## Before the session

- [ ] Check `python project/pipeline.py` runs on a clean checkout, from the repo root, with
      `.venv` active
- [ ] Find the repetitive task he named in session 1, and have it on screen for slide 4
- [ ] Ask him to bring the data for that task (a CSV or Excel file, on his laptop). If it lives
      on a work machine, agree beforehand what can be exported, and what is private
- [ ] Ask whether he requested the Spotify export after session 10, and whether it has arrived
- [ ] Decide the date of session 12; two weeks out is comfortable (see Milestones below)

## Milestones and the date of session 12

The plan assumes a two-week gap before session 12: milestone 1 (the homework) in week one,
milestones 2 and 3 in week two. If session 12 has to be one week away, the homework becomes
milestones 1 and 2, the could list is cut entirely, and milestone 3 is the evening before.
Say which plan you are on before he leaves, because it changes how much he should attempt.

A short message mid-way (after milestone 1) is worth arranging: "send me the output of
`python project/pipeline.py`". It catches a stalled project while there is time to rescue it.

## The Spotify route

The ambitious option, and a good one for him: it is his own data, it is large (years of
listening), and the questions are ones he will care about. The cost is the wait, a JSON format
he has not met, and some decisions the course data never needed.

**Requesting it** (slide 15): on a computer, spotify.com, **Account privacy**, **Download your
data**, tick **Extended streaming history** only (the "Account data" option gives one year,
with fewer fields), confirm from the email, wait for a second email with a ZIP.

**What arrives:** the whole history since the account began, as JSON files named like
`Streaming_History_Audio_2024_0.json` (split at roughly 12 MB each), plus a *Read Me First -
Extended Streaming History* file describing every field.

**The fields this course uses**, and what Spotify says they hold:

| Field | Meaning |
|---|---|
| `ts` | date and time the stream **ended**, in UTC |
| `ms_played` | milliseconds played |
| `master_metadata_track_name` | track name (empty for podcasts) |
| `master_metadata_album_artist_name` | artist name |
| `master_metadata_album_album_name` | album name |
| `spotify_track_uri` | unique track identifier |
| `episode_name`, `episode_show_name` | podcast episode and show (empty for music) |
| `platform` | device or app used |
| `conn_country` | country where **he** was when streaming, not the artist's |
| `reason_start`, `reason_end` | why the stream started and ended |
| `shuffle`, `skipped`, `offline`, `incognito_mode` | true/false flags |

**Loading it:** `pd.read_json(path)` per file, `pd.concat(..., ignore_index=True)`, then
`pd.to_datetime(streams["ts"], utc=True)`. The stretch notebook does all of it on a practice
export it generates itself, so the route can be rehearsed before the data arrives.

**What was verified, and what was not** (checked October 2026):

- Spotify's support article *Understanding my data* describes the 21 data elements of the
  extended history (end time in UTC, milliseconds played, track, artist, album, track URI,
  episode and show, platform, country, IP address, user agent, start and end reasons,
  shuffle, skipped, offline, offline timestamp, private session) and says the files are JSON.
  It does **not** give the technical field names; it refers to the *Read Me First* file.
- The field names above are the ones published from real exports (for example
  blog.ortham.net, December 2024, which lists `ts`, `platform`, `ms_played`, `conn_country`,
  `ip_addr`, the `master_metadata_*` fields, `spotify_track_uri`, `episode_name`,
  `episode_show_name`, `spotify_episode_uri`, `reason_start`, `reason_end`, `shuffle`,
  `skipped`, `offline`, `offline_timestamp` and `incognito_mode`). Older exports are reported
  to have had extra or differently named fields (a username, and IP and user-agent fields).
  The course deliberately uses none of the identifying ones.
- The `Streaming_History_Audio_*.json` file pattern is from several published guides and tools.
  Some exports are reported to contain other files beside the audio ones; the pattern picks
  only audio, on purpose.
- The request steps are from Spotify's support pages and published guides. The account page
  itself could not be checked without logging in, so menu names may differ slightly.
- The waiting time: Spotify's page states up to 30 days (the GDPR limit). Published reports
  range from about four hours to two weeks.
- Not verified: the exact `platform`, `reason_start` and `reason_end` values. The practice
  export uses plausible ones (`android`, `trackdone`, `fwdbtn`...). He checks his own with
  `value_counts(dropna=False)`.
- There is **no genre field**. A Spotify project asks about artists, tracks, time and devices.
  Genres would need the Spotify Web API (an account, keys, many requests): a "won't, this
  time".

**The rule that protects the project:** he checks the field names against his own *Read Me
First* file and `df.columns` before trusting anything in the notebook. If a name differs, the
logic stays the same and only the name changes.

## If there is time left

The stretch notebook is the Spotify route, rehearsed on a practice export with the real file
and field names and made-up values. It is for when the first run finishes early, and it is
the head start for anyone whose project will use the real export. Six stretches, each adding
one idea:

| # | Stretch | What it adds |
|---|---|---|
| 1 | A JSON file is a list of dictionaries | `json.load`, then `pd.read_json`: the session 4 shape, again. `ts` arrives as text and `skipped` as `float64` |
| 2 | All the files at once | `Path.glob`, `pd.concat`, and why file names (`2024-2025_1` sorts before `2024_0`) must not decide the row order |
| 3 | What time was it, really? | `to_datetime(utc=True)` and `tz_convert("Europe/Amsterdam")`: 35 of 600 streams change date; `ts` is the *end* of the stream |
| 4 | Music or podcast? | 556 music and 44 podcast streams, and the podcasts carry more minutes |
| 5 | What counts as a play? | Top artist by streams is Glass Tram counting everything and DJ Kompas counting 30 seconds or more; 123 missing `skipped` values to decide about |
| 6 | Into the shape of the course data | `spotify_to_plays`: course column names, so the pipeline's analysis can be reused; and the discovery that there is no genre |

Number 5 is the one to talk through rather than just check. The same file gives a different
winner depending on what a "play" is, which is session 9's lesson in a form he will meet in
real work. Number 6's "no genre" moment is the other one: it is a scoping fact, and finding it
in a stretch is much cheaper than finding it in week two.

## Watch out for

- **The project that will not stop growing.** Every "and also" goes on the could or won't
  list, out loud, while he watches. Writing it down is what lets him let go of it.
- **Data he does not have yet.** "Once I get the data" is the most common way a project dies.
  If it is not on his laptop today, the first run uses data that is, and the real file is
  swapped in later.
- **A file that reads without an error but wrongly.** Dutch Excel saves CSVs with `;` and
  decimal commas, and `read_csv` happily produces one column. The first look catches it; the
  notebook demonstrates it.
- **Excel files.** `pd.read_excel` needs `openpyxl`, which is not in
  `project/requirements.txt`. For today, *Save As CSV*. If the project needs the `.xlsx`,
  install `openpyxl` into the project venv and add it to `requirements.txt`.
- **`save_csv` dropping the labels.** It writes with `index=False`, so an `analyse` that ends
  with the labels in the index loses them silently. `.reset_index()` at the end of `analyse`.
- **`check` and `save_chart` expecting the music columns.** They will fail on his table.
  Rename the columns or comment the calls out with a `TODO`; milestone 1 and 2 bring them back.
- **Changing everything at once.** Six steps, a run after each. When it breaks, the last step
  is the culprit.
- **`git add .` with private data in `project/data/`.** Slide 17, before the first commit.
- **Underestimating.** His estimates will be optimistic; everybody's are. If must plus should
  comes to six hours on paper, it is probably nine. That is why the limit is six.

## Definition of done

A filled-in worksheet with one question, one dataset, one output and a must / should / could /
won't table; `python project/pipeline.py` has run on his own data (or a stand-in with the
same shape) and written a rough must output to `project/output/`; private data is ignored;
the worksheet and pipeline are committed and pushed; and the date of session 12 is agreed.
