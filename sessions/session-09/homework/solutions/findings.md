# Findings

An example of the written half of the session 9 homework. Yours should cover your own
charts and your own decisions. The point of this file is not the charts; it is being able
to say what they do and do not show.

Charts produced by `sessions/session-09/notebooks/04-three-charts-solved.ipynb`.

---

## Chart 1: minutes per month, by year

Both years show the same shape: a dip through June, July and August, and the heaviest
listening in the autumn and midwinter. The summer months average about 245 minutes against
about 397 for the rest of the year, so the effect is large rather than marginal. 2025 came
to 4,187 minutes against 4,421 in 2024, so it was about 5% quieter overall.

**What this does not show:** anything about why. A holiday, a change of job, or a different
way of listening that this log does not capture would all produce the same picture. It also
cannot tell me whether 2025 being lower is a trend or two years of noise, because two points
is not a trend.

## Chart 2: skip rate by device

Ignoring the `unknown` group, the speaker has the highest skip rate at 14.0% and the car the
lowest at 9.3%. The ordering is plausible: skipping a track in the car means reaching for a
phone while driving.

`unknown` actually tops the list at 15.4%. That may be a coincidence on 65 plays, or the
device may go unrecorded precisely when a play is abandoned quickly. I do not know, and the
chart cannot tell me.

**What this does not show:** that any of these differences are real. The gap between the top
and bottom device is about five percentage points, on group sizes from 65 to 964 plays, so
ordinary luck could produce it. I would want several times this much data before telling
anyone the car matters.

## Chart 3: how long is a play?

Play lengths cluster between about three and six minutes, with a sharp spike of very short
plays. 98% of skips last under two minutes, and the longest skip in the whole dataset is
2.67 minutes.

**What this does not show, and I nearly wrote it anyway:** that short plays are skips. Only
64% of the plays under two minutes were skipped. "Nearly every skip is short" and "nearly
every short play is a skip" are different claims, and this chart only supports the first. I
had the title the wrong way round in my first draft, which is a good argument for checking
the number behind every sentence you write.

---

## Cleaning decisions, and what they cost

I removed 134 of 2,223 rows, which is 6.0% of the file.

- **40 exact duplicates**, identical down to the `play_id`, which is supposed to be unique.
  Removing them is safe, and that uniqueness is the reason it is safe: without a unique id,
  two identical rows might be two real plays.
- **94 rows with no duration.** I dropped them because every question I asked is about
  minutes, and a play with no minutes cannot answer any of them.

The alternative was to fill those 94 with the average, which keeps every row and puts the
total at 8,995 minutes instead of 8,608, a difference of about 4%. I did not, because the
totals in chart 1 would then partly be numbers I had invented. For a question about *counts*
rather than minutes I would have kept them.

I **kept** the rows with a missing device, genre or country and labelled them `unknown`,
since they are still real plays. That does mean chart 2 has an `unknown` bar covering 65
plays, which is honest and easy to misread as a kind of device, and it happens to carry the
highest skip rate on the chart.

Dates arrived in three formats. I parsed each one explicitly rather than using
`pd.to_datetime(..., format="mixed", dayfirst=True)`, which runs without complaint and
misreads all 1,793 ISO dates in the file: `2025-09-06` becomes the 9th of June. Every monthly
chart above would have been wrong, and nothing would have warned me.

## What I would do differently with more time

- Check whether the summer dip is in the number of plays, the length of each play, or both.
  Chart 1 mixes the two, and they are different findings.
- Look at whether the `unknown` device rows cluster in time. If they are all from one
  fortnight, that is a logging fault rather than a property of listening.
