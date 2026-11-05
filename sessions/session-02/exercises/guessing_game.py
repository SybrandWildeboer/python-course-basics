"""LIVE EXERCISE: the guessing game.

The computer picks a number from 1 to 100. You keep guessing. It tells you
higher or lower, and when you get it, it says how many guesses you took.

Build it in six steps and RUN IT after every single one:

    1. pick a secret number and print it (cheat mode, so you can debug)
    2. ask for one guess and say whether it is right
    3. wrap step 2 in a while loop so it keeps asking
    4. add the higher / lower feedback
    5. count the guesses, and report the count when they win
    6. delete the cheat print

The only new thing you need is at the top: random.randint(1, 100) gives you a
whole number from 1 to 100, and unlike range() it DOES include 100.
"""

import random

secret = random.randint(1, 100)

# TODO step 1: print the secret while you are building (remove this at the end)

# TODO step 2: ask for a guess. Remember input() gives you text, and you need
#              a number to compare it with.
guess = int(input("take a guess "))

# TODO step 3: put it in a while loop that keeps going until the guess is right
# while secret != guess:
#     guess = int(input("take another guess "))
# print("You guessed the number")

# TODO step 4: inside the loop, say "higher" or "lower"
# while secret != guess:
#     if (guess > secret): 
#         print ("Lower") 
#     else: 
#         print ("Higher")
#     guess = int(input("take another guess "))

# TODO step 5: count the guesses and print the total when they win
count = 0
while secret != guess:
    count += 1
    if (guess > secret): 
        print ("Lower") 
    else: 
        print ("Higher")
    guess = int(input("take another guess "))
print (f"It took you {count} tries ")