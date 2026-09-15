# Session 1 homework

Two tasks. The first one you can definitely finish. The second one you might not, and that is
deliberate, and where you get stuck is what we open session 2 with.

Budget: 2–4 hours. **Saturday:** send one line, either `Homework done` or `Homework not done`.

---

## Task 1: Temperature converter

Write `temperature.py`. It should:

1. ask for a temperature in Celsius,
2. convert it to Fahrenheit using `F = C × 9/5 + 32`,
3. print a sentence containing both numbers.

```
$ python3 temperature.py
Temperature in Celsius: 21.5
21.5°C is 70.7°F
```

**Stretch:** print the Fahrenheit value to exactly one decimal place. Look up "python
f-string round to 1 decimal". Looking things up is a real skill, so start now.

## Task 2: A three-question summary

Write `summary.py`. It should ask **three** questions, where at least one answer is a number
you do arithmetic on, then print a small summary paragraph using all three answers.

For example: name, number of hours slept last night, favourite drink, then print something
that mentions all three and says how many hours that is per week.

Requirements:

- at least one `int()` or `float()` conversion,
- at least one calculation,
- output that reads like a sentence a human wrote, not `Sam 7 tea`,
- a comment at the top saying what the script does.

**If it breaks:** copy the *last line* of the error message and the line it points at, and
send them to me. Do not spend an hour stuck, but do spend ten minutes reading the message
first, because that is the skill.

---

## When you are done

Both files live in `sessions/session-01/homework/`, in the repo you cloned today. Just save
them there. From session 5 you will commit them properly with git, and everything you have
written so far goes in at that point, so nothing is lost by leaving it for now.
