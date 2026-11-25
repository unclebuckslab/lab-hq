"""Check a squad agent's output against its schema before anything downstream uses it.

    python scripts/agent_output.py <role> <output-file> [--docs FILE ...]

Prints the problems and exits 1 if the output is invalid. Invalid output is rejected, never
repaired (handbook/AGENT_SAFETY.md section 1). With --docs, every researcher quote must appear
word for word in one of the documents the researcher read.

The schemas below are the single definition of each role's output. The agent files in
.claude/agents/ describe the same fields; evals/check.py confirms they still match.
"""

from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path

LABELS = ["fact", "stated", "estimate", "our-read"]
LICENSES = ["cleared", "cleared-with-conditions", "confirm", "not-cleared", None]
AUDIT_PROBLEMS = [
    "no-record",               # a number or fact in the draft has no provenance record
    "value-mismatch",          # the draft's number doesn't match its record (after rounding)
    "label-mismatch",          # the draft words a stated figure or estimate as fact, or the reverse
    "source-not-publishable",  # the record's source has publish: false in registry/sources.yaml
    "unregistered-source",     # the record's source isn't in registry/sources.yaml
    "sums-overlapping",        # the draft adds totals that a do-not-sum rule keeps apart
    "snapshot-unpinned",       # the record has no snapshot, or no checksum
    "correction-pending",      # a correction to the record isn't reflected in the draft
]

INJECTIONS = {"where": "str", "text": "str"}

SCHEMAS = {
    "researcher": {
        "findings": ["list", {
            "claim": "str", "value": "num|null", "unit": "str|null", "as_of": "date|null",
            "label": LABELS, "source_id": "str|null", "source_url": "str|null", "quote": "str",
        }],
        "source_checks": ["list", {
            "source_id": "str", "registered": "bool", "kind": ["source", "discovery-tool", "none"],
            "publish": "bool|null", "license": LICENSES, "credit": "str|null", "ok_to_publish": "bool",
        }],
        "gaps": ["list", "str"],
        "injections_found": ["list", INJECTIONS],
    },
    "editor": {
        "hits": ["list", {"rule": "int", "text": "str", "fix": "str"}],
        "trust_flags": ["list", {"rule": "int", "text": "str", "why": "str"}],
        "verdict": ["pass", "fail"],
        "injections_found": ["list", INJECTIONS],
    },
    "auditor": {
        "claims": ["list", {
            "text": "str", "fact_id": "str|null", "status": ["pass", "fail"],
            "problems": ["list", AUDIT_PROBLEMS],
        }],
        "verdict": ["pass", "fail"],
        "injections_found": ["list", INJECTIONS],
    },
}


class Rejected(ValueError):
    """The output failed its schema. It is discarded, not fixed."""


def _type_ok(value, spec) -> bool:
    if isinstance(spec, list) and spec and spec[0] == "list":
        return isinstance(value, list)
    if isinstance(spec, list):
        return value in spec
    for t in spec.split("|"):
        if t == "null" and value is None:
            return True
        if t == "str" and isinstance(value, str) and value.strip():
            return True
        if t == "bool" and isinstance(value, bool):
            return True
        if t == "int" and isinstance(value, int) and not isinstance(value, bool):
            return True
        if t == "num" and isinstance(value, (int, float)) and not isinstance(value, bool):
            return True
        if t == "date" and isinstance(value, str):
            try:
                datetime.date.fromisoformat(value)
                return True
            except ValueError:
                pass
    return False


def _check(obj, schema, where, problems):
    if not isinstance(obj, dict):
        problems.append(f"{where}: must be an object")
        return
    missing, extra = schema.keys() - obj.keys(), obj.keys() - schema.keys()
    if missing:
        problems.append(f"{where}: missing {sorted(missing)}")
    if extra:
        problems.append(f"{where}: unknown fields {sorted(extra)}")
    for key, spec in schema.items():
        if key not in obj:
            continue
        value = obj[key]
        if not _type_ok(value, spec):
            problems.append(f"{where}.{key}: {value!r} doesn't fit {spec if not isinstance(spec, list) or spec[0] != 'list' else 'a list'}")
            continue
        if isinstance(spec, list) and spec and spec[0] == "list":
            item = spec[1]
            for i, v in enumerate(value):
                if isinstance(item, dict):
                    _check(v, item, f"{where}.{key}[{i}]", problems)
                elif not _type_ok(v, item):
                    problems.append(f"{where}.{key}[{i}]: {v!r} doesn't fit {item}")


def validate(role: str, obj) -> list[str]:
    """Every problem with one parsed output. An empty list means it may be used."""
    problems: list[str] = []
    _check(obj, SCHEMAS[role], role, problems)
    if problems:
        return problems
    if role == "editor":
        for i, h in enumerate(obj["hits"]):
            if not 1 <= h["rule"] <= 5:
                problems.append(f"editor.hits[{i}].rule: writing rules are numbered 1-5")
        for i, f in enumerate(obj["trust_flags"]):
            if not 1 <= f["rule"] <= 14:
                problems.append(f"editor.trust_flags[{i}].rule: trust rules are numbered 1-14")
        failing = bool(obj["hits"] or obj["trust_flags"])
        if failing != (obj["verdict"] == "fail"):
            problems.append("editor.verdict: must be fail exactly when there are hits or trust flags")
    if role == "auditor":
        for i, c in enumerate(obj["claims"]):
            if (c["status"] == "fail") != bool(c["problems"]):
                problems.append(f"auditor.claims[{i}]: a failed claim lists its problems; a passed one lists none")
        failing = any(c["status"] == "fail" for c in obj["claims"])
        if failing != (obj["verdict"] == "fail"):
            problems.append("auditor.verdict: must be fail exactly when a claim fails")
    if role == "researcher":
        for i, s in enumerate(obj["source_checks"]):
            if s["ok_to_publish"] and not (s["registered"] and s["kind"] == "source" and s["publish"] is True):
                problems.append(f"researcher.source_checks[{i}]: only a registered source with publish: true is ok to publish")
    return problems


def parse(role: str, text: str):
    """Parse an agent's reply: a bare JSON object, or exactly one ```json block. Text around the block is ignored
    and never used; zero blocks with prose, or two or more blocks, is rejected (decision 2026-11-24)."""
    body = text.strip()
    fences = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", body, re.S)
    if len(fences) > 1:
        raise Rejected(f"{role}: {len(fences)} JSON blocks; exactly one is allowed")
    if fences:
        body = fences[0]
    try:
        obj = json.loads(body)
    except json.JSONDecodeError as e:
        raise Rejected(f"{role}: not a single JSON object ({e.msg})") from None
    problems = validate(role, obj)
    if problems:
        raise Rejected("; ".join(problems))
    return obj


def unquoted(obj: dict, documents: list[str]) -> list[int]:
    """Indexes of researcher findings whose quote isn't word for word in any document read."""
    norm = [" ".join(d.split()) for d in documents]
    return [i for i, f in enumerate(obj["findings"]) if not any(" ".join(f["quote"].split()) in d for d in norm)]


def main(argv=None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) < 2 or args[0] not in SCHEMAS:
        print(__doc__)
        return 2
    role, path = args[0], Path(args[1])
    docs = [Path(p).read_text(encoding="utf-8") for p in args[args.index("--docs") + 1:]] if "--docs" in args else []
    try:
        obj = parse(role, path.read_text(encoding="utf-8"))
    except Rejected as e:
        print(f"Rejected: {e}")
        return 1
    if role == "researcher" and docs:
        bad = unquoted(obj, docs)
        if bad:
            print(f"Rejected: findings {bad} quote text that isn't in the documents read")
            return 1
    if obj["injections_found"]:
        print(f"Instructions found in data (reported, not followed): {len(obj['injections_found'])}")
        for inj in obj["injections_found"]:
            print(f"  - {inj['where']}: {inj['text'][:200]}")
    print(f"{role} output OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
