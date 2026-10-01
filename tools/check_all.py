"""Run every check on the course materials.

    python3 tools/check_all.py            # everything
    python3 tools/check_all.py --fast     # skip notebook execution

Four checks:

    slides      every slide fits in 1280x720, no code overflows, notes present
    sql         every query runs, and returns the row count its comment claims
    notebooks   valid JSON, no saved output, every code cell compiles
    scripts     every .py file parses, and the runnable demos actually run

The slide and notebook-execution checks need extras:

    pip install playwright nbformat nbclient ipykernel
    playwright install chromium

If those are missing, the check is reported as skipped rather than failed, so
this is still useful on a machine with only the standard library and pandas.
"""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Scripts that run start to finish with no input. Anything interactive is
# listed in SKIP below, with the reason.
RUNNABLE = [
    "sessions/session-02/demos/control_flow.py",
    "sessions/session-02/demos/errors_on_purpose.py",
    "sessions/session-03/demos/functions.py",
    "sessions/session-03/solutions/statistics_functions.py",
    "sessions/session-02/homework/solutions/statistics.py",
    "sessions/session-03/homework/solutions/small_functions.py",
    "sessions/session-04/demos/lists_and_dicts.py",
    "sessions/session-04/demos/files_and_csv.py",
    "sessions/session-04/solutions/explore_plays.py",
    "sessions/session-04/homework/solutions/filter_plays.py",
    "sessions/session-04/homework/solutions/questions.py",
    "sessions/session-08/demos/pandas_basics.py",
    "sessions/session-09/demos/clean_and_chart.py",
    "sessions/session-10/solutions/pipeline.py",
    "data/scripts/build_dataset.py",
]

SKIP = {
    "sessions/session-01/demos/basics.py": "asks for input",
    "sessions/session-01/exercises/about_me.py": "asks for input",
    "sessions/session-01/solutions/about_me.py": "asks for input",
    "sessions/session-02/exercises/guessing_game.py": "asks for input",
    "sessions/session-02/solutions/guessing_game.py": "asks for input",
    "sessions/session-03/homework/solutions/menu.py": "asks for input",
    "sessions/session-10/exercises/pipeline.py": "skeleton, raises NotImplementedError",
    "project/src/pipeline.py": "template, raises NotImplementedError",
}


def run(label: str, command: list[str]) -> tuple[str, bool | None]:
    """Run a checker and return its outcome. None means it could not run."""
    print(f"\n{'=' * 62}\n{label}\n{'=' * 62}")
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    output = (result.stdout + result.stderr).strip()

    missing = ("ModuleNotFoundError" in output
               or "Executable doesn't exist" in output
               or "playwright install" in output)
    if missing:
        print("skipped: a dependency is missing")
        print("  " + output.splitlines()[-1][:100])
        return label, None

    print(output[-2500:] if output else "(no output)")
    return label, result.returncode == 0


def check_scripts(fast: bool) -> bool:
    """Parse every .py file, and run the ones that take no input."""
    print(f"\n{'=' * 62}\nscripts\n{'=' * 62}")

    ok = True
    files = sorted(p for p in ROOT.rglob("*.py") if ".git" not in p.parts)
    for path in files:
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as error:
            print(f"  ! {path.relative_to(ROOT)}: {error.msg} (line {error.lineno})")
            ok = False
    print(f"  {len(files)} python files parse")

    for name, reason in sorted(SKIP.items()):
        print(f"  - {name}: skipped, {reason}")

    if fast:
        print("  (--fast: not running them)")
        return ok

    for name in RUNNABLE:
        path = ROOT / name
        if not path.exists():
            print(f"  ! {name}: missing")
            ok = False
            continue
        result = subprocess.run([sys.executable, str(path)], cwd=ROOT,
                                capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"  ran   {name}")
        else:
            last = (result.stderr.strip().splitlines() or ["?"])[-1]
            print(f"  ! FAILED {name}: {last[:90]}")
            ok = False

    return ok


def main() -> int:
    fast = "--fast" in sys.argv
    python = sys.executable

    results = [
        run("slides", [python, "tools/check_slides.py"]),
        run("sql", [python, "tools/check_sql.py"]),
        run("notebooks: structure", [python, "tools/nbtool.py", "check"]),
    ]

    if not fast:
        results.append(run("notebooks: execution", [python, "tools/nbtool.py", "run"]))
    else:
        print("\n(--fast: skipping notebook execution)")

    results.append(("scripts", check_scripts(fast)))

    print(f"\n{'=' * 62}\nsummary\n{'=' * 62}")
    failed = 0
    for label, outcome in results:
        if outcome is None:
            print(f"  skipped  {label}")
        elif outcome:
            print(f"  ok       {label}")
        else:
            print(f"  FAILED   {label}")
            failed += 1

    print()
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
