"""HOMEWORK 2: statistics by hand, worked solution.

Total, average, highest and lowest with loops only.
"""

numbers = [12, 7, 41, 3, 28, 19, 7, 55, 2, 33]

# The total: start at zero, add each number in turn.
total = 0
for number in numbers:
    total += number

# The average: the total divided by how many there are. len() counts the list.
average = total / len(numbers)

# The highest: start by assuming the FIRST number is the winner, then replace
# it whenever we meet something bigger.
highest = numbers[0]
for number in numbers:
    if number > highest:
        highest = number

# The lowest: the same idea, with the comparison flipped.
lowest = numbers[0]
for number in numbers:
    if number < lowest:
        lowest = number

print(f"Count:   {len(numbers)}")
print(f"Total:   {total}")
print(f"Average: {average:.1f}")
print(f"Highest: {highest}")
print(f"Lowest:  {lowest}")

# The stretch goal: how many are above the average.
above = 0
for number in numbers:
    if number > average:
        above += 1
print(f"{above} of {len(numbers)} numbers are above the average")


# ---------------------------------------------------------------------------
# Why "highest = numbers[0]" and not "highest = 0"
#
# Starting at zero works for this list, purely by luck, because every number
# in it is positive. Try it with:
#
#     numbers = [-5, -2, -9]
#
# Nothing in that list is bigger than 0, so the if never fires and the answer
# comes out as 0, which is not even one of the numbers. The bug does not
# crash, it just quietly lies. Those are the expensive ones.
#
# Starting with the first item of the list cannot have that problem: the
# answer is always a number that was actually in the data. The same trick
# works for lowest.
#
# (In real code you would write max(numbers) and min(numbers), and they do
# exactly this internally. Writing it once by hand is the point of the
# exercise.)
#
# One edge case: numbers[0] fails on an empty list with an IndexError, and
# total / len(numbers) fails with a ZeroDivisionError. Session 12 talks about
# handling that properly with try/except.
