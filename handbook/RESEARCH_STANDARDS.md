# Research standards

Research quality is what the lab is known for, or nothing is. These standards apply to every project that publishes a claim.

## Before the research

Every significant piece of research writes these down first, in the project repo:

- The question, and what answer would change a decision.
- The method, the sources and why those sources.
- Definitions and assumptions, especially for numbers that sound similar but aren't.
- Known limits of the data.

## Sources

1. **Primary sources first.** A filing, a law, a dataset, an official record. News coverage is a lead, not a source.
2. **Registered sources only.** A project pulls only from a source in [registry/sources.yaml](../registry/sources.yaml), and publishes it only where that record says `publish: true`. A new source gets a record, with a proposed tier, before its first pull.
3. **Record the retrieval.** Every source has a link and a retrieval date.
4. **Archive what might change.** Every pull is saved as a snapshot (below).
5. **Never fabricate a citation.** If a source can't be found, the claim doesn't run.

## Snapshots

Every pull is saved, never overwritten, so any published number can be rebuilt from the exact bytes it came from.

**Where they live.** Bulk data never goes on `main`. The repo that owns the pipeline keeps its newest runs on a `snapshots` branch, laid out as `<dataset>/<stamp>/`, where the stamp is the UTC date (`2026-11-15`) or, for sources pulled more than once a day, the UTC time (`2026-10-31T0000Z`). When the branch passes about 100 MB, older runs move to monthly `history-YYYY-MM` release assets and the branch is rewritten. A branch, unlike Actions artifacts, can be read from Claude's workspace.

**The manifest.** Each snapshot folder holds a `manifest.json`:

```json
{
  "source": "cbo",
  "dataset": "cbo-health-2026-07",
  "retrieved_utc": "2026-11-16T03:02:48+00:00",
  "pipeline": {"repo": "unclebuckslab/dorkgraphs", "path": "pipeline/ingest/fetch_sources.py", "commit": "99580b2"},
  "route": "archive",
  "files": [
    {"file": "62539-Health-Insurance.pdf",
     "url": "https://www.cbo.gov/system/files/2026-07/62539-Health-Insurance.pdf",
     "fetched_url": "https://web.archive.org/web/2026id_/https://www.cbo.gov/system/files/2026-07/62539-Health-Insurance.pdf",
     "sha256": "ef8b1557…",
     "bytes": 1409132}
  ],
  "checks": {"passed": true, "notes": []}
}
```

- `source` is the record id in `registry/sources.yaml`; `dataset` names what was pulled.
- `route` is `publisher` or `archive`. An archive route records both the publisher's URL (`url`, which gets the credit) and the URL actually fetched (`fetched_url`).
- `checks` records the pipeline's guards. A pull that fails them isn't saved as a snapshot.
- Personal data is scrubbed before anything is written (names reduced to flags), as each source's conditions require.

**Pinning.** Analysis reads a named snapshot, never a live fetch: a provenance record points at the repo, dataset, stamp, file and checksum. Pipelines that come before this format (the AI Money Report's run profiles) keep their own manifest until they next change, then adopt it.

**Shared sources.** A source used by more than one project is pulled once, in `unclebuckslab/lab-data`, and every project reads that repo's snapshots ([decision](../decisions/2026-11-21-lab-data-layer.md)). A source only one project uses stays in that project's repo.

## The provenance record

Every published number or fact has a record in the project's data, in this shape:

```yaml
fact_id: example-corp-capex-12m-2026q3
claim: "Example Corp spent $2.4B on buildings and equipment in the 12 months to September"
value: 2400000000
unit: USD
as_of: 2026-09-30
source: sec-edgar        # id in registry/sources.yaml
source_url: https://www.sec.gov/Archives/edgar/data/<cik>/<filing>.htm
source_title: Example Corp Form 10-Q, quarter ended Sep 30
retrieved: 2026-11-03
snapshot:
  repo: unclebuckslab/ai-money-report
  dataset: financials
  stamp: 2026-11-03T2032Z
  file: quarterly.jsonl
  sha256: "<checksum from the manifest>"
method: Sum of the last four quarters of PaymentsToAcquirePropertyPlantAndEquipment
label: fact              # fact | stated | estimate | our-read
```

A draft's numbers are checked against these records before review. A number with no record doesn't ship.

## Checked facts

A provenance record that has passed its project's checks becomes a checked fact that other projects can reuse without redoing the work. The AI Money Report's verified footnote commitments, for example, can go into a DorkGraphs chart as they are.

- **Where they live.** Each project keeps its checked facts in `facts/` on `main`, one JSONL file per issue, report or finding (`facts/issue-002.jsonl`). They're small text and belong with the work.
- **What gets added.** The provenance record above, plus three fields: `project` (registry id), `checked` (how it was verified: `code`, `quote-match`, `human` or a list of them) and `checked_on` (date).
- **Reuse.** A project that reuses a fact cites it as `{project, fact_id, commit}` and keeps its label (fact, stated, estimate, our read) and its source's credit and conditions. It never rewords a stated figure as a fact.
- **Corrections travel.** A correction to a checked fact is logged in the owning project's corrections log by `fact_id`. A project's pre-publish check confirms that no fact it reuses has a later correction.
- **No new facts by reuse.** Combining checked facts into a new number (a sum, a ratio) creates a new estimate with its own record and method. Totals that the owning project marks as overlapping are never added together.

## Labels

Keep these apart in the data and in the writing:

- **Fact:** what the document shows.
- **Stated:** what a company or official says, in their own words.
- **Estimate:** a number the lab calculated or modeled, with its method.
- **Our read:** the lab's interpretation, clearly marked.

For money, also keep apart: announced, committed, actually spent and forecast. They are different numbers and are never summed together.

For political and financial research, keep different kinds of activity in separate categories rather than combining them into one misleading total.

## Checking

- Material claims are verified independently of the person or agent that found them.
- Claims the lab expects to be true get checked hardest.
- Important analyses are reproducible from the repo: the code, the pinned snapshots and the steps.
- Uncertainty is stated next to the claim it affects, not in a footnote nobody reads.
