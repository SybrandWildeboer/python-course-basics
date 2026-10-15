"""HOMEWORK, task 1: your session 5 answers, in pandas.

Run it from the repository root:

    python sessions/session-06/homework/answers_in_pandas.py

Your own answers.sql from the session 5 homework is the answer key. For each
question, write the pandas version, print the answer, and check it matches
your SQL. If it does not, find out which one is wrong.

In a script nothing shows unless you print() it.
"""

import pandas as pd

pd.set_option("display.width", 120)

plays = pd.read_csv("data/clean/plays.csv")
artists = pd.read_csv("data/clean/artists.csv")

print(plays.shape, artists.shape)


# 1. How many artists are in the database?


# 2. Which artists are from the Netherlands? Show name and genre.


# 3. Which artists have an unknown formed_year?
#    (Look at artists.dtypes first. Why is formed_year a decimal?)


# 4. What are the five longest plays? Show the track and the minutes.


# 5. How many plays happened in 2024, and how many in 2025?
#    (plays["played_at"].str[:4] slices every date at once.)


# 6. Which tracks were played more than 40 times? Most played first.


# 7. What is the total listening time in minutes for each device,
#    rounded to a whole number?


# 8. Which genres have five or more artists?


# 9. What proportion of plays on each device were skipped?
#    Show device, total plays, skipped plays, and the percentage to one
#    decimal place.


# 10. What was the busiest single day, by number of plays?


# ---------------------------------------------------------------------------
# Your join-type question from task 3 of the session 5 homework, in pandas,
# once with how="inner" and once with how="left". awards.csv is in data/clean.

# My question:
# Same two answers as my SQL?


# Easier in SQL:
# Easier in pandas:
# About the same:
#
# The one I would reach for, and when:
