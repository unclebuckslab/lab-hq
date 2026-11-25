# Site build: hosting, design, lists and privacy

Made Nov 21, 2026, after the site audit and the research in lab-desk `audit/2026-11-20/`.

| Decision | Reason |
| --- | --- |
| The full name is **Uncle Buck's Laboratory**; **unclebuckslab** is the short form. "Uncle Buck's Research Club" in the Nov 20 build brief is superseded | Garrett, Nov 20 |
| The audit's unified build plan is the M2 plan | One plan, not two |
| The site runs on **Cloudflare Workers static assets**, not Pages. Workers Builds deploys merges to `main` and posts a preview link on every PR. Changes part of `2026-11-10-site-and-newsletters.md` | Already deployed there; Annual Outings uses the same platform (its ADR-001); static output keeps moving hosts a DNS change |
| Connect GitHub to Workers Builds and attach `unclebuckslab.com` (with `www` redirecting to it) **before launch**, with the whole site `noindex` until launch | Previews and real URLs now; search engines later |
| PR previews sit **behind Cloudflare Access** | Only Garrett can open them; never indexed |
| No deploy token for agents. Cloudflare holds the build token | Least privilege |
| Lab standard is **WCAG 2.2 AA** | Small step from 2.1; Annual Outings already targets it |
| **Two design layers.** The umbrella brand has its own system for the lab's own surfaces and one presentation pattern per kind of work. Product and brand systems (DorkGraphs, AI Money Report, Annual Outings, Denver) stay in their repos, and the umbrella never restyles their output | The lab houses independently branded work |
| The umbrella look is **Workshop + Fog** (light and dark): Fraunces, IBM Plex Sans and Mono, hard rules, kind-of-work labels, overcast-gray ground, fir, slate, moss, madrona-rust accent. Evergreen is dropped. No contour lines, ridgelines or regional icons | Garrett's pick; Pacific Northwest research, Nov 21 |
| The umbrella design system's source of truth is `lab-hq/design/` (DTCG tokens). Until that exists, lab-site holds the tokens and the lab-hq owner copies them over. A Design System artifact may mirror it, never lead it | One source of truth |
| **Before launch, the lab's launch projects show on the site** (AI Money Report, Congress Cards, Annual Outings, DorkGraphs), labeled **In the lab**, next to live work (Denver). This sets aside the Nov 11 finished-work rule until the launch review | Garrett, Nov 21: these are the building-block projects of the lab's launch |
| A **Thoughts** section (between Work and About) holds Garrett's writing as Markdown posts; drafts show only on previews | Garrett, Nov 21 |
| No Subscribe button in the header. The rust accent appears only on the signup button at the bottom of the page | Garrett, Nov 21 |
| **One newsletter list at launch** (the lab dispatch) on beehiiv's free plan. The site's own form posts to a small Worker that calls beehiiv's API: no beehiiv script on the site. The AI Money Report list starts when beehiiv is upgraded | No external scripts; $0 until there's a reason to pay |
| **Move private registry fields** (`notes`, `agents`, private repo names) out of public lab-hq into lab-desk; lab-hq's registry keeps public fields only | lab-hq is public, so those fields are public today |
| **Signups are built but off until the first report is ready.** The beehiiv form works only on PR previews, where test signups are tagged `utm_source: preview`; the live site shows it disabled and the Worker refuses signups on the live domain. Going live flips `SIGNUPS_LAUNCHED` (lab-site `src/lib/env.ts`) and `SIGNUPS_OPEN` (`wrangler.jsonc`) in one PR, and the preview test subscribers are deleted | Garrett, Nov 21: "I don't want it to be live yet since the report isn't ready." Tested end to end on a preview the same day |
| beehiiv keys live only as Cloudflare secrets, set by Garrett for Production and the Previews base, never in chat or code. A preview copies the base secrets only when it is first created | Least privilege; found while testing |
| Site launch follows lab-site `LAUNCH.md`: voice copy, Privacy and Disclosures reviewed, first Thoughts post, then one PR that switches signups on and removes noindex | One checklist, one switch-on PR |
| Link-preview images are drawn from the registry and tokens (`npm run og`) and committed; the site ships a sitemap and an RSS feed for Thoughts | No external services; works with the static build |

## Open

- Move private registry fields (`notes`, `agents`, private repo names) out of public lab-hq into lab-desk. Not done yet.
- `lab-hq/design/` tokens: lab-site still holds them.

Committed Nov 24, 2026, from lab-desk `audit/2026-11-20/` (merged as lab-desk #3), as approved in chat on Nov 21.
