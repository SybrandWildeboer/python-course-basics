"""The session 12 walkthrough, part one: errors you expect, and try / except.

Run it from any folder; the paths are built from __file__, as in session 10:

    python sessions/session-12/demos/try_except.py

Part two is pytest: statistics_functions.py and test_statistics_functions.py,
in this folder.
"""

import csv
from pathlib import Path

from statistics_functions import average

# parents[0] is demos, [1] session-12, [2] sessions, [3] the repository root.
ROOT = Path(__file__).resolve().parents[3]
PLAYS = ROOT / "data" / "clean" / "plays.csv"
MESSY = ROOT / "data" / "messy" / "plays_messy.csv"


def load_rows(path):
    """Return the CSV at path as a list of dictionaries, one per row."""
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def minutes_on(rows, device):
    """Return the minutes_played of every play on one device, as numbers."""
    return [float(row["minutes_played"]) for row in rows if row["device"] == device]


rows = load_rows(PLAYS)
phone = minutes_on(rows, "phone")
radio = minutes_on(rows, "radio")           # a device that is not in the data
print(len(phone), "plays on the phone,", len(radio), "on the radio")   # 1039, 0


# ------------------------------------------------ the empty list, for real
# average(radio)
# ZeroDivisionError: division by zero

try:
    result = average(radio)
except ZeroDivisionError:
    result = None
print("average on the radio:", result)      # None

try:
    average(radio)
except ZeroDivisionError as error:
    print("could not average:", error)      # division by zero


# ------------------------------------------------ never a bare except
# This "works", and hides a typo. The real error was a NameError.
try:
    result = averag(radio)                  # typo on purpose: averag
except:                                     # the thing not to do
    result = None
print("with a bare except and a typo:", result)    # None, and no complaint

# With the error named, the typo crashes loudly, which is what you want:
# try:
#     result = averag(radio)
# except ZeroDivisionError:
#     result = None
# NameError: name 'averag' is not defined


# ------------------------------------------------ sometimes an if is better
def safe_average(numbers):
    """Return the mean of a list, or None if the list is empty."""
    if len(numbers) == 0:
        return None
    return average(numbers)


print("safe_average:", safe_average(radio), round(safe_average(phone), 2))   # None 4.15


# ------------------------------------------------ text that may not be a number
def to_number(text):
    """Return text as a float, or None if it is not a number."""
    try:
        return float(text)
    except ValueError:
        return None


assert to_number("21.5") == 21.5
assert to_number(" -3 ") == -3.0
assert to_number("1e3") == 1000.0         # the session 3 isdigit() check refused this
assert to_number("abc") is None
assert to_number("") is None


def ask_number(prompt):
    """Ask until the person types something that is actually a number.

    The session 3 menu, without the isdigit() workaround. Not called here,
    because input() needs a person at the keyboard.
    """
    while True:
        number = to_number(input(prompt))
        if number is not None:
            return number
        print("That does not look like a number. Have another go.")


with open(MESSY, encoding="utf-8") as f:
    raw = [row["minutes played "] for row in csv.DictReader(f)]

numbers = [to_number(text) for text in raw]
good = [n for n in numbers if n is not None]
bad = [text for text, n in zip(raw, numbers) if n is None]
print(f"messy minutes: {len(good)} numbers, {len(bad)} not")       # 2033, 190
print("recoverable like '4.2 min':", sum(t.endswith(" min") for t in bad),   # 96
      "| empty:", sum(t == "" for t in bad))                                 # 94


# ------------------------------------------------ a file that is not there
# load_rows(ROOT / "data" / "clean" / "play.csv")
# FileNotFoundError: [Errno 2] No such file or directory: '.../data/clean/play.csv'
#
# Do NOT catch it inside load_rows and return []. That turns "the file is
# missing" into "the file has no plays", and every number after it lies.
# Let it travel up to the outer layer, which knows a person is waiting.

def report(path):
    """The outer layer: load, summarise, and say what happened in words."""
    try:
        rows = load_rows(path)
    except FileNotFoundError:
        return (f"No file called {path.name} in {path.parent}. "
                f"Check the spelling of the name.")
    return f"{len(rows)} plays in {path.name}"


print(report(PLAYS))                           # 2183 plays in plays.csv
print(report(PLAYS.with_name("play.csv")))     # No file called play.csv in ...


# ---------------------------------------------------------------------------
# The rule, extended from session 3:
#
#   functions that calculate return, and let errors travel;
#   only the outer layer prints, and decides what to do about errors.
#
# In a script the outer layer is main(), and stopping with a message is:
#
#   def main():
#       try:
#           rows = load_rows(PLAYS)
#       except FileNotFoundError:
#           raise SystemExit(f"No file at {PLAYS}. Check the name and the folder.")
