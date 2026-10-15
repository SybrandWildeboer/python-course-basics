# Session 4 homework

Budget: 2 to 4 hours. **Saturday:** one line, `Homework done` or `Homework not done`.

Run everything from the repository root, so the relative paths to `data/` work:

```
python3 sessions/session-04/homework/filter_plays.py
```

---

## Task 1: Write a filtered CSV

In `filter_plays.py`, read `data/clean/plays.csv`, keep only the rows that meet a condition
**you choose**, and write them to a new file in `output/`.

Some conditions worth trying:

- every play longer than five minutes,
- everything played on the speaker,
- everything from 2025,
- every play that was skipped.

Requirements:

- print how many rows went in and how many came out,
- the output file has the same columns, in the same order, with a header row,
- open the result in VS Code (or a spreadsheet) afterwards and check it looks right.

**Watch out for:** `"w"` replaces the output file without asking, and the `output/` folder has
to exist before you write into it. `os.makedirs("output", exist_ok=True)` handles that.

## Task 2: Two real questions

In `questions.py`, answer both of these and print the answers as readable sentences.

### 1. Which genre has the highest average minutes per play?

Not the highest total: the highest **average**. A genre with 500 short plays should not beat
a genre with 100 long ones.

**The hint, because this is the interesting bit:** you need **two** dictionaries. One counting
the plays per genre, one adding up the minutes per genre. Then divide one by the other,
genre by genre.

That insight, "totals and counts, kept side by side", is exactly what `GROUP BY` does for you
in session 6. Doing it by hand once makes SQL feel obvious rather than magic.

### 2. Which artist was played most in 2025 only?

The dates are text, like `"2025-04-17"`. Text has a `.startswith()` method, and
`"2025-04-17".startswith("2025")` is `True`.

Print the top five artists for 2025 with their play counts, not just the winner.

---

## Stretch, if you want it

Which **device** has the highest proportion of skipped plays? Same two-dictionary shape:
one counting all plays per device, one counting only the skipped ones.
