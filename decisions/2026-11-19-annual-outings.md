# Annual Outings joins the lab

Made Nov 19, 2026, in chat.

| Decision | Reason |
| --- | --- |
| Annual Outings is a lab project and the lab's first product: something people sign up for and use, not something they read | It shows the lab builds working things, not just content about AI |
| It is free to users. The Ringleader's $30 fee, Stripe and the price tests are cut | The founder wants friends using it and giving feedback first. Money comes later without charging users |
| Friends' crews go first, and their feedback shapes the next version | A small group of real users teaches more than a pricing test |
| The build is documented as content, and what works is packaged into Kits and blueprints | People pay for how it's built, not for using the app. This follows the lab's revenue model |
| It runs on its own timeline, separate from the lab launch (L1), but a real V1 ships soon | The launch's 36 hours stay protected without parking the product |
| Reader and user data is never sold or shared ([MONEY_RULES.md](../handbook/MONEY_RULES.md) rule 5 applies) | Any later money must come from somewhere other than users' data |

## Still open

- Which other ways of making money are allowed later, such as disclosed referral links or sponsorships, and which are ruled out. Decide before the first real users, because it shapes what data the app collects.
- Nothing else for V1. The Nov 19 Decision Brief is superseded by the V1 decisions below.

## V1 decisions, Nov 19

From the [V1 Plan](https://claude.ai/artifact/H7CgPgaF5gsSNC7f3aSg29). Every one was decided as recommended.

| # | Decision |
| --- | --- |
| Scope | V1 is the Build Plan's R0 and R1, live Mon Dec 14 for two friend crews; R2, experiments, pricing and strangers wait |
| A2 | Cloudflare Worker, Hono, D1, plain SQL |
| A3 | Private answers not encrypted in V1; private fields stay off admin and backups get their own token. Encrypt before strangers |
| A5 | Email sends from a subdomain of unclebuckslab.com |
| A7 | Four profile questions, plus a private kids question only if a crew has parents |
| A8 | No health details anywhere in V1 |
| A11 | Prototype design calls approved as a batch |
| A12 | Single-use claim links; the planner never holds a member's link |
| B1 | Planner sees who hasn't answered, never what they answered |
| B2 | Members see "fits everyone / doesn't" plus their own private line; counts go to the planner at 4+ budgets |
| B3 | Early lock only when everyone has answered; no lock if over half say Can't; shares round up to the dollar |
| B4, B8, B10, B12, B15, B16 | Quiet hours 9 PM to 9 AM; leaning line daily at 4+ answers; open-in-browser card; "Suggested text"; trimmed copy; rate once joined |
| B5 | Members can mute all reminders except the deadline-day email while they owe an answer |
| B6 | Cloudflare Access with MFA on /admin from the first release |
| B7 | The founder approves each production deploy; freezes around pilot deadlines; maintenance mode pre-approved for a serious outage |
| C3 | AI rules deferred until AI features start |
| C6 | Data deletion and export by request in V1; self-serve before strangers |
