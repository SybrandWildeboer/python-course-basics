# Example of the homework notes file

This is an **example** of what task 1 asks for, not an answer to copy. Yours should be about
your own repo and your own confusions. It is here so you can see the level of detail that
makes a notes file worth writing.

---

# My Python course notes

## What this is

A twelve session course in Python, SQL and git, one evening a week with homework in between.
I started in January having never written code. I want to stop doing the Monday report by
hand, and I want to be able to answer questions about our data without asking someone else
to run a query for me.

## What is in this repo

| Folder | What is in it |
|---|---|
| `sessions/session-01/` | Setup, first scripts. `about_me.py` was my first working program |
| `sessions/session-02/` | The guessing game, and the statistics script without `sum()` |
| `sessions/session-03/` | Those statistics rewritten as four functions, and the menu program |
| `sessions/session-04/` | Reading the listening log CSV, counting by device and genre |
| `my-work/` | My own experiments, mostly broken on purpose |
| `data/` | The listening log we use all course |

## Three things I did not know five weeks ago

1. **Reading the last line of an error first.** I used to see a wall of red text and assume
   the whole thing was broken. It is usually one line, and the message says which one.
2. **The difference between `return` and `print`.** A function that prints looks like it
   works, right up until you try to use the answer for anything. `None + 1` was the moment
   this clicked.
3. **That a list of dictionaries is just a table.** Once I saw that, the CSV reader stopped
   feeling like magic. It hands back rows, and a row is a dictionary.

## What is still confusing

- **When to use `.get()` instead of square brackets.** I understand the mechanics, I cannot
  yet feel which one a situation wants.
- **File paths.** I still get `FileNotFoundError` and have to think about where the terminal
  is, rather than knowing.
- **`lambda`** in that `sorted()` line. I copy it, it works, I could not write it from
  scratch or explain it to anyone.

## On my own commit messages

Looking back through `git log --oneline`, the ones from the first day are useless. "update"
tells me nothing. The later ones, like "Fix average minutes, was dividing by total rows",
I can read months from now and know exactly which change they are. The difference is whether
I said what changed rather than that something changed.
