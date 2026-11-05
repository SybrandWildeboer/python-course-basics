"""HOMEWORK 1: four small functions.

Each one RETURNS its answer. None of them print.

    is_even(4)                    -> True
    celsius_to_fahrenheit(21.5)   -> 70.7
    initials("Sam Kelly")         -> "S.K."
    longest_word("a bc def")      -> "def"

Give each one a one-line docstring, and check each one with at least two
assert lines. Include the awkward cases: is_even(0), and what longest_word
should do with an empty string.

You will need to look up how to split a sentence into words. That is meant to
happen. Search for "python split string into words".
"""


# TODO: def is_even(n):
def is_even(a):
    if a % 2 == 0: 
        return True
    else: return False

print(is_even(5))


# TODO: def celsius_to_fahrenheit(c):

def celsius_to_fahrneheit(c):
    f = (c * 9 / 5 + 32)
    return f

print(celsius_to_fahrneheit(24))


# # TODO: def initials(full_name):
# def initials(full_name):
#     a = full_name[0]

#     for i in range(len(full_name)): # ca sa citesc pozitia trebuie sa folosesc range(len(x)); for i in ... citeste fiecare caracter.
#         if full_name[i]== " ":
#             i += 1
#             break
#     b = full_name[i]

#     print (f"{a}.{b}.")

# initials("Emi Grosu")

def initials(full_name):
    """Return the initials of a name, as in "Sam Kelly" -> "S.K."."""
    letters = []
    for part in full_name.split():          # split() chops on whitespace
        letters.append(part[0].upper())     # [0] is the first character
    return ".".join(letters) + "."

print(initials("Emi Grosu"))

# TODO: def longest_word(sentence):
def longest_word(sentence):
    """Return the longest word in a sentence, or "" if there are no words.

    Ties go to the first of the longest words.
    """
    best = ""
    for word in sentence.split():
        if len(word) > len(best):
            best = word
    return best

print (longest_word("as sdfdafs vsdgasdgasdgsag"))


# TODO: assert lines for all four

print("checks passed")
