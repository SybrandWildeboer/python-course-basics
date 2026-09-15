"""LIVE EXERCISE: about me, worked solution.

Do not open this until you have had a real attempt. Reading a solution feels
like learning and is not.
"""

CURRENT_YEAR = 2026

name = input("What is your name? ")
birth_year = int(input("What year were you born? "))

# "About", because we do not know whether their birthday has happened yet.
age = CURRENT_YEAR - birth_year

print(f"Hello {name}, you are about {age} years old.")

# The extras
print(f"In 2030 you will be about {2030 - birth_year}.")
print(f"Shouting your name: {name.upper()}")


# A note on why int() is on the outside:
#
#   birth_year = int(input("What year were you born? "))
#                ^^^      ^^^^^^^
#                 2         1
#
# Step 1 runs first: input() collects text like "1985".
# Step 2 wraps it: int("1985") gives the number 1985.
#
# Without the int(), the next line would fail with:
#   TypeError: unsupported operand type(s) for -: 'int' and 'str'
