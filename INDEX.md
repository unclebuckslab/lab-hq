# Index

Every lab session reads this file first. It lists each handbook file and what it's for. When files are added or renamed, only this index changes, so project instructions never need re-pasting.

Claude Projects and other tools read these files by link, never as uploaded copies. Raw links start with `https://raw.githubusercontent.com/unclebuckslab/lab-hq/main/`.

## Who we are

| File | Read it for |
| --- | --- |
| [handbook/IDENTITY.md](handbook/IDENTITY.md) | The name, the brand architecture, the persona, the mission, what the lab makes |
| [handbook/PRINCIPLES.md](handbook/PRINCIPLES.md) | The seven principles and the standing guardrails |
| [handbook/WRITING_RULES.md](handbook/WRITING_RULES.md) | The five things lab writing never does |
| [handbook/MONEY_RULES.md](handbook/MONEY_RULES.md) | What's free, what's paid, disclosure, sponsors, holdings |

## How we work

| File | Read it for |
| --- | --- |
| [handbook/GOVERNANCE.md](handbook/GOVERNANCE.md) | What agents may do alone, the approval tiers, the kill switch |
| [handbook/SESSIONS.md](handbook/SESSIONS.md) | Which session owns which repo, the one record of status, how hours are estimated |
| [handbook/SYSTEM_OF_RECORD.md](handbook/SYSTEM_OF_RECORD.md) | Where each kind of information lives, and where it never lives |
| [handbook/RESEARCH_STANDARDS.md](handbook/RESEARCH_STANDARDS.md) | Sources, snapshots, provenance records, checked facts, labels, reproducibility |
| [handbook/TRUST_RULES.md](handbook/TRUST_RULES.md) | The rules every publication follows before it ships |
| [handbook/AGENT_SAFETY.md](handbook/AGENT_SAFETY.md) | The read/act boundary, token scopes, run budgets, eval gates |
| [handbook/CONVENTIONS.md](handbook/CONVENTIONS.md) | Repo layout, naming, branches, labels, hours logging |

## Records

| File | Read it for |
| --- | --- |
| [registry/projects.yaml](registry/projects.yaml) | Every project: type, stage, status, repo, hours |
| [registry/milestones.yaml](registry/milestones.yaml) | Lab milestones: estimated vs actual hours, status, what done means |
| [registry/sources.yaml](registry/sources.yaml) | Every data source: tier, license, credit, known breaks, which repo pulls it, which projects use it |
| [registry/README.md](registry/README.md) | The registry's fields and how to update them |
| [decisions/](decisions/) | Lab-level decisions, one dated file each |

## Building

| File | Read it for |
| --- | --- |
| [playbooks/data-product.md](playbooks/data-product.md) | Building a data source to pipeline to page product |
| [playbooks/report.md](playbooks/report.md) | Building a recurring, sourced report |
| [playbooks/weekly-briefing.md](playbooks/weekly-briefing.md) | What the weekly briefing checks and how it reports |
| [templates/project/](templates/project/) | The starting files for a new project repo |

## The squad

| File | Read it for |
| --- | --- |
| [.claude/agents/](.claude/agents/) | The researcher, editor and auditor subagents: read-only, JSON output |
| [.claude/skills/](.claude/skills/) | `research-brief`, `pre-publish` and `new-project` |
| [config/agents.yaml](config/agents.yaml) | Each role's model, tools and budget |
| [evals/](evals/) | Gold sets per role and how to run them; `scripts/agent_output.py` checks every reply |

## Coming next

Not written yet; don't look for them.

- `handbook/VOICE.md` and `handbook/CHARACTER.md`, plus `brand/` (interviews and writing samples): milestone B1.
- The scheduled headless briefing and ops check in Actions, an eval workflow and the away runbook: the rest of milestone M3.
- The `unclebuckslab/lab-data` repo with shared ingest: milestone D3, built when Congress Cards starts.
