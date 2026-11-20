# Weekly briefing runs as a Claude scheduled task

Made Nov 19, 2026, in chat.

| Decision | Reason |
| --- | --- |
| The weekly briefing ships now, ahead of the rest of milestone M3 | The AI Money Report pipeline was down for two weeks in November before anyone caught it. A weekly cross-repo check is the cheapest fix |
| It runs as a Claude scheduled task, not in GitHub Actions as [AGENT_SAFETY.md](../handbook/AGENT_SAFETY.md) section 5 describes | A scheduled task can see the founder's other scheduled tasks, which Actions can't, and it needs no new API key or secret. Revisit when the rest of M3 moves agents into Actions |
| Briefings post as issues in `lab-desk`, never a public repo | They cover the founder's personal scheduled tasks as well as lab work |
