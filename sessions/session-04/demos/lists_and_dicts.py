"""The session 4 walkthrough: lists and dictionaries.

Run it from the repository root:

    python3 sessions/session-04/demos/lists_and_dicts.py
"""

# ================================================================== LISTS ==
devices = ["phone", "laptop", "speaker", "car"]

print(devices[0])       # phone     counting starts at 0
print(devices[2])       # speaker
print(devices[-1])      # car       the last one, however long the list
print(devices[-2])      # speaker
print(len(devices))     # 4
# print(devices[9])     # IndexError: list index out of range

# --- slicing: the end position is not included, same as range() -----------
nums = [10, 20, 30, 40, 50, 60]
print(nums[1:4])        # [20, 30, 40]
print(nums[:3])         # [10, 20, 30]
print(nums[3:])         # [40, 50, 60]
print(nums[-2:])        # [50, 60]

# --- growing and changing -------------------------------------------------
genres = ["Folk", "Jazz"]
genres.append("Rock")
print(genres)           # ['Folk', 'Jazz', 'Rock']

genres[0] = "Indie"
print(genres)           # ['Indie', 'Jazz', 'Rock']

print("Jazz" in genres)     # True
print("Metal" in genres)    # False

print(sorted(genres))   # a NEW sorted list
print(genres)           # the original, untouched

genres.sort()           # sorts the list itself and returns None
print(genres)
# genres = genres.sort()    # <- this throws your data away. Never do it.

# --- looping --------------------------------------------------------------
minutes = [4.65, 2.42, 7.10, 3.05]

total = 0
for value in minutes:
    total += value
print(f"{total:.2f} minutes")

for i, value in enumerate(minutes):
    print(f"{i}: {value}")

for n, value in enumerate(minutes, start=1):
    print(f"row {n} is {value}")


# =========================================================== DICTIONARIES ==
play = {
    "artist_name": "Fjord & Flint",
    "track_name": "Golden Garden",
    "genre": "Folk",
    "minutes_played": 4.65,
}

print(play["genre"])            # Folk
print(play["minutes_played"])   # 4.65
# print(play["mood"])           # KeyError: 'mood'

# --- adding, updating, and the difference between [] and .get() -----------
counts = {"Folk": 438, "Jazz": 154}
counts["Rock"] = 130            # add
counts["Folk"] = 439            # update
print(counts)

print("Jazz" in counts)         # True
# print(counts["Metal"])        # KeyError
print(counts.get("Metal"))      # None, no crash
print(counts.get("Metal", 0))   # 0, a default you chose

# --- looping over a dictionary --------------------------------------------
for genre in counts:                    # keys, by default
    print(genre)

for number in counts.values():          # just the values
    print(number)

for genre, number in counts.items():    # both, and the one you will use most
    print(f"{genre}: {number}")

# Sorted by value, biggest first. Copy this recipe and keep it; lambda gets
# a proper explanation later in the course.
for genre, number in sorted(counts.items(),
                            key=lambda pair: pair[1],
                            reverse=True):
    print(f"{genre:12} {number:>5}")


# ==================================== THE BIG IDEA: A TABLE IN PYTHON ======
# One dictionary is a row. One key is a column. A list of them is a table.
rows = [
    {"genre": "Folk", "minutes": 4.65},
    {"genre": "Jazz", "minutes": 7.10},
    {"genre": "Folk", "minutes": 2.42},
]

print(rows[0]["genre"])         # Folk       row 0, column "genre"
print(len(rows))                # 3          three rows

# Everything from here to the end of the course is a variation on this shape:
# the csv module gives you this, SQL returns this, and a pandas DataFrame in
# session 8 is this with a much faster engine underneath.
