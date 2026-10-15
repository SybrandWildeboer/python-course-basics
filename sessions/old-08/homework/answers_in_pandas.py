"""HOMEWORK: your session 6 answers, in pandas.

Run it from the repository root:

    python3 sessions/session-08/homework/answers_in_pandas.py

Your own sessions/session-06/homework/answers.sql is the answer key. For each
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
# TASK 2: your own two questions from session 6, in pandas.

# My question A:
# Same answer as my SQL?


# My question B:
# Same answer as my SQL?


# Easier in SQL:
# Easier in pandas:
# About the same:
#
# The one I would reach for, and when:
