"""Validate registry/projects.yaml, registry/milestones.yaml and registry/sources.yaml.

Run from the repo root: python registry/validate.py
Exits 1 and lists every problem if anything is wrong.

    python registry/validate.py --report

also prints what needs the founder (unapproved tiers, unchecked licenses) and the
cross-project overlap the weekly briefing reads: sources pulled by more than one repo
outside lab-data, and sources several projects use that are still pulled inside one project.
"""

import datetime
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

PROJECT_FIELDS = {
    "id", "name", "working_name", "endorsement", "type", "stage", "status",
    "show_on_site", "priority", "repo", "public_url", "summary", "playbook",
    "agents", "next_milestone", "notes",
}
TYPES = {"recurring-report", "dashboard", "reference-database", "visual", "brand", "product", "writing"}
STAGES = {"idea", "explore", "define", "build", "review", "launch", "operate", "improve", "archived"}
STATUSES = {"in-the-lab", "live", "paused", "archived", "parked"}

MILESTONE_FIELDS = {"id", "name", "after", "est_hours", "actual_hours", "status", "done_means"}
MILESTONE_STATUSES = {"not-started", "in-progress", "done"}

SOURCE_FIELDS = {
    "id", "name", "tier", "tier_approved", "license", "license_checked", "conditions",
    "credit", "covers", "known_breaks", "access", "status", "publish", "pipelines",
    "used_by", "notes",
}
TIERS = {"A", "B", "R", "C", None}
LICENSES = {"cleared", "cleared-with-conditions", "confirm", "not-cleared"}
SOURCE_STATUSES = {"active", "listed", "blocked", "retired"}
PIPELINE_FIELDS = {"repo", "path", "schedule"}
TOOL_FIELDS = {"id", "name", "checked", "rule"}
LAB_DATA_REPO = "unclebuckslab/lab-data"
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def load(name):
    with open(ROOT / "registry" / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def check_milestones(problems):
    milestones = load("milestones.yaml")["milestones"]
    ids = [m.get("id") for m in milestones]
    if len(ids) != len(set(ids)):
        problems.append("milestones: duplicate ids")
    for m in milestones:
        where = f"milestone {m.get('id')}"
        missing = MILESTONE_FIELDS - m.keys()
        extra = m.keys() - MILESTONE_FIELDS
        if missing:
            problems.append(f"{where}: missing {sorted(missing)}")
        if extra:
            problems.append(f"{where}: unknown fields {sorted(extra)}")
        if m.get("status") not in MILESTONE_STATUSES:
            problems.append(f"{where}: status '{m.get('status')}' not in {sorted(MILESTONE_STATUSES)}")
        for dep in m.get("after") or []:
            if dep not in ids:
                problems.append(f"{where}: depends on unknown milestone '{dep}'")
        est = m.get("est_hours")
        if not isinstance(est, (int, float)) or est <= 0:
            problems.append(f"{where}: est_hours must be a positive number")
        actual = m.get("actual_hours")
        if actual is not None and (not isinstance(actual, (int, float)) or actual < 0):
            problems.append(f"{where}: actual_hours must be null or a number >= 0")
        if m.get("status") == "done" and m.get("est_hours") is None:
            problems.append(f"{where}: done milestones need an estimate")
    return set(ids)


def check_projects(problems, milestone_ids):
    projects = load("projects.yaml")["projects"]
    ids = [p.get("id") for p in projects]
    if len(ids) != len(set(ids)):
        problems.append("projects: duplicate ids")
    for p in projects:
        where = f"project {p.get('id')}"
        missing = PROJECT_FIELDS - p.keys()
        extra = p.keys() - PROJECT_FIELDS
        if missing:
            problems.append(f"{where}: missing {sorted(missing)}")
        if extra:
            problems.append(f"{where}: unknown fields {sorted(extra)}")
        if p.get("type") not in TYPES:
            problems.append(f"{where}: type '{p.get('type')}' not in {sorted(TYPES)}")
        if p.get("stage") not in STAGES:
            problems.append(f"{where}: stage '{p.get('stage')}' not in {sorted(STAGES)}")
        if p.get("status") not in STATUSES:
            problems.append(f"{where}: status '{p.get('status')}' not in {sorted(STATUSES)}")
        if p.get("status") == "parked" and p.get("show_on_site"):
            problems.append(f"{where}: parked projects can't show on the site")
        if p.get("next_milestone") is not None and p["next_milestone"] not in milestone_ids:
            problems.append(f"{where}: next_milestone '{p['next_milestone']}' isn't in milestones.yaml")
        playbook = p.get("playbook")
        if playbook is not None and not (ROOT / playbook).exists():
            problems.append(f"{where}: playbook '{playbook}' doesn't exist")
    return set(ids)


def is_date_or_none(value):
    return value is None or isinstance(value, datetime.date)


def check_sources(problems, project_ids):
    data = load("sources.yaml")
    sources = data["sources"]
    ids = [s.get("id") for s in sources]
    tool_ids = [t.get("id") for t in data.get("discovery_tools") or []]
    if len(ids) != len(set(ids)):
        problems.append("sources: duplicate ids")
    if set(ids) & set(tool_ids):
        problems.append(f"sources: ids used as both a source and a discovery tool: {sorted(set(ids) & set(tool_ids))}")
    for s in sources:
        where = f"source {s.get('id')}"
        missing = SOURCE_FIELDS - s.keys()
        extra = s.keys() - SOURCE_FIELDS
        if missing:
            problems.append(f"{where}: missing {sorted(missing)}")
        if extra:
            problems.append(f"{where}: unknown fields {sorted(extra)}")
        if s.get("tier") not in TIERS:
            problems.append(f"{where}: tier '{s.get('tier')}' not in A, B, R, C or null")
        if s.get("license") not in LICENSES:
            problems.append(f"{where}: license '{s.get('license')}' not in {sorted(LICENSES)}")
        if s.get("status") not in SOURCE_STATUSES:
            problems.append(f"{where}: status '{s.get('status')}' not in {sorted(SOURCE_STATUSES)}")
        for field in ("tier_approved", "license_checked"):
            if not is_date_or_none(s.get(field)):
                problems.append(f"{where}: {field} must be a date (YYYY-MM-DD) or null")
        if s.get("license_checked") is None and s.get("license") != "confirm":
            problems.append(f"{where}: only a 'confirm' license may have no check date")
        if not isinstance(s.get("publish"), bool):
            problems.append(f"{where}: publish must be true or false")
        if s.get("license") in {"confirm", "not-cleared"} and s.get("publish"):
            problems.append(f"{where}: a '{s.get('license')}' license can't be published; set publish: false")
        if s.get("status") == "blocked" and s.get("publish"):
            problems.append(f"{where}: blocked sources can't be published")
        for field in ("conditions", "known_breaks", "pipelines", "used_by"):
            if not isinstance(s.get(field), list):
                problems.append(f"{where}: {field} must be a list (use [] for none)")
        pipelines = s.get("pipelines") or []
        if s.get("status") == "active" and not pipelines:
            problems.append(f"{where}: active sources need at least one pipeline")
        if s.get("status") in {"listed", "blocked", "retired"} and pipelines:
            problems.append(f"{where}: only active sources have pipelines")
        for p in pipelines:
            if not isinstance(p, dict) or set(p) != PIPELINE_FIELDS:
                problems.append(f"{where}: each pipeline needs exactly {sorted(PIPELINE_FIELDS)}")
                continue
            if not REPO_RE.match(str(p["repo"])):
                problems.append(f"{where}: pipeline repo '{p['repo']}' isn't owner/name")
        for project in s.get("used_by") or []:
            if project not in project_ids:
                problems.append(f"{where}: used_by '{project}' isn't in projects.yaml")
    for t in data.get("discovery_tools") or []:
        where = f"discovery tool {t.get('id')}"
        if set(t) != TOOL_FIELDS:
            problems.append(f"{where}: needs exactly {sorted(TOOL_FIELDS)}")
        if not is_date_or_none(t.get("checked")):
            problems.append(f"{where}: checked must be a date or null")
    return sources


def report(sources):
    """What needs the founder, and where projects overlap. Informational; never fails."""
    approve = [s["id"] for s in sources if s["tier_approved"] is None and s["tier"] is not None]
    unchecked = [s["id"] for s in sources if s["license"] == "confirm" and s["status"] != "blocked"]
    year_ago = datetime.datetime.now(datetime.timezone.utc).date() - datetime.timedelta(days=365)
    stale = [s["id"] for s in sources if s["license_checked"] and s["license_checked"] < year_ago and s["status"] != "retired"]
    print("\nNeeds the founder:")
    print(f"  - tier not yet approved: {', '.join(approve) or 'none'}")
    print(f"  - license to confirm before publishing (in use or planned): {', '.join(unchecked) or 'none'}")
    print(f"  - license check older than a year: {', '.join(stale) or 'none'}")

    print("\nOverlap (weekly briefing):")
    duplicated = []
    for s in sources:
        repos = {p["repo"] for p in s["pipelines"] if p["repo"] != LAB_DATA_REPO}
        if len(repos) > 1:
            duplicated.append(f"{s['id']} ({', '.join(sorted(repos))})")
    print(f"  - pulled by more than one repo outside lab-data: {', '.join(duplicated) or 'none'}")
    candidates = []
    for s in sources:
        repos = {p["repo"] for p in s["pipelines"]}
        if s["status"] == "active" and len(s["used_by"]) > 1 and repos and LAB_DATA_REPO not in repos:
            candidates.append(f"{s['id']} ({', '.join(s['used_by'])})")
    print(f"  - used by several projects, still pulled inside one: {', '.join(candidates) or 'none'}")


def main():
    problems = []
    milestone_ids = check_milestones(problems)
    project_ids = check_projects(problems, milestone_ids)
    sources = check_sources(problems, project_ids)
    if problems:
        print("Registry problems:")
        for line in problems:
            print(f"  - {line}")
        sys.exit(1)
    print("Registry OK")
    if "--report" in sys.argv[1:]:
        report(sources)


if __name__ == "__main__":
    main()
