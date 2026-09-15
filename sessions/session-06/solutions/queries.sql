-- ===========================================================================
-- LIVE EXERCISE: the ladder of ten questions, worked solutions.
--
-- The `expect:` comments are checked by tools/check_sql.py, so every row count
-- on this page is the real answer from data/music.db.
-- ===========================================================================


-- 1. Every column of the first 10 plays.
-- expect: 10 rows
SELECT * FROM plays LIMIT 10;


-- 2. Just the track name and minutes played, for all plays.
-- expect: 2183 rows
SELECT track_name, minutes_played FROM plays;


-- 3. Only the plays longer than 9 minutes.
-- expect: 32 rows
SELECT track_name, minutes_played FROM plays
WHERE minutes_played > 9;


-- 4. Only the plays on the speaker, in 2025.
--    Two conditions, joined with AND. The year is the first four characters of
--    the date, so a >= and a <= pair does the job. BETWEEN would too.
-- expect: 174 rows
SELECT played_at, track_name, minutes_played FROM plays
WHERE device = 'speaker'
  AND played_at >= '2025-01-01'
  AND played_at <= '2025-12-31';


-- 5. The same, longest first.
-- expect: 174 rows
SELECT played_at, track_name, minutes_played FROM plays
WHERE device = 'speaker'
  AND played_at BETWEEN '2025-01-01' AND '2025-12-31'
ORDER BY minutes_played DESC;


-- 6. How many plays were skipped?
--    Answer: 258
-- expect: 1 rows
SELECT COUNT(*) AS skipped_plays FROM plays
WHERE skipped = 1;


-- 7. How many different devices appear in the data?
--    Answer: 5. Two ways to ask, and both are worth knowing.
-- expect: 1 rows
SELECT COUNT(DISTINCT device) AS devices FROM plays;

-- expect: 5 rows
SELECT DISTINCT device FROM plays;


-- 8. How many plays per device, biggest first?
--    phone 1039, laptop 524, speaker 336, car 179, tablet 105
-- expect: 5 rows
SELECT device, COUNT(*) AS plays
FROM plays
GROUP BY device
ORDER BY plays DESC;


-- 9. The average minutes per device, to two decimal places.
--    car comes out top at 4.34, which is a small surprise: people skip less in
--    the car, because reaching for the phone is inconvenient.
-- expect: 5 rows
SELECT device,
       COUNT(*)                      AS plays,
       ROUND(AVG(minutes_played), 2) AS avg_min
FROM plays
GROUP BY device
ORDER BY avg_min DESC;


-- 10. Only the devices with more than 300 plays.
--     phone, laptop, speaker. COUNT(*) is an aggregate, so the filter has to be
--     HAVING and not WHERE: at WHERE time no counting has happened yet.
-- expect: 3 rows
SELECT device, COUNT(*) AS plays
FROM plays
GROUP BY device
HAVING COUNT(*) > 300
ORDER BY plays DESC;
