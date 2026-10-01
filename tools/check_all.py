"""Run every check on the course materials, with one command.

    python3 tools/check_all.py            # everything
    python3 tools/check_all.py --fast     # skip notebook execution and script runs

On Windows, type `python` instead of `python3`.

Six checks:

    slides      every slide fits in 1280x720, no code overflows, notes present
    sql         every query runs, and returns the row count its comment claims
    notebooks   valid JSON, no saved output, every code cell compiles
                (and, without --fast, every notebook runs top to bottom)
    scripts     every .py file parses, and every script under sessions/ and
                project/ runs from the repository root without an error
    pytest      the session 12 tests pass (demos, solutions and homework)
    git         running the scripts wrote nothing outside the gitignored
                output folders

Scripts are found automatically, so a new file is checked the moment it
exists. A script is only left out for a reason that is written down: it asks
for input (listed in SKIP below), or it is a test file, which pytest runs
instead. Every other script runs with no keyboard attached, so one that starts
asking for input without being listed fails straight away rather than hanging.
Starter, exercise and homework files are run too: they are written to run
cleanly with their TODOs still in place.

The slide, notebook-execution and pytest checks need extras:

    pip install playwright nbformat nbclient ipykernel pytest
    playwright install chromium

Those three are looked for before anything runs. If one is not installed, its
check is reported as skipped rather than failed, so this is still useful on a
machine with only the standard library, pandas and matplotlib. Anything else
that goes wrong is a failure.
"""

from __future__ import annotations

import ast
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# The folders whose scripts are run. Everything under them is found by rglob.
SCRIPT_FOLDERS = ["sessions", "project"]

# Scripts that cannot run without a person at the keyboard. A path here that
# no longer exists is an error, so this list cannot quietly go stale.
SKIP = {
    "sessions/session-01/demos/basics.py": "asks for input",
    "sessions/session-01/solutions/about_me.py": "asks for input",
    "sessions/session-01/homework/solutions/summary.py": "asks for input",
    "sessions/session-01/homework/solutions/temperature.py": "asks for input",
    "sessions/session-02/exercises/guessing_game.py": "asks for input",
    "sessions/session-02/solutions/guessing_game.py": "asks for input",
    "sessions/session-02/homework/solutions/guessing_game_limited.py": "asks for input",
    "sessions/session-03/homework/solutions/menu.py": "asks for input",
}

# Where pytest runs. The exercises folder is left out on purpose: its tests
# fail until the learner fixes the code, which is the point of the exercise.
PYTEST_FOLDERS = [
    "sessions/session-12/demos",
    "sessions/session-12/solutions",
    "sessions/session-12/homework",
]
PYTEST_LEFT_OUT = {
    "sessions/session-12/exercises": "the tests fail until the learner fixes the code",
}

TIMEOUT = 300  # seconds per script

# Keep __pycache__ folders out of the working tree while we run things.
# UTF-8 both ways, so a Windows console does not choke on a stray character.
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "MPLBACKEND": "Agg",
       "PYTHONIOENCODING": "utf-8", "PYDEVD_DISABLE_FILE_VALIDATION": "1"}

LINE = "=" * 62


def header(label: str) -> None:
    print(f"\n{LINE}\n{label}\n{LINE}")


def show(output: str, limit: int = 2500) -> None:
    """Print the end of a checker's output, starting at a whole line."""
    if not output:
        print("(no output)")
    elif len(output) <= limit:
        print(output)
    else:
        tail = output[-limit:]
        print("  ...\n" + tail[tail.find("\n") + 1:])


def installed(*modules: str) -> list[str]:
    """Return the modules from this list that cannot be imported."""
    return [m for m in modules if importlib.util.find_spec(m) is None]


def run(label: str, command: list[str], needs: tuple[str, ...] = ()) -> tuple[str, bool | None]:
    """Run a checker and return its outcome. None means it was skipped."""
    header(label)
    missing = installed(*needs)
    if missing:
        print(f"skipped: not installed: {', '.join(missing)}")
        return label, None

    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", env=ENV)
    output = (result.stdout + result.stderr).strip()
    show(output)
    return label, result.returncode == 0


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def python_files() -> list[Path]:
    """Every .py file in the repository, leaving out hidden and venv folders."""
    ignored = {"__pycache__", "venv", "env"}
    return sorted(
        p for p in ROOT.rglob("*.py")
        if not any(part.startswith(".") or part in ignored
                   for part in p.relative_to(ROOT).parts[:-1])
    )


def git_status() -> set[str] | None:
    """The lines of `git status --porcelain`, or None when git is unavailable."""
    try:
        result = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"],
                                cwd=ROOT, capture_output=True, text=True)
    except OSError:
        return None
    return set(result.stdout.splitlines()) if result.returncode == 0 else None


def check_scripts(fast: bool) -> bool:
    """Parse every .py file, and run every script that needs no person."""
    header("scripts")
    ok = True

    files = python_files()
    for path in files:
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as error:
            print(f"  ! {relative(path)}: {error.msg} (line {error.lineno})")
            ok = False
    print(f"  {len(files)} python files parse")

    for name in sorted(SKIP):
        if not (ROOT / name).exists():
            print(f"  ! {name}: listed in SKIP but missing, remove it from the list")
            ok = False

    scripts = sorted(
        p for folder in SCRIPT_FOLDERS for p in (ROOT / folder).rglob("*.py")
        if p in files
    )
    tests = [p for p in scripts if p.name.startswith("test_")]
    skipped = [p for p in scripts if relative(p) in SKIP]
    runnable = [p for p in scripts if p not in tests and p not in skipped]

    for path in skipped:
        print(f"  - {relative(path)}: skipped, {SKIP[relative(path)]}")
    print(f"  - {len(tests)} test_*.py files: run by pytest, not as scripts")

    if fast:
        print(f"  (--fast: not running the {len(runnable)} scripts)")
        return ok

    for path in runnable:
        name = relative(path)
        try:
            result = subprocess.run([sys.executable, str(path)], cwd=ROOT,
                                    stdin=subprocess.DEVNULL, capture_output=True,
                                    text=True, encoding="utf-8", errors="replace",
                                    env=ENV, timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            print(f"  ! FAILED {name}: still running after {TIMEOUT} seconds")
            ok = False
            continue
        if result.returncode == 0:
            print(f"  ran    {name}")
        else:
            last = (result.stderr.strip().splitlines() or ["(no error message)"])[-1]
            print(f"  ! FAILED {name}: {last[:90]}")
            ok = False

    print(f"  {len(runnable)} scripts run")
    return ok


def check_pytest() -> tuple[str, bool | None]:
    """Run the session 12 tests, and notice any test file nobody runs."""
    label = "pytest"
    header(label)
    if installed("pytest"):
        print("skipped: not installed: pytest")
        return label, None

    ok = True
    for folder in PYTEST_FOLDERS:
        if not (ROOT / folder).is_dir():
            print(f"  ! {folder}: listed in PYTEST_FOLDERS but missing")
            ok = False

    covered = PYTEST_FOLDERS + list(PYTEST_LEFT_OUT)
    for path in python_files():
        name = relative(path)
        if path.name.startswith("test_") and not any(name.startswith(f + "/") for f in covered):
            print(f"  ! {name}: a test file in no pytest folder, add its folder to the list")
            ok = False
    for folder, reason in PYTEST_LEFT_OUT.items():
        print(f"  - {folder}: left out, {reason}")

    folders = [f for f in PYTEST_FOLDERS if (ROOT / f).is_dir()]
    result = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *folders],
                            cwd=ROOT, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", env=ENV)
    output = (result.stdout + result.stderr).strip()
    show(output)
    return label, ok and result.returncode == 0


def check_git(before: set[str] | None) -> tuple[str, bool | None]:
    """Anything new in `git status` was written outside the output folders."""
    label = "git: nothing written outside output folders"
    header(label)
    after = git_status()
    if before is None or after is None:
        print("skipped: git is not available here")
        return label, None

    new = sorted(after - before)
    if not new:
        print("  working tree as it was before the scripts ran")
        return label, True
    print("  these changed while the checks ran. A script should write only to a")
    print("  gitignored output folder (or someone else was editing at the same time):")
    for line in new:
        print(f"  ! {line}")
    return label, False


def main() -> int:
    sys.stdout.reconfigure(errors="replace")
    fast = "--fast" in sys.argv
    python = sys.executable
    before = git_status()

    results = [
        run("slides", [python, "tools/check_slides.py"], needs=("playwright",)),
        run("sql", [python, "tools/check_sql.py"]),
        run("notebooks: structure", [python, "tools/nbtool.py", "check"]),
    ]

    if not fast:
        results.append(run("notebooks: execution", [python, "tools/nbtool.py", "run"],
                           needs=("nbformat", "nbclient", "ipykernel")))
    else:
        print("\n(--fast: skipping notebook execution)")

    results.append(("scripts", check_scripts(fast)))
    results.append(check_pytest())
    results.append(check_git(before))

    header("summary")
    failed = 0
    for label, outcome in results:
        if outcome is None:
            print(f"  skipped  {label}")
        elif outcome:
            print(f"  ok       {label}")
        else:
            print(f"  FAILED   {label}")
            failed += 1

    print(f"\n{f'{failed} of {len(results)} checks failed' if failed else 'everything holds together'}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
