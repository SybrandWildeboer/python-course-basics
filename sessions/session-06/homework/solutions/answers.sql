-- ===========================================================================
-- Session 6 homework: worked answers.
--
-- Every `expect:` comment is checked by tools/check_sql.py, so the row counts
-- and the figures in the notes are real results from data/music.db.
-- ===========================================================================


-- 1. How many artists are in the database?
--    Answer: 40
-- expect: 1 rows
SELECT COUNT(*) AS artists FROM artists;


-- 2. Which artists are from the Netherlands? Show name and genre.
--    Neon Harbour, DJ Kompas, The Long Commute
-- expect: 3 rows
SELECT artist_name, genre
FROM artists
WHERE country = 'Netherlands'
ORDER BY artist_name;


-- 3. Which artists have an unknown formed_year?
--    Rosewood Lane and Cassette Revival.
--
--    This is one of the two that needs care. WHERE formed_year = NULL runs
--    happily and returns nothing at all, because NULL means unknown and an
--    unknown is not equal to anything, including another unknown. IS NULL is
--    the only way to ask.
-- expect: 2 rows
SELECT artist_name, country, genre
FROM artists
WHERE formed_year IS NULL;


-- 4. What are the five longest plays?
--    Paper Avenue 11.01, Harbour Season 10.96, Broken Lines 10.77,
--    Static Wires 10.72, Northern Window 10.04
-- expect: 5 rows
SELECT track_name, played_at, minutes_played
FROM plays
ORDER BY minutes_played DESC
LIMIT 5;


-- 5. How many plays in 2024, and how many in 2025? One query, two rows.
--    2024: 1122, 2025: 1061
--
--    This is the other one that needs something new. The year is not a column,
--    so you have to make one. Two ways, both fine:
--
--    strftime('%Y', played_at) is the date-formatting function, and it is the
--    one worth learning because it also gives you months and weekdays.
-- expect: 2 rows
SELECT strftime('%Y', played_at) AS year,
       COUNT(*)                  AS plays
FROM plays
GROUP BY year
ORDER BY year;

--    substr(played_at, 1, 4) just takes the first four characters. Slightly
--    cruder, works only because the dates are stored as YYYY-MM-DD text.
-- expect: 2 rows
SELECT substr(played_at, 1, 4) AS year, COUNT(*) AS plays
FROM plays
GROUP BY year
ORDER BY year;


-- 6. Which tracks were played more than 40 times, most played first?
--    Broken Lines 67, Salt Lines 63, Amber Ferry 55, Broken Mornings 52,
--    Open Orbit 44. Only five tracks clear the bar, out of 168.
-- expect: 5 rows
SELECT track_name, COUNT(*) AS plays
FROM plays
GROUP BY track_name
HAVING COUNT(*) > 40
ORDER BY plays DESC;


-- 7. Total listening time per device, to the nearest minute.
--    phone 4308, laptop 2144, speaker 1335, car 778, tablet 416
-- expect: 5 rows
SELECT device,
       ROUND(SUM(minutes_played)) AS total_minutes
FROM plays
GROUP BY device
ORDER BY total_minutes DESC;


-- 8. Which genres have five or more artists?
--    Electronic 7, Indie 6, then Folk, Jazz, Latin and Rock on 5 each.
-- expect: 6 rows
SELECT genre, COUNT(*) AS artists
FROM artists
GROUP BY genre
HAVING COUNT(*) >= 5
ORDER BY artists DESC, genre;


-- 9. What proportion of plays on each device were skipped?
--    phone 11.4%, laptop 11.5%, speaker 14.0%, car 10.6%, tablet 13.3%
--
--    Two numbers per group: COUNT(*) for all plays, and SUM(skipped) for the
--    skipped ones, which works because skipped is already a 0 or a 1.
--
--    The trap is the division. In SQLite, 19 / 179 with two whole numbers is
--    0, because it throws the fraction away. Multiplying by 100.0 first, with
--    the decimal point, forces a proper division.
-- expect: 5 rows
SELECT device,
       COUNT(*)      AS plays,
       SUM(skipped)  AS skipped,
       ROUND(100.0 * SUM(skipped) / COUNT(*), 1) AS skipped_pct
FROM plays
GROUP BY device
ORDER BY skipped_pct DESC;


-- 10. The busiest single day, by number of plays.
--     2024-03-24, with 11 plays. Nothing new needed: played_at is already one
--     value per day, so it groups like any other column.
-- expect: 1 rows
SELECT played_at, COUNT(*) AS plays
FROM plays
GROUP BY played_at
ORDER BY plays DESC
LIMIT 1;

--     Worth a second look, though. The top day has 11 plays and the runner
--     up has 10, out of 731 days. "The busiest day" sounds like a finding and
--     is really a coin toss between a handful of ordinary days. Same lesson as
--     the tied artists in session 4: look at second place before believing a
--     single-row answer.
-- expect: 5 rows
SELECT played_at, COUNT(*) AS plays
FROM plays
GROUP BY played_at
ORDER BY plays DESC
LIMIT 5;


-- ===========================================================================
-- TASK 2: two examples of invented questions
-- ===========================================================================

-- Question A: does listening get longer as the year goes on, or is that just
-- a feeling?
--
-- Expected: more listening in winter, and maybe longer plays too.
-- Got: half right. The quiet months really are June, July and August, with
-- 120 to 133 plays each against 239 in October. But the average play length
-- hardly moves all year: 3.93 at the lowest, 4.46 at the highest. So the
-- seasonal effect is in HOW MUCH gets played, not how long each play lasts.
-- Those are two different questions, and it would have been easy to write
-- one query, see a seasonal pattern, and report the other.
-- expect: 12 rows
SELECT strftime('%m', played_at)     AS month,
       COUNT(*)                      AS plays,
       ROUND(AVG(minutes_played), 2) AS avg_min
FROM plays
GROUP BY month
ORDER BY month;


-- Question B: which artists get skipped most? A high skip rate on an artist
-- you play a lot is more interesting than one on an artist played twice.
--
-- Expected: no idea, which is the honest answer and a good reason to ask.
-- Got: the HAVING clause is doing the real work here. Without it the top of
-- the list is artists with two plays and one skip, at 50%, which is noise
-- rather than a finding.
-- expect: 10 rows
SELECT artist_id,
       COUNT(*)     AS plays,
       SUM(skipped) AS skips,
       ROUND(100.0 * SUM(skipped) / COUNT(*), 1) AS skip_pct
FROM plays
GROUP BY artist_id
HAVING COUNT(*) >= 30
ORDER BY skip_pct DESC
LIMIT 10;

-- That query shows artist_id rather than artist_name, because the name lives
-- in the other table. Fixing that is exactly what next session is for.
