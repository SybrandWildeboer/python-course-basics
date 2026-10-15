# Your ten-minute presentation

Ten minutes, five parts, one chart. Then questions.

This is not a performance. It is practice at the thing that matters most in data work and
gets taught least: telling somebody what you found, honestly, in a way they can check.

---

## The five parts

| # | Part | Time | What to say |
|---|---|---|---|
| 1 | **The question** | 1 min | One sentence, from section 2 of your session 11 scoping worksheet. Which repetitive task it started from, and why you cared. |
| 2 | **The data** | 2 min | Where it came from, how many rows, what one row is. The cleaning decisions from section 7 that changed the answer, with how many rows each touched. |
| 3 | **One chart** | 3 min | The chart from `project/output/`, with the answer in its title. Walk through it: what each axis is, where to look, what it shows. |
| 4 | **What surprised you** | 2 min | Something in the data, or in the work, that you did not expect. A bug that taught you something counts. |
| 5 | **What you would do next** | 2 min | Your *could* list, and what you would need to do it. Including what you would do differently if you started again. |

Write a few words for each part below. Notes, not a script.

### 1. The question

### 2. The data

### 3. One chart

### 4. What surprised you

### 5. What you would do next

---

## Before the session

- [ ] Run `python project/pipeline.py` from a fresh terminal. It finishes, and the chart in
      `project/output/` is the current one.
- [ ] Open the chart and read its title out loud. Is it the answer, or only the topic?
- [ ] Know the one number you would bet on, and how you checked it a second way.
- [ ] Say the whole thing out loud once, with a timer. Everybody runs long the first time.

## Showing it

- Show the chart full screen, not the code. If somebody asks how you did something, then
  open the code.
- Have `project/pipeline.py` open in VS Code in the background, for the code review that
  follows.
- If something does not work on the day, say so and show what you have. A half-finished
  project explained honestly is a better presentation than a finished one explained vaguely.

## The questions you will be asked

These are the questions any reviewer asks of any analysis. Have an answer to each, even if
the answer is "I do not know yet":

1. How do you know the number is right?
2. What did cleaning remove, and would the answer change if it had not?
3. What is the smallest change to the data that would change your conclusion?
4. Who else could run this, and what would they need?
