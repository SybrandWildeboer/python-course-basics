"""HOMEWORK 1: four small functions, worked solution."""


def is_even(n):
    """Return True if n divides by 2 exactly."""
    return n % 2 == 0


def celsius_to_fahrenheit(c):
    """Return the Celsius temperature c converted to Fahrenheit."""
    return c * 9 / 5 + 32


def initials(full_name):
    """Return the initials of a name, as in "Sam Kelly" -> "S.K."."""
    letters = []
    for part in full_name.split():          # split() chops on whitespace
        letters.append(part[0].upper())     # [0] is the first character
    return ".".join(letters) + "."


def longest_word(sentence):
    """Return the longest word in a sentence, or "" if there are no words.

    Ties go to the first of the longest words.
    """
    best = ""
    for word in sentence.split():
        if len(word) > len(best):
            best = word
    return best


# --- checks, including the awkward cases ----------------------------------
assert is_even(4) is True
assert is_even(7) is False
assert is_even(0) is True            # zero is even, and easy to get wrong

assert celsius_to_fahrenheit(0) == 32
assert celsius_to_fahrenheit(100) == 212
assert round(celsius_to_fahrenheit(21.5), 1) == 70.7

assert initials("Sam Kelly") == "S.K."
assert initials("ana maria de vries") == "A.M.D.V."
assert initials("Prince") == "P."

assert longest_word("a bc def") == "def"
assert longest_word("all the same") == "same"    # first of the longest wins
assert longest_word("") == ""                    # no words at all

print("checks passed")


# ---------------------------------------------------------------------------
# Notes on the two that need looking up:
#
# split()  with no arguments chops a string on any run of whitespace and
#          throws away the empty pieces, so it copes with double spaces and
#          with a trailing space. split(" ") does NOT, which is why the bare
#          version is the better default.
#
# join()   is the opposite of split, and it is written back to front from how
#          most people expect: the separator goes first, and you give it the
#          list. ".".join(["S", "K"]) is "S.K".
#
# The empty-string case in longest_word is the one worth noticing. Starting
# best at "" means an empty sentence returns "" rather than crashing, and any
# real word is longer than "" so the comparison still works. Compare that to
# starting at sentence.split()[0], which raises an IndexError on empty input.
