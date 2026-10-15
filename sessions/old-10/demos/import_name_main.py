"""Import name_main.py, and watch which of its lines run.

    python sessions/session-10/demos/import_name_main.py

Python looks for imports next to the file being run, so this finds
name_main.py whichever folder your terminal is in.
"""

import name_main

print(name_main.shout("imported"))
