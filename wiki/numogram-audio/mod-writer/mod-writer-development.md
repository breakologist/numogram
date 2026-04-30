# Development Guide

## Packaging
The project uses **setuptools** via `pyproject.toml`. To build or install:

```bash
# Editable install (development)
pip install -e .

# Build wheel
python -m build
```

The distribution name is `mod-writer`; the import name is `mod_writer` (setuptools maps hyphen to underscore automatically).

## Running tests
Pytest is used for the triangular semantics suite:

```bash
pytest tests/ -v
# or
python -m pytest tests/
```

All tests must pass before commit. They validate:
- Triangular length computation
- 64‑row cap
- Zero‑padding of unused channels
- Row overflow handling

## Project structure
```
mod-writer/
├── pyproject.toml
├── .gitignore
├── LICENSE
├── CREDITS.md
├── SKILL.md
├── mod_writer/
│   ├── __init__.py
│   ├── cli.py
│   ├── composer.py
│   ├── writer.py
│   ├── utils.py
│   ├── mapping.py
│   └── plugin.py
├── tests/
│   ├── __init__.py
│   └── test_triangular_semantics.py
├── data/
│   └── canonical_vectors.json
└── examples/
```

## License
- **Code**: MIT License (see `LICENSE`)
- **Data/Assets** (canonical vectors, motif tables): CC0 1.0 Universal (public domain)

## Contributing
When extending the Mod-Writer:
- Add unit tests for new algorithmic behaviour (triangular, entropy, etc.).
- Update `TRIAD_MOTIF_POLICY` and the wiki motif reference when introducing new motifs.
- Follow the existing import style (`mod_writer.` absolute or relative `.` within the package).
- Ensure `pytest` passes and `mod-writer --help` reflects new flags.
- Document flags and examples in `SKILL.md` and the wiki.

## Contact
See the Hermes Agent skill ecosystem or the `CREDITS.md` file for authorship and lineage information.
