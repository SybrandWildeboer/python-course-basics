"""Run every .sql file in the course against the database and report failures.

A query on a slide that does not actually run is worse than no query at all, so
this executes all of them. It also checks the row count of any statement that
carries a `-- expect: N rows` comment, which is how the answer files pin their
results.

    python3 tools/check_sql.py                    # every .sql file
    python3 tools/check_sql.py sessions/session-07

Read only: the connection is opened in read-only mode, so a stray UPDATE in a
file would fail loudly rather than damage the data.
"""

from __future__ import annotations

import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "music.db"

EXPECT = re.compile(r"--\s*expect:\s*(\d+)\s*rows?", re.IGNORECASE)


def statements(sql: str) -> list[tuple[str, int | None]]:
    """Split a file into (statement, expected_row_count) pairs.

    Comments are stripped before splitting on semicolons, but an `expect`
    comment is pulled out first and attached to the statement that follows it.
    """
    out: list[tuple[str, int | None]] = []
    buffer: list[str] = []
    expected: int | None = None

    for line in sql.splitlines():
        found = EXPECT.search(line)
        if found:
            expected = int(found.group(1))
        code = line.split("--")[0]
        buffer.append(code)
        if ";" in code:
            statement = "\n".join(buffer).strip().rstrip(";").strip()
            if statement:
                out.append((statement, expected))
            buffer = []
            expected = None

    leftover = "\n".join(buffer).strip().rstrip(";").strip()
    if leftover:
        out.append((leftover, expected))
    return out


def check(path: Path, con: sqlite3.Connection) -> int:
    pairs = statements(path.read_text(encoding="utf-8"))
    problems = 0

    for number, (statement, expected) in enumerate(pairs, start=1):
        one_line = " ".join(statement.split())
        try:
            rows = con.execute(statement).fetchall()
        except sqlite3.Error as error:
            print(f"  ! {path.name} statement {number}: {error}")
            print(f"      {one_line[:90]}")
            problems += 1
            continue

        if expected is not None and len(rows) != expected:
            print(f"  ! {path.name} statement {number}: expected {expected} rows, "
                  f"got {len(rows)}")
            print(f"      {one_line[:90]}")
            problems += 1

    print(f"  {path.relative_to(ROOT)}: {len(pairs)} statements"
          f"{'' if not problems else f', {problems} problems'}")
    return problems


def main() -> int:
    if not DB.exists():
        print("data/music.db is missing. Run: python3 data/scripts/build_dataset.py")
        return 1

    targets = [Path(a) for a in sys.argv[1:]] or [ROOT / "sessions"]
    files: list[Path] = []
    for target in targets:
        target = target if target.is_absolute() else ROOT / target
        files.extend(sorted(target.rglob("*.sql")) if target.is_dir() else [target])

    if not files:
        print("no .sql files found")
        return 0

    # Read only, so a stray write in a course file fails instead of landing.
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    problems = sum(check(path, con) for path in files)
    con.close()

    print(f"\n{'problems found: ' + str(problems) if problems else 'all queries run clean'}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
