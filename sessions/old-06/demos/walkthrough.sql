-- ===========================================================================
-- Session 6 walkthrough: every query from the slides, in order.
--
-- Open data/music.db in DB Browser for SQLite, go to the Execute SQL tab, and
-- run these one at a time. Ctrl+Enter (Cmd+Enter on a Mac) runs the query the
-- cursor is sitting in.
--
-- Nothing here changes the data. Every query only reads.
-- ===========================================================================


-- --------------------------------------------------------------- SELECT ---
-- Which columns, from which table. That is the shape of all of SQL.

SELECT track_name, minutes_played FROM plays;

SELECT * FROM plays;                 -- every column. Fine for exploring
SELECT artist_name, genre, formed_year FROM artists;


-- ---------------------------------------------------------------- WHERE ---
-- Which rows. Note: ONE equals sign, and SINGLE quotes for text.

SELECT track_name, minutes_played FROM plays
WHERE minutes_played > 8;            -- 82 rows

SELECT * FROM plays WHERE device = 'phone';          -- 1039 rows
SELECT * FROM plays WHERE skipped != 0;              -- 258 rows
SELECT * FROM plays WHERE played_at >= '2025-01-01'; -- 1061 rows

-- Dates are text in YYYY-MM-DD form, which compares and sorts correctly as
-- text. That is exactly why the format is worth insisting on.


-- ------------------------------------------------------ AND, OR, NOT ------
SELECT * FROM plays
WHERE device = 'phone' AND minutes_played > 8;

SELECT * FROM plays
WHERE device = 'car' OR device = 'tablet';           -- 284 rows

SELECT * FROM plays
WHERE NOT skipped = 1 AND played_at >= '2025-01-01';

-- AND binds tighter than OR, so bracket anything mixed. Without the brackets
-- below you would get "car, or (tablet and long)", which is not the question.
SELECT * FROM plays
WHERE (device = 'car' OR device = 'tablet')
  AND minutes_played > 5;


-- ------------------------------------------- IN, BETWEEN, LIKE ------------
SELECT * FROM plays WHERE device IN ('car', 'tablet');   -- 284 rows

SELECT * FROM plays
WHERE played_at BETWEEN '2025-06-01' AND '2025-08-31';   -- 175 rows
-- BETWEEN includes BOTH ends, unlike Python's range() and slicing.

SELECT artist_name FROM artists WHERE artist_name LIKE 'The %';  -- 5 rows
SELECT * FROM plays WHERE track_name LIKE '%Lines';
--   %  any run of characters, including none
--   _  exactly one character


-- ------------------------------------------------------------- NULL -------
-- NULL means UNKNOWN. Not zero, not empty text.

SELECT artist_name FROM artists WHERE formed_year = NULL;
-- 0 rows, no error, no warning. An empty result that looks like an answer.
-- Asking whether an unknown equals an unknown gives "unknown", which is not
-- true, so no row comes back.

SELECT artist_name, formed_year, still_active FROM artists
WHERE formed_year IS NULL OR still_active IS NULL;
-- Rosewood Lane, Cassette Revival, Iron Fernway

SELECT COUNT(*) FROM artists WHERE formed_year IS NOT NULL;   -- 38 of 40

-- Aggregates skip NULLs, so this is the average of 38 values, not 40.
SELECT ROUND(AVG(formed_year), 1) FROM artists;


-- --------------------------------------------- ORDER BY and LIMIT ---------
SELECT track_name, minutes_played FROM plays
ORDER BY minutes_played DESC
LIMIT 5;
-- Paper Avenue 11.01, Harbour Season 10.96, Broken Lines 10.77, ...

SELECT artist_name, formed_year FROM artists ORDER BY formed_year ASC;

SELECT device, minutes_played FROM plays
ORDER BY device, minutes_played DESC;    -- sort by two columns

-- Without ORDER BY, a database makes no promise about row order. LIMIT 5 on
-- its own gives five arbitrary rows, not the first five of anything.


-- --------------------------------------------------------- DISTINCT -------
SELECT DISTINCT device FROM plays;              -- 5 values
SELECT DISTINCT genre FROM artists ORDER BY genre;
SELECT COUNT(DISTINCT track_name) FROM plays;   -- 168 tracks in 2183 plays

-- Run DISTINCT on every categorical column of a table you have not seen
-- before. It is how you discover that somebody has been typing Phone, phone
-- and PHONE, which is what session 9 is about.


-- -------------------------------------------------------- aggregates ------
SELECT COUNT(*) FROM plays;                     -- 2183

SELECT
  COUNT(*)                      AS plays,
  ROUND(SUM(minutes_played))    AS total_min,
  ROUND(AVG(minutes_played), 2) AS avg_min,
  MAX(minutes_played)           AS longest,
  MIN(played_at)                AS first_day
FROM plays;
-- 2183 | 8980 | 4.11 | 11.01 | 2024-01-01

-- COUNT(*) counts rows. COUNT(column) counts rows where that column is not
-- NULL. Here is the difference, in one query:
SELECT COUNT(*) AS rows_total,
       COUNT(formed_year) AS have_year,
       COUNT(still_active) AS have_active
FROM artists;
-- 40 | 38 | 39


-- ---------------------------------------------------------- GROUP BY ------
-- One answer per group. This is your session 4 counting dictionary, in one
-- line, with the database doing the looping.

SELECT
  device,
  COUNT(*)                      AS plays,
  ROUND(AVG(minutes_played), 2) AS avg_min
FROM plays
GROUP BY device
ORDER BY plays DESC;
-- phone 1039 4.15 | laptop 524 4.09 | speaker 336 3.97 | car 179 4.34 | tablet 105 3.97


-- The GROUP BY trap. track_name is neither grouped nor aggregated, so which
-- of the 1039 phone track names should appear? SQLite picks one and says
-- nothing. Most other databases refuse.
SELECT device, track_name, COUNT(*) FROM plays GROUP BY device;

-- Say what you actually meant. Either group by both:
SELECT device, track_name, COUNT(*) FROM plays GROUP BY device, track_name;

-- or aggregate the other column:
SELECT device,
       COUNT(DISTINCT track_name) AS tracks,
       COUNT(*)                   AS plays
FROM plays
GROUP BY device;

-- The rule: every column in the SELECT is either in the GROUP BY or wrapped
-- in an aggregate. No exceptions, even though SQLite lets you break it.


-- ------------------------------------------------------------ HAVING -----
SELECT country, COUNT(*) AS artists
FROM artists
GROUP BY country
HAVING COUNT(*) >= 3
ORDER BY artists DESC;
-- United States 4 | United Kingdom 4 | Netherlands 3

-- WHERE filters ROWS before grouping. HAVING filters GROUPS after grouping.
-- Both together, doing different jobs:
SELECT device, COUNT(*) AS plays
FROM plays
WHERE played_at >= '2025-01-01'      -- narrow the rows first
GROUP BY device
HAVING COUNT(*) > 100                -- then narrow the groups
ORDER BY plays DESC;


-- ------------------------------------------------- the order it runs in ---
-- FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
--
-- Which explains two things that otherwise look arbitrary:
--   * WHERE cannot see a COUNT, because no counting has happened yet
--   * a name you invent with AS cannot be used in the WHERE, but can in the
--     ORDER BY, because the SELECT runs later than one and earlier than the
--     other
