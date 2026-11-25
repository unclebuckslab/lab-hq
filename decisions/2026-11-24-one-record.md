# One record of status, one owner per repo

Made Nov 24, 2026, in the planning Project.

| Decision | Reason |
| --- | --- |
| `registry/milestones.yaml` is the lab's one record of milestone status and hours. BOARD.md and the Lab Desk page show what it says and hold no status of their own | Three records written by six sessions disagreed within three days |
| Every session's closing PR updates its milestone's status and hours in the registry | Status changes in the same review as the work, so it can't be forgotten |
| Hours are estimated by each session from its commit and message times, not logged by the founder. The PR says the estimate and how it was made; the founder corrects it there | Actual hours were blank for every milestone; a rule that depends on hand-logging didn't hold |
| Each repo has one owning session, listed in `handbook/SESSIONS.md`. Others touch it only when the founder asks in chat | Sessions were editing each other's repos and records |
| The registry gets the missing milestones: P3 Annual Outings V1 live, P4 DorkGraphs system v1 (18 h from the scope proposal, not yet approved). B1, M2 and M6 move to in-progress; M5 and M6 take their current names; hours through Nov 23 come from the Lab Desk | The registry now matches the work |

## Not now

Automating the Lab Desk from the registry, flags for PRs open more than five days, and a check for chat decisions not yet in `decisions/`. Revisit after the public launch, or sooner if the records drift apart again.

## Open

- P3 and P4 were AO1 and DG1 on the Lab Desk; the Lab Desk switches to the registry ids.
- Hours for work since Nov 23 (M3 agent squad, Annual Outings AO-04 to AO-07, AI Money Report P1 work, DorkGraphs report 001) are added by each owning session at its next closing PR.

**Superseded in part Nov 25, 2026:** the hours parts of this record (hours in the first and second rows, the third row, and the Open item on hours since Nov 23) are superseded by [2026-11-25-status-not-hours](2026-11-25-status-not-hours.md). Hours tracking is retired; milestones keep `status` and `done_means`.
