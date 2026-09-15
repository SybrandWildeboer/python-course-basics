-- ===========================================================================
-- Session 7 walkthrough: joins, fan-out, subqueries and CTEs.
--
-- Run these in DB Browser against data/music.db, one at a time. Only the view
-- at the very end writes anything, and it is dropped again immediately.
-- ===========================================================================


-- ============================================================ FIRST JOIN ==
-- Read the ON as the matching rule: "bring me the artists row whose artist_id
-- matches this play's artist_id".
-- expect: 5 rows
SELECT p.played_at, a.artist_name, p.track_name, p.minutes_played
FROM plays AS p
JOIN artists AS a ON a.artist_id = p.artist_id
ORDER BY p.played_at
LIMIT 5;


-- Ambiguous column names. This one fails, on purpose: both tables have an
-- artist_id, so "artist_id" on its own is not a question with one answer.
-- Uncomment to see the error.
--
-- SELECT artist_id, artist_name
-- FROM plays JOIN artists ON artists.artist_id = plays.artist_id;
-- Error: ambiguous column name: artist_id

-- Qualify it and it is fine.
-- expect: 5 rows
SELECT p.artist_id, a.artist_name, p.track_name
FROM plays p
JOIN artists a ON a.artist_id = p.artist_id
LIMIT 5;


-- USING, when the key has the same name on both sides. Same query as above,
-- and it merges the column so artist_id needs no prefix.
-- expect: 5 rows
SELECT artist_id, artist_name, track_name
FROM plays
JOIN artists USING (artist_id)
LIMIT 5;


-- ============================================================= LEFT JOIN ==
-- INNER JOIN: only artists that have plays.  38
-- expect: 1 rows
SELECT COUNT(DISTINCT a.artist_id) AS artists_with_plays
FROM artists a
JOIN plays p USING (artist_id);

-- LEFT JOIN: every artist, played or not.  40
-- expect: 1 rows
SELECT COUNT(DISTINCT a.artist_id) AS all_artists
FROM artists a
LEFT JOIN plays p USING (artist_id);


-- The two artists the inner join hides: Iron Fernway and Gravel Choir.
--
-- Note COUNT(p.play_id), not COUNT(*). After a left join an unmatched artist
-- still produces one row, with every plays column NULL. COUNT(*) counts that
-- row and says 1. COUNT(p.play_id) skips NULLs and correctly says 0.
-- expect: 4 rows
SELECT a.artist_name, a.genre, COUNT(p.play_id) AS plays
FROM artists a
LEFT JOIN plays p USING (artist_id)
GROUP BY a.artist_id
ORDER BY plays
LIMIT 4;

-- The wrong version, for comparison. Iron Fernway now shows 1 play.
-- expect: 4 rows
SELECT a.artist_name, COUNT(*) AS plays_wrong
FROM artists a
LEFT JOIN plays p USING (artist_id)
GROUP BY a.artist_id
ORDER BY plays_wrong
LIMIT 4;


-- ===================================================== JOIN THEN GROUP ====
-- Sara Lindqvist has the most PLAYS (242). Glass Tram has the most MINUTES
-- (1175.1). Both are correct answers to different questions.
-- expect: 5 rows
SELECT a.artist_name,
       a.country,
       COUNT(*)                        AS plays,
       ROUND(SUM(p.minutes_played), 1) AS minutes
FROM plays p
JOIN artists a USING (artist_id)
GROUP BY a.artist_id
ORDER BY minutes DESC
LIMIT 5;


-- ============================================================== FAN-OUT ===
-- The honest total: 8980.4 minutes.
-- expect: 1 rows
SELECT ROUND(SUM(minutes_played), 1) AS true_total FROM plays;

-- The same total with awards joined on: 9732.1. Nothing was filtered and
-- nothing was added, and the number went up by 751 minutes. No warning.
-- expect: 1 rows
SELECT ROUND(SUM(p.minutes_played), 1) AS inflated_total
FROM plays p
JOIN awards w ON w.artist_id = p.artist_id;

-- Count the rows and it is obvious: 2183 plays became 2371 rows.
-- expect: 1 rows
SELECT COUNT(*) AS rows_after_join
FROM plays p
JOIN awards w ON w.artist_id = p.artist_id;


-- One artist, in detail. Fjord & Flint (artist_id 35) has 237 plays worth
-- 846.2 minutes, and 3 awards.
-- expect: 1 rows
SELECT COUNT(*) AS plays, ROUND(SUM(minutes_played), 1) AS minutes
FROM plays WHERE artist_id = 35;

-- expect: 3 rows
SELECT award_name, year FROM awards WHERE artist_id = 35;

-- After the join: 237 x 3 = 711 rows, and the minutes counted three times.
-- expect: 1 rows
SELECT COUNT(*) AS rows_now, ROUND(SUM(p.minutes_played), 1) AS minutes_now
FROM plays p
JOIN awards w ON w.artist_id = p.artist_id
WHERE p.artist_id = 35;
-- 711 | 2538.5

-- Every play met every award. The join has no idea the awards have nothing to
-- do with the listening; it only follows the rule you gave it.


-- ------------------------------------------ the obvious fix is also wrong --
-- SUM(DISTINCT) adds each DIFFERENT VALUE once. Two separate plays that both
-- happened to last 4.65 minutes are two real plays, and it throws one away.
-- expect: 1 rows
SELECT ROUND(SUM(DISTINCT p.minutes_played), 1) AS also_wrong
FROM plays p
JOIN awards w ON w.artist_id = p.artist_id
WHERE p.artist_id = 35;
-- 680.6, when the true answer is 846.2
--
--   no join                846.2   correct
--   joined                2538.5   three times too big
--   joined, SUM(DISTINCT)  680.6   too small
--
-- Two wrongs, sitting either side of the right answer, and both looked like
-- fixes. When a number looks wrong, work out what the rows are before
-- reaching for the switch that makes it look right.


-- --------------------------------------------------------- the real fix ---
-- Aggregate plays down to one row per artist FIRST. After that the awards
-- join cannot duplicate a play, because there are no play rows left to
-- duplicate.
--
-- As a subquery:
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

-- And the same thing as a CTE, which reads top to bottom instead of
-- inside-out. Identical result. Prefer this once a query needs scrolling.
-- expect: 3 rows
WITH per_artist AS (
    SELECT artist_id,
           COUNT(*)                      AS plays,
           ROUND(SUM(minutes_played), 1) AS minutes
    FROM plays
    GROUP BY artist_id
)
SELECT a.artist_name, s.plays, s.minutes, COUNT(w.award_id) AS awards
FROM per_artist s
JOIN artists a USING (artist_id)
LEFT JOIN awards w USING (artist_id)
GROUP BY a.artist_id
ORDER BY s.minutes DESC
LIMIT 3;
-- Glass Tram 229 1175.1 2 | DJ Kompas 215 1169.2 1 | Fjord & Flint 237 846.2 3
--
-- Fjord & Flint is back to 846.2, which matches the standalone query exactly.
-- The fix is confirmed by an independent calculation, not by looking sensible.


-- ================================================================ VIEWS ===
-- A view stores the QUERY, not the data, so it is always current. Useful when
-- one join keeps reappearing: define it once, correctly, and everything
-- downstream inherits the correct version.
DROP VIEW IF EXISTS artist_summary;

CREATE VIEW artist_summary AS
SELECT a.artist_id,
       a.artist_name,
       a.country,
       a.genre,
       COUNT(p.play_id)                AS plays,
       ROUND(SUM(p.minutes_played), 1) AS minutes
FROM artists a
LEFT JOIN plays p USING (artist_id)
GROUP BY a.artist_id;

-- Now use it like any table.
-- expect: 2 rows
SELECT artist_name, genre FROM artist_summary WHERE plays = 0;

-- expect: 3 rows
SELECT country, ROUND(SUM(minutes), 1) AS minutes
FROM artist_summary
GROUP BY country
ORDER BY minutes DESC
LIMIT 3;

DROP VIEW artist_summary;
