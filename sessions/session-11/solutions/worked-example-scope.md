# Worked example: a scoped project on the music data

This is the scoping worksheet filled in for a project on the course's own listening log, the
way it would look at the end of session 11. Every number in it comes from
`notebooks/01-scoping-a-question.ipynb` and `notebooks/03-milestone-1-solved.ipynb`, which
compute them.

It starts with the first draft, because the first draft is the useful part. Nobody's first
draft is scoped.

---

## The first draft (before scoping)

> "I want to analyse my listening habits: which artists and genres I like, how it changes
> over time, whether I skip more on my phone, what time of day I listen, and maybe predict
> what I will like next. With a dashboard."

That is five questions, at least three outputs, and one of them ("predict what I will like")
is a research project. Every part is interesting, and that is exactly the problem: there is
no point at which it is finished. The scoping below keeps the one question that came from a
real repeated task and moves everything else to *could* or *won't*.

---

## 1. The task you started from

> Every January I export last year's listening into a spreadsheet, paste it next to the year
> before, and build a pivot table of minutes per genre for each year. Then I work out by hand
> which genres went up and which went down. It takes about an hour, and I get a formula wrong
> about one year in two.

The answer I am after:

> Which genres I am listening to more, and which less, than the year before.

## 2. The question

> **Question:** Which genres did I listen to more in 2025 than in 2024, and which less?

What the answer looks like:

> "Jazz grew most, by 54.0 minutes. Electronic shrank most, by 106.1 minutes." Plus the same
> for every genre in a small table.

Why I care:

> It is the yearly task, so the script saves me an hour every January, and every year after.

## 3. The data

| | |
|---|---|
| What file or files | `data/clean/plays.csv` |
| Where it comes from | the listening log, one row per play |
| Roughly how many rows | 2,183 |
| Do you have it **today**? | yes |
| Which columns the question needs | `played_at`, `genre`, `minutes_played` (plus `play_id` to check for duplicates) |
| Is any of it private? | no: it is generated data. A real export would be (see the Spotify notes in the session README) |

## 4. The output

> **Must output:** `project/output/summary.csv`: one row per genre, with the minutes in
> 2024, the minutes in 2025, and the change, smallest change first.

## 5. Must, should, could, won't

| | What | Honest estimate |
|---|---|---|
| Must | The genre change table, written by `project/pipeline.py`, with logged cleaning and checks | 2 hours |
| Should | One bar chart of the change per genre, the answer in the title, saved as a PNG by the pipeline | 1 hour |
| Could | The same comparison as **share** of each year's listening, next to the minutes | 30 minutes |
| Could | Month by month per genre, as a line chart | 2 hours |
| Won't (this time) | Skips by device, time of day, per-artist breakdowns | |
| Won't (this time) | Predicting what I will like next | |
| Won't (this time) | A dashboard | |

Must plus should: about three hours. Comfortably inside the six-hour limit, which leaves room
for the unexpected and for presenting. On real data, expect the must line to take twice as
long as it does here.

## 6. What the data looks like

- Rows and columns: 2,183 rows, 9 columns.
- Columns that are not the type you expected: `played_at` is text. Fine: the year is the first
  four characters, and milestone 1 parses it into real dates anyway.
- Missing values in columns you need: none.
- Date range, and does it cover the question: 2024-01-01 to 2025-12-31. Two complete years,
  so the comparison is fair.
- Anything else that surprised you: total listening **fell**, from 4,596.6 minutes in 2024 to
  4,383.8 in 2025 (down 212.8). So part of every genre's "loss" is just listening less overall.
  That led to decision 3.

## 7. Decisions

1. **Skipped plays are kept.** A skipped play still has the minutes actually played, and the
   question is about minutes listened. Dropping them would answer "minutes of songs I did not
   skip", which is a different question. Rows touched: none dropped.
2. **Dates must be `YYYY-MM-DD`; anything else is dropped, not guessed.** Session 9 showed a
   guessed date can swap day and month without any error. Rows touched: 0 on this file. If it
   were hundreds, the parsing would need fixing instead, and the presentation would say so.
3. **Minutes, not share.** By minutes, Electronic shrank most (−106.1). By share of each year's
   listening, Folk shrank most (−1.5 percentage points, from 18.1% to 16.6%). Jazz grew most
   either way. The question says "listened to more", which is minutes, so the must output uses
   minutes and the share version is a *could*. Session 12 will mention both, because a listener
   could reasonably have meant either.

## 8. Milestones

| Milestone | Done when | Date |
|---|---|---|
| 0. First run | `python project/pipeline.py` writes a rough genre table | session 11 |
| 1. It loads, it cleans, you can prove it | the four logged cleaning steps, `find_problems` returns an empty list, the Jazz and Folk cells checked by a filter as well as the `groupby`, committed and pushed | end of week 1 |
| 2. The should item | the bar chart, titled "Jazz grew most from 2024 to 2025, Electronic shrank most", saved to `project/output/` | middle of week 2 |
| 3. Ready to present | `project/README.md` updated, a clean run from a fresh terminal, the story rehearsed once | the day before session 12 |

## 9. The scope check

- [x] One question, one dataset, one output
- [x] I have the data today
- [x] The one-number test passed: five lines for the table, fifteen with the checks
- [x] Must plus should is about six hours or less: about three
- [x] I know which parts of the data are private: none, here
- [x] `python project/pipeline.py` ran on the data, and the output file holds the rough table

---

## What made this scoping work

- **It started from a task that really repeats.** That gave a question with a natural "done":
  the table I used to build by hand.
- **The won't list is long.** Every item on it is a good idea. Writing them down is what made
  it possible to stop thinking about them.
- **The first number came before the plan was final.** The one-number test is what found the
  falling total, and the falling total is what found decision 3. Neither would have shown up
  in a plan made without looking at the data.
