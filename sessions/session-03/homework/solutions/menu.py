"""HOMEWORK 2: the menu program, worked solution.

Run it from this folder so the import finds small_functions.py:

    cd sessions/session-03/homework/solutions
    python3 menu.py
"""

from small_functions import (
    celsius_to_fahrenheit,
    initials,
    is_even,
    longest_word,
)

MENU = """
1. Is a number even?
2. Celsius to Fahrenheit
3. Initials from a name
4. Longest word in a sentence
5. Quit
"""


def ask_number(prompt):
    """Ask until the person types something that is actually a number.

    This is the awkward bit of the homework. str.replace and .isdigit() get us
    there without try/except, which is session 12 material. It is not elegant,
    and knowing that it is not elegant is worth as much as the code.
    """
    while True:
        answer = input(prompt).strip()
        if answer.lstrip("-").replace(".", "", 1).isdigit():
            return float(answer)
        print("That does not look like a number. Have another go.")


def main():
    """Run the menu until the user quits."""
    while True:
        print(MENU)
        choice = input("Pick an option: ").strip()

        if choice == "1":
            number = ask_number("A whole number: ")
            print(f"{number:.0f} is {'even' if is_even(number) else 'odd'}")

        elif choice == "2":
            celsius = ask_number("Temperature in Celsius: ")
            print(f"{celsius}C is {celsius_to_fahrenheit(celsius):.1f}F")

        elif choice == "3":
            name = input("Full name: ")
            print(f"Initials: {initials(name)}")

        elif choice == "4":
            sentence = input("A sentence: ")
            word = longest_word(sentence)
            print(f"Longest word: {word!r} ({len(word)} letters)")

        elif choice == "5":
            print("Bye.")
            return

        else:
            print("That is not one of the options. Try again.")


main()


# ---------------------------------------------------------------------------
# Two things to notice about the shape of this file:
#
# 1. The four functions are imported, not rewritten. If you fix a bug in
#    small_functions.py, this program gets the fix for free. That is the
#    whole argument for functions in one sentence.
#
# 2. All the printing lives in main(), and none of it lives in the four
#    functions. That is why they are reusable here at all: is_even() does not
#    care whether its answer ends up on screen, in a file, or in a chart.
#
# The chain of elif works fine for five options and starts to sag at fifteen.
# Next session brings dictionaries, which turn a menu like this into a lookup
# table instead of a ladder.
