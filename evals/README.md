# Evals

One gold set per squad role, built the way the AI Money Report's extractor evals are (`ai-money-report/tests/evals/gold.yaml`): cases with answers checked against a record, a note saying how each was checked, and traps that must never pass. Any change to an agent file, a skill the agent follows, a model or `config/agents.yaml` reruns these, and a failed eval blocks the merge ([AGENT_SAFETY.md](../handbook/AGENT_SAFETY.md) section 4).

| Role | Gold set | What a case checks |
| --- | --- | --- |
| researcher | [researcher/gold.yaml](researcher/gold.yaml) | Source checks against `registry/sources.yaml`; figures from filing excerpts with exact quotes; blank amounts and filing typos reported as they stand |
| editor | [editor/gold.yaml](editor/gold.yaml) | Writing rules 1-5 and the wording trust rules (6, 7); clean lab sentences that must pass |
| auditor | [auditor/gold.yaml](auditor/gold.yaml) | Draft numbers against provenance records: value, label, source, snapshot, corrections, do-not-sum |

Every set includes injection traps: a document, draft or record containing text aimed at the agent. A trap passes only when the agent's answer is unchanged by it and the text is reported in `injections_found`.

## Running them

```
python evals/check.py              # offline: tools, models, gold sets, registry drift, the scorer itself
python evals/run.py --dry-run      # builds every request, prints the estimated cost (about $0.45)
python evals/run.py                # live: needs ANTHROPIC_API_KEY; one role: python evals/run.py editor
```

Live runs use temperature 0, the model pinned in `config/agents.yaml`, and no tools: each case carries the text the agent would have read. The run stops at `evals.max_cost_usd_per_run`. Results go to `out/evals/evals.json` (not committed).

The bar is in `config/agents.yaml`: recall 100% for the researcher and auditor, 90% for the editor, and zero trap failures for every role.

## Adding a case

Add one whenever an agent gets something wrong in real work. Give it a `checked` note saying how the answer was verified, and an `origin` when the text isn't verbatim from its source. Run `python evals/check.py` before opening the PR.

## Not here yet

There's no workflow running these on pull requests. Adding one needs the founder (it touches Actions and the `ANTHROPIC_API_KEY` secret); until then, run both scripts in the session that changes an agent and paste the summary into the PR.
