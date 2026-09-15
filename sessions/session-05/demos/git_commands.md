# Session 5 command reference

Everything typed in this session, in order, with what each line is for. Follow along in
your own repo rather than copying the whole thing at once.

---

## One time only: tell git who you are

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

git config --global init.defaultBranch main   # call the first branch main
git config --global pull.rebase false         # merge when pulling, do not rebase

git config --list                             # check it took
```

Without a name and email, git refuses to commit. The message is friendly about it.

---

## The loop you will run a thousand times

```bash
git status            # where is everything? Run this constantly

git add path/to/file.py     # stage one file
git add .                   # stage everything that changed
git status                  # now it says "changes to be committed"

git commit -m "Answer the session 4 questions"
git status                  # clean again

git log --oneline           # the history, one line per commit
git log -3                  # just the last three
```

`git status` is not a formality. It tells you which of the three places your work is in, and
it usually suggests the command you want next.

---

## Seeing what changed

```bash
git diff                 # changes you have NOT staged yet
git diff --staged        # changes you HAVE staged
git diff HEAD~1          # what changed since the previous commit
git show HEAD            # the most recent commit in full
git show HEAD~3:file.py  # how a file looked three commits ago
```

In a diff, `-` lines were removed and `+` lines were added. A changed line appears as both.
Everything else is context so you can see where you are.

VS Code shows the same information side by side in its Source Control panel, which is
easier on the eyes.

---

## Your own repo on GitHub

You cloned the course repo in session 1, so your copy points at mine and you cannot push to
it. Keep both: rename mine, add yours.

```bash
git remote -v            # see where your copy currently points

git remote rename origin course
git remote add origin https://github.com/YOUR-NAME/python-course.git

git push -u origin main  # send everything to YOUR repo
```

From now on:

```bash
git push                 # send your work to your repo
git pull                 # get your own work from another machine
git pull course main     # collect updates I make to the course
```

A remote is nothing more than a nickname for a URL. `git remote -v` lists the nicknames.

---

## Authentication

GitHub stopped accepting passwords for git years ago. Pick one of these, in this order of
preference:

```bash
gh auth login            # GitHub CLI. Four questions, approve in the browser, done
```

If `gh` is not available: create a **personal access token** on github.com under Settings,
Developer settings, Personal access tokens. Paste it when git asks for a password. You
cannot view it again, so save it in your password manager.

An **SSH key** is the grown-up option and the fiddliest to set up. Worth doing eventually.

---

## Branches

```bash
git switch -c add-readme    # create a branch and move onto it
git branch                  # list branches, * marks where you are

# ... edit, add, commit as normal ...

git switch main             # back to main
git merge add-readme        # bring the branch's work into main
git branch -d add-readme    # delete the label, the commits stay
git push
```

A branch is a label on a line of commits. Switching changes your files to match that line.
Work on one branch is invisible on the other until you merge.

---

## Getting out of trouble

| You want to | Type |
|---|---|
| Throw away changes to one file | `git restore path/to/file.py` |
| Unstage something added by mistake | `git restore --staged file.py` |
| Undo a commit by adding an opposite one | `git revert <commit>` |
| See how a file looked earlier | `git show HEAD~3:file.py` |
| Work out what is going on | `git status`, then `git log --oneline` |

**Once something is committed it is very hard to lose.** Git keeps almost everything,
including things you think you deleted. If you end up in a mess: stop, run `git status`, and
send me what it says. Do not delete the folder and start over, which is the traditional move
and almost never necessary.

One command is deliberately missing from this page: `git reset --hard`. It does genuinely
throw work away, you do not need it yet, and everything above is safer.

---

## What not to commit

See `.gitignore` in the repo root. The rule of thumb: commit what a human wrote, ignore what
a machine generated, anything enormous, and **anything secret**.

Once a password or key is pushed, treat it as public forever, even if the next commit
deletes it. The history keeps it. That is the one git mistake that is genuinely expensive.
