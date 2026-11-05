"""HOMEWORK 2: a three-question summary.

Ask three questions. At least one answer must be a number that you then do
arithmetic on. Print a small paragraph that uses all three answers and reads
like a sentence a person wrote.

Ideas, if nothing comes to mind:
  * name, hours slept last night, favourite drink -> hours per week
  * city, monthly rent, number of housemates      -> cost per person per year
  * name, number of siblings, birth year          -> age, and family size

Requirements:
  * at least one int() or float() conversion
  * at least one calculation
  * output that reads like English
  * a comment at the top saying what the script does
"""

# The script you will provide a summary of your preferred activity you practice in your free time and give an estimated time spent for it per year starting for a weekly estimate.

# TODO: question 1
activity = input ("What's the actvity you like the most to do in your spare time? 'to ")
print (activity)

# TODO: question 2 (make this the numeric one)
activity_week_time = float(input("How many hours you allocate for this activity per week? "))
print (activity_week_time)

# TODO: question 3
last_time=input("When was the last time you practiced this actity? ")
print(last_time)

# TODO: the calculation
activity_year_time = activity_week_time / 7 * 364.25

# TODO: print the summary paragraph
print (f"Hi, I am Emilian and I love to {activity} in my free time. Usually, I spend around {activity_week_time:.2f} hours per week, while on a yearly bassis it would be around {activity_year_time:.1f} hours. Last time I did this was {last_time}")