-- ===========================================================================
-- Session 5 homework: worked answers.
--
-- Every `expect:` comment is checked by tools/check_sql.py, so the row counts
-- and the figures in the notes are real results from data/music.db.
--
-- Task 1: the two that need something new are 3 (IS NULL, because = NULL
-- finds nothing) and 5 (a year column built from the date).
-- Task 2: the two that need a CTE are 13 and 15. Both run without one, and
-- both give a number that is too big, because awards fans the plays out.
-- ===========================================================================


-- ===========================================================================
-- TASK 1: ten questions about one table at a time
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
--     up has 10, out of 682 days with any listening. "The busiest day" sounds
--     like a finding and is really a coin toss between a handful of ordinary
--     days. Same lesson as
--     the tied artists in session 4: look at second place before believing a
--     single-row answer.
-- expect: 5 rows
SELECT played_at, COUNT(*) AS plays
FROM plays
GROUP BY played_at
ORDER BY plays DESC
LIMIT 5;


-- ===========================================================================
-- TASK 2: five questions across tables
-- ===========================================================================

-- 11. Which artists get skipped most? Names this time, 30 or more plays.
--    Mireille Basset 20.0%, The Paper Kites Society 18.6%,
--    Pale Cartography 17.5%, Kito Ndungu 17.4%, Yuki Tanaka Trio 17.2%.
--
--    Without the join this is the same query grouped by artist_id, and the
--    answer is a list of numbers nobody can read. The join brings the name
--    in. Group by a.artist_id rather than the name, so two artists who
--    happened to share a name would stay apart.
--
--    The HAVING still matters. Without it, Circuit Sparrow (2 skips in 7 plays,
--    28.6%) and Kanto Kids (2 in 8, 25.0%) go to the top, which is noise.
-- expect: 10 rows
SELECT a.artist_name,
       COUNT(*)       AS plays,
       SUM(p.skipped) AS skips,
       ROUND(100.0 * SUM(p.skipped) / COUNT(*), 1) AS skip_pct
FROM plays p
JOIN artists a USING (artist_id)
GROUP BY a.artist_id
HAVING COUNT(*) >= 30
ORDER BY skip_pct DESC
LIMIT 10;


-- 12. Listening by the decade the artist was formed in.
--    2010s: 22 artists, 1087 plays, 4556.9 minutes, far ahead of the rest.
--
--    formed_year / 10 * 10 uses integer division on purpose: 1996 / 10 is
--    199, and times 10 is 1990. In question 9 it was the trap; here it is the tool.
--
--    Two things to notice in the answer:
--
--    * The first row has a decade of NULL: 2 artists, 53 plays. Those are
--      Rosewood Lane and Cassette Revival, the unknown formed_year from
--      question 3. GROUP BY keeps the unknowns together as one group
--      rather than dropping them, which is the honest thing to do.
--
--    * The 1990s show 1 artist, but two artists were formed in the 1990s.
--      Iron Fernway (1996) has no plays, so the inner join removed him before
--      anything was counted. That is fine for "how much do you listen", and
--      wrong for "how many artists come from each decade".
-- expect: 5 rows
SELECT a.formed_year / 10 * 10        AS decade,
       COUNT(DISTINCT a.artist_id)     AS artists,
       COUNT(*)                        AS plays,
       ROUND(SUM(p.minutes_played), 1) AS minutes
FROM plays p
JOIN artists a USING (artist_id)
GROUP BY decade
ORDER BY decade;

--    COUNT(DISTINCT a.artist_id) is safe here, unlike SUM(DISTINCT) in the
--    fan-out block: artist_id is a key, so two equal values really are the
--    same artist.


-- 13. What share of each device's listening went to award winners?
--    phone 56.0%, laptop 57.5%, speaker 54.2%, car 50.6%, tablet 52.6%.
--    Across all devices, 4979.6 of the 8980.4 minutes, 55.4%.
--
--    THIS IS ONE OF THE TWO THAT NEEDS A CTE. The obvious query joins awards
--    straight onto plays:
-- expect: 5 rows
SELECT p.device,
       ROUND(SUM(p.minutes_played), 1) AS total_minutes,
       ROUND(SUM(CASE WHEN w.award_id IS NOT NULL
                      THEN p.minutes_played ELSE 0 END), 1) AS winner_minutes,
       ROUND(100.0 * SUM(CASE WHEN w.award_id IS NOT NULL
                              THEN p.minutes_played ELSE 0 END)
                   / SUM(p.minutes_played), 1) AS winner_pct
FROM plays p
LEFT JOIN awards w USING (artist_id)
GROUP BY p.device
ORDER BY total_minutes DESC;
--    phone 6726.5 minutes, 71.8% to winners. WRONG.
--
--    How to tell: question 7 said the phone has 4308 minutes in
--    total. Here it has 6726.5. A total that grows when you join something on
--    is fan-out. An artist with 3 awards has every play repeated 3 times, so
--    the winners' minutes are inflated, and so is the total they are divided
--    by. Both numbers are wrong, and the percentage is wrong too (71.8 against
--    56.0), because the winners were inflated far more than everyone else.
--
--    The fix: reduce awards to one row per artist FIRST, so the join can match
--    each play at most once.
-- expect: 5 rows
WITH winners AS (
    SELECT artist_id, COUNT(*) AS awards
    FROM awards
    GROUP BY artist_id
)
SELECT p.device,
       ROUND(SUM(p.minutes_played), 1) AS total_minutes,
       ROUND(SUM(CASE WHEN w.artist_id IS NOT NULL
                      THEN p.minutes_played ELSE 0 END), 1) AS winner_minutes,
       ROUND(100.0 * SUM(CASE WHEN w.artist_id IS NOT NULL
                              THEN p.minutes_played ELSE 0 END)
                   / SUM(p.minutes_played), 1) AS winner_pct
FROM plays p
LEFT JOIN winners w USING (artist_id)
GROUP BY p.device
ORDER BY total_minutes DESC;
--    phone 4308.2, laptop 2143.6, speaker 1334.6, car 777.6, tablet 416.4:
--    exactly question 7. The check is a number you got from an
--    independent query, not a number that looks plausible.
--
--    LEFT JOIN, not JOIN: an inner join to winners would throw away every
--    play by an artist with no award, and the "total" would only be the
--    winners' minutes, so every device would show 100%.
--
--    A subquery works too, and is just as correct:
--      CASE WHEN p.artist_id IN (SELECT artist_id FROM awards) THEN ...
--    It gives the same five percentages. The idea is the same either way:
--    the awards table never gets the chance to multiply the plays.

--    The overall figure, for the record.
-- expect: 1 rows
WITH winners AS (
    SELECT DISTINCT artist_id FROM awards
)
SELECT ROUND(SUM(p.minutes_played), 1) AS winner_minutes,
       ROUND(100.0 * SUM(p.minutes_played)
             / (SELECT SUM(minutes_played) FROM plays), 1) AS winner_pct
FROM plays p
JOIN winners USING (artist_id);


-- 14. Artists no longer active that you still listen to.
--    The Quiet Wires 64 plays, Rosewood Lane 40, Cassette Revival 13,
--    Velvet Aqueduct 3. All four were last played in 2025.
-- expect: 4 rows
SELECT a.artist_name,
       COUNT(*)                        AS plays,
       ROUND(SUM(p.minutes_played), 1) AS minutes,
       MAX(p.played_at)                AS last_played
FROM plays p
JOIN artists a USING (artist_id)
WHERE a.still_active = 0
GROUP BY a.artist_id
ORDER BY plays DESC;

--    Two artists are missing from that answer, for two different reasons.
--
--    * Gravel Choir is inactive and has no plays, so the inner join drops it.
--      Correct here: the question was who you STILL listen to.
--
--    * Iron Fernway has still_active = NULL, unknown. WHERE still_active = 0
--      does not match an unknown, exactly like = NULL in question 3. He has no
--      plays either, so he would not appear anyway, but on another day the
--      unknown could hide an artist you do play. Worth a look at the column:
-- expect: 3 rows
SELECT still_active, COUNT(*) AS artists
FROM artists
GROUP BY still_active;
--    NULL 1, 0 5, 1 34.


-- 15. Do award winners get listened to more, per artist?
--    Award winners: 17 artists, 292.9 minutes each on average.
--    No award:      23 artists, 173.9 minutes each.
--    So yes, by about 120 minutes per artist.
--
--    THIS IS THE OTHER ONE THAT NEEDS A CTE, for two reasons at once.
--
--    First, it is an average OF totals: one total per artist, then the average
--    of those. That needs two levels of grouping, and a CTE is where the first
--    level goes.
--
--    Second, awards fans the plays out. The obvious attempt joins everything
--    and divides by the number of artists:
-- expect: 2 rows
SELECT CASE WHEN w.award_id IS NULL THEN 'no award'
            ELSE 'award winner' END    AS grp,
       COUNT(DISTINCT a.artist_id)     AS artists,
       COUNT(*)                        AS rows_after_join,
       ROUND(SUM(p.minutes_played) / COUNT(DISTINCT a.artist_id), 1)
                                       AS minutes_per_artist
FROM artists a
LEFT JOIN plays  p USING (artist_id)
LEFT JOIN awards w USING (artist_id)
GROUP BY grp;
--    award winner 572.5. WRONG, nearly twice the real 292.9.
--
--    How to tell: the award winners' group has 2371 rows and 9732.1 minutes,
--    which is more minutes than the whole plays table holds (8980.4). That is
--    the wrong total from the session, turning up again. The no-award
--    group happens to be right, because those artists have no award rows to
--    multiply by, which makes the wrong answer even harder to spot.
--
--    The fix: one row per artist for plays, one row per artist for awards,
--    then join.
-- expect: 2 rows
WITH per_artist AS (
    SELECT artist_id, SUM(minutes_played) AS minutes
    FROM plays
    GROUP BY artist_id
),
awards_per_artist AS (
    SELECT artist_id, COUNT(*) AS awards
    FROM awards
    GROUP BY artist_id
)
SELECT CASE WHEN aw.artist_id IS NULL THEN 'no award'
            ELSE 'award winner' END            AS grp,
       COUNT(*)                                AS artists,
       ROUND(AVG(COALESCE(s.minutes, 0)), 1)   AS avg_minutes_per_artist
FROM artists a
LEFT JOIN per_artist        s  USING (artist_id)
LEFT JOIN awards_per_artist aw USING (artist_id)
GROUP BY grp;
--    The question said to count every artist, so the query starts FROM
--    artists and uses LEFT JOINs, and COALESCE turns the two never-played
--    artists' NULL into 0. Both of them are in the no-award group. Leave
--    them out and that group averages 190.5 over 21 artists instead: a real
--    difference, and the kind of thing task 3 is about.
--
--    One more wrong answer worth knowing: AVG(p.minutes_played) per group
--    gives 4.1 against 3.92. That is the average PLAY, not the average
--    ARTIST, and answers a different question entirely.


-- ===========================================================================
-- TASK 3: an example of a question where the join type changes the answer
-- ===========================================================================

-- Question: on average, how many awards does an artist in each genre have?

-- With an inner join: 7 genres. Rock says 3.0 awards per artist.
-- expect: 7 rows
SELECT a.genre,
       COUNT(DISTINCT a.artist_id) AS artists,
       COUNT(w.award_id)           AS awards,
       ROUND(1.0 * COUNT(w.award_id) / COUNT(DISTINCT a.artist_id), 2)
                                   AS awards_per_artist
FROM artists a
JOIN awards w USING (artist_id)
GROUP BY a.genre
ORDER BY awards_per_artist DESC;

-- With a left join: 8 genres. Rock says 0.6 awards per artist.
-- expect: 8 rows
SELECT a.genre,
       COUNT(DISTINCT a.artist_id) AS artists,
       COUNT(w.award_id)           AS awards,
       ROUND(1.0 * COUNT(w.award_id) / COUNT(DISTINCT a.artist_id), 2)
                                   AS awards_per_artist
FROM artists a
LEFT JOIN awards w USING (artist_id)
GROUP BY a.genre
ORDER BY awards_per_artist DESC;

-- Which one answers the question: the left join.
--
-- The question was about an artist in each genre, and most artists have no
-- awards: only 17 of the 40 have one. The inner join quietly changed the
-- question to "how many awards does an award WINNER have". For Rock that is a
-- single artist with 3 awards, against 5 Rock artists in total, so 3.0 became
-- the headline when the honest answer is 0.6. Afrobeat disappeared altogether,
-- because none of its 3 artists has won anything, and "0 awards" is an answer,
-- not a missing row.
--
-- The same thing happens with plays. Average plays per artist in Rock is 43.3
-- with an inner join and 26.0 with a left join, because Iron Fernway and
-- Gravel Choir are both Rock artists with no plays.
--
-- Neither query is wrong SQL. They answer different questions, and choosing
-- between them means deciding which question you meant.
