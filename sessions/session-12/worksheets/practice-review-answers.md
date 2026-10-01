# Practice review: the answers

For `practice-review.diff`. Try it with the checklist first.

There are five problems planted in the diff, and two things done well. The numbers below come
from running both versions of the file on the course data (`data/clean/plays.csv`,
`awards.csv` and `artists.csv` copied into the project's `data/` folder).

---

## The two that change the answer

### 1. Fan-out from the awards merge (the expensive one)

```python
return plays.merge(awards, on="artist_name", how="left")
```

An artist with three awards now has every play repeated three times. Nothing complains,
because nothing went wrong as far as pandas is concerned.

| | Before the commit | After the commit |
|---|---|---|
| rows going into `analyse` | 2,183 | 3,391 |
| total minutes, all genres | 8,980.4 | 13,732.9 |
| Folk minutes | 1,562.2 | 4,025.9 |
| Rock minutes | 523.3, last of eight | 1,048.2, third |
| Folk "awards" | 9 really | 1,095 |

The awards column is wrong too, and worse: `count` of `award_id` after the merge counts one
award *per play*, so Folk's 9 awards become 1,095.

This is session 7's fan-out, in pandas, in the wild. The comment to write: **"How many rows
come out of `add_awards`? Can you add `validate=` to the merge?"** With
`validate="many_to_one"` the merge stops with an error the first time it would duplicate a
play.

**The fix** is the session 7 fix: aggregate first, then join. Minutes per genre come from
`plays` alone; awards per genre come from `artists` and `awards`; the two genre-level tables
are joined one to one at the end.

```python
def awards_per_genre(awards, artists):
    """Return the number of awards won by the artists of each genre."""
    per_artist = awards.groupby("artist_id", as_index=False).agg(awards=("award_id", "count"))
    with_genre = artists.merge(per_artist, on="artist_id", how="left", validate="one_to_one")
    return with_genre.groupby("genre", as_index=False).agg(awards=("awards", "sum"))


def analyse(plays, awards, artists):
    """Return total minutes and awards per genre, biggest first."""
    minutes = plays.groupby("genre", as_index=False).agg(minutes=("minutes_played", "sum"))
    summary = minutes.merge(awards_per_genre(awards, artists), on="genre",
                            how="left", validate="one_to_one")
    return summary.sort_values("minutes", ascending=False)
```

That gives the original minutes back (8,980.4 in total, Rock last again at 523.3), and awards
per genre that add up to 33, the number of rows in `awards.csv`. That last check is the
independent confirmation: the parts add up to the whole.

### 2. The bare `except` that returns an empty DataFrame

```python
try:
    return pd.read_csv(path)
except:
    return pd.DataFrame()
```

The commit message says this stops the pipeline crashing on missing files. It does not. On
any machine without Sam's file (see 3), `load` hands back an empty DataFrame and the pipeline
crashes anyway, one function later, with:

```
KeyError: 'artist_name'
```

which says nothing about files at all. And because the `except` is bare, it would also hide a
typo, a permissions problem, or a malformed CSV, and turn each of them into the same
misleading `KeyError`.

The comment: **"Can `load` let `FileNotFoundError` through, and `main()` catch it with a
message?"**

## The three that make it fragile

### 3. A path that exists on one laptop

```python
PLAYS = Path("C:/Users/sam/Desktop/plays.csv")
```

The line above it, `HERE / "data" / "plays.csv"`, worked everywhere. This one works for Sam,
on one machine, until the Desktop is tidied. Combined with 2, everyone else gets a confusing
`KeyError` instead of a clear error naming the missing file. Put the file in `project/data/`
and change the line back.

### 4. A `print` inside `analyse`

```python
print(summary)
```

Probably left over from debugging. `analyse` is a calculating function, so it returns and
does not print (session 3). In a notebook or a test, every call now dumps a table nobody asked
for. Delete it; `main()` is the place for output.

### 5. Two changes in one commit

"Add awards per genre, **and** stop crashing on missing files" is two commits. Separately,
the second would have been easy to review and the first would have stood out on its own. The
comment: "Could these be two commits next time?" Not a blocker, but worth saying once.

## Two things to keep

- **`save` got a docstring and `mkdir(parents=True, exist_ok=True)`.** Small, correct, and
  `parents=True` means it works even when the folder above `output/` is missing.
- **`AWARDS` and `ARTISTS` are built from `HERE`,** the right way, which makes the `PLAYS`
  line stand out all the more. Point that out; it suggests the absolute path was a quick hack
  rather than a misunderstanding.

---

## If you only had time for two comments

1 and 2. Fan-out silently changes every number in the output, and the bare `except` turns a
clear error into an obscure one. The other three are real but cheap.
