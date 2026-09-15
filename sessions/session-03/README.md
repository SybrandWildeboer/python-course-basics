# Session 3: Functions

**Goal:** they stop writing one long script and start writing pieces. And `return` versus
`print` finally lands.

**Slides:** [`slides/session-03.html`](../../slides/session-03.html) (20 slides)

---

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00–0:15 | Homework review: the guessing limit, and `highest = 0` | Slide 2 |
| 0:15–0:30 | Why functions, `def`, parameters | Slides 3–6 |
| 0:30–0:50 | **`return` versus `print`.** Do not rush this | Slides 7–8 |
| 0:50–1:00 | Break | |
| 1:00–1:25 | Early return, defaults, scope, docstrings, composing | Slides 9–14 |
| 1:25–1:50 | Rebuild the statistics script as four functions | Slide 17 |
| 1:50–2:00 | Mistakes table, homework briefing | Slides 18–20 |

## The block that matters

Slide 7 is the one to protect. Both versions of `double` are on screen; make them predict
all six outputs before running anything. The moment that teaches is
`print(double_p(5) + 1)` failing with `NoneType`, because until then "print" and "return"
both look like "the function produced an answer".

Then give them the rule of thumb and repeat it all session: **functions that calculate
return; only the outer layer of your program prints.**

## What they type

| File | What it is |
|---|---|
| `demos/functions.py` | The walkthrough, in slide order, with the errors commented out |
| `exercises/statistics_functions.py` | The live exercise starter |
| `solutions/statistics_functions.py` | Worked version, with asserts on the awkward cases |
| `homework/small_functions.py` | Homework 1 starter |
| `homework/menu.py` | Homework 2 starter |
| `homework/solutions/` | Both answers, plus notes on `split` and `join` |

## The trick that sells functions

Let them finish the four functions and the summary line. Then ask, as if it just occurred to
you: "now do the same for `[4, 8, 15, 16, 23, 42]`". It is one extra line. In the session 2
version it would have been forty. That single moment does more than any explanation.

## Watch out for

- **Printing inside the function instead of returning.** Do not correct it straight away.
  Ask for one summary line containing all four numbers, and let the requirement force the
  change.
- **Defining a function and never calling it.** No error, no output, total confusion.
- **Missing brackets on the call.** `greet` instead of `greet()`.
- **Trying to use a variable from inside a function outside it.** The `NameError` is the
  lesson; read it together.
- **A `return` inside an `if` with no other path.** Returns `None` silently for some inputs.
- **Reaching for `global`.** If they find it, say it exists, that it is almost always the
  wrong tool, and steer back to parameters and return values.

## Definition of done

Four working functions, used on two different lists without any copied logic, and they can
explain in their own words why `print` inside a function is a dead end.
