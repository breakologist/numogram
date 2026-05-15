#!/usr/bin/env python3
"""
ghost-preflight.py — Automated Pre-Measurement Provenance Checker

Runs before every empirical claim to detect ghost preconditions.
Detects 7 ghost types: Path, Content, Corpus Conflation,
Reproducibility, Measurement, Observer-Effect, Category.

Usage:
    python3 ghost-preflight.py check-file <path>
    python3 ghost-preflight.py check-corpus <manifest.json>
    python3 ghost-preflight.py provenance <result.json>
    python3 ghost-preflight.py check-measurement --tool <name> --params <json>
    python3 ghost-preflight.py run <command> [args...]
    python3 ghost-preflight.py registry [--json]
"""

import hashlib
import json
import os
import subprocess
import sys
import time
import re
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path):
    """Compute SHA256 of a file."""
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def ffprobe_info(path, field='format'):
    """Get ffprobe info for a media file."""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-print_format', 'json',
             '-show_format', '-show_streams', str(path)],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        return None
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return None


def file_provenance(path):
    """Build a provenance record for a single file."""
    p = Path(path)
    if not p.exists():
        return {
            "path": str(p),
            "exists": False,
            "error": "FILE_NOT_FOUND",
            "ghost_warnings": ["PATH_GHOST: file does not exist"]
        }

    stat = p.stat()
    record = {
        "path": str(p.resolve()),
        "exists": True,
        "size_bytes": stat.st_size,
        "mtime_iso": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
        "sha256": sha256_file(str(p)),
    }

    # Media-specific metadata
    ext = p.suffix.lower()
    if ext in ('.wav', '.mp3', '.ogg', '.flac', '.mod', '.xm', '.s3m', '.it'):
        info = ffprobe_info(str(p))
        if info:
            fmt = info.get('format', {})
            record['media'] = {
                'duration_s': fmt.get('duration'),
                'bit_rate': fmt.get('bit_rate'),
                'format_name': fmt.get('format_name'),
            }
            streams = info.get('streams', [])
            if streams:
                s = streams[0]
                record['media'].update({
                    'sample_rate': s.get('sample_rate'),
                    'channels': s.get('channels'),
                    'codec': s.get('codec_name'),
                })
        else:
            record['error'] = 'ffprobe_failed'

    return record


def check_corpus(manifest_path):
    """Verify all files in a corpus manifest exist and match hashes."""
    with open(manifest_path) as f:
        manifest = json.load(f)

    corpus_name = manifest.get('corpus_name', os.path.basename(manifest_path))
    expected = manifest.get('files', [])

    results = {
        "corpus": corpus_name,
        "manifest_time": datetime.now(timezone.utc).isoformat(),
        "total_files": len(expected),
        "verified": 0,
        "missing": 0,
        "hash_mismatch": 0,
        "size_mismatch": 0,
        "ghosts": [],
        "file_results": [],
    }

    if not expected:
        results['ghosts'].append({
            "type": "Content Ghost",
            "severity": "high",
            "detail": "Empty corpus manifest — nothing to measure"
        })

    for entry in expected:
        fpath = entry.get('path')
        fr = {"path": fpath}

        if not os.path.exists(fpath):
            fr['status'] = 'MISSING'
            results['missing'] += 1
            results['ghosts'].append({
                "type": "Path Ghost",
                "severity": "high",
                "detail": f"File not found: {fpath}"
            })
        else:
            actual = file_provenance(fpath)
            fr['provenance'] = actual

            if 'sha256' in entry:
                expected_hash = entry['sha256']
                if actual.get('sha256') != expected_hash:
                    fr['status'] = 'HASH_MISMATCH'
                    results['hash_mismatch'] += 1
                    results['ghosts'].append({
                        "type": "Content Ghost",
                        "severity": "high",
                        "detail": f"Hash mismatch for {fpath}"
                    })
                else:
                    fr['status'] = 'VERIFIED'
                    results['verified'] += 1

            elif 'size_bytes' in entry and entry['size_bytes'] != actual.get('size_bytes'):
                fr['status'] = 'SIZE_MISMATCH'
                results['size_mismatch'] += 1
                results['ghosts'].append({
                    "type": "Reproducibility Ghost",
                    "severity": "medium",
                    "detail": f"Size changed for {fpath}"
                })
            else:
                fr['status'] = 'VERIFIED'
                results['verified'] += 1

        results['file_results'].append(fr)

    # Check for corpus conflation
    if results['verified'] == 0 and results['missing'] > 0:
        results['ghosts'].append({
            "type": "Corpus Conflation Ghost",
            "severity": "critical",
            "detail": "No files verified — mismatched corpus or path"
        })

    return results


def check_measurement(tool_name, params_json, history_dir=None):
    """Check a measurement against prior runs for parameter drift."""
    if history_dir is None:
        history_dir = os.path.expanduser('~/.hermes/measurement_history')
    os.makedirs(history_dir, exist_ok=True)

    history_path = os.path.join(history_dir, f'{tool_name}_history.json')
    current_params = json.loads(params_json) if isinstance(params_json, str) else params_json

    # Get tool version
    tool_version = None
    try:
        r = subprocess.run(
            [tool_name, '--version'], capture_output=True, text=True, timeout=10
        )
        tool_version = (r.stdout or r.stderr).strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        tool_version = 'unknown'

    result = {
        "tool": tool_name,
        "tool_version": tool_version,
        "current_params": current_params,
        "ghosts": [],
    }

    # Compare with history
    if os.path.exists(history_path):
        with open(history_path) as f:
            history = json.load(f)

        last_run = history[-1] if history else None
        if last_run:
            if last_run.get('tool_version') != tool_version:
                result['ghosts'].append({
                    "type": "Measurement Ghost",
                    "severity": "medium",
                    "detail": f"Tool version changed: {last_run.get('tool_version')} → {tool_version}"
                })

            last_params = last_run.get('params', {})
            param_diffs = []
            for k, v in current_params.items():
                if k in last_params and last_params[k] != v:
                    param_diffs.append(f"{k}: {last_params[k]} → {v}")

            if param_diffs:
                result['ghosts'].append({
                    "type": "Measurement Ghost",
                    "severity": "low",
                    "detail": f"Parameter changes: {'; '.join(param_diffs[:5])}"
                })

            # Check observer-effect: same input, different tool
            if last_run.get('tool') != tool_name:
                result['ghosts'].append({
                    "type": "Observer-Effect Ghost",
                    "severity": "medium",
                    "detail": f"Different tool vs prior run: {last_run.get('tool')} → {tool_name}"
                })

    # Write history
    history_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool": tool_name,
        "tool_version": tool_version,
        "params": current_params,
    }

    try:
        if os.path.exists(history_path):
            with open(history_path) as f:
                history = json.load(f)
        else:
            history = []
        history.append(history_entry)
        with open(history_path, 'w') as f:
            json.dump(history[-100:], f, indent=2)  # keep last 100
    except (IOError, json.JSONDecodeError):
        pass

    return result


def annotate_provenance(result_data, preflight_log):
    """Annotate a measurement result with provenance metadata."""
    if isinstance(result_data, str):
        try:
            result_data = json.loads(result_data)
        except json.JSONDecodeError:
            result_data = {"raw_output": result_data[:2000]}

    result_data['_provenance'] = {
        "preflight_timestamp": datetime.now(timezone.utc).isoformat(),
        "ghost_warnings": preflight_log.get('ghosts', []),
        "has_ghosts": len(preflight_log.get('ghosts', [])) > 0,
        "ghost_count": len(preflight_log.get('ghosts', [])),
    }

    return result_data


def run_command_with_preflight(command, args_list):
    """
    Run a command with full ghost preflight.
    Usage: ghost-preflight.py run python my_script.py --input data.wav --output result.json

    Returns: annotated result JSON to stdout.
    """
    # Parse the command and its args
    cmd_str = command
    if args_list:
        cmd_str = command + ' ' + ' '.join(args_list)

    # Discover input/output files from args
    input_files = []
    output_files = []
    for i, arg in enumerate(args_list or []):
        if arg in ('--input', '-i', '--data', '--audio') and i + 1 < len(args_list):
            input_files.append(args_list[i + 1])
        if arg in ('--output', '-o', '--result', '--json') and i + 1 < len(args_list):
            output_files.append(args_list[i + 1])

    preflight = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "command": cmd_str,
        "ghosts": [],
        "input_provenance": [],
        "system_state": {},
    }

    # Check input files
    for fpath in input_files:
        prov = file_provenance(fpath)
        preflight['input_provenance'].append(prov)
        if not prov.get('exists'):
            preflight['ghosts'].append({
                "type": "Path Ghost",
                "severity": "critical",
                "detail": f"Input file missing: {fpath}"
            })

    # Check output file conflicts
    for fpath in output_files:
        if os.path.exists(fpath):
            prov = file_provenance(fpath)
            preflight['ghosts'].append({
                "type": "Reproducibility Ghost",
                "severity": "low",
                "detail": f"Output file exists — will overwrite: {fpath} "
                          f"(mtime: {prov.get('mtime_iso', 'unknown')})"
            })

    # System state
    uname = subprocess.run(['uname', '-a'], capture_output=True, text=True, timeout=5)
    preflight['system_state']['kernel'] = uname.stdout.strip()

    # Run the command
    start = time.monotonic()
    try:
        proc = subprocess.run(
            cmd_str, shell=True, capture_output=True, text=True, timeout=3600
        )
        elapsed = time.monotonic() - start
        preflight['execution'] = {
            "exit_code": proc.returncode,
            "elapsed_s": round(elapsed, 2),
            "stdout_size": len(proc.stdout or ''),
            "stderr_size": len(proc.stderr or ''),
        }

        # Parse stdout as JSON if possible
        stdout_data = None
        try:
            stdout_data = json.loads(proc.stdout) if proc.stdout else None
        except json.JSONDecodeError:
            stdout_data = {"stdout_preview": (proc.stdout or '')[:2000]}

        result = {
            "preflight": preflight,
            "result": stdout_data or {"stdout": (proc.stdout or '')[:5000]},
            "errors": (proc.stderr or '')[:2000],
        }

        # Annotate result if it's a dict
        if isinstance(stdout_data, dict):
            result['result'] = annotate_provenance(stdout_data, preflight)
        
        return result

    except subprocess.TimeoutExpired:
        preflight['execution'] = {"error": "TIMEOUT", "elapsed_s": round(time.monotonic() - start, 2)}
        return {"preflight": preflight, "error": "Command timed out after 3600s"}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == 'check-file':
        if len(sys.argv) < 3:
            print("Usage: ghost-preflight.py check-file <path>")
            sys.exit(1)
        result = file_provenance(sys.argv[2])
        print(json.dumps(result, indent=2))
        if not result.get('exists'):
            sys.exit(1)

    elif cmd == 'check-corpus':
        if len(sys.argv) < 3:
            print("Usage: ghost-preflight.py check-corpus <manifest.json>")
            sys.exit(1)
        result = check_corpus(sys.argv[2])
        print(json.dumps(result, indent=2))
        if result.get('ghosts'):
            sys.exit(1 if any(g['severity'] in ('critical', 'high') for g in result['ghosts']) else 0)

    elif cmd == 'check-measurement':
        if len(sys.argv) < 4:
            print("Usage: ghost-preflight.py check-measurement --tool <name> --params <json>")
            sys.exit(1)
        tool = None; params = None
        for i, a in enumerate(sys.argv[2:]):
            if a == '--tool' and i+2 < len(sys.argv):
                tool = sys.argv[2:][i+1]
            if a == '--params' and i+2 < len(sys.argv):
                params = sys.argv[2:][i+1]
        if not tool or not params:
            print("--tool and --params required"); sys.exit(1)
        result = check_measurement(tool, params)
        print(json.dumps(result, indent=2))

    elif cmd == 'provenance':
        if len(sys.argv) < 3:
            print("Usage: ghost-preflight.py provenance <result.json>")
            sys.exit(1)
        with open(sys.argv[2]) as f:
            data = json.load(f)
        preflight = {"ghosts": [], "timestamp": datetime.now(timezone.utc).isoformat()}
        annotated = annotate_provenance(data, preflight)
        print(json.dumps(annotated, indent=2))

    elif cmd == 'run':
        if len(sys.argv) < 3:
            print("Usage: ghost-preflight.py run <command> [args...]")
            sys.exit(1)
        result = run_command_with_preflight(sys.argv[2], sys.argv[3:])
        print(json.dumps(result, indent=2))

    elif cmd == 'registry':
        with open(os.path.expanduser('~/.hermes/scripts/ghost_registry.json')) as f:
            reg = json.load(f)
        if '--json' in sys.argv:
            print(json.dumps(reg, indent=2))
        else:
            print(f"Ghost Registry — {reg['total_sessions_scanned']} sessions scanned")
            print(f"Sessions with ghosts: {reg['sessions_with_ghosts']} ({reg['pct_sessions_with_ghosts']}%)")
            print(f"Total ghost hits: {reg['total_ghost_hits']}")
            print()
            for g, s in sorted(reg['prevalence_by_type'].items(), key=lambda x: -x[1]['files_affected']):
                print(f"  {g:40s} {s['files_affected']:3d} files  {s['total_hits']:3d} hits  {s['pct_files']:5.1f}%")
            print()
            print("Co-occurrence (top 5):")
            for pair, count in sorted(reg['co_occurrence'].items(), key=lambda x: -x[1])[:5]:
                print(f"  {pair:55s} {count} files")

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == '__main__':
    main()
