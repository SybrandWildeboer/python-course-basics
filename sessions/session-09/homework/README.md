# Session 9 homework

Budget: 2 to 4 hours. **Saturday:** one line, `Homework done` or `Homework not done`.

Work in `notebooks/04-decisions-homework.ipynb`, or in the two scripts here if you prefer.
Run scripts from the repository root, so the relative paths to `data/` work:

```
python sessions/session-09/homework/decisions.py
```

Both tasks import `load_messy` and `clean_plays` from `solutions/cleaning.py`. If your own
functions from the live exercise passed every check, use yours instead.

---

## Task 1: A decision diary

**Which device gets skipped most?** Answer it five times, once after each decision:

1. the messy file exactly as loaded, no cleaning at all
2. device text stripped and lower-cased, blank devices left out, duplicates still in
3. the same, with duplicates dropped
4. the full `clean_plays`, with `"unknown"` as a device
5. the clean file, which real life never gives you

Write one function, `skip_rates(df)`, that returns a table with one row per device, the
number of plays and the percentage skipped, highest first. Use it at every step.

Then fill in the diary (winner, rate, number of plays at each step) and answer:

- Which single decision changed the answer most?
- What should you do about `"unknown"` in step 4? It is a real group of plays, so it should
  not be hidden. Should it be allowed to win?
- Step 1's winner has very few plays. Try the `min_plays` idea from the session 4 stretch on
  it, with a minimum of 30. Does it rescue the answer?

## Task 2: One chart that answers one question

Pick your own question about the listening log and answer it with **one** chart. If you need
ideas: the artists with the most minutes in 2025, plays per day of the week, the countries
whose artists you play most.

Requirements, from the checklist in notebook 02:

- the question, written as one sentence
- a title that **gives the answer**, with numbers formatted with `:.1f`
- bars for categories, a line for time, and bars that start at zero
- axis labels with units
- saved to `output/` with `fig.savefig(...)`, **before** `plt.show()`
- one sentence underneath: what you would say about it in a meeting

**Watch out for:** a title you cannot back up. If the top two are close, check how many of
their plays have missing minutes before you name a winner.

---

## Stretch, if you want it

Make a second chart for the same question from the **messy file**, doing only the cleaning
you need to make the code run at all. Put the two side by side and write one sentence about
what changed. That is the whole of today's session in one picture.
