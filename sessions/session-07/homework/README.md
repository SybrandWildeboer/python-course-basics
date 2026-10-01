# Session 7 homework

Budget: 2 to 4 hours. **Saturday:** one line, `Homework done` or `Homework not done`.

Work in `data/music.db` with DB Browser. Write your answers in `answers.sql`, with the
question as a `--` comment above each query, then commit and push the file.

Keep this file next to your session 6 `answers.sql`. You will have both open in session 8,
when we rewrite some of these queries in pandas.

---

## Task 1: Five questions

Every one of these needs a join **and** an aggregate.

1. Finish question B from last week's homework. Which artists get skipped most? Show the
   artist's **name** this time, not the id, with plays, skips and the skip percentage to one
   decimal place. Only count artists with 30 or more plays, and show the top ten.
2. How much do you listen to artists by the decade they were formed in? Show the decade
   (1990, 2000, and so on), the number of artists, the plays and the total minutes.
3. What share of the listening time on each device went to artists who have won at least
   one award? Show the device, the total minutes, the award-winner minutes, and the
   percentage to one decimal place.
4. Which artists that are no longer active do you still listen to? Show each one with the
   number of plays, the total minutes, and the date you last played them.
5. Do award winners get listened to more? Compare the average total minutes **per artist**
   for artists who have won an award against artists who have not. Count every artist,
   including any you have never played.

**Two of these need a CTE to be correct.** The other three are a join and a `GROUP BY`. The
two that need more will still run without one, and give you a confident wrong answer.
Working out which two, and how you could tell, is part of the exercise.

If you get stuck on one for more than fifteen minutes, send me the query you tried and what
came back. Do not lose an evening to it.

## Task 2: Find a question where the join type changes the answer

Write one question of your own that gives a **different answer** with an inner join than
with a left join.

Show both queries and both answers. Then explain, in a comment, which one answers the
question you actually asked, and why.

Remember the shape of the data: two artists have no plays at all, and only 17 of the 40
artists have ever won an award. Both facts are places where the join type decides the
answer.

This task is the deeper of the two, and you might not finish it. The SQL is short. The
sentence about which query is right is the part that counts, because choosing the join type
is a decision about the question, not a technical detail.

---

## Hints, if you want them

<details>
<summary>Question 2</summary>

The decade is not a column, so you have to make one, like the year in last week's question 5.
This time the integer division from last week's question 9 is useful rather than a trap:
`formed_year / 10` throws away the last digit, so `1996 / 10 * 10` is `1990`.

Then look at the first row of your answer. Last week's question 3 should come back to mind.
</details>

<details>
<summary>Any of them: checking a total</summary>

Before you trust a total, check it against a number you already know. Last week's question 7
gave you the minutes per device, `plays` has 2,183 rows, and the whole table is 8,980.4
minutes. If your join makes any of those bigger, count the rows after the join and ask why
there are more of them.
</details>

<details>
<summary>Question 4</summary>

Look at the `still_active` column for every artist before you filter on it. One of the
values is not a 0 or a 1.
</details>
