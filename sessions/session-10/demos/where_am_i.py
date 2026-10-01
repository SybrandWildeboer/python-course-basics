"""Where am I? Two different answers to the same question.

Run it twice, from two different folders, and compare:

    python sessions/session-10/demos/where_am_i.py
    cd sessions/session-10
    python demos/where_am_i.py

The first line changes. The second does not. That difference is the whole
reason scripts build their paths from __file__.
"""

import os
from pathlib import Path

# ----------------------------------------------- two meanings of "here"
print("the terminal is in:   ", os.getcwd())                     # changes
print("this file lives in:   ", Path(__file__).resolve().parent)  # never changes

# A relative path is counted from the terminal's folder, so it only works
# from the repository root.
relative = Path("data/clean/plays.csv")
print("relative path found:  ", relative.exists())

# A path built from __file__ is counted from the script, so it always works.
# parents[0] is demos, [1] session-10, [2] sessions, [3] the repository root.
ROOT = Path(__file__).resolve().parents[3]
plays = ROOT / "data" / "clean" / "plays.csv"
print("__file__ path found:  ", plays.exists())


# ----------------------------------------------- a short tour of Path
# The / operator joins pieces, with the right separator for your system:
# backslashes on Windows, forward slashes on macOS. You never type either.
print()
print("name:   ", plays.name)            # plays.csv
print("stem:   ", plays.stem)            # plays
print("suffix: ", plays.suffix)          # .csv
print("parent: ", plays.parent.name)     # clean

output = ROOT / "output"
output.mkdir(exist_ok=True)              # the pathlib way of os.makedirs
print("output folder exists:", output.exists())


# ---------------------------------------------------------------------------
# Expected, from the repository root:
#     relative path found:   True
#     __file__ path found:   True
#
# Expected, from sessions/session-10:
#     relative path found:   False
#     __file__ path found:   True
#
# __file__ only exists when Python runs a file. In a notebook there is no
# file being run, so __file__ is a NameError, and notebooks in this course
# walk up from the working folder instead (the first cell of every one).
