# notebooks

Where you explore, think, and try things out.

Once a piece of work has settled, move it into `src/` and import it back:

```python
import sys
sys.path.append("../src")

from pipeline import load, clean
plays = clean(load())
```

Nothing gets copied twice, and the script stays the single place the logic lives.

Before you commit a notebook, use **Restart and Run All**. If it cannot run cleanly from top
to bottom, it is not finished, however good the output looks on screen.
