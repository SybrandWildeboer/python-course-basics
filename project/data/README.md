# Put your input data here

The file (or files) your pipeline reads go in this folder. Then point `INPUT` at the top of
`pipeline.py` at it:

```python
INPUT = PROJECT / "data" / "my_export.csv"
```

Out of the box the pipeline reads the course's own messy file,
`data/messy/plays_messy.csv` at the repository root, so this folder starts empty.

## Three rules

- **Never edit the raw file by hand.** If something in it needs fixing, fix it in
  `clean()`. Then the fix is written down, and it happens again next time you get a new
  export. A hand edit is forgotten by next month.
- **Keep the original name and date** of an export, or note them in your project README.
  "Which version of the data was this?" is a question you will be asked.
- **It is not committed.** The repository's `.gitignore` ignores everything in this folder
  except this README, because your own spending, messages or listening history are
  personal and do not belong on GitHub. So write in your project README where the data
  comes from and how to get it again; that sentence is what goes in git instead of the
  file.
