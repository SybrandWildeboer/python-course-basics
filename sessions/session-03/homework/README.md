# Session 3 homework

Budget: 2 to 4 hours. **Saturday:** one line, `Homework done` or `Homework not done`.

Every function you write this week should **return** its answer. None of them should print.
The only printing happens in the code that calls them.

---

## Task 1: Four small functions

In `small_functions.py`, write these four:

| Function | Given | Returns |
|---|---|---|
| `is_even(n)` | `4` | `True` |
| `celsius_to_fahrenheit(c)` | `21.5` | `70.7` |
| `initials(full_name)` | `"Sam Kelly"` | `"S.K."` |
| `longest_word(sentence)` | `"a bc def"` | `"def"` |

Requirements:

- each one has a one-line docstring saying what it returns,
- each one is checked with at least two `assert` lines,
- include the awkward cases: what should `is_even(0)` say? What does
  `longest_word("")` do?

**You will need to look something up.** `longest_word` needs a way to chop a sentence into
words. Search for "python split string into words". That is part of the exercise, not
cheating: looking things up as you need them is what programming actually is.

## Task 2: A menu program

In `menu.py`, write a small program that:

1. prints a numbered menu of the four functions,
2. asks the user to pick one,
3. asks for whatever input that function needs,
4. prints the result,
5. loops until they choose quit.

```
1. Is a number even?
2. Celsius to Fahrenheit
3. Initials from a name
4. Longest word in a sentence
5. Quit

Pick an option: 2
Temperature in Celsius: 21.5
21.5C is 70.7F

Pick an option: 9
That is not one of the options. Try again.

Pick an option: 5
Bye.
```

Requirements:

- `import` your functions or copy them in, but do not rewrite them,
- a bad option gets a polite message and another go, rather than a crash,
- typing a word where a number is expected should not take the whole program down.
  (That last one is genuinely hard right now. If you get it, excellent. If you decide it
  needs a tool you do not have yet, you are right: it is `try` / `except`, and it is on the
  map for session 12.)

---

## The one thing to check before you send "done"

Search your files for `print` inside a function definition. If you find one in the four
functions from task 1, that function is a dead end: you can see its answer but the menu
program cannot use it.
