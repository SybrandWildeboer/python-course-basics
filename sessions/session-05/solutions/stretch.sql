-- ===========================================================================
-- STRETCH: the queries from notebooks/06-stretch-solved.ipynb.
--
-- The notebook is the place to read the reasoning. This file exists so that
-- tools/check_sql.py pins the row counts the notebook prose relies on: if the
-- dataset changes, this is what tells you the notebook needs a look.
--
-- 1 to 3 use one table. 4 to 8 use joins.
-- ===========================================================================


-- 1. How many artists are still active?
--    39 (wrong: counts every non-NULL value, the 0s included), 34, 34.
-- expect: 1 rows
SELECT COUNT(still_active) AS active FROM artists;

-- expect: 1 rows
SELECT SUM(still_active) AS active FROM artists;

-- expect: 1 rows
SELECT COUNT(*) AS active FROM artists WHERE still_active = 1;

--    5 not active. 34 + 5 is 39, not 40: Iron Fernway is NULL and drops out
--    of both.
-- expect: 1 rows
SELECT COUNT(*) AS not_active FROM artists WHERE still_active != 1;

-- expect: 1 rows
SELECT artist_name, still_active FROM artists WHERE still_active IS NULL;


-- 2. Tracks played on all five devices: 35 of 168.
-- expect: 35 rows
SELECT track_name,
       COUNT(DISTINCT device) AS devices,
       COUNT(*)               AS plays
FROM plays
GROUP BY track_name
HAVING COUNT(DISTINCT device) = 5
ORDER BY plays DESC;

--    Only plays that were not skipped: 30. The condition is about each row,
--    so it belongs in WHERE.
-- expect: 30 rows
SELECT track_name,
       COUNT(DISTINCT device) AS devices,
       COUNT(*)               AS plays
FROM plays
WHERE skipped = 0
GROUP BY track_name
HAVING COUNT(DISTINCT device) = 5
ORDER BY plays DESC;

--    The trap version, with skipped = 0 in HAVING, gives 29 rows of nonsense
--    on this database. Not pinned, because which play's value SQLite picks
--    for an ungrouped column is not something to rely on.
SELECT track_name, COUNT(DISTINCT device) AS devices
FROM plays
GROUP BY track_name
HAVING COUNT(DISTINCT device) = 5 AND skipped = 0;


-- 3. Weekend against weekday. 1573 against 610 plays, but per day with
--    listening it is 3.19 against 3.23.
-- expect: 2 rows
SELECT CASE
           WHEN strftime('%w', played_at) IN ('0', '6') THEN 'weekend'
           ELSE 'weekday'
       END                        AS part_of_week,
       COUNT(*)                   AS plays,
       COUNT(DISTINCT played_at)  AS days,
       ROUND(1.0 * COUNT(*) / COUNT(DISTINCT played_at), 2) AS plays_per_day
FROM plays
GROUP BY part_of_week;


-- 4. Who did I not play in 2025? The wrong version first: the WHERE on the
--    right-hand table throws away the unmatched rows, so 35 rows, not 40,
--    and nobody shows 0.
-- expect: 35 rows
SELECT a.artist_name, COUNT(p.play_id) AS plays_2025
FROM artists a
LEFT JOIN plays p ON p.artist_id = a.artist_id
WHERE p.played_at >= '2025-01-01'
GROUP BY a.artist_id
ORDER BY plays_2025, a.artist_name;


--    The fix: the date condition moves into the ON. All 40 artists, five of
--    them with 0 plays in 2025.
-- expect: 40 rows
SELECT a.artist_name, COUNT(p.play_id) AS plays_2025
FROM artists a
LEFT JOIN plays p
       ON p.artist_id = a.artist_id
      AND p.played_at >= '2025-01-01'
GROUP BY a.artist_id
ORDER BY plays_2025, a.artist_name;


--    Only the unmatched ones: left join, then WHERE p.play_id IS NULL.
--    Amara Diallo, Gravel Choir, Iron Fernway, Neon Harbour, Odessa Brass.
-- expect: 5 rows
SELECT a.artist_name, a.genre
FROM artists a
LEFT JOIN plays p
       ON p.artist_id = a.artist_id
      AND p.played_at >= '2025-01-01'
WHERE p.play_id IS NULL
ORDER BY a.artist_name;


-- 5. Spot the bug: both counts fan out. Folk claims 1095 awards out of 33.
-- expect: 8 rows
SELECT a.genre,
       COUNT(w.award_id) AS awards,
       COUNT(p.play_id)  AS plays
FROM artists a
LEFT JOIN awards w USING (artist_id)
LEFT JOIN plays  p USING (artist_id)
GROUP BY a.genre
ORDER BY a.genre;


--    Repaired with COUNT(DISTINCT key): Electronic 10, Folk 9 awards, and
--    the plays add up to 2183 again.
-- expect: 8 rows
SELECT a.genre,
       COUNT(DISTINCT w.award_id) AS awards,
       COUNT(DISTINCT p.play_id)  AS plays
FROM artists a
LEFT JOIN awards w USING (artist_id)
LEFT JOIN plays  p USING (artist_id)
GROUP BY a.genre
ORDER BY a.genre;


--    Harder: with minutes, which DISTINCT cannot repair. Aggregate first.
-- expect: 8 rows
WITH plays_per_artist AS (
    SELECT artist_id,
           COUNT(*)            AS plays,
           SUM(minutes_played) AS minutes
    FROM plays
    GROUP BY artist_id
),
awards_per_artist AS (
    SELECT artist_id, COUNT(*) AS awards
    FROM awards
    GROUP BY artist_id
)
SELECT a.genre,
       COALESCE(SUM(aw.awards), 0)           AS awards,
       COALESCE(SUM(pp.plays), 0)            AS plays,
       ROUND(COALESCE(SUM(pp.minutes), 0), 1) AS minutes
FROM artists a
LEFT JOIN plays_per_artist  pp USING (artist_id)
LEFT JOIN awards_per_artist aw USING (artist_id)
GROUP BY a.genre
ORDER BY a.genre;


-- 6. 2024 against 2025, three CTEs. Mireille Basset +71.7 at the top,
--    Glass Tram -84.0 at the bottom. Starts from artists, so all 40 are there.
-- expect: 40 rows
WITH minutes_2024 AS (
    SELECT artist_id, ROUND(SUM(minutes_played), 1) AS minutes
    FROM plays
    WHERE played_at < '2025-01-01'
    GROUP BY artist_id
),
minutes_2025 AS (
    SELECT artist_id, ROUND(SUM(minutes_played), 1) AS minutes
    FROM plays
    WHERE played_at >= '2025-01-01'
    GROUP BY artist_id
),
compared AS (
    SELECT a.artist_name,
           COALESCE(y1.minutes, 0.0) AS min_2024,
           COALESCE(y2.minutes, 0.0) AS min_2025
    FROM artists a
    LEFT JOIN minutes_2024 y1 USING (artist_id)
    LEFT JOIN minutes_2025 y2 USING (artist_id)
)
SELECT artist_name, min_2024, min_2025,
       ROUND(min_2025 - min_2024, 1) AS change
FROM compared
ORDER BY change DESC;


--    Harder: played in 2024, not at all in 2025. Neon Harbour, Amara Diallo,
--    Odessa Brass.
-- expect: 3 rows
WITH minutes_2024 AS (
    SELECT artist_id, ROUND(SUM(minutes_played), 1) AS minutes
    FROM plays
    WHERE played_at < '2025-01-01'
    GROUP BY artist_id
),
minutes_2025 AS (
    SELECT artist_id, ROUND(SUM(minutes_played), 1) AS minutes
    FROM plays
    WHERE played_at >= '2025-01-01'
    GROUP BY artist_id
),
compared AS (
    SELECT a.artist_name,
           COALESCE(y1.minutes, 0.0) AS min_2024,
           COALESCE(y2.minutes, 0.0) AS min_2025
    FROM artists a
    LEFT JOIN minutes_2024 y1 USING (artist_id)
    LEFT JOIN minutes_2025 y2 USING (artist_id)
)
SELECT artist_name, min_2024
FROM compared
WHERE min_2024 > 0 AND min_2025 = 0
ORDER BY min_2024 DESC;


-- 7. The same fix three ways: a nested subquery, an IN subquery, a view.
--
--    The real fix from the session, written as a nested subquery instead of
--    a CTE. Identical result: Glass Tram, DJ Kompas, Fjord & Flint 846.2.
-- expect: 3 rows
SELECT a.artist_name, s.plays, s.minutes, COUNT(w.award_id) AS awards
FROM (
    SELECT artist_id,
           COUNT(*)                      AS plays,
           ROUND(SUM(minutes_played), 1) AS minutes
    FROM plays
    GROUP BY artist_id
) AS s
JOIN artists a USING (artist_id)
LEFT JOIN awards w USING (artist_id)
GROUP BY a.artist_id
ORDER BY s.minutes DESC
LIMIT 3;


--    A subquery after IN: plays by Dutch artists, with no join at all. 240.
-- expect: 1 rows
SELECT COUNT(*) AS dutch_plays
FROM plays
WHERE artist_id IN (SELECT artist_id FROM artists WHERE country = 'Netherlands');

--    The same count with a join: 240 again.
-- expect: 1 rows
SELECT COUNT(*) AS dutch_plays
FROM plays p
JOIN artists a USING (artist_id)
WHERE a.country = 'Netherlands';


--    A view stores the query, not the data. TEMP means it lives only as long
--    as this connection, so nothing is written into music.db.
DROP VIEW IF EXISTS artist_summary;

CREATE TEMP VIEW artist_summary AS
SELECT a.artist_id,
       a.artist_name,
       a.country,
       a.genre,
       COUNT(p.play_id)                AS plays,
       ROUND(SUM(p.minutes_played), 1) AS minutes
FROM artists a
LEFT JOIN plays p USING (artist_id)
GROUP BY a.artist_id;

--    Used like any table: the two never-played artists.
-- expect: 2 rows
SELECT artist_name, genre FROM artist_summary WHERE plays = 0;

--    Top three countries: Germany 1285.1, Netherlands 1265.2, Norway 1184.0,
--    the same as question 1 of the joins exercise.
-- expect: 3 rows
SELECT country, ROUND(SUM(minutes), 1) AS minutes
FROM artist_summary
GROUP BY country
ORDER BY minutes DESC
LIMIT 3;

DROP VIEW artist_summary;


-- 8. The top artist in every genre, with RANK(). Glass Tram 1175.1 first.
-- expect: 8 rows
WITH per_artist AS (
    SELECT artist_id, SUM(minutes_played) AS minutes
    FROM plays
    GROUP BY artist_id
),
ranked AS (
    SELECT a.genre,
           a.artist_name,
           ROUND(s.minutes, 1) AS minutes,
           RANK() OVER (PARTITION BY a.genre ORDER BY s.minutes DESC) AS position
    FROM per_artist s
    JOIN artists a USING (artist_id)
)
SELECT genre, artist_name, minutes
FROM ranked
WHERE position = 1
ORDER BY minutes DESC;


--    Harder: the top two per genre. Glass Tram and DJ Kompas 5.9 apart.
-- expect: 16 rows
WITH per_artist AS (
    SELECT artist_id, SUM(minutes_played) AS minutes
    FROM plays
    GROUP BY artist_id
),
ranked AS (
    SELECT a.genre,
           a.artist_name,
           ROUND(s.minutes, 1) AS minutes,
           RANK() OVER (PARTITION BY a.genre ORDER BY s.minutes DESC) AS position
    FROM per_artist s
    JOIN artists a USING (artist_id)
)
SELECT genre, position, artist_name, minutes
FROM ranked
WHERE position <= 2
ORDER BY genre, position;
