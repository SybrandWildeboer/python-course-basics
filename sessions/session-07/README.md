# Session 7: Data visualization

**Goal:** one question, one chart, and a reader who gets the answer without you in the room.
By the end they can pick the chart from the kind of question, keep it honest, point the
reader at what matters, and rebuild a bad chart while saying why at every step.

**Slides:** [`slides/session-07.html`](../../slides/session-07.html) (24 slides)

Two halves. The first is one chart at a time: how a figure is built, which chart for which
question, and the ways a chart misleads with every number right. The second is what real
questions need: time on the x-axis, eight groups at once, the one line that matters, colour
for every reader, and a figure fit to hand to someone. The makeover ties both together. If
you run short, shorten the colour slide and the four-panel figure, **never the honest axes,
"out of what", or the makeover**.

---

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00–0:10 | Homework review: session 6's pandas answers and the decision diary | Slide 2 |
| 0:10–0:20 | The anatomy of a figure: `fig` and `ax`, `plt.` against `ax.`, pandas `.plot()` | Slides 3–5 |
| 0:20–0:50 | One question, one chart: answer titles, choosing the chart, bar or line, **honest axes, out of what**, scatter, why not a pie, saving | Slides 6–13 |
| 0:50–1:00 | Break | |
| 1:00–1:25 | Real dates and annotations, small multiples, highlighting, colour | Slides 14–18 |
| 1:25–1:30 | One figure, four panels, ready to share | Slide 19 |
| 1:30–1:50 | **Live exercise: the chart makeover** | Slides 20–21 |
| 1:50–2:00 | Homework briefing, and the part to do before session 8 | Slides 22–24 |

Notebook 01 carries the first hour, notebook 02 the half hour after the break, and
notebook 03 the makeover.

## The slides that carry the session

**Slide 9, honest axes.** The same skip rates, 14.0% for speaker and 10.6% for car, drawn
from 10% and from zero. The zoomed one needed `set_ylim(10, 14.5)` to do the damage, so the
lie takes effort. Out of 336 speaker plays, the difference is about eleven skips.

**Slide 10, "out of what?".** The stacked histogram: the same 190 short skips are 73.6% of
the 258 skips and 84.4% of the 225 short plays. Move the line for "short" to two minutes and
it is 98.4% against 65.0%, the other way round. Read the two sentences aloud, "most skips
are short" and "most short plays are skips", and ask which one the title makes.

**Slide 11, what this does not show.** The scatter: Sara Lindqvist has the most plays
(242), Glass Tram the most minutes (1,175.1), because a Glass Tram play lasts 5.1 minutes
against 3.2. The chart shows *that*, not *why*. From here on every chart ends with that
sentence, and the homework asks for it.

**Slides 16 and 17, small multiples and highlighting.** Plays per quarter for eight genres:
first as spaghetti, then as a 2-by-4 grid with `sharey=True` (without it Rock, never above
24, looks as big as Electronic, never below 47), then as one chart with seven grey lines and
Folk in colour: 236 plays in 2024, 202 in 2025, and spring 2025 at 39 against 58.

**Slides 20 and 21, the makeover.** Two lines through alphabetical genres in red and green,
the axis from 55, titled "Genre data". The step that unlocks it is seeing that the question
is about **change**, so the chart should show the change: Afrobeat +16.9%, Folk -14.4%, and
only Afrobeat and Jazz grew. Then what it does not show: all listening fell 5.4% (1,122 to
1,061 plays), so Electronic (-3.9%) and Indie (-4.0%) actually gained share. With the overall
change as a dashed line, the title becomes "4 of 8 genres fell less than listening as a
whole". Two true titles for one chart; the question decides.

## Promises this session keeps

- **Session 1:** `:.1f` "comes back for chart labels". Slide 6, in the title f-string and in
  `ax.bar_label(bars, fmt="{:.1f}")`, and again as `:+.1f` in the makeover.
- **Session 4:** the homework's "highest average, not highest total" question is the first
  chart, and the scatter draws the same total-versus-average lesson.
- **Session 6:** the monthly tables built with `resample` and `pivot_table` are what part two
  plots, and the stretch draws what `format="mixed"` does to the dates.

## What they use

| File | What it is |
|---|---|
| `demos/charts.py` | Walkthrough part one as a script: five charts saved to `output/` |
| `demos/time_and_panels.py` | Walkthrough part two: the annotated line, small multiples, the highlighted line, the four-panel figure |
| `exercises/makeover.py` | The live exercise starter: draws the bad chart, steps listed at the top |
| `solutions/makeover.py` | Worked makeover, both titles, with the asserts |
| `homework/README.md` | The two chart tasks and the before-session-8 part |
| `homework/my_chart.py`, `homework/makeover.py` | Homework starters |
| `homework/solutions/` | Both answers, with the reasoning in comments |

Everything reads the clean CSVs in `data/clean/`, so the charts never wait on cleaning. The
one exception is the worked homework, which reads the messy file only to find which 94 plays
had no minutes. Scripts save charts rather than showing them: `plt.show()` in a script opens
a window and stops until it is closed. Every PNG goes into `output/`, which git ignores.

## Notebooks

| Notebook | What it is |
|---|---|
| `notebooks/01-charts.ipynb` | Part one: `fig` and `ax`, `plt.` against `ax.`, pandas `.plot()`, answer titles and `:.1f`, the five kinds of question, bar or line, the misleading axis, histogram and "out of what", scatter, why not a pie, saving, the checklist |
| `notebooks/02-time-and-panels.ipynb` | Part two: real dates, `axhline`, `axvspan` and `annotate`, two years on one axis, spaghetti and small multiples, highlighting, colour and the greyscale test, the four-panel figure |
| `notebooks/03-makeover-exercise.ipynb` | The live exercise: a bad chart and ten steps |
| `notebooks/03-makeover-solved.ipynb` | Worked version, with why at every step |
| `notebooks/04-my-chart-homework.ipynb` | The homework: one chart of their own, and the device-pie makeover |
| `notebooks/04-my-chart-solved.ipynb` | Worked versions: "edged out", and a dumbbell chart |
| `notebooks/05-stretch-exercise.ipynb` | Optional stretch exercises, for when the makeover finishes early |
| `notebooks/05-stretch-solved.ipynb` | Worked versions, with the reasoning written out |

## Before the session

- [ ] Check the dataset is generated: `python data/scripts/build_dataset.py`
- [ ] Run `notebooks/01-charts.ipynb` once, so matplotlib has built its font cache before
  the learner watches it do so
- [ ] Check `sessions/session-08/prework/scoping-worksheet.md` exists, so the
  before-session-8 part of the homework points at something real
- [ ] Optional: `pip install seaborn` on the learner's machine, if you expect to reach
  stretch 6

## If there is time left

The stretch notebook has six exercises that get harder as you go. Use as many as the time
allows; you don't need to finish it. None of them repeat the walkthrough, the exercise or the
homework, and each one adds one idea:

| # | Exercise | What it adds |
|---|---|---|
| 1 | An honest skip-rate chart | `barh` with `"15.6% of 154"` labels built with `zip`; is the winner a finding or chance? |
| 2 | Draw the wrong dates | Two lines on one `ax` with a legend: `format="mixed"` on the messy file moves 158 plays |
| 3 | A slope chart | Two points per genre, grey for context, direct labels for the two that matter |
| 4 | Noise and a rolling average | `resample("W")`, a partial last week to drop, `.rolling(4).mean()` over a grey line |
| 5 | A heatmap | `imshow` with `"Blues"`, a colour bar, numbers in the cells: day of week against month |
| 6 | The same small multiples in seaborn | `sns.relplot` with `col=`, long data; needs `pip install seaborn` |

Numbers 1 and 4 are the ones to talk through rather than just check. In 1, Jazz is skipped
most, 24 of 154 plays, where the overall 11.8% would predict 18.2: about six skips, the
kind of gap chance makes all the time. Ask what the title should say now. In 4, the last
`resample("W")` week runs to 4 January 2026 and holds only three days of data; left in, it is
a fake drop at the end of the chart. And the smooth line hides the single quietest week (8
plays) inside the quietest stretch (12.0 a week, July 2025): smoothing is a choice.

## Watch out for

- **`plt.` and `ax.` mixed in one chart.** It works until there are two charts, then the
  `plt.` lines land on whichever was made last. Translate online answers to `ax.` as you
  paste them.
- **Lines through categories.** `per_year.plot()` on a table with genres in the index draws
  exactly the makeover's bad chart. pandas draws a line unless told otherwise.
- **`set_ylim(bottom=0)` on each panel of a shared grid.** With `sharey=True`, the first
  call freezes the top at the first panel's data and the others get clipped. Set it once,
  after the loop.
- **Day or month names in alphabetical order.** `groupby(...dt.day_name())` puts Friday
  first. Sort by `dt.dayofweek`, or `reindex` with the names in order.
- **`plt.savefig` after `plt.show()`.** Blank PNG in a script. Save first.
- **A percentage without its "out of what".** Slide 10, and again in the makeover: down in
  plays and down in share are different claims.
- **A legend for two lines.** Label the line ends instead. A legend is the reader looking
  away from the data.
- **A colour per bar "to look nice".** Colour should mean one thing; otherwise it makes the
  reader look for a meaning that is not there.

## Definition of done

They can say which of the five kinds a question is and draw the chart for it, with a title
that gives the answer, an honest axis and a "what this does not show" sentence. They have
rebuilt the makeover chart and can explain each step, and they know what to do before
session 8, including the Spotify request if they want their own data.
