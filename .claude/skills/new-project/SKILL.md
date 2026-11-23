---
name: new-project
description: Start a new lab project from the template - register it in lab-hq, copy templates/project/ into the founder-created repo, and fill in its CLAUDE.md - as two pull requests. Use when the founder asks to set up a new project. Does steps 1, 3 and 4 of templates/README.md; creating the repo stays with the founder.
---

# New project

Follows [templates/README.md](../../../templates/README.md). The founder creates the repo (step 2); this skill never creates, deletes or changes the settings of a repo.

## 1. Confirm scope with the founder

Propose answers rather than interviewing, and get a yes on:

- Name, and whether it's a working name.
- Type: `recurring-report`, `dashboard`, `reference-database`, `visual`, `brand`, `product` or `writing`.
- Playbook, if one fits (`playbooks/data-product.md`, `playbooks/report.md`).
- Point of view: none, or the declared one (TRUST_RULES.md 10).
- Public or private repo (CONVENTIONS.md: public unless the data or plans are private).
- First milestone and its estimate, if he wants one now.

## 2. Register it (lab-hq PR)

On a branch `chief-of-staff/register-<id>`:

- Add a record to `registry/projects.yaml` with `stage: define`, `status: in-the-lab`, `show_on_site: false`, `repo` set to the repo the founder created (or `null` until he has), and every field in `registry/README.md`.
- If there's a first milestone, add it to `registry/milestones.yaml` with an id prefix from the README.
- Run `python registry/validate.py`; it must pass.
- Open the PR. The site doesn't list the project until the founder sets `show_on_site`.

## 3. Copy the template (project repo PR)

Once the repo exists and is attached to the session, on a branch `chief-of-staff/from-template`:

- Copy everything in `templates/project/`, including `.github/`.
- Replace every `PROJECT NAME`.
- Fill in `CLAUDE.md` first: purpose, type, playbook, point of view, and the link back to lab-hq's `INDEX.md`. Point to lab-hq handbook files; never copy them (SYSTEM_OF_RECORD.md).
- Leave workflow files and `permissions:` blocks out. Pipelines arrive later through their own PRs, which the founder merges himself.
- Open the PR.

## 4. Stop

Report both PR links and what's left for the founder: merge both, set `show_on_site` when ready, and start the playbook.
