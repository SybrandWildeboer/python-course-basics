"""The session 3 walkthrough, in slide order.

The section on return versus print is the one to slow down on. Predict what
each line prints before you run it.
"""

# # ------------------------------------------------------------ 1. def / call
# def greet():
#     print("Hello there")


# greet()          # defining taught Python the recipe; this runs it
# greet()          # and again

# print(greet)     # without brackets you get the function itself, not a call


# # ---------------------------------------------------------- 2. parameters
# def greet_person(name):
#     print(f"Hello {name}")


# greet_person("Sam")
# greet_person("Ana")


# def describe(name, age):
#     print(f"{name} is {age}")


# describe("Sam", 41)               # by position
# describe(age=41, name="Sam")      # by name, so order stops mattering


# # ------------------------------------------------- 3. return versus print
# def double_p(n):
#     print(n * 2)          # shows a human


# def double_r(n):
#     return n * 2          # hands a value back to the program


# double_p(5)               # prints 10
# result = double_p(5)      # prints 10 again, and result is None
# print(result)             # None, because print doesn't store the value. you need to use return in order to be able to store and transfer the value to a diff variable

# double_r(5)               # prints NOTHING. The value goes nowhere.
# result = double_r(5)      # the value has been transferred
# print(result)             # 10, since result now has a value coming from double_r (return stored it)
# print(double_r(5) + 1)    # 11, because there is a real number to add to
# print(double_r(double_r(3)))   # 12, feeding one into the other

# The only diff between return and direct print is that return stores the value. you could use return as a function and use print on the function, instead of defining a function as print and calling just the function

# # Uncomment to see the error the print version (vs using return) causes:
# print(double_p(25) + 1)
# # TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'


# ----------------------------------------------------------------- 4. None
# def save_it(text):
#     print(f"saving {text}")
#     # no return line, so None comes back; unless you are calling the function with the corresponding value. since the function is a print with the f formatter, the function call expects a string.


# x = save_it("hello")
# print(x, type(x))         # None <class 'NoneType'>; because I have not used return, so x doesn't have anything to read from, because print doesn't store anything

# def save_it_as_return(text):
#     return f"saving this {text}"

# x = save_it_as_return("shit")
# print(x)


# def risky(n):
#     if n > 0:
#         return "positive"
#     # falls off the end for anything else

# print(risky(5))           # positive
# print(risky(-5))          # None  <- the bug to recognise


# -------------------------------------------------------- 5. return early
# def check(age):
#     """Return a short verdict on an age. Guard clauses first."""
#     if age < 0:
#         return "not a real age"
#     if age < 18:
#         return "too young"
#     return "fine"


# print(f"{check(-3)}, while {check(12)}, while {check(41)}")


# ------------------------------------------------------------ 6. defaults
# def greeting_for(name, greeting="Hello"):
#     return f"{greeting} {name}"


# print(greeting_for("Sam")) # we have a default value for the 2nd argument
# print(greeting_for("Sam", "Morning")) # we can change the default argument by specifying a different value when calling the function
# print(greeting_for(greeting="Oi", name="Sam")) # we can change the order of the arguments, but we need to specify their names. otherwise it will conflict with the order from the function definition.


# --------------------------------------------------------------- 7. scope
# def calculate():
#     subtotal = 100            # born here, dies when the function ends!
#     return subtotal * 1.21


# print(calculate())
# print(subtotal)             # NameError: name 'subtotal' is not defined

VAT = 1.21                    # defined outside, so visible inside


# def calculate_again(amount): # this is the right way of creating a function. you add the argument inside the function so when you call the function to be able to specify a diff value of the argument each time
#     return amount * VAT


# print(calculate_again(100))


# --------------------------------------------- 8. docstrings and composing
# def total(numbers):
#     """Return the sum of a list of numbers."""
#     running = 0
#     for number in numbers:
#         running += number
#     return running

# # print (total([10,15,20]))


# def average(numbers):
#     """Return the mean of a list of numbers."""
#     return total(numbers) / len(numbers)      # reuse, do not repeat

# # print (average([5,10,17]))


# def summarise(numbers):
#     """Return one readable line describing a list of numbers.""" # this is used as a descirption of the function and can be accessed afterwards in the code with print (function's name . _doc_)
#     return (f"{len(numbers)} values, "
#             f"total {total(numbers)}, "
#             f"average {average(numbers):.1f}") # we can use as a good practice paranthesis all the time even for a singe string in return. here it is needed because I have multiple strings.


# print(summarise([12, 7, 41, 3]))
# # help(average)

# print (summarise.__doc__)


# ---------------------------------------------------- 9. checking yourself
def is_even(n):
    """Return True if n divides by 2 exactly."""
    return n % 2 == 0


assert is_even(4) is True
assert is_even(7) is False
assert is_even(0) is True      # the awkward case, checked on purpose
print("all checks passed")

# assert can be used as a validation point. if it is not respected, the code stops and Python will display an error message
