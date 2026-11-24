# Sessions and the repos they own

Each repo has one owning session. Only that session opens PRs in it, unless the founder asks another one to in chat. A session that finds work for a repo it doesn't own notes it for the owner instead.

| Repo | Owning session | Covers |
| --- | --- | --- |
| lab-hq | Lab HQ (chief of staff) | Rules, handbook, registry, source library, decisions, agents and skills |
| lab-desk | Lab HQ (chief of staff) | BOARD.md, the Lab Desk page's data, briefings |
| lab-site | Lab site | The site and its launch checklist |
| ai-money-report | AI Money Report | Pipelines, drafts, evals |
| annual-outings | Annual Outings | The app and its build plan |
| dorkgraphs | DorkGraphs | Pipelines, discovery, reports and posts |

Scheduled tasks (the weekly briefing and the data workflows) read any repo and write only where their playbook says.

When the founder starts or retires a session, this table changes in the same week.

## The one record

`registry/milestones.yaml` is the record of every milestone's status and hours. BOARD.md and the Lab Desk page show what it says and keep no status of their own. If they disagree with it, the registry wins and the other is corrected.

## Hours

Nobody logs hours by hand. Each session estimates its own focus hours from its commit and message times, adds them to the milestone in its closing PR, and says how it got the number. The founder corrects an estimate in the PR.
