"""The session 8 material as a plain script, for comparison with the notebook.

The notebook is the better tool for this session: you want to look at each
table as it appears. This file exists so you can see what the same work looks
like in the other shape.

Notice what changes:
  * every result needs an explicit print(), because there is no cell output
  * the tables are harder to read, so .to_string() earns its keep
  * you cannot poke at an intermediate result without editing and re-running
  * but it runs start to finish in one command, unattended, every time

Run it from the repository root:

    python3 sessions/session-08/demos/pandas_basics.py
"""

import sqlite3

import pandas as pd

CSV = "data/clean/plays.csv"
DB = "data/music.db"

pd.set_option("display.width", 110)


def load_from_csv(path=CSV):
    """Return the listening log from the CSV, with real dates."""
    return pd.read_csv(path, parse_dates=["played_at"])


def load_from_db(path=DB):
    """Return (plays, artists, awards) from the SQLite database."""
    con = sqlite3.connect(path)
    try:
        plays = pd.read_sql("SELECT * FROM plays", con, parse_dates=["played_at"])
        artists = pd.read_sql("SELECT * FROM artists", con)
        awards = pd.read_sql("SELECT * FROM awards", con)
    finally:
        con.close()          # a script should tidy up after itself
    return plays, artists, awards


def orient(plays):
    """Print the first-five-minutes summary of any new table."""
    print(f"shape: {plays.shape}")
    print(f"\ndtypes:\n{plays.dtypes}")
    print(f"\nhead:\n{plays.head(3).to_string()}")
    print(f"\ndescribe:\n{plays.describe().round(2).to_string()}")


def by_device(plays):
    """Return plays, total and average minutes for each device."""
    return (plays.groupby("device")
                 .agg(plays=("play_id", "count"),
                      minutes=("minutes_played", "sum"),
                      avg=("minutes_played", "mean"))
                 .round(2)
                 .sort_values("plays", ascending=False)
                 .reset_index())


def top_artists(plays, artists, n=5):
    """Return the n artists with the most total minutes."""
    return (plays.merge(artists, on="artist_id")
                 .groupby("artist_name")["minutes_played"]
                 .sum()
                 .round(1)
                 .nlargest(n)
                 .reset_index(name="minutes"))


def show_fan_out(plays, awards):
    """Print the fan-out demonstration: the same wrong number as session 7."""
    print(f"true total:   {plays['minutes_played'].sum():.1f}")

    fan = plays.merge(awards, on="artist_id")
    print(f"rows before:  {len(plays)}")
    print(f"rows after:   {len(fan)}")
    print(f"merged total: {fan['minutes_played'].sum():.1f}   <- wrong")

    # validate= states the shape you expect, and complains when you are wrong.
    # It turns a silent wrong answer into an error message.
    try:
        plays.merge(awards, on="artist_id", validate="many_to_one")
    except Exception as error:                    # pandas raises MergeError
        print(f"validate caught it: {type(error).__name__}")


def main():
    plays = load_from_csv()
    orient(plays)

    print("\n--- per device ---")
    print(by_device(plays).to_string(index=False))

    db_plays, artists, awards = load_from_db()

    print("\n--- top artists by minutes ---")
    print(top_artists(db_plays, artists).to_string(index=False))

    print("\n--- fan-out ---")
    show_fan_out(db_plays, awards)


if __name__ == "__main__":
    main()
