#!/usr/bin/env python3
"""
Parse Blacklist Violations — Stdout → JSON Corrections (P6 pattern)

Transforms the stdout of `phase4-blacklist-gate.py` into a deterministic JSON
corrections list compatible with the BIG pipeline P6 pattern (Phase 4 sub-step
4.4).

Why this script exists:
    The Phase 4 sub-step 4.4 used to ask the orchestrator (LLM) to write the
    corrections JSON based on the gates verdicts. The LLM frequently shortcut
    by reading only the finishing-gate verdict (often WARN) and ignored
    blacklist-gate FAILs — producing an empty corrections list while real
    violations remained in the HTML. Replacing the LLM step with this
    deterministic parser eliminates the shortcut.

Usage:
    python3 parse-blacklist-violations.py <stdout_file> <output_json> \\
        --concept N --stage {v0|v1|art|iter0|iter1}

Exit codes:
    0 — parsed successfully (verdict PASS or FAIL with corrections written)
    1 — error writing the JSON output
    2 — input file missing or empty
"""

import argparse
import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

# Matches lines like:  "  ❌ hover-letter-spacing (2x)"  or  "  ❌ rule-id"
RULE_HEADER_RE = re.compile(
    r'^\s*❌\s+(?P<rule_id>[\w\-]+)(?:\s*\((?P<count>\d+)x\))?\s*$'
)

# Matches lines like:  "     Ligne 415: letter-spacing au hover — cliché ..."
VIOLATION_LINE_RE = re.compile(
    r'^\s+Ligne\s+(?P<line>\d+):\s*(?P<description>.+?)\s*$'
)

VERDICT_PASS_RE = re.compile(r'^\s*VERDICT:\s*PASS\b', re.MULTILINE)
VERDICT_FAIL_RE = re.compile(r'^\s*VERDICT:\s*FAIL\b', re.MULTILINE)


def split_description(description: str) -> tuple[str, str]:
    """Split a violation description on the em-dash separator.

    Format expected: "<current> — <fix>"
    The em-dash used by the gate is U+2014 ("—"). We also tolerate a regular
    hyphen with surrounding spaces (" - ") as a fallback.
    Returns ("<current>", "<fix>") or ("<description>", "") if no separator.
    """
    for sep in (' — ', ' – ', ' - '):
        if sep in description:
            current, fix = description.split(sep, 1)
            return current.strip(), fix.strip()
    return description.strip(), ''


def parse_violations(stdout_text: str) -> list[dict]:
    """Parse the stdout of phase4-blacklist-gate.py into correction entries.

    Returns one entry per violation occurrence (NOT per category).
    """
    corrections: list[dict] = []
    current_rule_id: str | None = None

    for raw_line in stdout_text.splitlines():
        # Try to match a category header first.
        header_match = RULE_HEADER_RE.match(raw_line)
        if header_match:
            current_rule_id = header_match.group('rule_id')
            continue

        # Otherwise, try to match a violation line under the current category.
        if current_rule_id is None:
            continue

        violation_match = VIOLATION_LINE_RE.match(raw_line)
        if violation_match:
            line_num = int(violation_match.group('line'))
            description = violation_match.group('description')
            current, fix = split_description(description)
            corrections.append({
                'rule_id': current_rule_id,
                'severity': 'critical',
                'line': line_num,
                'current': current,
                'fix': fix,
                'reason': 'Pattern daté détecté par phase4-blacklist-gate.py',
                'source_gate': 'blacklist',
            })
            continue

        # A blank line between categories resets the active rule_id so that a
        # stray "Ligne N: ..." outside any "❌ ..." header is never attributed
        # to a previous category by mistake.
        if raw_line.strip() == '':
            current_rule_id = None

    return corrections


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description='Parse phase4-blacklist-gate.py stdout into a JSON '
                    'corrections list (P6 pattern).'
    )
    parser.add_argument('stdout_file', type=str,
                        help='Path to the .stdout file from blacklist gate.')
    parser.add_argument('output_json', type=str,
                        help='Path to the JSON corrections file to produce.')
    parser.add_argument('--concept', type=int, required=True,
                        help='Concept number (e.g. 2).')
    parser.add_argument('--stage', type=str, required=True,
                        choices=['v0', 'v1', 'art', 'iter0', 'iter1'],
                        help='Pipeline stage.')
    args = parser.parse_args()

    stdout_path = Path(args.stdout_file)
    output_path = Path(args.output_json)

    # --- Read stdout file ---------------------------------------------------
    if not stdout_path.exists():
        print(f'[ERROR] stdout file not found: {stdout_path}', file=sys.stderr)
        return 2

    try:
        stdout_text = stdout_path.read_text(encoding='utf-8')
    except OSError as exc:
        print(f'[ERROR] cannot read stdout file: {exc}', file=sys.stderr)
        return 2

    if not stdout_text.strip():
        print(f'[ERROR] stdout file is empty: {stdout_path}', file=sys.stderr)
        return 2

    # --- Determine verdict --------------------------------------------------
    has_pass = bool(VERDICT_PASS_RE.search(stdout_text))
    has_fail = bool(VERDICT_FAIL_RE.search(stdout_text))

    if has_pass and not has_fail:
        verdict = 'PASS'
        produced_by = 'parse-blacklist-no-violations'
        corrections: list[dict] = []
    elif has_fail:
        verdict = 'FAIL'
        produced_by = 'parse-blacklist-violations.py'
        corrections = parse_violations(stdout_text)
    else:
        # Malformed input — no VERDICT line found.
        print('[WARN] no VERDICT line found in stdout — treating as malformed '
              'input (empty corrections)', file=sys.stderr)
        verdict = 'UNKNOWN'
        produced_by = 'parse-blacklist-malformed-input'
        corrections = []

    # --- Build payload ------------------------------------------------------
    payload = {
        'corrections': corrections,
        'produced_by': produced_by,
        'concept': args.concept,
        'stage': args.stage,
        'blacklist_verdict': verdict,
        'violations_count': len(corrections),
    }

    # --- Write JSON ---------------------------------------------------------
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open('w', encoding='utf-8') as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
            fh.write('\n')
    except OSError as exc:
        print(f'[ERROR] cannot write JSON output: {exc}', file=sys.stderr)
        return 1

    # --- Console summary ----------------------------------------------------
    print(f'=== PARSE BLACKLIST VIOLATIONS ===')
    print(f'Stdout : {stdout_path}')
    print(f'Output : {output_path}')
    print(f'Verdict: {verdict}')
    print(f'Violations parsed: {len(corrections)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())


# ---------------------------------------------------------------------------
# Example invocation:
#
#   python3 parse-blacklist-violations.py \
#       "$sd/.gates-blacklist-c2-v0.stdout" \
#       "$sd/.finishing-gate-c2-v0-corrections-blacklist.json" \
#       --concept 2 --stage v0
# ---------------------------------------------------------------------------
