# Session 6 homework

Budget: 2 to 4 hours. **Saturday:** one line, `Homework done` or `Homework not done`.

Work in `notebooks/07-answers-and-decisions-homework.ipynb`, or in the two scripts here if you
prefer. Run scripts from the repository root, so the relative paths to `data/` work:

```
python sessions/session-06/homework/answers_in_pandas.py
python sessions/session-06/homework/decisions.py
```

Commit and push when you are done.

---

## Task 1: your session 5 answers, in pandas

In session 5 you answered questions 1 to 10 of the homework in SQL, in `answers.sql`.
Answer the same ten again in pandas.

**Your own `answers.sql` is the answer key.** Open it next to the notebook. For each question:

1. write the pandas version,
2. check that it gives the same answer as your SQL,
3. if it does not, find out which one is wrong. Do not assume it is the pandas one.

The ten questions are written out in the notebook and the script, so you do not need to go
looking for them. Use `data/clean/plays.csv` and `data/clean/artists.csv`: the plays file
already has the artist, genre and country on every row, so none of the ten needs a merge.

Three of the ten are worth slowing down for. Two hide a trap that pandas shares with SQL, and
one hides a trap that SQL had and pandas does not. Say which ones in a comment.

Then two short extras:

- **Your join-type question.** Take the question you wrote for task 3 of the session 5
  homework, where the inner join and the left join gave different answers, and answer it in
  pandas with `how="inner"` and `how="left"`. Same two answers as your SQL?
- **A verdict.** Sort the eleven into three lists: **easier in SQL**, **easier in pandas**,
  **about the same**. Finish with two or three sentences: which one would you reach for, and
  when? There is no right answer; an opinion based on eleven real comparisons is the point.

## Task 2: a decision diary

**Which device gets skipped most?** Answer it five times, once after each cleaning decision:

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

Task 2 imports `load_messy` and `clean_plays` from `sessions/session-06/solutions/cleaning.py`.
If your own functions from the live exercise passed every check, use yours instead.

---

## Hints, if you want them

<details>
<summary>Question 3</summary>

Look at `artists.dtypes` first. `formed_year` is a decimal, and the reason is the answer to
the question. Then remember session 5: what happened when you wrote `= NULL`? Try the
pandas equivalent, `== None`, and see what it does.
</details>

<details>
<summary>Question 5</summary>

`played_at` is text. Every text column has `.str`, which does a string operation to every
value at once: `plays["played_at"].str[:4]` is the first four characters of every date.
After that it is a `value_counts()`. Or turn it into real dates first, as in notebook 05,
and use `.dt.year`.
</details>

<details>
<summary>Question 9</summary>

`groupby("device")` with an `agg` that counts the plays and sums `skipped`. Then make a new
column by assigning to it: `table["pct"] = ...`.

Remember the integer division trap from session 5? Try it in pandas and see whether it is
still there.
</details>

<details>
<summary>Task 2: skip_rates</summary>

`df.groupby("device")["skipped"].agg(plays="size", rate="mean")` gives both columns at once.
The mean of a column of 0s and 1s is the share of 1s, so multiply it by 100 for a
percentage.
</details>
