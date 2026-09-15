# Python cheatsheet

Everything from sessions 1 to 4, on one page. Written in the order you met it.

---

## Printing and f-strings

```python
print("Hello")
print("Hello", "world")           # a space between the parts
print(3 + 4)                      # 7, the maths happens first

name, age = "Sam", 41
print(f"Hi {name}, you are {age}")
print(f"Next year: {age + 1}")    # any expression fits

print(f"{1234.5678:.1f}")         # 1234.6      one decimal place
print(f"{1234.5678:,.2f}")        # 1,234.57    thousands separator
print(f"{name:12}|")              # pad to 12 characters
print(f"{age:>5}|")               # right-align in 5
```

Forget the `f` and you get the literal `{name}`. It is a useful bug to recognise on sight.

## Types

| Type | Is | Example |
|---|---|---|
| `str` | text | `"Sam"` |
| `int` | whole number | `41` |
| `float` | decimal | `4.65` |
| `bool` | `True` or `False` | `True` |
| `None` | nothing here | `None` |

```python
type(4.65)            # <class 'float'>

int("41")             # 41      text -> whole number
float("4.65")         # 4.65    text -> decimal
str(41)               # "41"    number -> text
int(4.99)             # 4       CHOPS, does not round
round(4.99)           # 5       rounds properly

4 + 4                 # 8       numbers add
"4" + "4"             # "44"    text joins
10 / 4                # 2.5     always a float
10 // 4               # 2       whole-number division
10 % 4                # 2       remainder
```

`input()` **always** gives you text, even when the person types digits:

```python
year = int(input("Birth year: "))     # read inside out
```

## Deciding

```python
5 > 3, 5 == 5, 5 != 5, 5 >= 5        # comparisons give True or False
"a" == "A"                            # False, capitals matter
```

`=` puts a value in. `==` asks a question.

```python
if score >= 90:
    print("Excellent")
elif score >= 70:
    print("Good")
else:
    print("Not yet")
```

Only one branch runs, top to bottom, first `True` wins. **Order matters.**

```python
if age > 18 and member: ...
if age < 12 or age > 65: ...
if not member: ...
```

Deal with exceptions first so the happy path stays unindented:

```python
if not logged_in:
    print("Please log in")
elif banned:
    print("Banned")
else:
    print("Welcome")
```

## Repeating

```python
for i in range(5):        # 0 1 2 3 4     five numbers from zero
for i in range(1, 6):     # 1 2 3 4 5     the end is NOT included
for i in range(0, 20, 5): # 0 5 10 15     every fifth
for letter in "cat": ...
for item in my_list: ...
for i, item in enumerate(my_list): ...            # position and value
for i, item in enumerate(my_list, start=1): ...   # counting from 1
```

The accumulate pattern, which you will use forever:

```python
total = 0                 # 1. set up BEFORE the loop
for value in values:
    total += value        # 2. update INSIDE
print(total)              # 3. use AFTER
```

```python
while count > 0:
    count -= 1            # the line that ends it

break        # leave the loop entirely
continue     # skip to the next item
```

Runaway loop: `Ctrl + C` in a terminal, the interrupt button in a notebook.

## Functions

```python
def average(numbers):
    """Return the mean of a list of numbers."""
    return total(numbers) / len(numbers)


average([1, 2, 3])                    # call it, with brackets
```

**`return` hands a value back. `print` shows a human.** A function that prints is a dead
end: you can see the answer but you cannot use it.

```python
def greet(name, greeting="Hello"):    # defaults come last
    return f"{greeting} {name}"


greet("Sam")
greet("Sam", "Morning")
greet("Sam", greeting="Oi")           # by name, order stops mattering
```

Guard clauses keep logic flat:

```python
def check(age):
    if age < 0:
        return "not a real age"
    if age < 18:
        return "too young"
    return "fine"
```

No `return` means `None` comes back. Variables inside a function are invisible outside it:
pass what you need in, return the answer out.

Check yourself on cases you can work out in your head:

```python
assert is_even(0) is True        # silence means it passed
```

## Lists

```python
devices = ["phone", "laptop", "speaker", "car"]

devices[0]        # phone      counting starts at 0
devices[-1]       # car        the last one
len(devices)      # 4

nums[1:4]         # from 1, up to but NOT 4
nums[:3]          # from the start
nums[3:]          # to the end
nums[-2:]         # the last two
rows[:5]          # peek at the first five of anything

devices.append("tablet")
devices[0] = "mobile"
"phone" in devices              # True
sorted(devices)                 # a NEW sorted list
devices.sort()                  # sorts in place, returns None
```

`x = x.sort()` throws your data away.

## Dictionaries

```python
play = {"genre": "Folk", "minutes": 4.65}

play["genre"]                   # Folk
play["mood"]                    # KeyError
play.get("mood")                # None, no crash
play.get("mood", "unknown")     # a default you chose

play["device"] = "phone"        # add
"genre" in play                 # True

for key in play: ...
for value in play.values(): ...
for key, value in play.items(): ...       # the useful one
```

Counting into a dictionary:

```python
counts = {}
for row in rows:
    counts[row["genre"]] = counts.get(row["genre"], 0) + 1
```

Sorted by value, biggest first:

```python
for key, n in sorted(counts.items(), key=lambda pair: pair[1], reverse=True):
    print(f"{key:12} {n:>5}")
```

**A list of dictionaries is a table.** One dictionary is a row, one key is a column. The
`csv` module gives you this, SQL returns this, and a pandas DataFrame is this with a faster
engine underneath.

## Files and CSV

```python
import csv

with open(path, encoding="utf-8") as f:       # with closes it for you
    rows = list(csv.DictReader(f))            # list() matters, see below

rows[0]["genre"]
list(rows[0].keys())                          # the column names
```

Without `list()` you get a reader you can only walk through once, and a second loop silently
does nothing.

**Everything from a CSV is text.** `float()` or `int()` before doing arithmetic.

```python
import os
os.makedirs("output", exist_ok=True)          # "w" fails if the folder is missing

with open(out, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(filtered)
```

- `"w"` replaces the file without asking
- `newline=""` stops blank lines on Windows
- `encoding="utf-8"` so accented names survive

A list comprehension builds a new list from an old one:

```python
jazz = [row for row in rows if row["genre"] == "Jazz"]
```

## Paths that work from anywhere

```python
from pathlib import Path

HERE = Path(__file__).resolve().parent        # where THIS file lives
DATA = HERE.parent / "data" / "plays.csv"
```

First thing to print on a `FileNotFoundError`:

```python
import os
print(os.getcwd())
```

The file is nearly always fine. Python is looking somewhere else.

## Strings, the useful methods

```python
"Sam Kelly".split()           # ['Sam', 'Kelly']   splits on any whitespace
".".join(["S", "K"])          # "S.K"              separator first
" Pop ".strip()               # "Pop"
"POP".lower(), "pop".upper(), "pop".title()
"2025-04-17".startswith("2025")
"hello".replace("l", "L")
len("hello")
"hello"[0], "hello"[-1]
```

## The errors, and what they mean

| Error | Means | Usually |
|---|---|---|
| `SyntaxError` | Python cannot read the line | Missing colon, quote or bracket |
| `IndentationError` | Spacing wrong at the start of a line | Mixed tabs and spaces |
| `NameError` | A name Python has never seen | Typo, or never assigned |
| `TypeError` | Right idea, wrong types | Text where a number belongs |
| `ValueError` | Right type, impossible value | `int("forty one")` |
| `ZeroDivisionError` | Divided by zero | A count that came out empty |
| `IndexError` | List position does not exist | Off-by-one, or an empty list |
| `KeyError` | Dictionary key is not there | Typo, or an unexpected column name |
| `FileNotFoundError` | Python is looking elsewhere | Relative path, wrong folder |
| `AttributeError` mentioning `NoneType` | Something returned `None` | A function that printed instead of returning |

**Read the last line first**, then the line number. Then the middle, which shows the route in.
