# Session 7 homework

Budget: 2 to 4 hours. **Saturday:** one line, `Homework done` or `Homework not done`.

Work in `notebooks/04-my-chart-homework.ipynb`, or in the two scripts here if you prefer.
Run scripts from the repository root, so the relative paths to `data/` work:

```
python sessions/session-07/homework/my_chart.py
```

The checklist at the end of notebook 01 is the marking scheme for both tasks. Part 3 is
different: it is the preparation for session 8, and it cannot wait until the night before.

---

## Task 1: One chart that answers one question

Pick your own question about the listening log and answer it with **one** chart. If you need
ideas: the artists with the most minutes in 2025, plays per day of the week, the countries
whose artists you play most, bands that are still active against bands that have split up
(`artists.csv` has `still_active`).

Requirements:

- the question, written as one sentence
- the right kind of chart for that kind of question: comparison, change over time,
  distribution, relationship, or part of a whole
- a title that **gives the answer**, with numbers formatted with `:.1f`
- bars that start at zero, axis labels with units
- colour that means something, and a reader who could do without it
- saved to `output/` with `fig.savefig(...)`, **before** `plt.show()`
- one sentence underneath: what you would say about it in a meeting
- one more sentence: **what this chart does not show**. Every chart answers one question,
  and readers happily take it as the answer to a nearby one. Name the nearby question yours
  does not answer

**Watch out for:** a title you cannot back up. If the top two are close, is the gap bigger
than one or two plays could change? And if you use day names, check the order they come out
in.

## Task 2: A makeover

Someone wanted to know whether the phone is losing ground to other devices, and made two
pie charts of device share, one for 2024 and one for 2025, turned a quarter apart, with
shadows, titled "Devices". `homework/makeover.py` draws them.

Rebuild it the way you rebuilt the genre chart in the live exercise:

1. list what is wrong with it, and why
2. write the question as one sentence
3. decide what number answers it, and what kind of chart shows it
4. draw it, with a title that gives the answer, and save it to
   `output/device_share_makeover.png`
5. one sentence on what your chart does not show. A share can go up while the count goes
   down. Does that happen here?

There is more than one good answer. A pie is not one of them.

---

## Part 3: Before session 8

Session 8 is your project, built together in one two-hour session. It goes well only if the
deciding is done before it starts. Do these three things this week:

1. **Fill in the scoping worksheet**,
   [`sessions/session-08/prework/scoping-worksheet.md`](../../session-08/prework/scoping-worksheet.md):
   your question, your data, and what "done" looks like. Short answers are fine; blank ones
   are not.
2. **Pick a dataset.** This listening log, a public dataset you care about, or your own data.
   Open it once, and check it has the columns your question needs.
3. **If you want to use your own Spotify data, request it now.** In Spotify, go to your
   account's privacy settings, find "Download your data", and request the **Extended
   streaming history**. It can take **up to 30 days** to arrive, so today is the day. (The
   quicker "Account data" export only covers about the last year, with less detail.) If it
   has not arrived by session 8, start on the listening log with the same question: the code
   barely changes when the file does.

---

## Stretch, if you want it

Take the chart from task 1 and make it part of a two-panel figure with
`plt.subplots(1, 2, layout="constrained")`: the answer on the left, and on the right the
chart that shows what the left one does not. One `fig.suptitle` over both, saved with
`dpi=200`.
