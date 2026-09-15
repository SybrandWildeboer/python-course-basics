# Session 6 homework

Budget: 2 to 4 hours. **Saturday:** one line, `Homework done` or `Homework not done`.

Work in `data/music.db` with DB Browser. Write your answers in `answers.sql`, with the
question as a `--` comment above each query, then commit and push the file.

That file is your own SQL reference for the rest of the course, and you will use it again in
session 8 when we do the same questions in pandas.

---

## Task 1: Ten questions

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

If you get stuck on one for more than fifteen minutes, send me the query you tried and what
came back. Do not lose an evening to it.

## Task 2: Two questions of your own

Invent two questions about this data that nobody has asked you, and answer them in SQL.

For each one, **write down what you expected before you ran it**, then whether the answer
surprised you.

That habit is worth more than the queries. Having a rough expectation is what makes a wrong
answer noticeable, and most bad analysis is a query that ran fine and answered a slightly
different question than the one intended.

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
