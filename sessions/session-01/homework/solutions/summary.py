"""HOMEWORK 2 — a three-question summary — worked solution.

Asks for a name, hours slept last night and a favourite drink, then prints a
summary that projects the sleep figure out over a week.
"""

HOURS_PER_WEEK_TARGET = 56      # 8 hours a night, for comparison

name = input("What is your name? ")
hours_slept = float(input("How many hours did you sleep last night? "))
drink = input("What is your favourite drink? ")

weekly = hours_slept * 7
difference = weekly - HOURS_PER_WEEK_TARGET

print()
print(f"Right then, {name}.")
print(f"You slept {hours_slept} hours last night. At that rate you would get "
      f"{weekly:.0f} hours of sleep in a week, which is {abs(difference):.0f} hours "
      f"{'more' if difference >= 0 else 'less'} than the eight-a-night ideal.")
print(f"Either way, have a {drink.lower()} about it.")


# Notes for the curious:
#
# * The long print() is split across three lines. Python joins adjacent string
#   literals automatically, which is why each piece needs its own f prefix.
#   Splitting long lines like this keeps them readable — no line should need
#   sideways scrolling.
#
# * abs() gives the size of a number without its sign, so the sentence reads
#   correctly whether the difference is positive or negative.
#
# * The {'more' if difference >= 0 else 'less'} bit is a conditional
#   expression. You do not need it yet — it is session 2 material, sneaking in
#   early. A plain if/else would be just as good.
