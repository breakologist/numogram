#!/usr/bin/env python3
"""
Ghost Registry Scanner — Phase 1 of Ghost Taxonomy Expansion

Scans all autonomous journal markdown files for ghost-related patterns,
builds a structured registry with prevalence counts, and outputs
a JSON registry + markdown summary.

Ghost types detected:
- Corpus Conflation Ghost — wrong dataset label
- Content Ghost — wrong data source
- Path Ghost — wrong file path
- Reproducibility Ghost — regenerated under different conditions
- Measurement Ghost — wrong tool/formula
- Hypothesis Ghost — plausible theory falsified
- Observer-Effect Ghost — measurement method influences value
- Category Ghost — wrong column/field classification

Usage:
    python3 ghost_registry_scanner.py [--journal-dir PATH] [--output REGISTRY.json]
"""

import os
import re
import json
import argparse
import sys
from datetime import datetime
from collections import defaultdict, Counter

# --- Ghost type patterns (scored by confidence) ---

GHOST_PATTERNS = {
    "Corpus Conflation Ghost": {
        "keywords": [
            "corpus confla", "mislabel", "wrong label", "label.*wrong",
            "corpus A.*corpus B", "corpus B.*corpus A",
            "attribution error", "attribution incorrect",
            "mis-labeling", "mislabeling", "misattribution",
            "dataset identity.*wrong", "wrong dataset",
        ],
        "weight": 0.9,
    },
    "Content Ghost": {
        "keywords": [
            "content ghost", "wrong data source", "wrong corpus",
            "different corpus", "measured the wrong",
            "attributed.*corpus", "wrong script",
        ],
        "weight": 0.85,
    },
    "Path Ghost": {
        "keywords": [
            "path ghost", "wrong path", "wrong file path",
            "file at wrong path", "file.*does not exist",
            "path.*changed", "different location",
        ],
        "weight": 0.8,
    },
    "Reproducibility Ghost": {
        "keywords": [
            "reproducibility ghost", "regenerated.*different",
            "re-generated.*different", "new.*mod.*instead.*wav",
            "new MODs.*different", "new.*conditions.*claim",
            "different parameters.*reproduc",
        ],
        "weight": 0.8,
    },
    "Measurement Ghost": {
        "keywords": [
            "measurement ghost", "wrong tool", "wrong formula",
            "different FFT", "different.*parameter",
            "wrong calculation", "fft.*parameter", "tool version",
        ],
        "weight": 0.75,
    },
    "Hypothesis Ghost": {
        "keywords": [
            "hypothesis ghost", "plausible theory", "falsified by",
            "falsified.*data", "hypothesis.*falsif",
        ],
        "weight": 0.7,
    },
    "Observer-Effect Ghost": {
        "keywords": [
            "observer.effect ghost", "measurement method.*influences",
            "measurement.*influenc", "presence.*measurement system",
            "left.channel.*vs.*combined", "L-only.*vs.*stereo",
            "different.*tool.*different.*value",
        ],
        "weight": 0.75,
    },
    "Category Ghost": {
        "keywords": [
            "category ghost", "wrong column", "wrong field",
            "dominant frequency.*centroid", "wrong classification",
        ],
        "weight": 0.8,
    },
}

# Accusations / retractions of ghosts
RETRACTION_PATTERNS = [
    r"retracted", r"reversal", r"retraction", r"corrected.*claim",
    r"falsified", r"false.*claim", r"❌", r"fabrication.*ghost.*retracted",
    r"quantitative fabrication.*retracted", r"never confirmed",
]

# Markers for ghost severity / status
STATUS_PATTERNS = {
    "confirmed": [r"✅confirmed", r"confirmed.*ghost", r"verified.*ghost", r"fixed ✅", r"resolved.*ghost"],
    "fixed": [r"fixed ✅", r"resolved.*ghost", r"renamed.*correct"],
    "retracted": [r"retracted", r"❌ falsif"],
}


def scan_file(filepath: str) -> dict:
    """Scan a single markdown file for ghost indicators."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    basename = os.path.basename(filepath)
    results = {
        "file": basename,
        "ghosts_found": [],
        "retractions": [],
        "status_mentions": [],
    }

    # Detect ghost patterns
    for ghost_type, config in GHOST_PATTERNS.items():
        for pattern in config["keywords"]:
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            if matches:
                contexts = []
                for m in matches:
                    start = max(0, m.start() - 40)
                    end = min(len(content), m.end() + 40)
                    ctx = content[start:end].replace('\n', ' ')
                    contexts.append(ctx.strip())
                results["ghosts_found"].append({
                    "type": ghost_type,
                    "count": len(matches),
                    "weight": config["weight"],
                    "context_snippets": contexts[:3],  # keep top 3
                })

    # Detect retractions
    for pattern in RETRACTION_PATTERNS:
        matches = list(re.finditer(pattern, content, re.IGNORECASE))
        for m in matches:
            start = max(0, m.start() - 50)
            end = min(len(content), m.end() + 50)
            ctx = content[start:end].replace('\n', ' ')
            results["retractions"].append({
                "pattern": pattern,
                "context": ctx.strip(),
            })

    # Detect status mentions
    for status, patterns in STATUS_PATTERNS.items():
        for pattern in patterns:
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            if matches:
                results["status_mentions"].extend([
                    {"status": status, "context": m.group()[:80]}
                    for m in matches
                ])

    # Extract session date from filename
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', basename)
    results["session_date"] = date_match.group(1) if date_match else "unknown"

    return results


def scan_journal_dir(journal_dir: str) -> dict:
    """Scan all markdown files in the journal directory."""
    all_results = {}
    md_files = sorted([
        f for f in os.listdir(journal_dir)
        if f.endswith('.md') and f != 'index.json'
    ])

    for fname in md_files:
        fpath = os.path.join(journal_dir, fname)
        if os.path.isfile(fpath):
            all_results[fname] = scan_file(fpath)

    return all_results


def compute_registry(scan_results: dict) -> dict:
    """Aggregate scan results into a structured registry."""
    # Overall stats
    total_files = len(scan_results)

    # Ghost type prevalence (count files each type appears in)
    type_counts = Counter()
    type_total_hits = Counter()
    all_ghost_events = []

    for fname, result in scan_results.items():
        for ghost in result["ghosts_found"]:
            type_counts[ghost["type"]] += 1
            type_total_hits[ghost["type"]] += ghost["count"]
            all_ghost_events.append({
                "file": fname,
                "session_date": result["session_date"],
                "type": ghost["type"],
                "count": ghost["count"],
                "weight": ghost["weight"],
            })

    # Retraction stats
    retraction_files = sum(1 for r in scan_results.values() if r["retractions"])
    total_retractions = sum(len(r["retractions"]) for r in scan_results.values())

    # Build prevalence table
    prevalence = {}
    for ghost_type in sorted(type_counts.keys()):
        prevalence[ghost_type] = {
            "files_affected": type_counts[ghost_type],
            "total_hits": type_total_hits[ghost_type],
            "pct_files": round(100 * type_counts[ghost_type] / total_files, 1),
            "ghost_weight": GHOST_PATTERNS.get(ghost_type, {}).get("weight", 0.5),
        }

    # Cross-ghost co-occurrence (which ghosts appear together)
    co_occurrence = Counter()
    for fname, result in scan_results.items():
        types_in_file = set(g["type"] for g in result["ghosts_found"])
        for t1 in types_in_file:
            for t2 in types_in_file:
                if t1 < t2:
                    co_occurrence[(t1, t2)] += 1

    registry = {
        "scan_timestamp": datetime.utcnow().isoformat(),
        "journal_dir": os.path.basename(os.path.dirname(
            list(scan_results.values())[0].get("file", "")
        )) if scan_results else "unknown",
        "total_sessions_scanned": total_files,
        "sessions_with_ghosts": sum(1 for r in scan_results.values() if r["ghosts_found"]),
        "pct_sessions_with_ghosts": round(
            100 * sum(1 for r in scan_results.values() if r["ghosts_found"]) / total_files, 1
        ) if total_files else 0,
        "total_ghost_hits": sum(
            g["count"] for r in scan_results.values() for g in r["ghosts_found"]
        ),
        "total_retractions": total_retractions,
        "files_with_retractions": retraction_files,
        "prevalence_by_type": prevalence,
        "co_occurrence": {
            f"{t1} ⊗ {t2}": count
            for (t1, t2), count in sorted(co_occurrence.items(), key=lambda x: -x[1])
        },
        "ghost_events": sorted(all_ghost_events, key=lambda x: x["session_date"]),
    }

    return registry


def format_markdown_summary(registry: dict) -> str:
    """Format the registry as a markdown summary."""
    lines = [
        "---",
        "title: \"Ghost Registry — Generated from Autonomous Journal Audit\"",
        f"date: {datetime.utcnow().strftime('%Y-%m-%d')}",
        "tags: [ghost-taxonomy, registry, autonomous-journal, empirical-validation]",
        "status: auto-generated",
        "---",
        "",
        f"# Ghost Registry — {registry.get('total_sessions_scanned', 0)} Sessions Scanned",
        "",
        f"**Scanned:** {registry.get('scan_timestamp', 'unknown')} UTC  ",
        f"**Sessions:** {registry.get('total_sessions_scanned', 0)} total, "
        f"{registry.get('sessions_with_ghosts', 0)} with ghost indicators "
        f"({registry.get('pct_sessions_with_ghosts', 0)}%)  ",
        f"**Total ghost hits:** {registry.get('total_ghost_hits', 0)}  ",
        f"**Retractions:** {registry.get('total_retractions', 0)} across "
        f"{registry.get('files_with_retractions', 0)} files",
        "",
        "## Prevalence by Ghost Type",
        "",
        "| Ghost Type | Files Affected | Total Hits | % Sessions | Confidence Weight |",
        "|---|---|---|---|---|",
    ]

    for ghost_type, stats in sorted(
        registry.get("prevalence_by_type", {}).items(),
        key=lambda x: -x[1]["files_affected"]
    ):
        lines.append(
            f"| {ghost_type} | {stats['files_affected']} | "
            f"{stats['total_hits']} | {stats['pct_files']}% | "
            f"{stats['ghost_weight']} |"
        )

    lines.extend([
        "",
        "## Ghost Co-occurrence (which ghosts appear together)",
        "",
        "| Ghost Pair | Files with both |",
        "|---|---|",
    ])

    for pair, count in sorted(
        registry.get("co_occurrence", {}).items(),
        key=lambda x: -x[1]
    ):
        lines.append(f"| {pair} | {count} |")

    lines.extend([
        "",
        "## All Ghost Events (chronological)",
        "",
        "| Session Date | File | Ghost Type | Hits | Weight |",
        "|---|---|---|---|---|",
    ])

    for event in registry.get("ghost_events", []):
        lines.append(
            f"| {event['session_date']} | {event['file'][:55]} | "
            f"{event['type']} | {event['count']} | {event['weight']} |"
        )

    lines.append("")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description="Ghost Registry Scanner")
    parser.add_argument(
        "--journal-dir", "-j",
        default=os.path.expanduser(
            "~/.hermes/obsidian/hermetic/wiki/autonomous-journal"
        ),
        help="Path to autonomous journal directory"
    )
    parser.add_argument(
        "--output", "-o",
        default=os.path.expanduser("~/.hermes/scripts/ghost_registry.json"),
        help="Output path for JSON registry"
    )
    parser.add_argument(
        "--markdown", "-m",
        default=os.path.expanduser("~/.hermes/scripts/ghost_registry.md"),
        help="Output path for markdown summary"
    )
    args = parser.parse_args()

    if not os.path.isdir(args.journal_dir):
        print(f"Error: Journal directory not found: {args.journal_dir}")
        sys.exit(1)

    print(f"Scanning {args.journal_dir}...")
    results = scan_journal_dir(args.journal_dir)
    registry = compute_registry(results)

    # Write JSON
    with open(args.output, 'w') as f:
        json.dump(registry, f, indent=2)
    print(f"Registry written to {args.output}")

    # Write markdown
    md = format_markdown_summary(registry)
    with open(args.markdown, 'w') as f:
        f.write(md)
    print(f"Markdown summary written to {args.markdown}")

    # Print quick stats
    print(f"\n--- Quick Stats ---")
    print(f"Sessions scanned: {registry['total_sessions_scanned']}")
    print(f"Sessions with ghosts: {registry['sessions_with_ghosts']} ({registry['pct_sessions_with_ghosts']}%)")
    print(f"Total ghost hits: {registry['total_ghost_hits']}")
    print(f"Ghost types: {len(registry['prevalence_by_type'])}")
    for g, s in sorted(registry['prevalence_by_type'].items(), key=lambda x: -x[1]['files_affected']):
        print(f"  {g}: {s['files_affected']} files, {s['total_hits']} hits ({s['pct_files']}%)")
    print(f"Retractions: {registry['total_retractions']} across {registry['files_with_retractions']} files")


if __name__ == '__main__':
    main()
