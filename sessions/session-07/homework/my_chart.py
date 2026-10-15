"""HOMEWORK 1: one chart that answers one question.

Run from the repository root:

    python sessions/session-07/homework/my_chart.py

Pick a question about the listening log, and answer it with one chart saved
to output/. Ideas, if you need one: the artists with the most minutes in
2025, plays per day of the week, the countries whose artists you play most,
bands that are still active against bands that have split up.

The checklist from the walkthrough:

    * the question, as one sentence (write it below)
    * the right kind of chart for that kind of question
    * a title that GIVES THE ANSWER, numbers formatted with :.1f
    * bars start at zero; axis labels with units
    * colour that means something, and a reader who could do without it
    * fig.savefig("output/...png", dpi=150, bbox_inches="tight")
    * one sentence: what you would say about it in a meeting
    * one more sentence: what this chart does NOT show

A script saves its chart instead of showing it: plt.show() would open a
window and wait for you to close it.
"""

import os

import matplotlib.pyplot as plt
import pandas as pd

plays = pd.read_csv("data/clean/plays.csv")
artists = pd.read_csv("data/clean/artists.csv")
os.makedirs("output", exist_ok=True)

# My question:
#

# TODO: calculate the answer


# TODO: draw it, title it with the answer, save it


# What I would say about it in a meeting:
#

# What this chart does not show:
#
