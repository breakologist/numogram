---
title: Wiki Navigation Guide — Finding Your Way Through the Hermetic Archive
created: 2026-05-04
updated: 2026-05-04
category: reference
status: draft
tags: [navigation, obsidian, dataview, tags, search, organization]
---

# Wiki Navigation Guide

> A comprehensive guide to navigating the Hermetic Archive — a vast repository of knowledge about the Numogram, Alphanumeric Qabbala, roguelike agents, and audio synthesis. This guide covers multiple methods for finding content, from simple searches to dynamic dataview tables.

---

## 📍 Table of Contents

- [Overview](#overview)
- [1. Main Index](#1-main-index)
- [2. Category Navigation](#2-category-navigation)
- [3. Tag-Based Navigation](#3-tag-based-navigation)
- [4. Dynamic Dataview Tables](#4-dynamic-dataview-tables)
- [5. Visual Maps](#5-visual-maps)
- [6. Search Enhancements](#6-search-enhancements)
- [7. Periodic Notes](#7-periodic-notes)
- [8. Task-Based Navigation](#8-task-based-navigation)
- [9. Backlinks and Graph View](#9-backlinks-and-graph-view)
- [10. External Tools](#10-external-tools)
- [Conclusion](#conclusion)

---

## Overview

The Hermetic Archive is organized as an Obsidian vault with over 300,000 files. Effective navigation requires multiple approaches working together. This guide presents a **multi-layered navigation system**:

1. **Main Index** — Hierarchical overview of major sections
2. **Category Navigation** — Topic-based grouping of pages
3. **Tag-Based Navigation** — Metadata filtering via tags
4. **Dynamic Dataview** — Live-updating tables and lists
5. **Visual Maps** — Excalidraw diagrams showing relationships
6. **Search Enhancements** — Advanced search operators and filters
7. **Periodic Notes** — Time-based organization (session logs, status updates)
8. **Task-Based Navigation** — Project tracking and to-do lists
9. **Backlinks** — See also relationships between pages
10. **External Tools** — Git, grep, and other command-line utilities

Each method complements the others, creating a robust navigation ecosystem.

---

## 1. Main Index

The **index.md** page serves as the primary entry point. It's hierarchically organized with:

- **Top-level categories**: Numogram, Audio, Visual, Roguelike, Phase Projects, etc.
- **Subcategories**: Each major category has its own section with links to key pages
- **Recent Additions**: New pages are added to the top for visibility

### Example Structure
```markdown
# Hermetic Archive Index

## Numogram Core
- [[numogram-overview]] — Introduction to the Numogram
- [[decimal-numogram-reference]] — Complete zone and gate reference
- [[alphanumeric-qabbala]] — AQ cipher calculations

## Audio Synthesis
- [[mod-writer]] — Module writer with numogram-native extensions
- [[audio-renderer]] — Audio rendering and analysis
- [[phase5-validation-report]] — Empirical validation results

## Visual Exhibits
- [[visual-hub]] — Gallery of diagrams, videos, and interactive exhibits
- [[barker-spiral-v2-exhibition]] — Barker Spiral visualizations
- [[manim-archive-exhibition]] — Manim-numogram video archive
```

### Enhancement: Dynamic Index with Dataview
We can enhance the index with a dataview table showing recently updated pages:

```dataview
// Recently Updated
table file.mtime as "Updated", file.path as "Path"
from "#wiki"
where file.mtime > date(today) - dur[P1W]
sort file.mtime desc
limit 10
```



## 2. Category Navigation

Pages are organized into logical categories based on their primary topic. Each category has:

- **A dedicated index page** listing all pages in that category
- **Category tags** for filtering (see Tag-Based Navigation)
- **Cross-links** to related categories

### Major Categories
- **Numogram** — Core numogram theory, zones, gates, demons
- **Audio** — Synthesis, MIR, classification, validation
- **Visual** — Diagrams, videos, interactive exhibits
- **Roguelike** — Agent techniques, dungeon generation, game design
- **Phase Projects** — Phase 4, Phase 5, and other project documentation
- **Tools & Skills** — Hermes Agent skills, external tools, workflows

### Example: Audio Category Index
```markdown
# Audio Synthesis & MIR

## Overview
The audio synthesis pipeline with numogram-native extensions.

## Key Pages
- [[mod-writer]] — Module writer with zone-constrained composition
- [[audio-renderer]] — WAV rendering and spectrogram generation
- [[phase5-validation-report]] — Empirical validation results
- [[mir-profile]] — MIR feature extraction and analysis

## Subcategories
- [[mod-writer/composer]] — Zone-constrained composition
- [[mod-writer/classifier]] — Zone classification pipeline
- [[audio-hallucination]] — VAE-based empty zone synthesis
```

---

## 3. Tag-Based Navigation

**Tags** are metadata labels that allow filtering and grouping of pages. Each page should have relevant tags in its frontmatter.

### Common Tag Groups
- **Topic Tags**: `#audio`, `#visual`, `#numogram`, `#ro-guelike`, `#phase5`
- **Status Tags**: `#status/active`, `#status/draft`, `#status/complete`
- **Type Tags**: `#type/exhibition`, `#type/tutorial`, `#type/reference`, `#type/logs`
- **Project Tags**: `#project/validation`, `#project/composition`, `#project/visualization`
### Using Tags for Navigation

Tags can be used in dataview queries to filter pages. For example:

```dataview
// Audio-Related Pages
list from "#audio" or #visual
where contains(file.tags, "#audio")
sort file.name
```
### Tag Conventions
- Use lowercase for tags: `#audio`, not `#Audio`
- Group related tags: `#phase5/validation`, `#phase5/m2`
- Avoid overusing tags — 3-5 relevant tags per page is sufficient

---

## 4. Dynamic Dataview Tables

**Dataview** is a powerful Obsidian plugin that can query page metadata and display it in tables, lists, or calendars. It's ideal for creating dynamic navigation aids that update as pages are added or modified.

### Examples

#### All Pages in the Wiki
```dataview
## All Wiki Pages

```dataview
table file.mtime, file.path
from "#wiki"
sort file.mtime desc
limit 50
```
#### Phase 5 Pages

```dataview
// Phase 5 Project Pages
table status as "Status", file.path as "Page"
from "#phase5"
sort file.name
#### Recent Changes

```dataview
// Recently Updated
table file.mtime as "Updated", file.path as "Page"
from "#wiki"
where file.mtime > date(today) - dur[P1W]
sort file.mtime desc
limit 20
```
### Dataview in Templates
Dataview can be used in templates to automatically generate navigation sections for specific page types.

---

## 5. Visual Maps

**Excalidraw** is a hand-drawn style diagramming tool that integrates with Obsidian. It's perfect for creating visual maps of complex relationships.

### Examples of Visual Maps
- **Numogram Structure Map** — Zones, gates, and currents in a single diagram
- **Project Timeline** — Phase 4 and Phase 5 milestones and dependencies
- **Audio-Visual Correlation** — How MIR features map to numogram zones
- **Skill Ecosystem** — Hermes Agent skills and their relationships

### Creating Visual Maps
1. Install the Excalidraw plugin
2. Create a new Excalidraw file in the `assets/` folder
3. Draw the map using simple shapes and connectors
4. Embed the map in wiki pages using `![[map-name.excalidraw]]`

### Example Map: Numogram Structure
![[assets/numogram-structure.excalidraw]]  <!-- Hypothetical map -->

---

## 6. Search Enhancements

Obsidian's built-in search is powerful but can be enhanced with operators and plugins.

### Search Operators
- `file:name` — Search in file names
- `path:folder` — Search in specific folder
- `tag:tagname` — Search by tag
- `content:keyword` — Search in content (default)
- `ctime:YYYY-MM-DD` — Filter by creation date
- `mtime:YYYY-MM-DD` — Filter by modification date

### Examples
- `tag:#audio path:mod-writer` — Find audio pages in mod-writer folder
- `file:validation content:96.4` — Find files with "96.4" in name or content
- `mtime:2026-05-04` — Find pages updated today

### Plugin: Omnisearch
The Omnisearch plugin adds advanced search capabilities:
- Boolean operators (AND, OR, NOT)
- Proximity search
- Field weighting
- Saved searches

---

## 7. Periodic Notes

**Periodic Notes** are notes organized by time periods (daily, weekly, monthly, yearly). They're ideal for:
- **Session logs** — What was worked on each day
- **Status updates** — Project progress summaries
- **Meeting notes** — Discussions and decisions
- **Idea journals** — Thoughts and insights over time

### Examples
- `2026-05-02.md` — Session log for May 2, 2026
- `status-2026-05.md` — Monthly status update
- `meeting-phase5-kickoff.md` — Project kickoff meeting

### Location
Periodic notes are typically stored in a `periodics/` folder:
```
.wiki/
├── periodics/
│   ├── daily/
│   │   ├── 2026-05-02.md
│   │   └── 2026-05-03.md
│   ├── weekly/
│   │   └── 2026-W18.md
│   └── monthly/
│       └── 2026-05.md
```

### Using Periodic Notes
- **Daily notes** — Quick logs, TODOs, scratch work
- **Weekly notes** — Progress summaries, goal setting
- **Monthly notes** — Status reports, project reviews

---

## 8. Task-Based Navigation

**Tasks** are to-do items that can be embedded in notes and tracked across the vault. They're useful for:
- **Project management** — Tracking Phase 5 tasks
- **TODO lists** — Page-specific action items
- **Checklist navigation** — Progress indicators for multi-step processes

### Examples
```markdown
## Phase 5 Tasks

- [x] Complete zone-constrained composition validation (≥90% accuracy)
- [ ] Implement VAE hallucination with iterative projection
- [ ] Integrate PureData for live audio feedback
- [ ] Expand dataset for zones 3-5, 8-9
```

### Querying Tasks
Tasks can be queried across the vault using the Tasks plugin:

```markdown
## All Open Tasks

```tasks
not done
```

## Phase 5 Tasks
```tasks
path includes "phase5"
not done
```
```

---

## 9. Backlinks and Graph View

Obsidian's **backlinks** and **graph view** show relationships between pages.

### Backlinks
- **Backlinks pane** shows all pages that link to the current page
- **Unlinked mentions** show pages that mention the current page without an explicit link
- Useful for discovering related content and navigation paths

### Graph View
- **Local graph** shows nearby pages and their connections
- **Global graph** shows the entire vault's link structure
- **Graph metrics** show centrality, density, and other network properties

### Using Backlinks for Navigation
- When reading a page, check the Backlinks pane to see what references it
- Use unlinked mentions to find related content that hasn't been explicitly linked
- Follow link chains to explore topics in depth

---

## 10. External Tools

For advanced navigation and analysis, external command-line tools can be used:

### Git
- `git log --oneline --since="2026-05-01"` — Recent commits
- `git diff --name-only HEAD~5..HEAD` — Files changed in last 5 commits
- `git grep -n "validation" -- "*.md"` — Search for "validation" in markdown files

### ripgrep (rg)
- `rg "Phase 5" --include="*.md"` — Find all mentions of "Phase 5"
- `rg "96\.4" --include="*.md"` — Find all 96.4% references
- `rg "^# " --files-with-matches` — Find all markdown files with headers

### find and ls
- `find . -name "*.md" -mtime -7` — Markdown files modified in last 7 days
- `ls -lt *.md | head -20` — Recently modified markdown files

---

## Conclusion

Effective navigation of the Hermetic Archive requires a **multi-layered approach** combining:

1. **Hierarchical index** for top-down exploration
2. **Category and tag-based** navigation for topic filtering
3. **Dynamic dataview** for live-updating content
4. **Visual maps** for understanding relationships
5. **Enhanced search** for finding specific content
6. **Time-based organization** for tracking progress
7. **Task management** for project tracking
8. **Link graph** for discovering connections
9. **External tools** for advanced analysis

By using these methods together, you can efficiently find and explore the vast amount of content in the archive.

---

**Next Steps:**
1.  Enhance the main index with dataview tables
2.  Create category index pages for major topics
3.  Add tags to all new pages
4.  Build visual maps for key concepts
5.  Set up periodic notes for session logs
6.  Use tasks to track project progress

