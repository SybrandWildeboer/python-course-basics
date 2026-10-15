"""The four statistics functions from session 3, as a module other files can import.

These are the exact functions from sessions/session-03/solutions/statistics_functions.py,
with one change: the asserts and the two summary prints at the bottom are gone.

Why remove them? Because `import statistics_functions` runs the whole file. In the
session 3 version that means every import prints two summary lines and reruns the
checks. A module that other code imports should only *define* things. The checks now
live in test_statistics_functions.py, next door, where pytest runs them.
"""


def total(numbers):
    """Return the sum of a list of numbers."""
    running = 0
    for number in numbers:
        running += number
    return running


def average(numbers):
    """Return the mean of a list of numbers.

    An empty list raises ZeroDivisionError. That is deliberate: there is no
    average of nothing, and a crash is more honest than a made-up 0.
    """
    return total(numbers) / len(numbers)


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
