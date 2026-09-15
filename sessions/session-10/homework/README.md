# Session 10 homework

Budget: 2 to 4 hours. **Saturday:** one line, `Homework done` or `Homework not done`.

---

## Task 1: One more analysis, one more output

Add a second question to your pipeline.

1. Write a new function alongside `minutes_by_genre()` that answers it and **returns a
   table**.
2. Write a new output function that saves it, either as a CSV or a chart.
3. Update `main()` to call both, and to print progress for the new step.

Keep the shape. The analysis function should not know that files exist, and the output
function should not know where the numbers came from. If you find yourself writing a function
that calculates *and* saves, split it.

Some second questions worth asking:

- minutes per country, as a bar chart
- the skip rate per device, as a table
- plays per weekday (`played_at.dt.day_name()`), which might show something about routine
- the top ten tracks by total minutes

## Task 2: Delete `output/` and run it

The real test.

```bash
rm -rf output/
python3 src/pipeline.py
```

Everything should come back. If something does not, your project depends on a file you
cannot regenerate, and finding that out now is much better than finding out in session 12.
The usual culprit is a notebook that quietly wrote a file the script reads.

Then do the same to the environment:

```bash
rm -rf .venv/
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 src/pipeline.py
```

If that works, your project runs on a machine that is not yours. That is the whole point of
`requirements.txt`, and this is the moment it stops being a ritual.

**If either rebuild fails, do not fix it silently.** Note what broke and send it to me. It is
exactly the kind of thing worth ten minutes of session 11.

---

## Before session 11

Come with:

- **one or two project ideas.** Not a plan, just a question you would like answered.
- **data you can actually get hold of.** This matters more than the idea. You should already
  have the file, or be able to download it in ten minutes.

Think about that repetitive thing at work from session 1. Automating one annoying task is
usually a better project than an ambitious analysis of data you do not have.

Fair warning: I am going to scope whatever you bring down, quite hard. First ideas are almost
always three projects wearing a coat, and finishing a small one beats abandoning a big one.
