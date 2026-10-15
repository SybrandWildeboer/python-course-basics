# Worked example: a scoped project on the music data

The scoping worksheet filled in for a project on the course's own listening log, the way it
should look when you arrive at session 8. Every number comes from
`notebooks/01-one-number-test.ipynb`, which computes and checks them.

It starts with the first draft, because the first draft is the useful part. Nobody's first
draft is scoped.

---

## The first draft (before scoping)

> "I want to analyse my listening habits: which artists and genres I like, how it changes
> over time, whether I skip more on my phone, what time of day I listen, and maybe predict
> what I will like next. With a dashboard."

Five questions, at least three outputs, and one of them ("predict what I will like") is a
research project. Every part is interesting, and that is exactly the problem: there is no
point at which it is finished. The scoping below keeps the one question that came from a real
repeated task, and moves everything else to *could* or *won't*.

---

## 1. The task

> Every January I export last year's listening into a spreadsheet, paste it next to the year
> before, and build a pivot table of minutes per genre for each year. Then I work out by hand
> which genres went up and which went down. It takes about an hour, and I get a formula wrong
> about one year in two.

The answer I am after: which genres I am listening to more, and which less, than the year
before.

## 2. The question

> **Question:** Which genres did I listen to more in 2025 than in 2024, and which less?

What the answer looks like: "Jazz grew most, by 54.0 minutes. Electronic shrank most, by
106.1 minutes." Plus the same for every genre in a small table. "Done" is that table, written
by the pipeline.

## 3. The data

| | |
|---|---|
| What file or files | `data/clean/plays.csv` |
| Where it comes from | the listening log, one row per play |
| Roughly how many rows | 2,183 |
| Is it on your laptop today? | yes |
| Which columns the question needs | `played_at`, `genre`, `minutes_played` (plus `play_id` to check for duplicates) |
| Is any of it private? | no: it is generated data. A Spotify export would be |

## 4. The output

> **Must output:** `project/output/summary.csv`: one row per genre, with the minutes in 2024,
> the minutes in 2025, and the change, smallest change first.

## 5. Must, should, could, won't

| | What | Honest estimate |
|---|---|---|
| Must | The genre change table, written by `project/pipeline.py`, with logged cleaning and checks | 2 hours |
| Should | One bar chart of the change per genre, the answer in the title, saved by the pipeline | 1 hour |
| Could | The same comparison as **share** of each year's listening | 30 minutes |
| Won't (this time) | Skips by device, time of day, per-artist breakdowns | |
| Won't (this time) | Predicting what I will like next; a dashboard | |

Must plus should: about three hours, comfortably inside six. On real data, expect the must
line to take twice as long as it does here.

## 6. The one-number test

Five lines of `groupby` and `unstack`, fifteen with the checks:

```python
plays["year"] = plays["played_at"].str[:4]
table = plays.groupby(["genre", "year"])["minutes_played"].sum().unstack("year").round(1)
table["change"] = (table["2025"] - table["2024"]).round(1)
table.sort_values("change")
```

> **My one number:** Jazz grew most (+54.0 minutes), Electronic shrank most (−106.1).
>
> **Checked by:** the table adds up to 8,980.5 minutes against 8,980.4 in the raw data. The
> table rounded sixteen cells, so a tenth is rounding; two hundred would be a bug.

## 7. What the data looks like

- Rows and columns: 2,183 rows, 9 columns.
- Columns that are not the type you expected: `played_at` is text. Fine: the year is the
  first four characters.
- Missing values in columns you need: none.
- Date range: 2024-01-01 to 2025-12-31. Two complete years, so the comparison is fair.
- Surprise: total listening **fell**, from 4,596.6 minutes in 2024 to 4,383.8 in 2025 (down
  212.8). So part of every genre's "loss" is just listening less overall. That led to
  decision 2.

## 8. Decisions

1. **Skipped plays are kept.** A skipped play still has the minutes actually played, and the
   question is about minutes listened. Rows dropped: none.
2. **Minutes, not share.** By minutes, Electronic shrank most (−106.1). By share of each
   year's listening, Folk shrank most (−1.5 percentage points, from 18.1% to 16.6%). Jazz
   grew most either way. The question says "listened to more", which is minutes, so the must
   uses minutes and the share version is a *could*. The project README mentions both,
   because a listener could reasonably have meant either.

## 9. Private data

Nothing private. A real export would stay in `project/data/`.

## 10. The scope check

- [x] One question, one dataset, one output
- [x] I can say what "done" means in one sentence
- [x] My data is on my laptop
- [x] The one-number test passed, and the number is checked a second way
- [x] Must plus should is about six hours or less: about three
- [x] I know which parts of the data are private: none, here

---

## What made this scoping work

- **It started from a task that really repeats.** That gave a question with a natural "done":
  the table I used to build by hand.
- **The won't list is long.** Every item on it is a good idea. Writing them down is what made
  it possible to stop thinking about them.
- **The first number came before the plan was final.** The one-number test found the falling
  total, and the falling total found decision 2. Neither would have shown up in a plan made
  without looking at the data.
