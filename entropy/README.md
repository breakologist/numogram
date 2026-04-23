# numogram-entropy

Hardware entropy digested through numogram traversal.

## Install
```bash
pip install -e .
```

## Usage
```python
from numogram_entropy.core import NumogramTraverser
t = NumogramTraverser()
path = t.traverse_from_hardware()
```

## Sources
12 collectors: thermal, CPU frequency, GPU, /proc/stat, timing jitter, fsync timing, etc.

See `pyproject.toml` for entry points and dependencies.
