# Session 5 homework

Budget: 2 to 4 hours. **Saturday:** one line, `Homework done` or `Homework not done`.

From this session on, every session ends with a commit and a push. It stops being a topic
and becomes a habit.

---

## Task 1: A branch, some notes, a merge

```bash
git switch -c add-notes
```

On that branch, write `MY-NOTES.md` in the root of your repo. Cover:

- what this course is and what you are trying to get out of it,
- what is in your repo, folder by folder,
- three things you have learned that you did not know five weeks ago,
- one thing that is still confusing. Be specific. That list is useful to both of us.

Then commit it, and merge it back:

```bash
git add MY-NOTES.md
git commit -m "Add my course notes"
git switch main
git merge add-notes
git branch -d add-notes
git push
```

Check on github.com that `MY-NOTES.md` is there.

## Task 2: Three commits, then read them back

Make three separate, meaningful commits:

1. improve one of your session 4 scripts, however you like,
2. add a comment to any file explaining something you found confusing,
3. tidy one thing: a better variable name, a removed leftover `print`, anything.

Each one gets its own `git add` and `git commit -m`. Three commits, not one.

Then look at what you made:

```bash
git log --oneline
git diff HEAD~3 HEAD
```

Finally, add two or three sentences to `MY-NOTES.md`: reading your own messages back, could
you tell what each commit did without looking at the code? Commit that too, and push.

---

## The point of task 2

It is the first time git history stops being an obligation and becomes something you use.
Almost everybody writes at least one message they cannot decode a week later, and noticing
that yourself is worth more than any amount of advice about commit messages.

## Before next session

Install **DB Browser for SQLite** if you have not already:
<https://sqlitebrowser.org>. Next session is SQL and we will be looking inside a real
database together.
