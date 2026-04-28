# Wiki Export Process

This document describes how the Obsidian vault in `~/.hermes/obsidian/hermetic/` is exported to this repository.

## Source vault

The canonical source lives locally at:
```
~/.hermes/obsidian/hermetic/
├── wiki/   ← full Obsidian vault (not pushed)
├── raw/    ← Tier-1/2 source dictionaries (not pushed)
└── docs/   ← clean export (this directory)
```

## Export pipeline

1. Vault pages (`wiki/*.md`) are copied to `docs/`:
   - `wiki/tetralogue-*.md` → `docs/wiki/tetralogue-*.md`
   - all other pages → `docs/<name>.md`
2. Obsidian-specific metadata (`.obsidian/`) is excluded.
3. Source dictionaries (`raw/`) are excluded (copyright considerations).
4. The export is committed and pushed to `origin/master`.

This keeps the GitHub repository focused on the public-facing documentation and code while preserving the full vault locally for development.
