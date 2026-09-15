# Session 9: Cleaning and visualization

**Goal:** turn a deliberately broken file into a chart that answers a question, and
understand that every cleaning step is a decision.

**Slides:** [`slides/session-09.html`](../../slides/session-09.html) (22 slides)

This is the most realistic session in the course. Say so at the start: cleaning is most of
real data work, and everything before now used clean data as a kindness.

---

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00–0:15 | Homework review: the five questions, and the awkward one | Slide 2 |
| 0:15–0:20 | Why cleaning is the job, not the detour | Slide 4 |
| 0:20–0:35 | Meet the mess, then `value_counts` on everything | Slides 5–6 |
| 0:35–0:50 | Renaming, text, types | Slides 7–8 |
| 0:50–1:00 | Break | |
| 1:00–1:20 | **The date trap**, duplicates, missing values, the `NA` trap | Slides 9–12 |
| 1:20–1:25 | Check what the cleaning threw away | Slide 13 |
| 1:25–1:45 | Figure and axes, which chart, labels, saving, misleading axes | Slides 15–19 |
| 1:45–1:55 | Clean it and chart it | Slide 20 |
| 1:55–2:00 | Homework, commit, push | Slides 21–22 |

## The slide that matters most

**Slide 9, the date trap.** The messy file has three date formats. The convenient one-liner,
`pd.to_datetime(..., format="mixed", dayfirst=True)`, runs without a word of complaint,
produces a plausible date for every row, and **silently corrupts 628 of the 2,183 rows**,
because `dayfirst=True` applies to the ISO dates too: `2025-09-06` becomes the 9th of June.

The notebook proves which version is right by cleaning the messy file and comparing it play
by play against `plays.csv`. Per-format parsing scores 100%; the convenient version scores
71%. Run that cell live.

Also worth doing live:

- **Slide 12, the `NA` trap.** 49 countries in the file are the literal text `NA`, and
  `read_csv` has already turned them into missing values without telling anyone. Fine here,
  because `NA` does mean "not recorded". Not fine if `NA` means Namibia.
- **Slide 11, the two totals.** Drop the 94 rows with no duration and the total is 8,608
  minutes. Fill them with the average and it is 8,995. Both honest. Put both on screen and
  ask which they would report, and to whom.
- **Slide 19, the cropped y-axis.** Same four numbers, two charts, completely different
  impressions.

## Notebooks

| Notebook | What it is |
|---|---|
| `notebooks/01-cleaning.ipynb` | The full clean, problem by problem, with the date comparison proved against the clean file, and ending with the whole thing as one function |
| `notebooks/02-charts.ipynb` | Figure and axes, four chart types, labels, the base-rate warning, and the cropped-axis pair side by side |
| `notebooks/03-clean-and-chart-exercise.ipynb` | The live exercise |
| `notebooks/04-three-charts-homework.ipynb` | Homework starter |
| `notebooks/04-three-charts-solved.ipynb` | Three worked charts, and the `findings.md` prose written out |

`demos/clean_and_chart.py` is the same work as a script that saves two PNGs. It is nearly the
session 10 pipeline, and worth showing at the end for that reason.

`homework/solutions/findings.md` is the written half, done properly. It is the thing to show
if they ask what "two or three sentences per chart" is supposed to look like.

## A note on the worked homework

Chart 3's first draft was titled "almost every play under two minutes is a skip", which the
data does not support: 98% of skips are short, but only 64% of short plays are skips. The
notebook and `findings.md` both keep that mistake visible and explain it, because confusing
those two statements is one of the most common ways to over-claim from a chart. If they make
the same slip, it is a good thing to have hit.

## Watch out for

- **`plt.show()` blocking** in a script. In a notebook it is harmless. Give them
  `matplotlib.use("Agg")` for scripts.
- **Charts with no labels.** Hold the line on this from the first chart.
- **Forgetting `fig, ax`** and stacking everything onto one plot. The `fig, ax =
  plt.subplots()` habit prevents it.
- **A bare `dropna()`**, which drops a row if *any* column is empty. Here that costs 238
  rows instead of 94. Demonstrate it.
- **Not checking `shape` before and after.** One line, and it is the difference between
  cleaning data and quietly deleting it.
- **Comparing unstripped text.** `" Pop "` and `"Pop"` are different strings and the
  difference is invisible on screen.

## Definition of done

They have a `clean_plays()` function they wrote, they can say what each step decided and what
it cost, and they have one labelled chart saved as a PNG that answers a question they can
state in a sentence.
