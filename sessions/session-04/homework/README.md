# Session 4 homework

Budget: 2 to 4 hours. **Saturday:** one line, `Homework done` or `Homework not done`.

Run everything from the repository root, so the relative paths to `data/` work:

```
python3 sessions/session-04/homework/filter_plays.py
```

From this session on, every piece of work ends with a commit and a push. It stops being a
topic and becomes a habit, so tasks 1 and 2 each finish with one.

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

Then commit the script and push. Run `git status` first: the CSV you wrote is not in the
list, because `output/` is in `.gitignore`. That is on purpose.

## Task 2: Two real questions

In `questions.py` (or `notebooks/05-questions-homework.ipynb`, if you prefer the notebook),
answer both of these and print the answers as readable sentences.

### 1. Which genre has the highest average minutes per play?

Not the highest total: the highest **average**. A genre with 500 short plays should not beat
a genre with 100 long ones.

**The hint, because this is the interesting bit:** you need **two** dictionaries. One counting
the plays per genre, one adding up the minutes per genre. Then divide one by the other,
genre by genre.

That insight, "totals and counts, kept side by side", is exactly what `GROUP BY` does for you
in session 5. Doing it by hand once makes SQL feel obvious rather than magic.

### 2. Which artist was played most in 2025 only?

The dates are text, like `"2025-04-17"`. Text has a `.startswith()` method, and
`"2025-04-17".startswith("2025")` is `True`.

Print the top five artists for 2025 with their play counts, not just the winner.

Commit and push this one too. If you used the notebook, run
`python tools/nbtool.py strip` first.

## Task 3: A branch, some notes, a merge

```bash
git switch -c add-notes
```

On that branch, write `MY-NOTES.md` in the root of your repo. Cover:

- what this course is and what you are trying to get out of it,
- what is in your repo, folder by folder,
- three things you have learned that you did not know four weeks ago,
- one thing that is still confusing. Be specific. That list is useful to both of us.

Then read your own history back:

```bash
git log --oneline
git diff HEAD~2 HEAD --stat
```

Add two or three sentences to `MY-NOTES.md`: reading your own messages back, could you tell
what each commit did without looking at the code?

Then commit it, and merge it back:

```bash
git add MY-NOTES.md
git commit -m "Add my course notes"
git switch main
git merge add-notes
git branch -d add-notes
git push
```

Check on github.com that `MY-NOTES.md` is there. There is an example in
`homework/solutions/MY-NOTES-example.md`, to show the level of detail, not to copy.

---

## Stretch, if you want it

Which **device** has the highest proportion of skipped plays? Same two-dictionary shape:
one counting all plays per device, one counting only the skipped ones.

## Before next session

Install **DB Browser for SQLite**: <https://sqlitebrowser.org>. Next session is SQL, and we
will be looking inside a real database together. Installing it live is five minutes you would
rather spend on queries.
