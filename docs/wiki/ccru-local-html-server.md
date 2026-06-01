---
title: Local HTML Server for CCRU Raw Archive
created: 2026-06-01
tags: [ccru, raw, server, html, local]
---

# Local HTML Server for CCRU Raw Archive

Use a simple Python HTTP server to browse the raw CCRU HTML archive at `raw/www.ccru.net` with relative paths, so rendered pages match the site's original URL structure.

## Command

```bash
python3 -m http.server 8080 --bind 127.0.0.1 -d /home/etym/.hermes/obsidian/hermetic/raw/www.ccru.net
```

- `-d` sets the web root so published paths are clean:
  - `http://127.0.0.1:8080/syzygy.htm`
  - `http://127.0.0.1:8080/occultures/mythlemuria.htm`
  - `http://127.0.0.1:8080/zones/zone6.htm`

## Quick health check

```bash
curl -I -s http://127.0.0.1:8080/syzygy.htm | head -n 1
```

## Open in browser

- `<http://127.0.0.1:8080/syzygy.htm>`
- `<http://127.0.0.1:8080/occultures/mythlemuria.htm>`
- `<http://127.0.0.1:8080/occultures/mesh.htm>`

## Notes

- `--directory` sets the web root, so published URLs are clean relative paths.
- Default port 8080; change if something is already bound.
- Stop with `pkill -f "http.server 8080"` or kill the recorded PID.

## Why it’s useful

Some CCRU pages depend on relative assets (`../images/ccrulogo.gif`, `occult.css`, `zoneimages/*.gif`). A proper web server restores those links; `web_extract` and raw file reads lose the visual and layout context that can change how you interpret a page.
