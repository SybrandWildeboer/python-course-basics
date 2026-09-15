"""The session 2 walkthrough, in slide order.

Type it, run it, change the values at the top and run it again. Seeing a
different branch fire because you changed one number is the whole idea.
"""

# ------------------------------------------------------- 1. comparisons
print(5 > 3)          # True
print(5 == 5)         # True   equal?
print(5 != 5)         # False  not equal?
print("a" == "A")     # False  capitals matter

# One = puts a value in a variable. Two == asks a question.
age = 41
print(age > 18)       # True

# ---------------------------------------------------------------- 2. if
temperature = 31

if temperature > 25:
    print("Warm out")
    print("Take water")

print("This always runs")      # not indented, so not part of the if

# ------------------------------------------------------- 3. elif / else
score = 72

if score >= 90:
    print("Excellent")
elif score >= 70:
    print("Good")
elif score >= 50:
    print("Pass")
else:
    print("Not yet")

# Order matters. Move the >= 50 test to the top and a 95 becomes a "Pass".
# Try it: the program still runs perfectly and the answer is wrong.

# ------------------------------------------------- 4. and / or / not
member = True

if age > 18 and member:
    print("Full access")

if age < 12 or age > 65:
    print("Reduced price")

if not member:
    print("Please sign up")

# ---------------------------------------------------- 5. for and range
for i in range(5):
    print(i)              # 0 1 2 3 4   five numbers, starting at zero

for i in range(1, 6):
    print(i)              # 1 2 3 4 5   the end is NOT included

for i in range(0, 20, 5):
    print(i)              # 0 5 10 15   every fifth number

for letter in "cat":
    print(letter)         # c a t

# ------------------------------------------------------ 6. accumulating
total = 0                 # 1. set up before the loop
for i in range(1, 11):
    total += i            # 2. update inside the loop
print(total)              # 3. use after the loop   -> 55

# Move total = 0 inside the loop to see the classic bug: it resets every
# time round, and the answer becomes just the last number.

# ------------------------------------------------------------- 7. while
count = 3
while count > 0:
    print(count)
    count -= 1            # without this line it never ends
print("Go")

# ------------------------------------------------ 8. break and continue
for i in range(1, 100):
    if i * i > 50:
        print(f"{i} squared passes 50")
        break             # found it, stop looping

for i in range(1, 11):
    if i % 2 == 0:
        continue          # skip the even ones
    print(i)              # 1 3 5 7 9
