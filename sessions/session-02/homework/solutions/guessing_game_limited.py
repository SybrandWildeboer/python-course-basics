"""HOMEWORK 1: the guessing game with a limit, worked solution."""

import random

LOWEST = 1
HIGHEST = 100
MAX_ATTEMPTS = 7

secret = random.randint(LOWEST, HIGHEST)
guesses = 0
guess = None

print(f"I am thinking of a number between {LOWEST} and {HIGHEST}.")
print(f"You have {MAX_ATTEMPTS} guesses.")

# Two reasons to keep going: they have not got it yet, AND they have attempts
# left. When either stops being true, the loop ends.
while guess != secret and guesses < MAX_ATTEMPTS:
    guess = int(input("Your guess: "))
    guesses += 1
    left = MAX_ATTEMPTS - guesses

    if guess == secret:
        print(f"Got it, {secret} in {guesses} guesses.")
    elif left == 0:
        print(f"Out of guesses. It was {secret}. Close one.")
    elif guess < secret:
        print(f"Higher. {left} {'guess' if left == 1 else 'guesses'} left.")
    else:
        print(f"Lower. {left} {'guess' if left == 1 else 'guesses'} left.")


# Two things worth noticing:
#
# 1. The order of the if branches matters. "Did they get it" has to come
#    first, otherwise a correct final guess gets told it ran out of attempts.
#    That is the session 2 ordering bug, in the wild.
#
# 2. The {'guess' if left == 1 else 'guesses'} bit fixes "1 guesses left".
#    Small, and it is the difference between a program that feels finished
#    and one that does not.
