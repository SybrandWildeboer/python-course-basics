-- ===========================================================================
-- LIVE EXERCISE: joins, worked solutions.
--
-- The `expect:` comments are checked by tools/check_sql.py, so every row count
-- here is a real result from data/music.db.
-- ===========================================================================


-- ===================================================== PART 1: answers ====

-- 1. Total minutes per country, highest first.
--    Germany 1285.1, Netherlands 1265.2, Norway 1184.0, and 22 more.
-- expect: 25 rows
SELECT a.country,
       COUNT(*)                        AS plays,
       ROUND(SUM(p.minutes_played), 1) AS minutes
FROM plays p
JOIN artists a USING (artist_id)
GROUP BY a.country
ORDER BY minutes DESC;


-- 2. Plays per genre, with the average minutes per play.
--    Jazz has by far the longest average play at 6.57, despite having the
--    second fewest plays. Total and average disagree, as usual.
-- expect: 8 rows
SELECT a.genre,
       COUNT(*)                        AS plays,
       ROUND(SUM(p.minutes_played), 1) AS minutes,
       ROUND(AVG(p.minutes_played), 2) AS avg_min
FROM plays p
JOIN artists a USING (artist_id)
GROUP BY a.genre
ORDER BY plays DESC;


-- 3. Every artist and their play count, including the never-played ones.
--
--    Two things make this correct. LEFT JOIN keeps the artists with no plays,
--    and COUNT(p.play_id) rather than COUNT(*) reports them as 0. With
--    COUNT(*), Iron Fernway and Gravel Choir would both say 1, because the
--    left join still produces one row for them, full of NULLs.
-- expect: 40 rows
SELECT a.artist_name,
       a.genre,
       COUNT(p.play_id)                AS plays,
       ROUND(SUM(p.minutes_played), 1) AS minutes
FROM artists a
LEFT JOIN plays p USING (artist_id)
GROUP BY a.artist_id
ORDER BY plays DESC;


-- 4. The top three artists in 2025 only, by minutes.
--
--    The year filter is a WHERE, because it removes rows and has nothing to do
--    with the grouping. Filtering rows is cheaper than filtering groups, so do
--    it here whenever you can.
-- expect: 3 rows
SELECT a.artist_name,
       COUNT(*)                        AS plays,
       ROUND(SUM(p.minutes_played), 1) AS minutes
FROM plays p
JOIN artists a USING (artist_id)
WHERE p.played_at >= '2025-01-01'
GROUP BY a.artist_id
ORDER BY minutes DESC
LIMIT 3;


-- ================================================ PART 2: break it ========

-- 5 and 6. Query 1, with awards joined on as well.
--
--    before: Germany 1285.1, Netherlands 1265.2, Norway 1184.0   (25 rows)
--    after:  Norway 2538.5, Germany 2350.1, Ireland 1318.0        (14 rows)
--
--    Nothing was filtered on purpose, nothing was added. Norway more than
--    doubled, the ranking changed, and eleven countries disappeared.
-- expect: 14 rows
SELECT a.country,
       COUNT(*)                        AS rows_now,
       ROUND(SUM(p.minutes_played), 1) AS minutes
FROM plays p
JOIN artists a USING (artist_id)
JOIN awards w ON w.artist_id = p.artist_id
GROUP BY a.country
ORDER BY minutes DESC;


-- 7. WHY.
--
--    The awards table has one row per award, and an artist can have several.
--    Fjord & Flint, from Norway, has 3 awards and 237 plays. The join matches
--    every play against every award for that artist, so those 237 plays become
--    711 rows and their minutes are counted three times over.
--
--    Norway jumped to the top because its most-played artist happens to have
--    three awards. The number is not measuring listening any more; it is
--    measuring listening multiplied by awards, which is not a quantity anybody
--    wanted.
--
--    There is a second bug in the same query, and it is easier to miss: the
--    country count dropped from 25 to 14. The inner join to awards silently
--    removed all eleven countries whose artists have never won anything. So
--    the numbers that remain are inflated AND rows have vanished.
--
--    The tell is the row count. 2,183 plays became 2,371 rows. After any join,
--    compare the row count with what it was before. If it went up and you did
--    not expect it to, stop.


-- 8. The fix: aggregate each table down to one row per artist FIRST, then
--    join. After that the awards join cannot duplicate a play, because there
--    are no play rows left to duplicate.
--
--    Germany 1285.1, Netherlands 1265.2, Norway 1184.0: back to the query 1
--    numbers exactly, all 25 countries present, now with award counts
--    alongside.
-- expect: 25 rows
WITH per_artist AS (
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
SELECT a.country,
       SUM(s.plays)                AS plays,
       ROUND(SUM(s.minutes), 1)    AS minutes,
       COALESCE(SUM(aw.awards), 0) AS awards
FROM per_artist s
JOIN artists a USING (artist_id)
LEFT JOIN awards_per_artist aw USING (artist_id)
GROUP BY a.country
ORDER BY minutes DESC;

--    Two details in that query worth pointing at:
--
--    * TWO CTEs, each reducing a table to one row per artist before anything is
--      joined. That is the general recipe: get both sides down to the same
--      grain, then join.
--
--    * COALESCE(x, 0) means "x, or 0 if x is NULL". Countries with no awards
--      would otherwise show NULL rather than 0, which is accurate and reads
--      badly in a report.
