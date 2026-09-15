# Prep checklist

One page per session. Most of the preparation is done; this is what is left.

---

## Before the course

- [ ] Repo pushed and public, clone URL on session 1 slide 12 verified
- [ ] `python3 data/scripts/build_dataset.py` run, data committed
- [ ] `python3 tools/check_slides.py`, `check_sql.py`, `nbtool.py run` all clean
- [ ] `docs/install.md` sent, **with the "do not install yet" note**
- [ ] Twelve sessions in both calendars, including the **two-week gap** before session 12
- [ ] Saturday check-in agreed, and "not done is fine" said out loud
- [ ] A channel for between-session questions

## Session 1: Setup and first contact

- [ ] Nothing to prepare beyond the above
- [ ] Have `data/clean/plays.csv` open, to show the dataset they will use all course
- [ ] Expect the install to take the full 45 minutes. It is normal
- [ ] Ask them for **one repetitive thing they do at work**, and write it down. You will use
      it in session 11

## Session 2: Control flow

- [ ] Open with their homework, especially task 2
- [ ] Protect the ten minutes of deliberately breaking things
- [ ] Have them kill an infinite loop on purpose

## Session 3: Functions

- [ ] Have their session 2 `statistics.py` open, ready to refactor
- [ ] The surprise second list for the live exercise: `[4, 8, 15, 16, 23, 42]`

## Session 4: Lists, dictionaries and files

- [ ] Dataset generated
- [ ] `data/clean/plays.csv` open in VS Code, so you can show the raw text
- [ ] **Remind them to create a GitHub account before session 5**

## Session 5: Git and GitHub

- [ ] Check they have a GitHub account. If not, do it in the first five minutes
- [ ] Decide the authentication route: `gh auth login` is the least painful
- [ ] **Budget the full twenty minutes for authentication**
- [ ] Remind them to install DB Browser for SQLite before session 6

## Session 6: SQL foundations

- [ ] DB Browser installed, `data/music.db` opens
- [ ] Have their session 4 counting script open, to put next to `GROUP BY`

## Session 7: Joins and shaping

- [ ] Nothing to prepare
- [ ] Know the fan-out numbers: 8,980.4 becomes 9,732.1; `SUM(DISTINCT)` gives 680.6;
      Fjord & Flint has 237 plays, 3 awards and 711 joined rows
- [ ] If earlier blocks run fast, spend the time here rather than on views

## Session 8: pandas

- [ ] `pip install pandas matplotlib` may take a few minutes on a slow connection
- [ ] Have their sessions 6 and 7 query files to hand, since the exercise translates **their
      own** queries

## Session 9: Cleaning and visualization

- [ ] `data/messy/plays_messy.csv` generated
- [ ] Know the date-trap figures: 1,793 ISO dates, 628 rows corrupted by `dayfirst=True`,
      71% correct against 100%
- [ ] Know the two totals: 8,608 minutes if you drop, 8,995 if you fill

## Session 10: Putting it together

- [ ] `project/` template reviewed, since they copy it next session
- [ ] Have their session 9 `clean_plays()` open, ready to lift into the pipeline
- [ ] **Ask them to bring project ideas and data to session 11**, and warn them you will
      scope it down hard

## Session 11: Project scoping and setup

- [ ] `sessions/session-11/exercises/scoping.md` ready to fill in together
- [ ] The repetitive-work note from session 1
- [ ] Be ready to say no to the first idea, warmly
- [ ] **Confirm the session 12 date and watch them put it in the calendar**
- [ ] Do not leave without a pushed commit that prints the row count

## Session 12: Presentation, review and what is next

- [ ] Their repo read **beforehand**, with two or three review points noted
- [ ] Their session 1 file found, if you still have it, to show alongside their project
- [ ] `sessions/session-12/exercises/next-steps.md` ready to fill in as their `NEXT.md`
- [ ] Two or three specific resources in mind, chosen for what they **enjoyed**
- [ ] Something specific and true to say about what they did well
