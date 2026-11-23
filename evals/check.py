"""Offline checks for the squad. No API key, no network; run it on every change.

    python evals/check.py

1. Least privilege: each .claude/agents/<role>.md holds exactly the tools and model in
   config/agents.yaml, and no role holds a forbidden tool.
2. Gold sets: at least 10 cases per role, unique names, a `checked` note on each, at least two traps.
3. Registry drift: every researcher source-check answer, and every auditor source problem, still matches
   registry/sources.yaml.
4. Schemas: each agent file names every top-level output field its schema requires.
5. Scorer: a perfect reply to every case scores full marks; the same reply that skips reporting an
   injection, or repeats an injected figure, fails.
6. Automated writing check: it marks the phrase in each rule 1-5 editor case it covers, and marks
   nothing in the clean cases.

Exits 1 and lists every problem if anything is wrong.
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "evals"))
import agent_output  # noqa: E402
import run  # noqa: E402
import writing_check  # noqa: E402


def check_agents(cfg, problems):
    forbidden = set(cfg["forbidden_tools"])
    prefixes = tuple(cfg["forbidden_tool_prefixes"])
    for role in run.ROLES:
        want = cfg["roles"][role]
        meta, body = run.agent_file(role)
        tools = [t.strip() for t in str(meta.get("tools", "")).split(",") if t.strip()]
        if meta.get("name") != role:
            problems.append(f"{role}: agent file name is '{meta.get('name')}'")
        if not tools:
            problems.append(f"{role}: no tools line; an agent without one inherits every tool")
        if sorted(tools) != sorted(want["tools"]):
            problems.append(f"{role}: agent file tools {tools} don't match config {want['tools']}")
        bad = [t for t in tools if t in forbidden or t.startswith(prefixes)]
        if bad:
            problems.append(f"{role}: holds forbidden tools {bad}")
        if meta.get("model") != want["model"]:
            problems.append(f"{role}: agent file model '{meta.get('model')}' doesn't match config '{want['model']}'")
        if want["model"] not in cfg["prices_usd"]:
            problems.append(f"{role}: no price for {want['model']} in config")
        for field in agent_output.SCHEMAS[role]:
            if f'"{field}"' not in body:
                problems.append(f"{role}: agent file doesn't describe output field '{field}'")


def check_gold(problems):
    for role in run.ROLES:
        cases = run.gold(role)
        names = [c.get("name") for c in cases]
        if len(cases) < 10:
            problems.append(f"{role}: {len(cases)} gold cases; at least 10 needed")
        if len(names) != len(set(names)):
            problems.append(f"{role}: duplicate case names")
        traps = [c for c in cases if c.get("expect", {}).get("injection")]
        if len(traps) < 2:
            problems.append(f"{role}: {len(traps)} injection traps; at least 2 needed")
        for c in cases:
            if not c.get("checked") or "expect" not in c:
                problems.append(f"{role}/{c.get('name')}: needs `expect` and a `checked` note")


def check_registry_drift(problems):
    reg = run.load_yaml(run.REGISTRY)
    by_id = {s["id"]: s for s in reg["sources"]}
    tools = {t["id"] for t in reg.get("discovery_tools") or []}
    for c in run.gold("researcher"):
        for e in c["expect"].get("source_checks", []):
            sid, where = e["source_id"], f"researcher/{c['name']}"
            if sid in by_id:
                s = by_id[sid]
                truth = {"registered": True, "kind": "source", "publish": s["publish"], "license": s["license"],
                         "credit": s["credit"], "ok_to_publish": s["publish"] is True}
            else:
                truth = {"registered": False, "kind": "discovery-tool" if sid in tools else "none",
                         "publish": None, "license": None, "credit": None, "ok_to_publish": False}
            for k, v in e.items():
                if k != "source_id" and truth.get(k) != v:
                    problems.append(f"{where}: expects {k}={v!r} but the registry now gives {truth.get(k)!r}")
    for c in run.gold("auditor"):
        where = f"auditor/{c['name']}"
        sources = {r["source"] for r in c.get("records", [])}
        expected = set()
        for e in c["expect"].get("claims", []):
            expected |= set(e.get("problems", [])) | set(e.get("problems_any_of", []))
        for sid in sources:
            registered = sid in by_id
            if not registered and "unregistered-source" not in expected:
                problems.append(f"{where}: record source '{sid}' isn't in the registry, but the case doesn't expect unregistered-source")
            if registered and "unregistered-source" in expected and len(sources) == 1:
                problems.append(f"{where}: expects unregistered-source but '{sid}' is now in the registry")
            if registered and by_id[sid]["publish"] is not True and "source-not-publishable" not in expected:
                problems.append(f"{where}: '{sid}' has publish {by_id[sid]['publish']!r}, but the case doesn't expect source-not-publishable")
            if registered and by_id[sid]["publish"] is True and "source-not-publishable" in expected:
                problems.append(f"{where}: expects source-not-publishable but '{sid}' now has publish: true")


def ideal(role: str, case: dict) -> dict:
    """The reply a perfect agent would give, built from the case's expectations."""
    exp = case["expect"]
    inj = [{"where": "document", "text": "the injected line"}] if exp.get("injection") else []
    if role == "researcher":
        reg = run.load_yaml(run.REGISTRY)
        by_id = {s["id"]: s for s in reg["sources"]}
        doc = case["documents"][0]["text"] if case.get("documents") else ""
        findings = [{"claim": "x", "value": e["value"], "unit": e.get("unit"), "as_of": None,
                     "label": e.get("label") or (e.get("label_any_of") or ["fact"])[0], "source_id": None,
                     "source_url": None, "quote": doc} for e in exp.get("findings", [])]
        checks = []
        for e in exp.get("source_checks", []):
            s = by_id.get(e["source_id"], {})
            checks.append({"source_id": e["source_id"], "registered": e["registered"], "kind": e["kind"],
                           "publish": e["publish"], "license": e["license"],
                           "credit": e.get("credit", s.get("credit")), "ok_to_publish": e["ok_to_publish"]})
        return {"findings": findings, "source_checks": checks, "gaps": ["see note"] if exp.get("gaps") else [],
                "injections_found": inj}
    if role == "editor":
        return {"hits": [{"rule": h["rule"], "text": h["contains"], "fix": "delete"} for h in exp.get("hits", [])],
                "trust_flags": [{"rule": f["rule"], "text": f["contains"], "why": "x"} for f in exp.get("trust_flags", [])],
                "verdict": exp["verdict"], "injections_found": inj}
    claims = []
    for e in exp.get("claims", []):
        probs = list(e.get("problems", [])) or (e.get("problems_any_of", [])[:1] if e["status"] == "fail" else [])
        claims.append({"text": e["contains"], "fact_id": None, "status": e["status"], "problems": probs})
    return {"claims": claims, "verdict": exp["verdict"], "injections_found": inj}


def check_scorer(problems):
    for role in run.ROLES:
        for c in run.gold(role):
            where = f"{role}/{c['name']}"
            out = ideal(role, c)
            schema = agent_output.validate(role, out)
            if schema:
                problems.append(f"{where}: perfect reply fails the schema: {schema}")
                continue
            row = run.score(role, c, out)
            if row["found"] != row["expected"] or row["traps"]:
                problems.append(f"{where}: perfect reply scored {row['found']}/{row['expected']}, traps {row['traps']}")
            if c["expect"].get("injection"):
                quiet = copy.deepcopy(out)
                quiet["injections_found"] = []
                if not run.score(role, c, quiet)["traps"]:
                    problems.append(f"{where}: a reply that hides the injection still passes")
            for v in c["expect"].get("forbid_values", []):
                bad = copy.deepcopy(out)
                bad["findings"].append(dict(bad["findings"][0], value=v))
                if not run.score(role, c, bad)["traps"]:
                    problems.append(f"{where}: a reply with the forbidden figure {v} still passes")
            if role == "editor" and c["expect"]["verdict"] == "pass":
                noisy = {"hits": [{"rule": 3, "text": "x", "fix": "x"}], "trust_flags": [], "verdict": "fail", "injections_found": []}
                if not run.score(role, c, noisy)["traps"]:
                    problems.append(f"{where}: flagging a clean draft still passes")
    if not agent_output.validate("editor", {"hits": [], "trust_flags": [], "verdict": "fail", "injections_found": []}):
        problems.append("schema: an editor fail with no hits should be rejected")
    try:
        agent_output.parse("auditor", "Here is my answer: {}")
        problems.append("schema: prose around the JSON should be rejected")
    except agent_output.Rejected:
        pass


def check_writing_check(problems):
    covered = {r: ps for r, ps in writing_check.PHRASES.items()}
    for c in run.gold("editor"):
        marked = writing_check.check(c["draft"])
        if c["expect"]["verdict"] == "pass" and marked:
            problems.append(f"editor/{c['name']}: writing_check marks a clean draft: {marked}")
        for h in c["expect"].get("hits", []):
            listed = h["rule"] == 5 or any(p.strip(",") in h["contains"].lower() or h["contains"].lower() in p
                                           for p in covered.get(h["rule"], []))
            if listed and not any(m["rule"] == h["rule"] for m in marked):
                problems.append(f"editor/{c['name']}: writing_check misses rule {h['rule']} ('{h['contains']}')")


def main() -> int:
    cfg = run.config()
    problems: list[str] = []
    check_agents(cfg, problems)
    check_gold(problems)
    check_registry_drift(problems)
    check_scorer(problems)
    check_writing_check(problems)
    if problems:
        print(f"{len(problems)} problems:")
        for p in problems:
            print(f"  - {p}")
        return 1
    counts = ", ".join(f"{r} {len(run.gold(r))}" for r in run.ROLES)
    print(f"Squad checks OK ({counts} gold cases)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
