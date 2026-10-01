-- ===========================================================================
-- STRETCH: the queries from notebooks/03-stretch-solved.ipynb.
--
-- The notebook is the place to read the reasoning. This file exists so that
-- tools/check_sql.py pins the row counts the notebook prose relies on: if the
-- dataset changes, this is what tells you the notebook needs a look.
-- ===========================================================================


-- 1. Who did I not play in 2025? The wrong version first: the WHERE on the
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


-- 2. Pairs of artists from the same country: a self-join. 22 pairs.
-- expect: 22 rows
SELECT a1.country,
       a1.artist_name AS artist,
       a2.artist_name AS same_country_as
FROM artists a1
JOIN artists a2
  ON a2.country = a1.country
 AND a2.artist_id > a1.artist_id
ORDER BY a1.country, a1.artist_name;


--    The same join with only the country condition: 84 rows, because every
--    artist meets itself and every pair appears twice.
-- expect: 1 rows
SELECT COUNT(*) AS rows_country_only
FROM artists a1
JOIN artists a2 ON a2.country = a1.country;


--    With <> instead of >: 44 rows, each pair still twice.
-- expect: 1 rows
SELECT COUNT(*) AS rows_not_equal
FROM artists a1
JOIN artists a2 ON a2.country = a1.country AND a2.artist_id <> a1.artist_id;


--    Harder: same country and same genre. Three pairs.
-- expect: 3 rows
SELECT a1.country, a1.genre, a1.artist_name AS artist, a2.artist_name AS also
FROM artists a1
JOIN artists a2
  ON a2.country = a1.country
 AND a2.genre = a1.genre
 AND a2.artist_id > a1.artist_id;


-- 3. 2024 against 2025, three CTEs. Mireille Basset +71.7 at the top,
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


-- 4. Spot the bug: both counts fan out. Folk claims 1095 awards out of 33.
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


-- 5. The top artist in every genre, with RANK(). Glass Tram 1175.1 first.
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


-- 6. Minutes per month with a running total. The last row is 8980.4.
-- expect: 24 rows
WITH monthly AS (
    SELECT strftime('%Y-%m', played_at) AS month,
           SUM(minutes_played)          AS minutes
    FROM plays
    GROUP BY month
)
SELECT month,
       ROUND(minutes, 1)                            AS minutes,
       ROUND(SUM(minutes) OVER (ORDER BY month), 1) AS running_total
FROM monthly
ORDER BY month;


--    Rounding each month first makes the last running total drift to 8980.7.
-- expect: 1 rows
WITH monthly AS (
    SELECT strftime('%Y-%m', played_at) AS month,
           ROUND(SUM(minutes_played), 1) AS minutes
    FROM plays
    GROUP BY month
)
SELECT ROUND(SUM(minutes), 1) AS drifted_total FROM monthly;


--    The halfway month: 2024-12, at 4596.6 against a halfway mark of 4490.2.
-- expect: 1 rows
WITH monthly AS (
    SELECT strftime('%Y-%m', played_at) AS month,
           SUM(minutes_played)          AS minutes
    FROM plays
    GROUP BY month
),
running AS (
    SELECT month, SUM(minutes) OVER (ORDER BY month) AS running_total
    FROM monthly
),
half AS (
    SELECT SUM(minutes_played) / 2 AS halfway
    FROM plays
)
SELECT r.month, ROUND(r.running_total, 1) AS running_total,
       ROUND(h.halfway, 1) AS halfway
FROM running r
CROSS JOIN half h
WHERE r.running_total >= h.halfway
ORDER BY r.month
LIMIT 1;


--    Harder: the running total restarts each year. The two Decembers are
--    4596.6 and 4383.8.
-- expect: 24 rows
WITH monthly AS (
    SELECT strftime('%Y-%m', played_at) AS month,
           SUM(minutes_played)          AS minutes
    FROM plays
    GROUP BY month
)
SELECT month,
       ROUND(minutes, 1) AS minutes,
       ROUND(SUM(minutes) OVER (PARTITION BY substr(month, 1, 4)
                                ORDER BY month), 1) AS running_in_year
FROM monthly
ORDER BY month;
