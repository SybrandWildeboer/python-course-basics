-- ===========================================================================
-- STRETCH: the queries from notebooks/03-stretch-solved.ipynb.
--
-- The notebook is the place to read the reasoning. This file exists so that
-- tools/check_sql.py pins the row counts the notebook prose relies on: if the
-- dataset changes, this is what tells you the notebook needs a look.
-- ===========================================================================


-- 1. The third table: which award is handed out most often?
--    Festival Headline Award, 8 times.
-- expect: 6 rows
SELECT award_name, COUNT(*) AS times_given
FROM awards
GROUP BY award_name
ORDER BY times_given DESC;

--    Artists with three awards, and how many of those were different.
-- expect: 6 rows
SELECT artist_id,
       COUNT(*)                   AS awards,
       COUNT(DISTINCT award_name) AS different_awards
FROM awards
GROUP BY artist_id
HAVING COUNT(*) >= 3
ORDER BY artist_id;

--    Artists who won the same award twice: 1, 7 and 39.
-- expect: 3 rows
SELECT artist_id, COUNT(*) AS awards
FROM awards
GROUP BY artist_id
HAVING COUNT(*) > COUNT(DISTINCT award_name);

-- expect: 3 rows
SELECT artist_id, artist_name FROM artists WHERE artist_id IN (1, 7, 39);


-- 2. How many artists are still active?
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


-- 3. Artists by decade. The 2010s with 22, plus a NULL group of 2.
-- expect: 5 rows
SELECT formed_year / 10 * 10 AS decade,
       COUNT(*)              AS artists
FROM artists
GROUP BY decade
ORDER BY decade;


-- 4. Tracks played on all five devices: 35 of 168.
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


-- 5. Weekend against weekday. 1573 against 610 plays, but per day with
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


-- 6. Plays per device, 2024 against 2025. The phone fell from 560 to 479.
-- expect: 5 rows
SELECT device,
       SUM(CASE WHEN played_at < '2025-01-01' THEN 1 ELSE 0 END)  AS plays_2024,
       SUM(CASE WHEN played_at >= '2025-01-01' THEN 1 ELSE 0 END) AS plays_2025,
       SUM(CASE WHEN played_at >= '2025-01-01' THEN 1 ELSE 0 END)
         - SUM(CASE WHEN played_at < '2025-01-01' THEN 1 ELSE 0 END) AS change
FROM plays
GROUP BY device
ORDER BY change;
