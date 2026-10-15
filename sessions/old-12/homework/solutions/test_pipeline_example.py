"""HOMEWORK: a worked example of tests for project/pipeline.py.

These test the pipeline exactly as it comes out of the box, on the music
data. Yours will differ as soon as you have made the pipeline your own, so
read these for the shape, then write your own for your own functions.

Run from the repository root:

    python -m pytest sessions/session-12/homework/solutions

Copied to project/test_pipeline.py, delete the two sys.path lines below and
run, from inside project/:

    python -m pytest
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

# So this file can find project/pipeline.py from where it is stored in the
# course. In project/, next to pipeline.py, you do not need these two lines.
REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "project"))

from pipeline import INPUT, analyse, clean, load, parse_dates, parse_minutes


# --- the cleaning helpers: one test per messy form ---------------------------

def test_parse_minutes_reads_every_messy_form():
    raw = pd.Series(["4.65", "1 234.50", "4.2 min"])
    assert parse_minutes(raw).tolist() == [4.65, 1234.5, 4.2]


def test_parse_minutes_leaves_empty_text_missing():
    # A decision, pinned down: an empty value is missing, not zero.
    assert parse_minutes(pd.Series([""])).isna().all()


def test_parse_dates_reads_all_three_formats_day_first():
    raw = pd.Series(["2024-03-05", "05/03/2024", "05-03-2024"])
    expected = pd.Timestamp("2024-03-05")              # 5 March, not 3 May
    assert (parse_dates(raw) == expected).all()


# --- clean: a few rows you can check in your head -----------------------------

def messy_rows():
    """Three raw rows shaped like the messy file, two of them identical."""
    return pd.DataFrame({
        "play_id": [1, 1, 2],
        "played_at": ["2024-01-01", "2024-01-01", "02/01/2024"],
        "artist_name": ["Glass Tram", "Glass Tram", "Glass Tram"],
        "genre": ["Electronic", "Electronic", " electronic "],
        "country": ["Germany", "Germany", "Germany"],
        "device": ["phone", "phone", "PHONE "],
        "skipped": [0, 0, 1],
        "minutes played ": ["4.65", "4.65", "4.2 min"],
    })


def test_clean_drops_exact_duplicates():
    assert len(clean(messy_rows())) == 2


def test_clean_renames_the_minutes_column():
    cleaned = clean(messy_rows())
    assert "minutes_played" in cleaned.columns
    assert "minutes played " not in cleaned.columns


def test_clean_gives_each_genre_and_device_one_spelling():
    cleaned = clean(messy_rows())
    assert cleaned["genre"].nunique() == 1
    assert cleaned["device"].nunique() == 1


# --- analyse ------------------------------------------------------------------

def test_analyse_gives_one_row_per_genre_biggest_first():
    data = pd.DataFrame({
        "play_id": [1, 2, 3],
        "genre": ["Jazz", "Folk", "Jazz"],
        "minutes_played": [6.0, 3.0, 4.0],
    })
    summary = analyse(data)
    assert summary["genre"].tolist() == ["Jazz", "Folk"]
    assert summary["plays"].tolist() == [2, 1]
    assert summary["minutes"].tolist() == [10.0, 3.0]


# --- load: a missing file must not be hidden ------------------------------------

def test_load_of_a_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load(tmp_path / "not_there.csv")


# --- one test on the real thing -------------------------------------------------

def test_cleaning_the_messy_file_gives_the_clean_row_count():
    # The session 9 check, kept forever: 2,223 messy rows, 40 exact
    # duplicates, 2,183 plays, the same as data/clean/plays.csv.
    cleaned = clean(load(INPUT))
    assert len(cleaned) == len(pd.read_csv(REPO / "data" / "clean" / "plays.csv"))
