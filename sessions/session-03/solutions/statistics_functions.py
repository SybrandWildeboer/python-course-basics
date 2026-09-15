"""LIVE EXERCISE: statistics as functions, worked solution."""

NUMBERS = [12, 7, 41, 3, 28, 19, 7, 55, 2, 33]
SECOND_LIST = [4, 8, 15, 16, 23, 42]


def total(numbers):
    """Return the sum of a list of numbers."""
    running = 0
    for number in numbers:
        running += number
    return running


def average(numbers):
    """Return the mean of a list of numbers."""
    return total(numbers) / len(numbers)      # reuse total, do not repeat it


def highest(numbers):
    """Return the largest value in a list of numbers."""
    best = numbers[0]                # start with a real value from the list
    for number in numbers:
        if number > best:
            best = number
    return best


def lowest(numbers):
    """Return the smallest value in a list of numbers."""
    worst = numbers[0]
    for number in numbers:
        if number < worst:
            worst = number
    return worst


def summarise(numbers):
    """Return one readable line describing a list of numbers."""
    return (f"{len(numbers):>2} values | "
            f"total {total(numbers):>4} | "
            f"average {average(numbers):>6.1f} | "
            f"range {lowest(numbers)} to {highest(numbers)}")


# Checks on cases we can work out in our heads, including the awkward ones.
assert total([1, 2, 3]) == 6
assert average([2, 4]) == 3
assert highest([-5, -2, -9]) == -2          # the bug from last week, pinned down
assert lowest([-5, -2, -9]) == -9
assert highest([7]) == 7                    # a single value is its own max

print(summarise(NUMBERS))
print(summarise(SECOND_LIST))


# ---------------------------------------------------------------------------
# The point of the exercise is the second print.
#
# Adding a whole second set of statistics cost one line, because the logic
# lives in one place. In the session 2 version it would have meant copying
# forty lines and renaming every variable, and then any bug would exist in
# two places.
#
# Note also that nothing above summarise() prints. The functions calculate
# and hand values back; printing happens once, at the edge of the program.
# That separation is what lets you reuse them later: in session 10 these same
# shapes get called by a pipeline that writes a CSV instead of printing.
