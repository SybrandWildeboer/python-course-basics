"""LIVE EXERCISE: rebuild your statistics script as functions.

Take the four calculations from session 2 homework and turn each one into a
function that TAKES a list and RETURNS a number. None of the four should print
anything.

    def total(numbers)      ->  the sum
    def average(numbers)    ->  the mean
    def highest(numbers)    ->  the biggest value
    def lowest(numbers)     ->  the smallest value

Then, once they work:

    1. print one summary line that uses all four
    2. run all four on SECOND_LIST too, without copying any logic
    3. rewrite average() so it calls your own total()
    4. give every function a one-line docstring

Still no sum(), max() or min(). Loops, as before.
"""

NUMBERS = [12, 7, 41, 3, 28, 19, 7, 55, 2, 33]
SECOND_LIST = [4, 8, 15, 16, 23, 42]


# TODO: def total(numbers):
def total(list_of_numbers):
    sum = 0
    for i in list_of_numbers:
        sum += i

    return sum

print(total(NUMBERS))


# TODO: def average(numbers):
def average(list_of_numbers):
    count = 0
    # sum = 0
    # for i in list_of_numbers:
    #     sum += i
    #     count += 1
    count = len(list_of_numbers)
    sum = total(list_of_numbers)
        

    return sum/count

print(average(NUMBERS))


# TODO: def highest(numbers):
def highest(list_of_numbers):
    a = 0
    for i in list_of_numbers:
        if i > a:
            a = i

    return a

print(highest(NUMBERS))


# TODO: def lowest(numbers):
def lowest(list_of_numbers):
    a = list_of_numbers[0]
    for i in list_of_numbers:
        if i < a:
            a = i

    return a

print(lowest(NUMBERS))


# TODO: print a summary line for NUMBERS
print(f"the sum is {total(NUMBERS)}, the average is {average(NUMBERS)}, the max is {highest(NUMBERS)}, the min is {lowest(NUMBERS)}")


# TODO: print a summary line for SECOND_LIST, reusing the same functions
print(f"the sum is {total(SECOND_LIST)}, the average is {average(SECOND_LIST)}, the max is {highest(SECOND_LIST)}, the min is {lowest(SECOND_LIST)}")
