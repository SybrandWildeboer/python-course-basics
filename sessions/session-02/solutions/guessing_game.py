"""LIVE EXERCISE: the guessing game, worked solution.

Written the way it ends up after the six build steps, with the cheat line
left in as a comment because it is genuinely useful while developing.
"""

import random

LOWEST = 1
HIGHEST = 100

secret = random.randint(LOWEST, HIGHEST)
# print(f"(cheat: the secret is {secret})")

guesses = 0
guess = None

print(f"I am thinking of a number between {LOWEST} and {HIGHEST}.")

while guess != secret:
    guess = int(input("Your guess: "))
    guesses += 1

    if guess < secret:
        print("Higher.")
    elif guess > secret:
        print("Lower.")

print(f"Got it, {secret} in {guesses} guesses.")


# Why "while guess != secret" rather than "while True" with a break:
#
# The condition says out loud what keeps the loop alive, so anybody reading it
# knows when it stops. That is worth the one slightly awkward line above it,
# guess = None, which exists only so the condition has something to compare on
# the very first pass.
#
# The alternative is just as respectable:
#
#     while True:
#         guess = int(input("Your guess: "))
#         guesses += 1
#         if guess == secret:
#             break
#         print("Higher." if guess < secret else "Lower.")
#
# Notice there is no "if guess == secret" in the version above. The loop
# condition already handles it: once the guess matches, the loop ends and the
# congratulations line runs. Not repeating a test is usually worth doing.
