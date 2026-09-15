# Session 2 homework

Budget: 2 to 4 hours. **Saturday:** one line, `Homework done` or `Homework not done`.

Task 2 is the one that teaches, and it is meant to be a bit too hard. Getting stuck on it is
the plan, not a failure.

---

## Task 1: Seven attempts only

Copy your guessing game to `guessing_game_limited.py` and add a limit.

1. The player gets a maximum of **7** attempts.
2. After each wrong guess, say how many they have left.
3. If they run out, print the secret number and something kind.

```
I am thinking of a number between 1 and 100.
Your guess: 50
Lower. 6 guesses left.
Your guess: 25
Higher. 5 guesses left.
...
Out of guesses. It was 31. Close one.
```

**Hint:** you now have two reasons to stop looping, so your `while` condition needs to
mention both. `and` is the word you want.

## Task 2: Statistics by hand

Write `statistics.py`. Put a list of numbers at the top of the file:

```python
numbers = [12, 7, 41, 3, 28, 19, 7, 55, 2, 33]
```

Print the **total**, the **average**, the **highest** and the **lowest**.

The catch: **no `sum()`, no `max()`, no `min()`**. Use loops. Those functions exist and you
should use them in real life, but writing them yourself once is how you understand what a
loop is actually for.

Requirements:

- the average should print to one decimal place,
- your code should still be correct if you change the list at the top,
- add a comment above each of the four calculations saying what it does.

**Where you will get stuck:** what do you set your "highest so far" variable to *before* the
loop starts? Zero is the obvious answer and it is wrong. Work out why by trying it with a
list of negative numbers like `[-5, -2, -9]`. Sitting with that for ten minutes is worth
more than being told the answer.

**Stretch, if you finish:** also print how many numbers are above the average.

---

We refactor this exact file into four functions in session 3, so make sure it exists even if
it is not perfect.
