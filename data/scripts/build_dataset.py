"""Build every version of the course dataset from one seeded generator.

The course uses a single dataset the whole way through: a personal music
listening log. This script produces four things from the same random seed, so
the numbers in the slides always match the numbers on the learner's machine:

    data/clean/plays.csv        denormalised listening log  (sessions 4, 8)
    data/clean/artists.csv      the artist lookup table     (sessions 4, 8)
                                (with a few gaps, on purpose)
    data/clean/awards.csv       one-to-many, for fan-out    (session 7)
    data/messy/plays_messy.csv  the same log, damaged       (session 9)
    data/music.db               SQLite, 3 tables            (sessions 6, 7, 10)

Run it from the repository root:

    python data/scripts/build_dataset.py

Standard library only, on purpose: it has to run in session 1, before anybody
has installed a package.
"""

from __future__ import annotations

import csv
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

SEED = 20260101
ROOT = Path(__file__).resolve().parents[2]
CLEAN = ROOT / "data" / "clean"
MESSY = ROOT / "data" / "messy"
DB_PATH = ROOT / "data" / "music.db"

START = date(2024, 1, 1)
END = date(2025, 12, 31)
N_PLAYS = 2400

# artist_name, country, genre, formed_year, still_active
ARTISTS = [
    ("Neon Harbour", "Netherlands", "Electronic", 2014, 1),
    ("The Paper Kites Society", "Australia", "Indie", 2009, 1),
    ("Marta Oliveira", "Portugal", "Jazz", 2016, 1),
    ("Glass Tram", "Germany", "Electronic", 2018, 1),
    ("Rosewood Lane", "United Kingdom", "Folk", 2011, 0),
    ("Kito Ndungu", "Kenya", "Afrobeat", 2019, 1),
    ("The Quiet Wires", "United States", "Rock", 2004, 0),
    ("Sara Lindqvist", "Sweden", "Pop", 2020, 1),
    ("Basement Cartography", "Canada", "Indie", 2013, 1),
    ("Orquesta Bellavista", "Colombia", "Latin", 1998, 1),
    ("Hollow Pines", "United States", "Folk", 2015, 1),
    ("DJ Kompas", "Netherlands", "Electronic", 2021, 1),
    ("Yuki Tanaka Trio", "Japan", "Jazz", 2007, 1),
    ("Velvet Aqueduct", "Italy", "Rock", 2012, 0),
    ("Amara Diallo", "Senegal", "Afrobeat", 2017, 1),
    ("Northern Signal", "Norway", "Electronic", 2016, 1),
    ("The Tuesday Club", "United Kingdom", "Pop", 2019, 1),
    ("Cassette Revival", "France", "Indie", 2010, 0),
    ("Luz de Enero", "Spain", "Latin", 2014, 1),
    ("Brannon Hill", "Ireland", "Folk", 2008, 1),
    ("Static Meadow", "United States", "Rock", 2018, 1),
    ("Mireille Basset", "France", "Jazz", 2011, 1),
    ("Kanto Kids", "Philippines", "Pop", 2022, 1),
    ("Iron Fernway", "United Kingdom", "Rock", 1996, 0),
    ("Selva Alta", "Peru", "Latin", 2015, 1),
    ("Hertz Garden", "Germany", "Electronic", 2020, 1),
    ("The Long Commute", "Netherlands", "Indie", 2017, 1),
    ("Odessa Brass", "Ukraine", "Jazz", 2013, 1),
    ("Pale Cartography", "Canada", "Folk", 2021, 1),
    ("Mango Static", "Brazil", "Latin", 2019, 1),
    ("Circuit Sparrow", "Japan", "Electronic", 2015, 1),
    ("Nora Whitlock", "United States", "Pop", 2018, 1),
    ("Gravel Choir", "Australia", "Rock", 2006, 0),
    ("Lagos Tape Club", "Nigeria", "Afrobeat", 2020, 1),
    ("Fjord & Flint", "Norway", "Folk", 2012, 1),
    ("Salon Mécanique", "Belgium", "Jazz", 2009, 1),
    ("Bright Utility", "United Kingdom", "Indie", 2023, 1),
    ("Casa Tropicana", "Cuba", "Latin", 2001, 1),
    ("Tundra Post", "Iceland", "Electronic", 2019, 1),
    ("The Slow Ferry", "Ireland", "Indie", 2016, 1),
]

TRACK_WORDS_A = [
    "Blue", "Paper", "Midnight", "Harbour", "Slow", "Static", "Golden", "Iron",
    "Velvet", "Quiet", "Electric", "Winter", "Summer", "Broken", "Open",
    "Northern", "Hollow", "Bright", "Salt", "Amber",
]
TRACK_WORDS_B = [
    "Lines", "Rooms", "Weather", "Machines", "Letters", "Signal", "Harbour",
    "Radio", "Garden", "Traffic", "Mornings", "Wires", "Ferry", "Kitchen",
    "Avenue", "Season", "Tape", "Window", "Orbit", "Parade",
]

DEVICES = ["phone", "laptop", "speaker", "car", "tablet"]
DEVICE_WEIGHTS = [46, 24, 16, 9, 5]

AWARD_NAMES = [
    "Critics Circle Album",
    "National Music Prize",
    "Best Live Act",
    "Newcomer of the Year",
    "Producer's Choice",
    "Festival Headline Award",
]


# A lookup table always has a few gaps in it, and session 6 needs real NULLs
# to teach IS NULL with. These are chosen by hand rather than at random, and
# only in columns that do not appear in plays.csv, so the clean CSV stays clean.
UNKNOWN_FORMED_YEAR = {5, 18}      # Rosewood Lane, Cassette Revival
UNKNOWN_STILL_ACTIVE = {24}        # Iron Fernway


def make_artists(rng: random.Random) -> list[dict]:
    rows = []
    for i, (name, country, genre, formed, active) in enumerate(ARTISTS, start=1):
        rows.append(
            {
                "artist_id": i,
                "artist_name": name,
                "country": country,
                "genre": genre,
                "formed_year": None if i in UNKNOWN_FORMED_YEAR else formed,
                "still_active": None if i in UNKNOWN_STILL_ACTIVE else active,
            }
        )
    return rows


def make_tracks(rng: random.Random, artists: list[dict]) -> dict[int, list[str]]:
    """Give every artist a small, fixed catalogue so repeat plays look real."""
    catalogue: dict[int, list[str]] = {}
    for artist in artists:
        n = rng.randint(4, 9)
        titles = set()
        while len(titles) < n:
            titles.add(f"{rng.choice(TRACK_WORDS_A)} {rng.choice(TRACK_WORDS_B)}")
        catalogue[artist["artist_id"]] = sorted(titles)
    return catalogue


def make_plays(rng: random.Random, artists: list[dict]) -> list[dict]:
    catalogue = make_tracks(rng, artists)

    # A listening log is not uniform: a handful of artists dominate.
    ids = [a["artist_id"] for a in artists]
    weights = [max(1, int(rng.gauss(10, 6))) for _ in ids]
    for favourite in rng.sample(ids, 5):
        weights[ids.index(favourite)] += 45

    # Two artists are deliberately never played, so LEFT JOIN has something
    # to show in session 7.
    for silent in (24, 33):  # Iron Fernway, Gravel Choir
        weights[ids.index(silent)] = 0

    genre_by_id = {a["artist_id"]: a["genre"] for a in artists}
    span_days = (END - START).days
    rows = []

    for play_id in range(1, N_PLAYS + 1):
        artist_id = rng.choices(ids, weights=weights, k=1)[0]
        track = rng.choice(catalogue[artist_id])

        # Listening rises in the winter months; gives the line charts a shape.
        day_offset = rng.randint(0, span_days)
        played = START + timedelta(days=day_offset)
        if played.month in (6, 7, 8) and rng.random() < 0.35:
            continue  # thinner summer

        genre = genre_by_id[artist_id]
        base = {"Jazz": 7.5, "Electronic": 5.8, "Rock": 4.4, "Folk": 4.0}.get(genre, 3.6)
        minutes = round(max(0.4, rng.gauss(base, 1.4)), 2)

        skipped = 1 if rng.random() < 0.12 else 0
        if skipped:
            minutes = round(max(0.15, minutes * rng.uniform(0.05, 0.3)), 2)

        rows.append(
            {
                "play_id": play_id,
                "played_at": played.isoformat(),
                "artist_id": artist_id,
                "track_name": track,
                "minutes_played": minutes,
                "device": rng.choices(DEVICES, weights=DEVICE_WEIGHTS, k=1)[0],
                "skipped": skipped,
            }
        )

    rows.sort(key=lambda r: (r["played_at"], r["play_id"]))
    # Renumber so play_id runs 1..n in date order, which is easier to talk about.
    for new_id, row in enumerate(rows, start=1):
        row["play_id"] = new_id
    return rows


def make_awards(rng: random.Random, artists: list[dict]) -> list[dict]:
    """One-to-many on purpose: some artists have several awards.

    This is what makes the session 7 fan-out demonstration work. Join plays to
    awards and SUM(minutes_played) and the answer is wrong, because a play by a
    three-award artist is counted three times.
    """
    rows = []
    award_id = 1
    for artist in artists:
        if rng.random() < 0.45:
            for _ in range(rng.randint(1, 3)):
                rows.append(
                    {
                        "award_id": award_id,
                        "artist_id": artist["artist_id"],
                        "award_name": rng.choice(AWARD_NAMES),
                        "year": rng.randint(2015, 2025),
                    }
                )
                award_id += 1
    return rows


def denormalise(plays: list[dict], artists: list[dict]) -> list[dict]:
    by_id = {a["artist_id"]: a for a in artists}
    rows = []
    for play in plays:
        artist = by_id[play["artist_id"]]
        rows.append(
            {
                "play_id": play["play_id"],
                "played_at": play["played_at"],
                "artist_name": artist["artist_name"],
                "track_name": play["track_name"],
                "genre": artist["genre"],
                "country": artist["country"],
                "minutes_played": play["minutes_played"],
                "device": play["device"],
                "skipped": play["skipped"],
            }
        )
    return rows


def damage(rng: random.Random, clean_rows: list[dict]) -> list[dict]:
    """Break the clean data in the specific ways real data is broken.

    Every kind of damage here has a matching fix in session 9:
      * inconsistent capitalisation and stray whitespace -> .str.strip().str.lower()
      * mixed date formats                               -> pd.to_datetime
      * thousands separators and empty strings in numbers-> pd.to_numeric
      * missing values                                   -> isna(), dropna/fillna
      * duplicated rows                                  -> duplicated(), drop_duplicates()
      * a stray column name with a trailing space        -> rename()
    """
    rows = [dict(r) for r in clean_rows]

    for row in rows:
        roll = rng.random()
        if roll < 0.18:
            row["genre"] = row["genre"].upper()
        elif roll < 0.30:
            row["genre"] = row["genre"].lower()
        elif roll < 0.36:
            row["genre"] = f"  {row['genre']} "

        if rng.random() < 0.15:
            row["device"] = row["device"].upper()
        if rng.random() < 0.08:
            row["device"] = f"{row['device']} "

        # Mixed date formats: ISO, European, and US written-out.
        roll = rng.random()
        y, m, d = row["played_at"].split("-")
        if roll < 0.14:
            row["played_at"] = f"{d}/{m}/{y}"
        elif roll < 0.20:
            row["played_at"] = f"{d}-{m}-{y}"

        # Numbers that arrive looking like text.
        if rng.random() < 0.06:
            row["minutes_played"] = f"{row['minutes_played']:,.2f}".replace(",", " ")
        if rng.random() < 0.04:
            row["minutes_played"] = f"{row['minutes_played']} min"

        # Holes.
        if rng.random() < 0.05:
            row["minutes_played"] = ""
        if rng.random() < 0.03:
            row["device"] = ""
        if rng.random() < 0.02:
            row["country"] = "NA"
        if rng.random() < 0.02:
            row["genre"] = ""

    # Exact duplicate rows, scattered.
    for row in rng.sample(rows, 40):
        rows.append(dict(row))

    rng.shuffle(rows)

    # One column name is subtly wrong in the export.
    renamed = []
    for row in rows:
        row = dict(row)
        row["minutes played "] = row.pop("minutes_played")
        renamed.append(row)
    return renamed


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {path.relative_to(ROOT)}  ({len(rows)} rows)")


def build_db(artists: list[dict], plays: list[dict], awards: list[dict]) -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
    con = sqlite3.connect(DB_PATH)
    con.executescript(
        """
        CREATE TABLE artists (
            artist_id    INTEGER PRIMARY KEY,
            artist_name  TEXT    NOT NULL,
            country      TEXT,
            genre        TEXT,
            formed_year  INTEGER,
            still_active INTEGER
        );

        CREATE TABLE plays (
            play_id        INTEGER PRIMARY KEY,
            played_at      TEXT    NOT NULL,
            artist_id      INTEGER REFERENCES artists(artist_id),
            track_name     TEXT    NOT NULL,
            minutes_played REAL,
            device         TEXT,
            skipped        INTEGER
        );

        CREATE TABLE awards (
            award_id   INTEGER PRIMARY KEY,
            artist_id  INTEGER REFERENCES artists(artist_id),
            award_name TEXT,
            year       INTEGER
        );

        CREATE INDEX idx_plays_artist ON plays(artist_id);
        CREATE INDEX idx_plays_date   ON plays(played_at);
        """
    )
    con.executemany(
        "INSERT INTO artists VALUES (:artist_id, :artist_name, :country, :genre,"
        " :formed_year, :still_active)",
        artists,
    )
    con.executemany(
        "INSERT INTO plays VALUES (:play_id, :played_at, :artist_id, :track_name,"
        " :minutes_played, :device, :skipped)",
        plays,
    )
    con.executemany(
        "INSERT INTO awards VALUES (:award_id, :artist_id, :award_name, :year)",
        awards,
    )
    con.commit()
    con.close()
    print(f"wrote {DB_PATH.relative_to(ROOT)}  "
          f"({len(artists)} artists, {len(plays)} plays, {len(awards)} awards)")


def main() -> None:
    rng = random.Random(SEED)
    artists = make_artists(rng)
    plays = make_plays(rng, artists)
    awards = make_awards(rng, artists)
    clean = denormalise(plays, artists)

    write_csv(CLEAN / "artists.csv", artists)
    write_csv(CLEAN / "awards.csv", awards)
    write_csv(CLEAN / "plays.csv", clean)
    write_csv(MESSY / "plays_messy.csv", damage(random.Random(SEED + 1), clean))
    build_db(artists, plays, awards)


if __name__ == "__main__":
    main()
