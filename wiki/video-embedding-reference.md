---
title: Video Embedding Reference
created: 2026-05-04
status: active
category: reference
tags: ["obsidian", "embedding", "video", "reference"]
---

# Video Embedding Reference

## Obsidian Video Embed Syntax

To embed videos in markdown pages for the Hermetic wiki, use the following syntax:

```markdown
![[filename.mp4]]
```

This will display the video inline when viewed in Obsidian. The file path should be relative to the wiki root, or you can use absolute paths from the vault root.

## Examples

### Local file in the wiki assets folder
```markdown
![[assets/my-video.mp4]]
```

### File in a subdirectory
```markdown
![[subfolder/video.mp4]]
```

### External file (like our Manim archive)
```markdown
![[../../../../numogame/media/videos/numogram_explainer/480p15/Scene1_TheVoid.mp4]]
```

## Best Practices

1. **Use descriptive filenames** - Name your video files clearly (e.g., `Scene1_TheVoid.mp4` instead of `video1.mp4`).

2. **Keep videos organized** - Store videos in a dedicated media folder with a logical structure.

3. **Add metadata** - Include file name, description, and concept information near the embed.

4. **Consider file size** - Large videos may slow down wiki loading. Use compression if needed.

5. **Link to higher resolutions** - For original high-resolution files, provide a link or note in the Access section.

## Current Video Archive

The Manim-numogram video archive is located at:
`~/numogame/media/videos/numogram_explainer/480p15/`

Embedded videos in this wiki:
- `manim-archive-exhibition.md`
