"""The session 3 walkthrough, in slide order.

The section on return versus print is the one to slow down on. Predict what
each line prints before you run it.
"""

# ------------------------------------------------------------ 1. def / call
def greet():
    print("Hello there")


greet()          # defining taught Python the recipe; this runs it
greet()          # and again

print(greet)     # without brackets you get the function itself, not a call


# ---------------------------------------------------------- 2. parameters
def greet_person(name):
    print(f"Hello {name}")


greet_person("Sam")
greet_person("Ana")


def describe(name, age):
    print(f"{name} is {age}")


describe("Sam", 41)               # by position
describe(age=41, name="Sam")      # by name, so order stops mattering


# ------------------------------------------------- 3. return versus print
def double_p(n):
    print(n * 2)          # shows a human


def double_r(n):
    return n * 2          # hands a value back to the program


double_p(5)               # prints 10
result = double_p(5)      # prints 10 again, and result is None
print(result)             # None

double_r(5)               # prints NOTHING. The value goes nowhere.
result = double_r(5)
print(result)             # 10
print(double_r(5) + 1)    # 11, because there is a real number to add to
print(double_r(double_r(3)))   # 12, feeding one into the other

# Uncomment to see the error the print version causes:
# print(double_p(5) + 1)
# TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'


# ----------------------------------------------------------------- 4. None
def save_it(text):
    print(f"saving {text}")
    # no return line, so None comes back


x = save_it("hello")
print(x, type(x))         # None <class 'NoneType'>


def risky(n):
    if n > 0:
        return "positive"
    # falls off the end for anything else


print(risky(5))           # positive
print(risky(-5))          # None  <- the bug to recognise


# -------------------------------------------------------- 5. return early
def check(age):
    """Return a short verdict on an age. Guard clauses first."""
    if age < 0:
        return "not a real age"
    if age < 18:
        return "too young"
    return "fine"


print(check(-3), check(12), check(41))


# ------------------------------------------------------------ 6. defaults
def greeting_for(name, greeting="Hello"):
    return f"{greeting} {name}"


print(greeting_for("Sam"))
print(greeting_for("Sam", "Morning"))
print(greeting_for("Sam", greeting="Oi"))


# --------------------------------------------------------------- 7. scope
def calculate():
    subtotal = 100            # born here, dies when the function ends
    return subtotal * 1.21


print(calculate())
# print(subtotal)             # NameError: name 'subtotal' is not defined

VAT = 1.21                    # defined outside, so visible inside


def calculate_again(amount):
    return amount * VAT


print(calculate_again(100))


# --------------------------------------------- 8. docstrings and composing
def total(numbers):
    """Return the sum of a list of numbers."""
    running = 0
    for number in numbers:
        running += number
    return running


def average(numbers):
    """Return the mean of a list of numbers."""
    return total(numbers) / len(numbers)      # reuse, do not repeat


def summarise(numbers):
    """Return one readable line describing a list of numbers."""
    return (f"{len(numbers)} values, "
            f"total {total(numbers)}, "
            f"average {average(numbers):.1f}")


print(summarise([12, 7, 41, 3]))
help(average)


# ---------------------------------------------------- 9. checking yourself
def is_even(n):
    """Return True if n divides by 2 exactly."""
    return n % 2 == 0


assert is_even(4) is True
assert is_even(7) is False
assert is_even(0) is True      # the awkward case, checked on purpose
print("all checks passed")
