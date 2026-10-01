"""HOMEWORK: a starter for project/test_pipeline.py.

Copy this file to project/test_pipeline.py, next to pipeline.py, delete the
two sys.path lines, and change the import to name your own functions. Then,
with the project's virtual environment active, from inside project/:

    python -m pip install pytest      (once)
    python -m pytest

Aim for at least five tests:

  * one for each cleaning decision you wrote in clean()'s docstring
  * one for analyse(), on three or four rows you made up, where you know the
    right answer without a calculator
  * one that checks an error DOES happen: load() on a missing file
  * one on your real data, checking a number you have verified another way

The example below is written for the pipeline as it comes out of the box.
"""

import sys
from pathlib import Path

import pandas as pd

# So this file can find project/pipeline.py from where it is stored in the
# course. In project/, next to pipeline.py, you do not need these two lines.
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "project"))

from pipeline import parse_minutes      # TODO: import your own functions


def test_parse_minutes_reads_a_plain_number():
    assert parse_minutes(pd.Series(["4.65"])).tolist() == [4.65]


# TODO: a test for each cleaning decision


# TODO: a test for analyse() on a tiny DataFrame you build by hand


# TODO: a test that load() on a missing file raises FileNotFoundError
#       (look up the tmp_path fixture, or see the stretch notebook)


# TODO: one test on your real data
