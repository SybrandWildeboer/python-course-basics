-- ===========================================================================
-- Session 5 homework: your answers.
--
-- Write each query under its question. Run it, check the answer is sensible,
-- then commit this file. Before each one, write down what you expect. After
-- every join, check the row count.
-- ===========================================================================


-- ---------------------------------------------------------------------------
-- TASK 1: ten questions about one table at a time.
-- ---------------------------------------------------------------------------

-- 1. How many artists are in the database?


-- 2. Which artists are from the Netherlands? Show name and genre.


-- 3. Which artists have an unknown formed_year?


-- 4. What are the five longest plays? Show the track and the minutes.


-- 5. How many plays happened in 2024, and how many in 2025?
--    One query, two rows.


-- 6. Which tracks were played more than 40 times?
--    Show the track and the count, most played first.


-- 7. What is the total listening time in minutes for each device,
--    rounded to a whole number?


-- 8. Which genres have five or more artists?


-- 9. What proportion of plays on each device were skipped?
--    Show device, total plays, skipped plays, and the percentage to one
--    decimal place.


-- 10. What was the busiest single day, by number of plays?


-- ---------------------------------------------------------------------------
-- TASK 2: five questions across tables. Each needs a join and an aggregate.
-- ---------------------------------------------------------------------------

-- 11. Which artists get skipped most? Show the artist's NAME, plays, skips and
--     the skip percentage to one decimal place. Only artists with 30 or more
--     plays, top ten.


-- 12. How much do you listen to artists by the decade they were formed in?
--     Show the decade, the number of artists, the plays and the total minutes.


-- 13. What share of the listening time on each device went to artists who
--     have won at least one award? Show device, total minutes, award-winner
--     minutes, and the percentage to one decimal place.


-- 14. Which artists that are no longer active do you still listen to?
--     Show plays, total minutes, and the date you last played each one.


-- 15. Do award winners get listened to more? Compare the average total minutes
--     per artist for award winners against everyone else. Count every artist,
--     including any you have never played.


-- ---------------------------------------------------------------------------
-- TASK 3: a question where the join type changes the answer.
--
-- Show both queries and both answers, then explain which one answers the
-- question you actually asked, and why.

-- My question:

-- With an inner join:
-- What I got:


-- With a left join:
-- What I got:


-- Which one answers my question, and why:
