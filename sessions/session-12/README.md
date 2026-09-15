# Session 12: Presentation, review and what is next

**Goal:** they present their project, you review it together, and they leave with a map and
two or three concrete first steps.

**Slides:** [`slides/session-12.html`](../../slides/session-12.html) (14 slides)

Today is mostly listening. Resist filling silence, and resist correcting things during the
presentation.

---

## Run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00–0:25 | **They present.** Do not interrupt; take notes | Slide 2 |
| 0:25–1:00 | Code review together, then fix two or three things live | Slides 4–6 |
| 1:00–1:45 | The map: extensions, git with people, SQL at scale, four directions | Slides 8–12 |
| 1:45–2:00 | Two or three concrete next steps, written into their repo | Slides 13–14 |

## During the presentation

Ask them to cover: the question and why they picked it, how they approached it, a walkthrough
of the code, the result (run live), and what was hardest or was abandoned.

**Take notes rather than interrupting.** Things worth writing down: naming, repetition,
functions doing too much, charts that over-claim, anything that would break if the data
changed slightly.

That last point of theirs, what they abandoned, tells you more about their thinking than the
finished code does. Deciding not to do something is a skill.

## The review: five questions

Work through the code with these, in this order.

1. **Is it readable?** Would they understand it in six months?
2. **Does each function do one thing?** If it cannot be named after one thing, it is more
   than one.
3. **What happens if the data changes slightly?** An extra column, a new category, a missing
   month, twice the rows. This one most reliably finds real fragility: hardcoded column
   lists, assumed date ranges, a groupby that silently drops a new category.
4. **Where is the repetition?**
5. **Does the conclusion follow from the analysis?** The most important one, and the one
   professionals get wrong most often. A correct calculation of the wrong thing is the most
   expensive bug there is.

Invite push-back, and mean it. If they defend a decision well, say so out loud: it is the
most useful thing that can happen today.

Then **pick two or three things and fix them live**, commit, push, and run the
delete-and-rerun test once more. A list of improvements they take away is a list they will
not do.

Say clearly and specifically what they did well. "Your `clean()` docstring records the
decisions, which most professionals do not bother with" is worth ten times "good job".

## The map, and how to pitch it

It is a map, not a syllabus. They do not need most of it, and knowing it exists is the point.

- **`try` / `except` is the single best recommendation** for most people: small, immediately
  useful, and they have wanted it since session 3.
- **Window functions** are the honest answer for SQL, because they solve the awkward question
  from session 8.
- **A documentation typo as a pull request** is the least intimidating way into the git
  workflow.
- **Be honest about machine learning.** It is mostly data work with a model at the end, their
  pandas and SQL are 80% of the job, and it is usually the wrong next step.
- **Streamlit is worth naming**, because seeing your own work as a web page is motivating in
  a way another script is not.

Slide 12 is the most important one in the session: build things you want to exist, look up
what you do not know as you need it, read error messages carefully. Say it plainly and do not
soften it with a reading list.

## The last fifteen minutes

Pick **two or three** next steps based on what they visibly enjoyed over the twelve weeks,
not on what sounds impressive. Somebody who lit up during the joins session should not be
pointed at machine learning.

Each one gets **one specific resource and one specific first task**, and write them into
their repo as `NEXT.md` before the session ends. A plan in a file survives; a plan discussed
out loud does not. There is a template at `exercises/next-steps.md`.

## No notebooks this session

By design. Today is their project, their code, their repo.

## To close

Show them their session 1 file if you still have it, next to their project. Twelve weeks, a
few hundred lines of their own code, a repo full of real commits, and a project they chose,
scoped, built and presented, from nothing.

End warmly and end on time. And tell them the questions channel stays open, because it costs
you very little and it matters a lot in the month after a course ends.
