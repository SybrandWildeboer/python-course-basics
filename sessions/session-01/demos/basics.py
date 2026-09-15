"""The session 1 walkthrough, in the order it appears on the slides.

Type this file yourself rather than reading it. Run it after every couple of
lines. That loop (edit, run, look) is the whole skill at this stage.
"""

# ---------------------------------------------------------------- 1. print()
print("Hello")
print("Hello", "world")      # print puts a space between the parts
print(7)
print(3 + 4)                 # the maths happens before printing: 7
print()                      # a blank line
print("Done")

# ------------------------------------------------------------- 2. variables
name = "Sam"
age = 41
print(name)
print(age)

age = age + 1                # read the right side, then store it under "age"
print(age)                   # 42

# ----------------------------------------------------------------- 3. types
print(type("Sam"))           # <class 'str'>   text
print(type(41))              # <class 'int'>   whole number
print(type(4.65))            # <class 'float'> decimal
print(type(True))            # <class 'bool'>  True or False

print(4 + 4)                 # 8   numbers add
print("4" + "4")             # 44  text joins
print(10 / 4)                # 2.5 dividing always gives a float
print(10 // 4)               # 2   whole-number division
print(10 % 4)                # 2   the remainder

# ------------------------------------------------------------- 4. f-strings
print("Hi " + name + ", you are " + str(age))   # the tedious way
print(f"Hi {name}, you are {age}")              # the good way
print(f"Next year: {age + 1}")                  # any expression fits
print(f"Shouted: {name.upper()}")

minutes = 1234.5678
print(f"{minutes:.1f} minutes")                 # 1234.6
print(f"{minutes:,.2f} minutes")                # 1,234.57

# ----------------------------------------------------------------- 5. input
# input() ALWAYS gives you text, even when the person types digits.
year_text = input("Birth year: ")
print(type(year_text))                          # <class 'str'>

year = int(year_text)                           # now it is a number
print(f"You are about {2026 - year}")

# ------------------------------------------------------------ 6. conversion
print(int("41"))        # 41
print(float("4.65"))    # 4.65
print(str(41))          # "41"
print(int(4.99))        # 4  chops, does not round
print(round(4.99))      # 5  rounds properly

# int("forty one") would stop the program with a ValueError. Try it, read the
# message, then put the # back.
