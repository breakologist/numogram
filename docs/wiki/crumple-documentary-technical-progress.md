---
title: Crumple/Reconstruct Documentary — Technical Progress Log
created: 2026-05-14
updated: 2026-05-14
tags: [documentary, manim, video-embedding, numogram, crumple-reconstruct]
status: in-progress
---

## Overview

This entry logs the engineering journey of embedding archival video clips into the **Crumple/Reconstruct Extended Documentary** (`manim_crumple_documentary.py`), from initial Manim Community failures through to the current 3b1b‑ManimGL setup. The core problem remains unsolved: `VideoMobject` renders as blank (opaque black) rectangles despite `moviepy` being available and the source MP4 files being valid.

---

## Problem Statement

- **Goal:** Render a 5‑act Manim documentary that plays three archival videos (Zone Spiral, Syzygy Cascade, single trajectory) *inside* the animation.
- **Approach:** Use `VideoMobject` to embed MP4s, combined with generative scenes for batch validation and correlation plots.
- **Obstacle:** Under **Manim Community** (`manim` package v0.20.1), `VideoMobject` is **not available**. A fallback placeholder was implemented, but the film was never “complete.”
- **Target:** Switch to **3b1b’s ManimGL** (`manimlib`), where `VideoMobject` exists and should display videos.

---

## Timeline & Interventions

### 1. Environment setup (2026‑05‑14)

| Step | Action | Outcome |
|------|--------|---------|
| pipx uninstall manim | remove Community version | ✓ |
| pipx install git+https://github.com/3b1b/manim.git | install 3b1b Manim (provides `manimgl` binary) | ✓ installed as `manimgl` package |
| pipx inject manimgl moviepy | add video decoding deps | ✓ `moviepy`, `imageio`, `imageio-ffmpeg` present |
| sudo pacman -S xorg-server-xvfb | install virtualframebuffer for headless OpenGL | ✓ |

### 2. Engine‑agnostic script (`manim_crumple_documentary.py`)

Created a dual‑engine import block:

```python
try:
    from manimlib import *
    _ENGINE = 'manimgl'
except Exception:
    from manim import *
    _ENGINE = 'manim'
```

Added conditional `VideoMobject` import:

```python
try:
    if _ENGINE == 'manimgl':
        from manimlib import VideoMobject
    else:
        from manim import VideoMobject
    _HAS_VIDEO = True
except ImportError:
    VideoMobject = None
    _HAS_VIDEO = False
```

Inserted **Create alias** for manimgl:

```python
if _ENGINE == 'manimgl' and 'Create' not in globals():
    Create = ShowCreation
```

### 3. First render attempts (manimgl)

- Command: `xvfb-run -a manimgl -wqm --file_name CrumpleDocumentary manim_crumple_documentary.py CrumpleDocumentary`
- Result: Scene detected, but `VideoMobject` surface stayed black (frames visible but no image).
- Confirmed: `moviepy` imports correctly; `ffmpeg` is in PATH; source MP4s play locally.

### 4. Double‑fade bug discovery

`play_video_clip()` performed:

```python
self.play(Create(video), run_time=0.5)
self.wait(run_time - 0.5)
self.play(FadeOut(video), run_time=0.5)  # ← internal fade
return video
```

Caller (`construct`) then also faded out the returned mobject. The video was re‑added during the second fade, causing it to **persist and overlay** subsequent acts.

**Fix:** Remove internal `FadeOut`; let caller handle removal exclusively.

```python
self.play(Create(video), run_time=0.5)
self.wait(run_time - 0.5)
return video  # no fade-out here
```

Added `video.set_z_index(0)` to keep videos on background layer.

### 5. Final render (commit `bc72bf8`)

- Render completed (61 animations, exit 0).
- Output size 0.4 MB (720p30) — *smaller than earlier renders, suspicious*.
- Video still blank in the final file.

---

## Current Status

| Item | State |
|------|-------|
| Script engine detection | ✓ working (prefers `manimlib`) |
| `Create` alias | ✓ defined |
| `VideoMobject` import | ✓ succeeds (no ImportError) |
| MP4 source files | ✓ exist, playable via `ffplay` |
| Render pipeline (`manimgl` + `xvfb-run`) | ✓ produces MP4 (non‑zero size, correct duration) |
| **Video content visible in final render** | ❌ blank frames (colored rectangle only) |

---

## Hypotheses (unresolved)

1. **Codec / pixel format mismatch**  
   ManimGL’s `VideoMobject` (via `moviepy`) may require specific codecs (e.g., YUV420p). Our MP4s are H.264/AAC — should work, but perhaps `moviepy` under the `manimgl` venv lacks `ffmpeg` binary access. Check: `imageio_ffmpeg.get_ffmpeg_exe()`.

2. **OpenGL context / headless acceleration**  
   `xvfb-run` provides an X display, but lacks GPU acceleration. `VideoMobject` may need a real GL context to upload texture frames. Could be silently failing.

3. **`moviepy` version / dependency conflict**  
   `pipx inject manimgl moviepy` pulled the latest `moviepy` (v2.x), which changed internals. The `manimgl` codebase expects older `moviepy` (v1.x). Try pinning: `pipx inject manimgl "moviepy<2"`.

4. **File path / permission issue**  
   `VideoMobject` loads frames via `imageio.get_reader`. Under `xvfb`, current working directory or path handling might break. Try absolute paths (already used), and verify `_HAS_VIDEO` True at runtime.

5. **Frame rate / audio stream conflict**  
   Some MP4s have audio; `VideoMobject` may drop video if audio codec unsupported. Try `ffmpeg -i input.mp4 -an -c:v copy output.mp4` to strip audio.

6. **ManimGL version quirk**  
   `manimgl` 1.7.2 may have a known `VideoMobject` bug under certain `moviepy` releases. Consider downgrading `manimgl` to an earlier commit (e.g., `@4d4dca7` Oct 2023) where video worked for others.

---

## Diagnostic Checklist

- [x] Verify `moviepy` importable in manimgl venv
- [x] Render succeeds (no Python exceptions)
- [x] `_HAS_VIDEO` flag is `True`
- [x] Video mobject created (`type(video) == VideoMobject`)
- [ ] Confirm `video.n_frames` > 0 inside `construct` (add print debug)
- [ ] Check `video` texture upload logs (enable `moviepy` debug)
- [ ] Try a *minimal* test scene with just `VideoMobject` (no other elements)
- [ ] Render *with* real X server (not `xvfb`) — if hardware available
- [ ] Install `opencv-python` and try `imageio` with `ffmpeg` plugin explicitly

---

## Next Steps (when returning)

1. **Minimal reproduction** — create `test_video_only.py`:

```python
from manim import *
config.media_dir = "./media"
class TestVideo(Scene):
    def construct(self):
        v = VideoMobject("ZoneSpiral.mp4")
        self.add(v)
        self.wait(5)
```

Render *without* xvfb if possible, or ensure `xvfb-run` has proper GL drivers (`mesa-glx`).

2. **Diagnose inside scene** — add prints:

```python
video = VideoMobject(path)
print(f"Video: n_frames={video.n_frames}, duration={video.duration}")
self.add(video)
```

3. **Check `moviepy` ffmpeg backend**:

```python
import imageio_ffmpeg
print(imageio_ffmpeg.get_ffmpeg_exe())
```

4. **Try audio‑stripped, yuv420p‑encoded MP4s**:

```bash
ffmpeg -i ZoneSpiral.mp4 -an -c:v copy ZoneSpiral_clean.mp4
```

Re‑encode all three archival clips and re‑render.

5. **Pin `moviepy==1.0.3`** (last pre‑2.x):

```bash
pipx inject manimgl "moviepy==1.0.3"
```

6. **Downgrade manimgl** to a known‑good commit:

```bash
cd ~/.local/share/pipx/venvs/manimgl
git checkout 4d4dca7  # Oct 2023 snapshot
```

7. **Render on real X server** — if a desktop session is available, omit `xvfb-run` and run `manimgl` directly. GPU/GL may resolve texture upload.

---

## Related Assets (tracked in repo)

| File | Purpose |
|------|---------|
| `manim_crumple_documentary.py` | Main documentary script (engine‑agnostic) |
| `crumple_documentary.mp4` | Current render (videos blank) |
| `ZoneSpiral.mp4` | Act I archival (0.5 MB) |
| `SyzygyCascade.mp4` | Act I archival (0.2 MB) |
| `crumple_trajectory_animation.mp4` | Act II single run (0.4 MB) |
| `trajectory_varentropy_both.json` | Batch stats for Act III |
| `media/videos/manim_crumple_documentary/` | Per‑animation partials (ignored) |

---

## Commit History (selected)

| Commit | Message |
|--------|---------|
| `bc72bf8` | fix: replace documentary with corrected render (videos no longer overlay) |
| `ec83a9b` | assets: add missing video archives (ZoneSpiral, SyzygyCascade, scene renders) and fix .gitignore ordering |
| `76302a5` | fix: videos no longer overlay; removed internal fade-out, added Create alias for manimgl |
| `c2dcf53` | chore: remove debug prints from documentary script |
| `ecab25c` | docs: render CrumpleDocumentary with manimgl (VideoMobject embedded, engine-agnostic) |

---

## Open Questions

- Why does `VideoMobject` appear as an opaque black rectangle even though the video object is created and added?
- Does `manimgl` require a specific `moviepy` version to function?
- Is `xvfb-run` the blocker (missing GL texture support), or is it a codec/audio issue?
- Will stripping audio from the MP4s change behaviour?

---

## When We Return

Start with the **minimal test scene** (no xvfb if possible), print `video.n_frames`, and verify `imageio` can read frames. Once a single video displays, the main documentary will follow naturally.

— *Hermes Agent, 2026‑05‑14*

