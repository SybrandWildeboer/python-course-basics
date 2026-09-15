# SQL cheatsheet

Sessions 6 and 7, on one page. Every query here runs against `data/music.db`.

---

## The shape of a query

```sql
SELECT   device, COUNT(*) AS plays     -- which columns
FROM     plays                         -- from which table
WHERE    minutes_played > 2            -- which rows
GROUP BY device                        -- collapsed into which groups
HAVING   COUNT(*) > 300                -- which groups to keep
ORDER BY plays DESC                    -- in which order
LIMIT    5;                            -- how many
```

**And the order it actually runs in:**

```
FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
```

Which explains two things that otherwise look arbitrary:

- `WHERE` cannot see a `COUNT`, because no counting has happened yet. `HAVING` can.
- a name you invent with `AS` cannot be used in the `WHERE`, but it can in the `ORDER BY`.

## Conventions

- keywords in capitals, so they stand out. SQL does not care
- one clause per line
- single quotes for text: `'phone'`. Double quotes mean something else
- `--` starts a comment
- `;` ends a statement

## Choosing rows

```sql
WHERE minutes_played > 8
WHERE device = 'phone'                 -- ONE equals sign
WHERE skipped != 0
WHERE played_at >= '2025-01-01'        -- YYYY-MM-DD text sorts correctly

WHERE device = 'phone' AND minutes_played > 8
WHERE device = 'car' OR device = 'tablet'
WHERE NOT skipped = 1

-- AND binds tighter than OR, so bracket anything mixed
WHERE (device = 'car' OR device = 'tablet') AND minutes_played > 5

WHERE device IN ('car', 'tablet')                       -- one of these
WHERE played_at BETWEEN '2025-06-01' AND '2025-08-31'   -- BOTH ends included
WHERE artist_name LIKE 'The %'                          -- starts with
WHERE track_name LIKE '%Lines'                          -- ends with
WHERE track_name LIKE '%Lines%'                         -- contains
```

`%` is any run of characters, `_` is exactly one.

## NULL

```sql
WHERE formed_year = NULL        -- WRONG. 0 rows, no error, no warning
WHERE formed_year IS NULL       -- right
WHERE formed_year IS NOT NULL
```

`NULL` means **unknown**, not zero and not empty text. An unknown is not equal to anything,
including another unknown, so `= NULL` matches nothing and says nothing about it.

Aggregates skip NULLs, so `AVG(formed_year)` over 40 artists with 2 gaps is the average of
38 values.

```sql
COALESCE(awards, 0)             -- "awards, or 0 if it is NULL"
```

## Sorting, cutting, listing

```sql
ORDER BY minutes_played DESC          -- DESC biggest first, ASC is the default
ORDER BY device, minutes_played DESC  -- by two columns
LIMIT 5
LIMIT 5 OFFSET 10                     -- skip the first ten

SELECT DISTINCT device FROM plays;
SELECT COUNT(DISTINCT track_name) FROM plays;
```

`ORDER BY x DESC LIMIT 5` is the "top five" recipe. **Without `ORDER BY` a database makes no
promise about row order**, so `LIMIT 5` alone gives five arbitrary rows.

Run `DISTINCT` on every categorical column of a table you have not seen before. It is how you
find out somebody has been typing `Phone`, `phone` and `PHONE`.

## Aggregates

```sql
SELECT COUNT(*)                      AS rows_total,
       COUNT(formed_year)            AS have_year,     -- skips NULLs!
       SUM(minutes_played)           AS total,
       ROUND(AVG(minutes_played), 2) AS average,
       MIN(played_at)                AS first_day,
       MAX(minutes_played)           AS longest
FROM plays;
```

`COUNT(*)` counts rows. `COUNT(column)` counts rows where that column is not NULL. That
difference is what makes "never played" work rather than reading as "played once".

## GROUP BY

```sql
SELECT device,
       COUNT(*)                      AS plays,
       ROUND(AVG(minutes_played), 2) AS avg_min
FROM plays
GROUP BY device
ORDER BY plays DESC;
```

**The rule:** every column in the `SELECT` is either in the `GROUP BY` or wrapped in an
aggregate. SQLite lets you break it and gives you a value picked at random. Most other
databases refuse, which is kinder.

```sql
GROUP BY device, genre          -- group by two things
HAVING COUNT(*) > 300           -- filter the GROUPS
```

`WHERE` filters rows before grouping. `HAVING` filters groups after. Both in one query do
different jobs.

## Percentages, and the integer-division trap

```sql
SELECT device,
       COUNT(*)     AS plays,
       SUM(skipped) AS skips,
       ROUND(100.0 * SUM(skipped) / COUNT(*), 1) AS skipped_pct
FROM plays
GROUP BY device;
```

In SQLite `19 / 179` is **0**, because two whole numbers divide to a whole number.
`100.0 *` first forces a proper division. `SUM(skipped)` works because the column is already
0 or 1.

## Dates

```sql
strftime('%Y', played_at)       -- '2025'    the year
strftime('%m', played_at)       -- '04'      the month
strftime('%Y-%m', played_at)    -- '2025-04' year and month
strftime('%w', played_at)       -- weekday, 0 is Sunday

substr(played_at, 1, 4)         -- cruder, works because it is YYYY-MM-DD text

SELECT strftime('%Y', played_at) AS year, COUNT(*)
FROM plays GROUP BY year;
```

## Joins

```sql
SELECT p.played_at, a.artist_name, p.minutes_played
FROM plays AS p
JOIN artists AS a ON a.artist_id = p.artist_id;

-- USING, when the key has the same name on both sides
FROM plays JOIN artists USING (artist_id)
```

Alias every table and qualify every column, even when you do not have to. Queries grow.

| Join | Keeps |
|---|---|
| `JOIN` (`INNER JOIN`) | only rows that matched on both sides |
| `LEFT JOIN` | every row of the first table; unmatched columns come back `NULL` |

**The question decides which.** "How long did I listen to each artist I played" is inner.
"Which artists have I never played" needs left, because the answer is made of rows with no
match:

```sql
SELECT a.artist_name, COUNT(p.play_id) AS plays
FROM artists a
LEFT JOIN plays p USING (artist_id)
GROUP BY a.artist_id
HAVING plays = 0;
```

`COUNT(p.play_id)`, not `COUNT(*)`. After a left join an unmatched row still exists, full of
NULLs, and `COUNT(*)` counts it as 1.

## Fan-out: the one to remember

```sql
SELECT ROUND(SUM(minutes_played), 1) FROM plays;
-- 8980.4    the truth

SELECT ROUND(SUM(p.minutes_played), 1)
FROM plays p JOIN awards w ON w.artist_id = p.artist_id;
-- 9732.1    nothing was filtered, nothing was added
```

An artist with 3 awards has each of their plays matched three times, so the minutes are
counted three times. **A one-to-many join multiplies rows**, and every `SUM`, `COUNT` and
`AVG` downstream is wrong.

**`SUM(DISTINCT x)` is not the fix.** It adds each different value once, so two real plays
that happened to last the same time become one. It gives 680.6: wrong in the other
direction.

**The fix is to aggregate first, then join:**

```sql
WITH per_artist AS (
    SELECT artist_id, COUNT(*) AS plays, SUM(minutes_played) AS minutes
    FROM plays
    GROUP BY artist_id
)
SELECT a.artist_name, s.plays, s.minutes, COUNT(w.award_id) AS awards
FROM per_artist s
JOIN artists a USING (artist_id)
LEFT JOIN awards w USING (artist_id)
GROUP BY a.artist_id;
```

**The habit:** after any join, compare the row count with what it was before. If it went up
and you did not expect it to, stop.

## Subqueries, CTEs and views

```sql
-- a subquery: runs first, treated as a table
SELECT * FROM (SELECT artist_id, COUNT(*) AS n FROM plays GROUP BY artist_id) AS s
WHERE s.n > 100;

-- the same thing as a CTE: named, at the top, reads top to bottom
WITH per_artist AS (
    SELECT artist_id, COUNT(*) AS n FROM plays GROUP BY artist_id
),
awarded AS (
    SELECT artist_id, COUNT(*) AS awards FROM awards GROUP BY artist_id
)
SELECT * FROM per_artist JOIN awarded USING (artist_id);

-- a view: a saved query that behaves like a table, always current
CREATE VIEW artist_summary AS SELECT ...;
SELECT * FROM artist_summary WHERE plays = 0;
DROP VIEW artist_summary;
```

Prefer a CTE to a nested subquery once the query needs scrolling. You can have several,
separated by commas, and each can use the ones above it.

## When the numbers look wrong

| Symptom | Likely cause | Check |
|---|---|---|
| Totals too large | Fan-out from a one-to-many join | Row count before and after |
| Rows missing | Inner join where you needed left | Swap it, compare counts |
| Everything empty | Join keys do not match | Compare a few values by eye |
| Counts one too many per group | `COUNT(*)` after a left join | `COUNT(other.key)` |
| A percentage is 0 | Whole-number division | `100.0 *` first |
| Nonsense in a grouped column | Column neither grouped nor aggregated | Add it to `GROUP BY` |

**Above all: know roughly what the answer should be before you run the query.** 8,980 minutes
over two years is about twelve minutes a day, which is plausible. 9,732 would have passed
unnoticed without something to compare it to.
