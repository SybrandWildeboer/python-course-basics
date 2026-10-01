"""STRETCH: tests for stretch.py. The notebook says what each one needs.

    python -m pytest sessions/session-12/exercises/test_stretch.py -v

Run only the tests whose names contain a word with -k, for example:

    python -m pytest sessions/session-12/exercises/test_stretch.py -k minutes
"""

import pandas as pd
import pytest

from stretch import average, celsius_to_fahrenheit, load_rows, skip_rate, to_minutes


# --- 2. raising your own error ----------------------------------------------

# TODO: test that average([]) raises ValueError, and that the message mentions
#       an empty list. pytest.raises takes match="..." for the message.


# --- 3. floats ---------------------------------------------------------------

# TODO: celsius_to_fahrenheit(36.6) should be 97.88. Try it with == first,
#       watch it fail, then fix the TEST, not the function, with pytest.approx


# --- 4. one test, many cases -------------------------------------------------

# TODO: one test for to_minutes, run on at least five (text, expected) pairs
#       with @pytest.mark.parametrize


# --- 5. a test that needs a file ---------------------------------------------

# TODO: a test that takes tmp_path as its argument, writes a two-row CSV into
#       it, and checks what load_rows gives back


# --- 6. pandas does not raise ------------------------------------------------

# TODO: build a four-row DataFrame by hand and test skip_rate on it, including
#       a device that is not there
