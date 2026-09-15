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
