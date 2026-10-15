# Session 5 homework

Budget: 2 to 4 hours. **Saturday:** one line, `Homework done` or `Homework not done`.

Work in `data/music.db` with DB Browser. Write your answers in `answers.sql`, with the
question as a `--` comment above each query, then commit and push the file. If you would
rather work in a notebook, `notebooks/05-questions-homework.ipynb` has the same questions.

That file is your own SQL reference for the rest of the course. In session 6 we answer the
first ten questions again in pandas, so keep it.

**Before you run each query, write down roughly what you expect.** Having a rough
expectation is what makes a wrong answer noticeable, and most bad analysis is a query that
ran fine and answered a slightly different question than the one intended.

---

## Task 1: Ten questions about one table at a time

1. How many artists are in the database?
2. Which artists are from the Netherlands? Show name and genre.
3. Which artists have an unknown `formed_year`?
4. What are the five longest plays? Show the track and the minutes.
5. How many plays happened in 2024, and how many in 2025? (One query, two rows.)
6. Which tracks were played more than 40 times? Show the track and the count, most played
   first.
7. What is the total listening time in minutes for each device, rounded to a whole number?
8. Which genres have five or more artists?
9. What proportion of plays on each device were skipped? Show the device, the total plays,
   the skipped plays, and the percentage to one decimal place.
10. What was the busiest single day, by number of plays?

**Two of these need something you have not been shown directly.** Both are within reach of
what is on the slides. Working out which two, and what they need, is part of the exercise.

## Task 2: Five questions across tables

Every one of these needs a join **and** an aggregate.

11. Which artists get skipped most? Show the artist's **name**, with plays, skips and the
    skip percentage to one decimal place. Only count artists with 30 or more plays, and
    show the top ten.
12. How much do you listen to artists by the decade they were formed in? Show the decade
    (1990, 2000, and so on), the number of artists, the plays and the total minutes.
13. What share of the listening time on each device went to artists who have won at least
    one award? Show the device, the total minutes, the award-winner minutes, and the
    percentage to one decimal place.
14. Which artists that are no longer active do you still listen to? Show each one with the
    number of plays, the total minutes, and the date you last played them.
15. Do award winners get listened to more? Compare the average total minutes **per artist**
    for artists who have won an award against artists who have not. Count every artist,
    including any you have never played.

**Two of these need a CTE to be correct.** The other three are a join and a `GROUP BY`. The
two that need more will still run without one, and give you a confident wrong answer.
Working out which two, and how you could tell, is part of the exercise.

If you get stuck on one for more than fifteen minutes, send me the query you tried and what
came back. Do not lose an evening to it.

## Task 3: Find a question where the join type changes the answer

Write one question of your own that gives a **different answer** with an inner join than
with a left join.

Show both queries and both answers. Then explain, in a comment, which one answers the
question you actually asked, and why.

Remember the shape of the data: two artists have no plays at all, and only 17 of the 40
artists have ever won an award. Both facts are places where the join type decides the
answer.

This task is the deepest of the three, and you might not finish it. The SQL is short. The
sentence about which query is right is the part that counts, because choosing the join type
is a decision about the question, not a technical detail.

---

## Hints, if you want them

<details>
<summary>Question 9</summary>

You need two numbers per device: how many plays, and how many of those were skipped.
`COUNT(*)` gives you the first. For the second, remember that `skipped` is already a 0 or a
1, so `SUM(skipped)` counts the skipped ones. Then divide, and multiply by 100.

Watch out: in SQLite, dividing one whole number by another throws away the fraction, so
`19 / 179` is `0`. Multiplying by `100.0` first, with the decimal point, keeps it honest.
</details>

<details>
<summary>Question 10</summary>

Nothing new needed. `played_at` is already one value per day, so it can be grouped like any
other column. Group, count, sort, limit.
</details>

<details>
<summary>Question 12</summary>

The decade is not a column, so you have to make one, like the year in question 5. This time
the integer division from question 9 is useful rather than a trap: `formed_year / 10`
throws away the last digit, so `1996 / 10 * 10` is `1990`.

Then look at the first row of your answer. Question 3 should come back to mind.
</details>

<details>
<summary>Questions 11 to 15: checking a total</summary>

Before you trust a total, check it against a number you already know. Question 7 gave you
the minutes per device, `plays` has 2,183 rows, and the whole table is 8,980.4 minutes. If
your join makes any of those bigger, count the rows after the join and ask why there are
more of them.
</details>

<details>
<summary>Question 14</summary>

Look at the `still_active` column for every artist before you filter on it. One of the
values is not a 0 or a 1.
</details>
