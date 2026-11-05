"""HOMEWORK 1: the guessing game, with a limit of seven attempts.

Start from your working guessing game and add:

    1. a maximum of 7 attempts
    2. a message after each wrong guess saying how many are left
    3. a kind message with the answer when they run out

Hint: you now have two reasons to stop looping, "they got it" and "they ran
out". Your while condition needs to cover both, and "and" is the word you
want.
"""

import random

MAX_ATTEMPTS = 7

secret = random.randint(1, 100)

# TODO: your game, with the attempt limit

count = 1
guess = int(input("take a guess "))

while guess != secret and count < MAX_ATTEMPTS:
    if guess > secret: 
        print("lower")
    else: print("higher")

    count += 1

    print(f"you have {MAX_ATTEMPTS - count} tries left")

    guess = int(input("take another guess "))

# print (f"you didn't find it") - whenever the while loop condition is broken it takes me out so I need to define a continuation.

if guess == secret:
    print (f"you got it after {count} tries, the number was {secret}")
else: 
    print(f"You have run out of tries. The answer was {secret}")


# while count < 6:
#     if guess == secret:
#         print("you got it")
#         break
#     elif guess < secret:
#         print("higher")
#     else: print("lower")

#     print(f"you have {MAX_ATTEMPTS-count-1} tries left")

#     count += 1

#     guess = int(input("take another guess "))
  
#     if count == 6: print(f"you have run out of tries")