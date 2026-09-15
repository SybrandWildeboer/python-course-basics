"""Build, check and run the course notebooks.

The notebooks are the main way the learner works, so they need to be correct,
and "correct" means three things: valid JSON, no stale saved output cluttering
up git, and every cell actually runs.

    python3 tools/nbtool.py check          # structure and syntax, fast
    python3 tools/nbtool.py run            # execute every notebook, slower
    python3 tools/nbtool.py run sessions/session-04
    python3 tools/nbtool.py convert file.py   # percent format -> .ipynb
    python3 tools/nbtool.py strip            # remove saved outputs

Notebook sources are written in "percent format", which is a plain .py file
with cell markers:

    # %% [markdown]
    # # A heading
    # Some prose, one comment line per line of markdown.

    # %%
    print("a code cell")

That format is readable in a diff, runs as an ordinary script, and converts to
a real .ipynb with `convert`. It is the same convention jupytext uses, so
editors that understand jupytext will pair the files automatically.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

KERNELSPEC = {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3",
}


# --------------------------------------------------------------------------
# building


def _cell(kind: str, source: str, index: int) -> dict:
    lines = source.splitlines(keepends=True)
    common = {"id": f"cell-{index:03d}", "metadata": {}, "source": lines}
    if kind == "markdown":
        return {"cell_type": "markdown", **common}
    return {"cell_type": "code", "execution_count": None, "outputs": [], **common}


def from_percent(text: str) -> dict:
    """Turn percent-format source into a notebook dictionary."""
    cells: list[tuple[str, list[str]]] = []
    kind = "code"
    buffer: list[str] = []

    def flush() -> None:
        if not buffer:
            return
        while buffer and not buffer[-1].strip():
            buffer.pop()
        if buffer:
            cells.append((kind, list(buffer)))
        buffer.clear()

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# %%"):
            flush()
            kind = "markdown" if "[markdown]" in stripped else "code"
            continue
        if kind == "markdown":
            # Markdown lines are comments in the .py form; undo that here.
            if stripped == "#":
                buffer.append("")
            elif line.startswith("# "):
                buffer.append(line[2:])
            elif stripped.startswith("#"):
                buffer.append(line.lstrip("#").lstrip())
            else:
                buffer.append(line)
        else:
            buffer.append(line)
    flush()

    return {
        "cells": [_cell(k, "\n".join(src), i) for i, (k, src) in enumerate(cells)],
        "metadata": {
            "kernelspec": KERNELSPEC,
            "language_info": {"name": "python", "version": "3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write(path: Path, notebook: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n",
                    encoding="utf-8")


# --------------------------------------------------------------------------
# checking


def notebooks(targets: list[str]) -> list[Path]:
    paths: list[Path] = []
    for target in targets or ["."]:
        base = Path(target)
        base = base if base.is_absolute() else ROOT / base
        if base.is_dir():
            paths.extend(sorted(p for p in base.rglob("*.ipynb")
                                if ".ipynb_checkpoints" not in p.parts))
        elif base.suffix == ".ipynb":
            paths.append(base)
    return paths


def label_for(path: Path) -> str:
    """A short, readable name for a path, which may sit outside the repo."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def check(paths: list[Path]) -> int:
    problems = 0
    for path in paths:
        label = label_for(path)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            print(f"  ! {label}: not valid JSON, {error}")
            problems += 1
            continue

        cells = data.get("cells", [])
        if not cells:
            print(f"  ! {label}: no cells")
            problems += 1

        saved_output = sum(1 for c in cells if c.get("outputs"))
        if saved_output:
            print(f"  ! {label}: {saved_output} cells have saved output "
                  f"(run: nbtool.py strip)")
            problems += 1

        for number, cell in enumerate(cells, start=1):
            if cell.get("cell_type") != "code":
                continue
            code = "".join(cell.get("source", []))
            if code.strip().startswith("!") or code.strip().startswith("%"):
                continue          # a shell or magic line, not plain Python
            try:
                compile(code, f"{label}:cell{number}", "exec")
            except SyntaxError as error:
                print(f"  ! {label} cell {number}: {error.msg} (line {error.lineno})")
                problems += 1

        code_cells = sum(1 for c in cells if c.get("cell_type") == "code")
        md_cells = len(cells) - code_cells
        print(f"  {label}: {code_cells} code, {md_cells} markdown")

    return problems


def strip(paths: list[Path]) -> int:
    """Remove saved outputs, so notebooks stay small and diffable in git."""
    changed = 0
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        touched = False
        for cell in data.get("cells", []):
            if cell.get("cell_type") != "code":
                continue
            if cell.get("outputs") or cell.get("execution_count") is not None:
                cell["outputs"] = []
                cell["execution_count"] = None
                touched = True
        if touched:
            write(path, data)
            print(f"  stripped {label_for(path)}")
            changed += 1
    print(f"{changed} notebooks stripped")
    return 0


def run(paths: list[Path]) -> int:
    """Execute every notebook and report the ones that fail.

    Notebooks are executed with the repository root as the working directory,
    because that is where the course tells the learner to run things from, and
    every data path in them is relative to it.
    """
    try:
        import nbformat
        from nbclient import NotebookClient
        from nbclient.exceptions import CellExecutionError
    except ImportError:
        print("nbformat and nbclient are needed for run:")
        print("    pip install nbformat nbclient ipykernel")
        return 1

    problems = 0
    for path in paths:
        label = label_for(path)
        # Starter notebooks are meant to be full of TODOs, so running them
        # proves nothing. They are named so we can skip them.
        if path.stem.endswith("-exercise") or path.stem.endswith("-homework"):
            print(f"  {label}: skipped (starter notebook)")
            continue

        book = nbformat.read(path, as_version=4)
        client = NotebookClient(book, timeout=120, kernel_name="python3",
                                resources={"metadata": {"path": str(ROOT)}})
        try:
            client.execute()
            print(f"  {label}: ran clean")
        except CellExecutionError as error:
            first = str(error).strip().splitlines()[-1] if str(error).strip() else "?"
            print(f"  ! {label}: {first[:130]}")
            problems += 1
        except Exception as error:                      # noqa: BLE001
            print(f"  ! {label}: {type(error).__name__}: {error}")
            problems += 1

    return problems


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    command, *rest = sys.argv[1:]

    if command == "convert":
        if not rest:
            print("convert needs a percent-format .py file")
            return 1
        for name in rest:
            source = Path(name)
            target = source.with_suffix(".ipynb")
            write(target, from_percent(source.read_text(encoding="utf-8")))
            print(f"  wrote {target}")
        return 0

    paths = notebooks(rest)
    if not paths:
        print("no notebooks found")
        return 0

    if command == "check":
        problems = check(paths)
    elif command == "run":
        problems = run(paths)
    elif command == "strip":
        return strip(paths)
    else:
        print(f"unknown command: {command}")
        return 1

    print(f"\n{'problems found: ' + str(problems) if problems else 'notebooks clean'}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
