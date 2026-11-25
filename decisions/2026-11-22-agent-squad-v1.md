# Agent squad v1

Proposed Nov 22, 2026, in the milestone M3 pull request. These decisions take effect when the founder merges it.

| Decision | Reason |
| --- | --- |
| The squad starts with three subagents: researcher, editor and auditor, in `.claude/agents/` | The researcher reads, the editor checks wording, the auditor checks numbers. RESEARCH_STANDARDS asks for claims to be verified independently of whoever found them, so the auditor is a separate role from the researcher |
| All three are read-only. The researcher holds Read, Grep, Glob, WebFetch and WebSearch; the editor and auditor hold Read, Grep and Glob. No role holds Write, Edit, Bash, agent spawning or any connector | Writing and acting stay with the founder-directed main session, which sees only validated output. A hijacked reader can't change a file, run a command or post anything |
| In Claude Code, "readers have no tools" (AGENT_SAFETY section 1) means no tools that write, run commands or send anything. The researcher keeps read and fetch tools | A researcher with no tools would need the main session to fetch pages for it, which puts untrusted text in front of the agent that can act. Keeping the fetching inside the read-only researcher is the stricter boundary |
| Every role's output is one JSON object checked by `scripts/agent_output.py` against a schema defined there. Invalid output is discarded, never repaired. Every role reports instructions it found in data in `injections_found` | AGENT_SAFETY section 1 |
| Models, tools and budgets live in `config/agents.yaml`; `evals/check.py` fails when an agent file drifts from it | AGENT_SAFETY section 3: one config file, so a model switch is a config change plus an eval run |
| Budgets in interactive sessions are instructions in the agent file and the skill; hard limits apply in eval runs (a cost cap) and will apply in headless runs | Claude Code doesn't enforce a per-subagent token or cost cap today. The Anthropic Console's monthly limit is the backstop |
| Each role has a gold set of at least 10 cases with at least two injection traps in `evals/<role>/gold.yaml`, scored by `evals/run.py` at temperature 0. Bars: recall 100% for researcher and auditor, 90% for the editor, zero trap failures for all | Modeled on the AI Money Report's extractor evals. Judging prose is less exact than reading a number |
| Three skills: `research-brief`, `pre-publish` and `new-project` | `pre-publish` is the check WRITING_RULES.md promises from M3; `new-project` is the one templates/README.md promises; `research-brief` is how the researcher gets dispatched safely |
| The automated half of the writing check is `scripts/writing_check.py`, a phrase list from WRITING_RULES.md; the editor is the model judge | WRITING_RULES.md, "How the check runs" |
| No eval workflow, schedule or secret in this milestone step. Evals run in the session that changes an agent until the founder adds the workflow | The founder asked for no schedules, secrets or Actions changes in this build |
| Agent files are treated as permission files: the founder merges changes to their `tools:` lines himself, not through a merge instruction in chat | The [Nov 9 merge decision](2026-11-09-merge-on-founder-say.md) keeps permission changes with the founder, and a tool list is a permission |

## Open after this decision

- The rest of M3: the scheduled headless briefing and ops check in Actions, and the away runbook.
- An eval workflow on pull requests, with the `ANTHROPIC_API_KEY` secret.
- How project repos reach these agents and skills. They load only in sessions where lab-hq is the working repo; options are copying them through the template, or packaging them as a plugin.
- Whether `ops` (listed for two projects in `registry/projects.yaml`) becomes a fourth role, and whether `auditor` is added to each publishing project's `agents` list.

**Amended Nov 24, 2026:** the "temperature 0" in the gold-set row no longer applies. The first live eval run failed because current models and the pinned `anthropic` library don't accept a temperature setting (the AI Money Report already runs without one). Evals now run on the pinned model with no sampling setting.
