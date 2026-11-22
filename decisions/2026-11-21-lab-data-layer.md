# A shared lab data layer

Made Nov 21, 2026, in chat. Revisits the founding decision not to build shared cross-project data ([2026-11-03](2026-11-03-founding-decisions.md)). The new reason: DorkGraphs joined on Nov 5 with its own source registry and ingest, and the lab now pulls or plans to pull LDA, EIA, Census, SEC and CPI data in more than one project, with three snapshot formats and three ways of documenting sources.

| Decision | Reason |
| --- | --- |
| The lab gets a shared data layer: one source registry, shared ingest for sources more than one project uses, one snapshot format, and checked facts that projects reuse | Congress Cards would be built almost entirely from sources the lab already has. Separate copies drift: Denver credits FRED for CPI while the DorkGraphs rule credits BLS, and CMS data was pulled for DorkGraphs report r001 without being in its source library |
| Shared means the same no matter who uses it: sources, ingest, snapshots, provenance, checked facts. Judgment and voice stay in each project: AI readers, prompts, analysis, drafts, charts | Keeps the shared layer small and each project's method its own |
| The library is curated, not exhaustive: a source is added when a project needs it and retired when nothing reads it | Every source needs upkeep (endpoints move, licenses get re-checked, quirks need handling); unused sources go stale unnoticed |
| The source registry is `registry/sources.yaml` in lab-hq, built from DorkGraphs' source library plus the AI Money Report and Denver sources, and checked by `validate.py` | DorkGraphs' library was the most complete of the three. The registry already holds the lab's other single sources of truth |
| A project pulls only from a registered source and publishes it only where the record says `publish: true`. `confirm` and `not-cleared` licenses are never published | Extends DorkGraphs' existing rule lab-wide. Data cleared for internal analysis isn't always cleared for public work (the AI Money Report's market data is already internal-only) |
| One snapshot and provenance format for every project, written into RESEARCH_STANDARDS.md, merging DorkGraphs' manifest with the lab provenance record | Any published number can be traced the same way in any project |
| Bulk data stays off `main`: newest runs on a `snapshots` branch, older runs in monthly release assets | The AI Money Report's snapshots branch hit 253 MB in five days; Actions artifacts can't be read from Claude's workspace but a branch can |
| DorkGraphs moves its raw pulls from `main` to a `snapshots` branch before its Jan 11 launch | It had 18 MB of raw files on `main` after its first report |
| Projects add to the library as well as read from it: facts that pass a project's checks go in that project's `facts/` folder for others to reuse, with their label, credit and conditions intact; corrections are logged by fact id and checked by every project that reused the fact | Verified facts are the hardest part of the library to copy, and reuse can't strip the context that made them trustworthy |
| Shared ingest lives in a new public repo, `unclebuckslab/lab-data`, created when Congress Cards starts (milestone D3). Its FEC and Congress.gov vote pipelines are built there from day one, and the AI Money Report's lobbying pipeline moves in | Congress Cards is the first project that needs a source another project already pulls. Building there from the start avoids a later migration |
| Other sources move into `lab-data` only when a second project reads them; single-use sources stay in their project | Avoids shared plumbing nobody uses |
| Every shared pipeline keeps the AI Money Report's protections: fail-closed guards, a run log, the daily health check and the two-run quality comparison | Shared data that breaks breaks several projects at once |
| The weekly briefing adds a source-overlap check (`validate.py --report`) | The overlap went unnoticed for two weeks because nothing looked across projects |
| None of this sits on the critical path for P1 or DorkGraphs' launch | D1 and D2 are small enough to fit around both; D3 waits for Congress Cards |
| Annual Outings is outside the data layer | Its prices are app data, not published research |
| A shared entity table (people and company matching) is still not built | A separate question from shared sources; revisit when Congress Cards matches lobbying clients to members |
| Denver's FRED-to-BLS credit fix happens when the Denver repo moves into the lab org, not before | The repo is in the founder's personal account and its URL is under review |
| Later, not now: the checked-facts layer can be exposed as a tool any Claude session can query | Waits until two projects have used the facts layer |

## Open after this decision

- The founder rules on the proposed tiers in `registry/sources.yaml` (CMS, ECB, the three state WARN sources, PJM, private deals, Denver open data).
- License checks before anything from these is published: CMS (DorkGraphs r001), the ECB reference rates and the three WARN sources (AI Money Report issue 001).
