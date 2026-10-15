"""What __name__ is, and why scripts end with the same two lines.

Run this file directly:

    python sessions/session-10/demos/name_main.py

Then run the file that imports it, and compare what gets printed:

    python sessions/session-10/demos/import_name_main.py
"""


def shout(text):
    """Return text in capitals with an exclamation mark."""
    return text.upper() + "!"


# Python sets __name__ for every file it loads. Run directly, it is the text
# "__main__". Imported, it is the file's own name, "name_main".
print("__name__ is", repr(__name__))


def main():
    """The outer layer: what should happen when this file is RUN."""
    print(shout("run as a script"))


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# Expected, run directly:
#     __name__ is '__main__'
#     RUN AS A SCRIPT!
#
# Expected, from import_name_main.py:
#     __name__ is 'name_main'
#     IMPORTED!
#
# The print at the top level ran both times: importing a file runs it. The
# line inside main() only ran when the file was the one being run. That is
# what the if buys you: a notebook, a test, or another script can import
# your functions without setting off the whole pipeline.
