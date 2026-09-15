"""HOMEWORK 1 — temperature converter — worked solution."""

celsius_text = input("Temperature in Celsius: ")

# float(), not int(): 21.5 is a perfectly reasonable temperature and int()
# would refuse it with a ValueError.
celsius = float(celsius_text)

fahrenheit = celsius * 9 / 5 + 32

# The stretch goal: :.1f means "a float, one digit after the point".
print(f"{celsius}°C is {fahrenheit:.1f}°F")


# Two things worth noticing:
#
# 1. Operator precedence does the right thing here. Python works out
#    celsius * 9 / 5 before adding 32, exactly as the maths intends. If you
#    are ever unsure, add brackets — (celsius * 9 / 5) + 32 — they cost
#    nothing and make the intent obvious.
#
# 2. int() would have thrown away the decimal part. float() keeps it.
#    Try int("21.5") to see it fail, then put the # back.
