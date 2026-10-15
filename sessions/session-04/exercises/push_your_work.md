# Session 4 live exercise, part two: your work on GitHub

No Python in this part. The exercise is your own repo, and it happens in the terminal.
Every command is in `sessions/session-04/demos/git_commands.md`.

## The exercise

1. `git status` and see what is uncommitted after four sessions, including the exercise
   you finished an hour ago.
2. Strip the saved output from your notebooks first, so it does not go into the history:
   ```bash
   python tools/nbtool.py check
   python tools/nbtool.py strip
   ```
3. Commit your work in **three or four separate commits**, grouped by session, each with a
   message that says what changed and why.
4. Create an empty repository called `python-course` on github.com. No README, no
   `.gitignore`, no licence.
5. Point your copy at it, keeping the course repo as a second remote:
   ```bash
   git remote rename origin course
   git remote add origin https://github.com/YOUR-NAME/python-course.git
   git push -u origin main
   ```
6. Open your repo in a browser and click into one commit. Read the diff GitHub shows you.

Then, for the feel of it:

7. Change one line in any file. Run `git diff` and read it out loud.
8. `git restore` that file to undo the change. Run `git status` to confirm it is gone.
9. `git log --oneline` and have a look at what you have built.

## Definition of done

`git status` says clean, `git log --oneline` shows several commits with real messages, and
your work is visible on github.com under your own account.

## If something goes wrong

Copy the **exact** error text and send it over. Authentication problems in particular are
not worth guessing at, and the message nearly always names the fix.
