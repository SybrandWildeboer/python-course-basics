# Session 2: Control flow

**Goal:** programs that make decisions and repeat themselves, and a learner who reads error
messages instead of flinching at them.

**Slides:** [`slides/session-02.html`](../../slides/session-02.html) (19 slides)

---

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00–0:15 | Homework review, starting with what broke | Slide 2. They run it, not you |
| 0:15–0:40 | Booleans, `if` / `elif` / `else`, `and` / `or` / `not` | Slides 4–7 |
| 0:40–0:50 | **Break things on purpose.** Five errors, typed by hand | Slides 8–10 |
| 0:50–1:00 | Break | |
| 1:00–1:20 | `for`, `range`, accumulating, `while`, `break` / `continue` | Slides 12–15 |
| 1:20–1:50 | The guessing game, built in six steps | Slide 17 |
| 1:50–2:00 | Homework briefing | Slides 18–19 |

## What they type

| File | What it is |
|---|---|
| `demos/control_flow.py` | The walkthrough, in slide order |
| `demos/errors_on_purpose.py` | Five commented-out errors to uncomment one at a time |
| `exercises/guessing_game.py` | The live exercise, with the six build steps in the docstring |
| `solutions/guessing_game.py` | Worked version, with a note on loop condition style |
| `homework/guessing_game_limited.py` | Homework 1 starter |
| `homework/statistics.py` | Homework 2 starter |
| `homework/solutions/` | Both answers, with the reasoning written out |

## The ten minutes that matter most

The error-reading block is the highest-value part of the whole course. Protect it.

Make them **type** each broken line rather than reading the table on the slide, run it, and
say the last line of the message out loud in their own words before fixing it. The goal is
not memorising error names; it is removing the small jolt of panic that stops people reading
the message at all.

Also worth doing live, because it takes twenty seconds each and removes real fear:

- write an infinite `while` loop and kill it with `Ctrl+C`,
- write `if age = 41:` and read Python's "did you mean `==`" hint.

## Notebooks

| Notebook | What it is |
|---|---|
| `notebooks/01-control-flow.ipynb` | The walkthrough, with cells to predict before running |
| `notebooks/02-errors-on-purpose.ipynb` | Five errors, commented out, to uncomment one at a time. Also covers the notebook-only error: a cell that passes because of something you ran ten minutes ago |
| `notebooks/03-statistics-homework.ipynb` | Homework 2, with `assert` checks to verify against |
| `notebooks/03-statistics-solved.ipynb` | Worked version, including the `highest = 0` bug demonstrated on negative numbers |

The guessing game stays a script, in `exercises/` and `homework/`, because it is interactive.

## Watch out for

- **`=` versus `==`.** Constant this week. Python's message is good, so let them read it.
- **`range(1, 10)` not including 10.** Say it, then show it, then let them be annoyed by it.
- **Forgetting the colon** at the end of `if` and `for` lines.
- **Indentation.** In Python it is grammar, not decoration. Mixed tabs and spaces is the
  nastiest version because it looks fine on screen.
- **`total = 0` inside the loop** instead of before it. Let them hit it, then ask what is
  resetting.
- **Deep nesting.** They will write the four-level version in the guessing game. Let them
  finish it first, then refactor it together. Showing beats telling.
- **Not converting the guess** with `int()`. Good revision, and the error message says
  exactly what is wrong.

## Definition of done

They have a guessing game they would happily hand to somebody else, and they can name five
error types and what each one means.
