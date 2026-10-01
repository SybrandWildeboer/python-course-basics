"""HOMEWORK 2: one chart that answers one question.

Run from the repository root:

    python sessions/session-09/homework/my_chart.py

Pick a question about the listening log, and answer it with one chart saved
to output/. Ideas, if you need one: the artists with the most minutes in
2025, plays per day of the week, the countries whose artists you play most.

The checklist from the walkthrough:

    * the question, as one sentence (write it below)
    * a title that GIVES THE ANSWER, numbers formatted with :.1f
    * bars for categories, a line for time; bars start at zero
    * axis labels with units
    * fig.savefig("output/...png", dpi=150, bbox_inches="tight")
    * one sentence: what you would say about it in a meeting

A script saves its chart instead of showing it: plt.show() would open a
window and wait for you to close it.
"""

import os
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, "sessions/session-09/solutions")
from cleaning import clean_plays, load_messy

plays = clean_plays(load_messy("data/messy/plays_messy.csv"))
os.makedirs("output", exist_ok=True)

# My question:
#

# TODO: calculate the answer


# TODO: draw it, title it with the answer, save it


# What I would say about it in a meeting:
#
