# Git cheatsheet

Session 5, on one page.

---

## The three places your work can be

```
working folder  --git add-->  staging area  --git commit-->  repository  --git push-->  GitHub
```

`git status` tells you which one everything is in, at any moment. Run it constantly.

## One time only

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --list
```

Without a name and email, git refuses to commit.

## The loop you will run a thousand times

```bash
git status                       # where is everything?
git add path/to/file.py          # stage one file
git add .                        # stage everything changed
git commit -m "Say what changed and why"
git log --oneline                # the history
git log -3                       # just the last three
git push                         # send it to GitHub
```

## Seeing what changed

```bash
git diff                 # changes NOT staged yet
git diff --staged        # changes you HAVE staged
git diff HEAD~1          # since the previous commit
git show HEAD            # the last commit in full
git show HEAD~3:file.py  # how a file looked three commits ago
```

In a diff, `-` lines were removed and `+` lines were added. A changed line appears as both.
Everything else is context.

## Commit messages

| Unhelpful | Useful |
|---|---|
| `stuff` | `Add device counts to the explore script` |
| `fix` | `Fix average minutes, was dividing by total rows` |
| `update` | `Filter plays to 2025 only` |
| `final` | `Rename count_by so the column is a parameter` |

Present tense, start with a verb, say **what changed and why**. Around fifty characters. If
you need more, it is probably two commits.

**The test:** in six months, reading only the message, would you know whether this is the
commit you are looking for?

## Remotes

```bash
git remote -v                    # which nicknames point at which URLs
git remote add origin <url>
git remote rename origin course
git clone <url>
```

A remote is a nickname for a URL, nothing more.

Course setup, keeping both:

```bash
git remote rename origin course
git remote add origin https://github.com/YOUR-NAME/python-course.git
git push -u origin main          # -u sets the default, so later it is just: git push
git pull course main             # collect course updates
```

**Commit is local. Push is remote.** A commit with no push is exactly as safe as your laptop.

## Authentication

GitHub stopped accepting passwords for git years ago. In order of preference:

```bash
gh auth login                    # GitHub CLI. Four questions, approve in a browser
```

Otherwise a **personal access token** from Settings, Developer settings, pasted when git asks
for a password. Save it in a password manager; you cannot view it again. An **SSH key** is
the grown-up option and the fiddliest to set up.

## Branches

```bash
git switch -c add-readme         # create one and move onto it
git branch                       # list them, * marks where you are
git switch main                  # move back
git merge add-readme             # bring the work in
git branch -d add-readme         # delete the label, the commits stay
```

A branch is a label on a line of commits. Switching changes your files to match that line.
Work on one branch is invisible on the other until you merge.

## Getting out of trouble

| You want to | Type |
|---|---|
| Throw away changes to one file | `git restore path/to/file.py` |
| Unstage something added by mistake | `git restore --staged file.py` |
| Undo a commit by adding an opposite one | `git revert <commit>` |
| See how a file looked earlier | `git show HEAD~3:file.py` |
| Work out what is going on | `git status`, then `git log --oneline` |

**Once something is committed it is very hard to lose.** If you end up in a mess: stop, run
`git status`, and ask somebody. Do not delete the folder and start again.

One command is deliberately missing from this page: `git reset --hard`. It does genuinely
throw work away, and everything above is safer.

## What not to commit

```
.venv/
__pycache__/
*.pyc
output/
.ipynb_checkpoints/
.DS_Store
```

Commit what a human wrote. Ignore what a machine generated, anything enormous, and
**anything secret**.

Once a password or key is pushed, treat it as public forever, even if the next commit deletes
it. The history keeps it. That is the one git mistake that is genuinely expensive.

## Notebooks in git

A `.ipynb` is JSON: your code, your prose, and the **output of every cell**. Three
consequences:

1. diffs are hard to read
2. outputs get committed, so files bloat and every run makes a diff
3. execution counts churn even when the code is identical

```bash
python3 tools/nbtool.py check    # is anything carrying saved output?
python3 tools/nbtool.py strip    # remove it
```

Before committing a notebook, use **Restart and Run All**. If it cannot run cleanly top to
bottom, it is not finished.
