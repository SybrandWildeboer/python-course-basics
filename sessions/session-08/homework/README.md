# Session 8 homework

Budget: 2 to 4 hours. **Saturday:** one line, `Homework done` or `Homework not done`.

Work in `notebooks/04-answers-in-pandas-homework.ipynb`, or in the script version if you
prefer:

```
python3 sessions/session-08/homework/answers_in_pandas.py
```

Run everything from the repository root, so the relative paths to `data/` work. Commit and
push when you are done.

---

## Task 1: your session 6 answers, in pandas

In session 6 you answered ten questions in SQL, in `answers.sql`. Answer the same ten again
in pandas.

**Your own `answers.sql` is the answer key.** Open it next to the notebook. For each question:

1. write the pandas version,
2. check that it gives the same answer as your SQL,
3. if it does not, find out which one is wrong. Do not assume it is the pandas one.

The ten questions are written out in the notebook and the script, so you do not need to go
looking for them. Use `data/clean/plays.csv` and `data/clean/artists.csv`: the plays file
already has the artist, genre and country on every row, so none of the ten needs a merge.

Three of the ten are worth slowing down for. Two hide a trap that pandas shares with SQL, and
one hides a trap that SQL had and pandas does not. Say which ones in a comment.

## Task 2: your own two questions, and a verdict

Take the two questions you invented in session 6 and answer them in pandas as well. Same
answer as your SQL?

Then, for all twelve questions, sort them into three lists: **easier in SQL**, **easier in
pandas**, **about the same**. Finish with two or three sentences: which one would you reach
for, and when?

There is no right answer to that. The point is that by next session you have an opinion based
on twelve real comparisons, rather than on what somebody told you.

---

## Hints, if you want them

<details>
<summary>Question 3</summary>

Look at `artists.dtypes` first. `formed_year` is a decimal, and the reason is the answer to
the question. Then remember session 6: what happened when you wrote `= NULL`? Try the
pandas equivalent, `== None`, and see what it does.
</details>

<details>
<summary>Question 5</summary>

`played_at` is text. Every text column has `.str`, which does a string operation to every
value at once: `plays["played_at"].str[:4]` is the first four characters of every date.
After that it is a `value_counts()`.
</details>

<details>
<summary>Question 9</summary>

`groupby("device")` with an `agg` that counts the plays and sums `skipped`. Then make a new
column by assigning to it: `table["pct"] = ...`.

Remember the integer division trap from session 6? Try it in pandas and see whether it is
still there.
</details>
