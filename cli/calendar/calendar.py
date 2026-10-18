#!/usr/bin/env python3
"""CLI wrapper: `python3 calendar.py ...` → numogram_calendar.main().

The logic lives in numogram_calendar.py. A *module* called calendar.py would shadow
Python's stdlib `calendar` for anything imported from this directory, so this file
is only a launcher: it removes its own directory from sys.path before any other
import (so stdlib `import calendar` elsewhere still resolves to the real module),
then loads numogram_calendar by file path.
"""
import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [p for p in sys.path if os.path.abspath(p or os.curdir) != _here]

import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "numogram_calendar", os.path.join(_here, "numogram_calendar.py"))
_mod = importlib.util.module_from_spec(_spec)
sys.modules["numogram_calendar"] = _mod
_spec.loader.exec_module(_mod)

if __name__ == "__main__":
    sys.exit(_mod.main())
