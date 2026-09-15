# Session 1 — Setup and first contact

**Goal:** a working environment, and a script the learner wrote themselves that does
something real.

**Slides:** [`slides/session-01.html`](../../slides/session-01.html) (25 slides)

---

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00–0:10 | What Python is, what an interpreter does | Slides 4–8. Ten minutes, hard stop |
| 0:10–0:50 | Install Python, VS Code, Git; verify all three | Slides 9–13. Their screen, their keyboard |
| 0:50–1:00 | Break | |
| 1:00–1:45 | First code: seven ideas, typing along | Slides 15–21, then the live exercise |
| 1:45–2:00 | Homework briefing, Saturday check-in, questions | Slides 24–25 |

If the install runs long, cut the intro next time — never cut the install.

## Before the session

- [ ] Send install links, with a note **not to install anything yet**
- [ ] Have `data/clean/plays.csv` ready to show (not used until session 4, but it helps to
      point at the dataset they will be working with all course)
- [ ] Ask them to have a terminal-capable machine and admin rights on it

## What they type

| File | What it is |
|---|---|
| `demos/hello.py` | The first file, run two ways |
| `demos/basics.py` | print, variables, types, f-strings — the typed-along walkthrough |
| `exercises/about_me.py` | The live exercise (starter with TODOs) |
| `solutions/about_me.py` | One correct version. Do not show it until they have tried |
| `homework/temperature.py` | Homework task 1 starter |
| `homework/summary.py` | Homework task 2 starter |
| `homework/solutions/` | Answers, for after the Saturday check-in |

## Watch out for

- **Windows PATH.** The "Add Python to PATH" box is unticked by default. If `python` is not
  recognised: close every terminal, reopen one, try again. If it still fails, re-run the
  installer → Modify → Add to PATH.
- **`python` vs `python3`.** On macOS and Linux it is `python3`. Agree on one spelling in
  session 1 and use it consistently for twelve sessions.
- **Not saving before running.** Point at the unsaved dot in the VS Code tab. This will
  happen at least three times today.
- **Smart quotes** from pasting out of a chat app. `“like this”` is not `"like this"`.
  When a `SyntaxError` looks impossible, retype the quotes.
- **Opening a file instead of a folder** in VS Code. Opening the folder is what makes the
  terminal start in the right place — it prevents a whole class of confusion in session 4.
- **The install running long.** It is normal. Do not rush the second half to catch up;
  drop material instead.

## Definition of done

They can run a file two ways, they have written a script that asks for input and prints a
calculated sentence, and they know what `int()` is for.
