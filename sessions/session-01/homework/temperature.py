"""HOMEWORK 1: temperature converter.

Ask for a temperature in Celsius, print it in Fahrenheit.

    F = C * 9/5 + 32

Stretch goal: print the Fahrenheit value to one decimal place.
"""

# TODO: ask for a temperature in Celsius and convert it to a number.
#       Careful: 21.5 is not a whole number, so int() is the wrong tool here.

# TODO: work out the Fahrenheit value.

# TODO: print one sentence containing both numbers.

temp_c = float(input("Give me the temperature in Celsius degrees "))
print (temp_c)

temp_f = temp_c * 9/5 + 32
print (f" {temp_f:.1f}")

print (f"The temperature in Celsius degrees is {temp_c}, while in Fahrenheit is {temp_f:.1f}")