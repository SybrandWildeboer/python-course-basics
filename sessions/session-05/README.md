# Session 5: Git and GitHub

**Goal:** four sessions of work under version control and pushed to their own GitHub repo,
plus enough understanding that git does not feel frightening.

**Slides:** [`slides/session-05.html`](../../slides/session-05.html) (20 slides)

---

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00–0:15 | Homework review: the filtered CSV and the 2025 tie | Slide 2 |
| 0:15–0:30 | Why version control, and the three places | Slides 4–6 |
| 0:30–0:50 | Configure git, then status / add / commit / log, for real | Slides 8–9 |
| 0:50–1:00 | Break | |
| 1:00–1:10 | Commit messages, diffs, `.gitignore` | Slides 10–12 |
| 1:10–1:30 | **Authentication.** Budget the whole twenty minutes | Slide 13 |
| 1:30–1:45 | Their own repo, push, branches, getting out of trouble | Slides 14–17 |
| 1:45–1:55 | The exercise: everything committed and pushed | Slide 18 |
| 1:55–2:00 | Homework, and a reminder to install DB Browser | Slides 19–20 |

## Budget for authentication

It reliably eats twenty minutes and it is miserable to debug over chat, so **do it in the
session**, never as homework. Order of preference:

1. `gh auth login`. Least painful, and it configures the git credential helper too.
2. A personal access token pasted at the password prompt. Always works. Have them save it
   in a password manager, because it is not viewable again.
3. An SSH key. The grown-up answer, the fiddliest today.

## The remote rename, and why

They cloned this repo in session 1, so `origin` points at the course. Rather than starting a
fresh repo and losing four sessions of history, have them keep both remotes:

```bash
git remote rename origin course
git remote add origin https://github.com/THEIR-NAME/python-course.git
git push -u origin main
```

Now `git push` goes to their repo and `git pull course main` collects course updates. Say out
loud that a remote is just a nickname for a URL; that one sentence removes most of the
mystery.

## What they use

| File | What it is |
|---|---|
| `demos/git_commands.md` | Every command from the session, with what each is for |
| `exercises/README.md` | The live exercise, which happens in the terminal |
| `homework/README.md` | Both homework tasks |
| `homework/solutions/MY-NOTES-example.md` | An example notes file, to show the level of detail |

## Watch out for

- **`user.name` and `user.email` not configured.** The most common first-commit failure.
  Do it before anything else.
- **Committing everything including junk.** Look at this repo's `.gitignore` together and
  point out that `output/` is why their session 4 CSVs never appeared in `git status`.
- **Commit messages like "stuff".** Do not lecture. Task 2 has them read their own messages
  back, which teaches it better than you can.
- **Fear of breaking things.** Say out loud, more than once, that committed work is very hard
  to lose. Fear is what stops people committing often, and committing often is the benefit.
- **`git reset --hard`.** Deliberately not taught. If they find it online, explain that it
  genuinely destroys work and that `git restore` and `git revert` cover what they need.
- **Merge conflicts.** Out of scope today. If one happens, resolve it together calmly; it is
  a good unplanned lesson.

## Definition of done

`git status` clean, several commits with real messages, and their work visible on github.com
under their own account. From here every session ends with a commit and a push.
