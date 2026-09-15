# Install guide

Send this before session 1, with **one instruction: do not install anything yet.** We do it
together in the session. People who pre-install arrive with half-broken setups that are then
debugged blind, which is a miserable way to spend the first hour.

Everything here is free and installs on Windows, macOS and Linux.

---

## What you will need, and why

| Tool | What it is | First used |
|---|---|---|
| **Python** | The language, and the program that runs your code | Session 1 |
| **VS Code** | The editor you write in, with a terminal and notebooks built in | Session 1 |
| **Jupyter** | Notebooks: code and notes in one document. How you will work most of the time | Session 1 |
| **Git** | Version control, the undo history for your whole project | Session 1 (to clone), explained in session 5 |
| **DB Browser for SQLite** | A window into a database, so SQL is not invisible | Session 6 |

---

## Links

- **Python:** <https://www.python.org/downloads/>
- **VS Code:** <https://code.visualstudio.com/>
- **Git:** <https://git-scm.com/downloads>
- **DB Browser for SQLite:** <https://sqlitebrowser.org/dl/>

Jupyter installs through Python itself, in the session:

```bash
pip install jupyterlab
```

---

## Windows

1. **Python.** Run the installer. On the very first screen, **tick "Add Python to PATH"**. It
   is unticked by default and it is the single most common setup problem on Windows. Then
   "Install Now".
2. **VS Code.** Default options are fine. Tick "Add to PATH" if offered.
3. **Git.** Lots of screens; the defaults are all fine. When asked about the default editor,
   pick VS Code if it is offered.
4. **DB Browser.** Standard installer, defaults fine.

Then open VS Code, press `Ctrl` `` ` `` for a terminal, and check:

```powershell
python --version
pip --version
git --version
```

If any of those says "not recognized": **close every terminal window and open a new one**,
then try again. PATH is only read when a terminal starts. If it still fails, re-run the
Python installer, choose **Modify**, and make sure "Add Python to PATH" is ticked.

## macOS

1. **Python.** Run the installer from python.org. macOS ships an old Python 2 that we do not
   want; the python.org one installs alongside it as `python3`.
2. **VS Code.** Drag it to Applications. Then open the Command Palette (`Cmd` `Shift` `P`)
   and run **Shell Command: Install 'code' command in PATH**, so `code .` works.
3. **Git.** Often already there. `git --version` will offer to install the developer tools if
   not.
4. **DB Browser.** Drag to Applications.

Then in VS Code press `Cmd` `` ` `` for a terminal:

```bash
python3 --version
pip3 --version
git --version
```

**It is `python3`, not `python`.** Plain `python` may point at the ancient Python 2, or at
nothing. We will use `python3` throughout the course.

## Linux

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git sqlitebrowser
```

VS Code from <https://code.visualstudio.com/> as a `.deb`, or your distribution's package
manager.

```bash
python3 --version && pip3 --version && git --version
```

If `pip install` complains about an "externally managed environment", that is your
distribution protecting the system Python. It is a good reason to use a virtual environment,
which session 10 covers:

```bash
python3 -m venv .venv && source .venv/bin/activate
```

---

## In the session: VS Code setup

1. **Extensions panel** (the squares icon in the left bar), install:
   - **Python** (Microsoft) for the play button, error highlighting and kernel picking
   - **Jupyter** (Microsoft) for notebooks inside VS Code
2. **Clone the course repo:**
   ```bash
   git clone https://github.com/SybrandWildeboer/python-course-basics.git
   cd python-course-basics
   code .
   ```
3. **Open the folder, not a file.** File, Open Folder, and pick
   `python-course-basics`. Opening the folder is what makes the terminal start in the right
   place, and it prevents a whole class of confusion in session 4.
4. **Open the first notebook:** `sessions/session-01/notebooks/01-first-steps.ipynb`. Top
   right, **Select Kernel**, and pick your Python. If VS Code offers to install anything,
   say yes.

---

## Things worth knowing before you start

**Put the folder somewhere with no spaces or accented characters in the path.**
`Documents/python-course` is fine. It saves genuine pain later.

**Save before you run.** Python runs the file on disk, not what is on your screen. VS Code
shows an unsaved file with a dot next to its name.

**Do not paste code from a chat app or a Word document.** You may get `“curly quotes”`
instead of `"straight quotes"`, which Python rejects with a `SyntaxError` that makes no
sense. The difference is nearly invisible. When that happens, retype the quotes by hand.

---

## Before session 5

**Create a GitHub account:** <https://github.com/signup>. Free, and it takes two minutes plus
an email verification. Doing it live costs ten minutes of a session.

Use an email address you will still have in five years.

---

## If something will not install

Send the **exact error text** rather than a description. Most installation problems are
one known fix away, and the message usually names it. `docs/troubleshooting.md` covers the
common ones.
