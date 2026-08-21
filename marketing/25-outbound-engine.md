# The Outbound Engine — Operating Manual

**Date:** Aug 19, 2026 · This is the standing GTM workflow. The dashboard (Mission Control) shows its live state; this file is how it runs.

## The pipeline (stage definitions)

```
SOURCED → VERIFIED → DRAFTED → SENT → REPLIED → CALL BOOKED → FOUNDING COHORT / CLIENT
```

| Stage | Meaning | Exit criteria |
|---|---|---|
| Sourced | Agent found the company from a public source | Passes ICP hard filters on paper |
| Verified | Company + decision maker + size confirmed with source URLs | Real person, real trigger where possible |
| Drafted | Personalized email/DM written, keyed to the trigger event | Robert has reviewed the draft |
| Sent | Robert sent it (email or manual LinkedIn DM) | Logged in tracker with date |
| Replied | Any response | Categorized: interested / not now / no |
| Call booked | Discovery call scheduled | On calendar |
| Cohort/Client | Founding-cohort slot or paid audit | Data pull scheduled |

**Single source of truth:** `marketing/outreach-tracker.csv`. Every send, reply, and stage change gets logged there same-day.

## The weekly cycle

| Day | Motion |
|---|---|
| Monday | Claude runs sourcing agents (10–15 new leads/segment) → verification → tracker |
| Tuesday | Claude drafts trigger-keyed emails for new verified leads → Robert reviews |
| Wed–Thu | **Robert sends** (10–20 personalized emails + up to 5 LinkedIn connection requests/day) |
| Friday | Follow-up pass (Day-4 bumps due), log replies, pipeline review, refresh dashboard |

Volume discipline: quality beats volume at this stage. 15 truly personalized sends/week outperform 100 template blasts — and protect sender reputation.

## Rules of the road (non-negotiable)

1. **No LinkedIn scraping or automation.** All LinkedIn actions (connects, DMs) are manual, by Robert, ≤5 connects/day. Sourcing is public-web only (directories, trade press, award lists, podcasts, company sites).
2. **No invented facts.** Every lead's contact and trigger has a source URL from the sourcing agent. If we can't verify, we don't send.
3. **CAN-SPAM for email:** accurate from-name/subject · a real physical mailing address in the footer · a working opt-out line ("reply 'no thanks' and I won't email again — honored immediately") · honor opt-outs forever.
4. **Send from a real mailbox, warmly.** ≤20 cold emails/day from the business mailbox. No bulk tooling until a domain + proper sending infrastructure (post-rename).
5. Never email an address that isn't publicly listed or clearly the business's contact channel. Contact-form-only companies get the contact form or LinkedIn.

## Trigger-event email system

Every first-touch email = **Trigger opener (1–2 lines) → Bridge (1 line) → Offer (2–3 lines) → Micro-CTA (1 line) → compliance footer.** Under 120 words. One link max. Subject lines: 2–6 words, lowercase-casual, reference the trigger not the pitch.

> **Note (rename pending):** templates say `{BRAND}` and `{SITE}`. Until the rebrand lands, that's "GrowthLabs AI" and growthlabs-ai.vercel.app; Claude swaps all drafts automatically at rename.

### T1 — Award / "Best of" list inclusion
**Subject:** `congrats on [award]`
> Hi [First] — saw [Company] made [list/award] ([month]). Congrats — [one specific detail from the story].
>
> Wins like that usually mean the work is dialed in. The numbers side is usually the part nobody's had time to look at — what to charge, which clients are quietly drifting, where the margin leaks.
>
> I run {BRAND}: we analyze the sales history you already have and hand you a short, plain-English list of what's worth fixing, ranked by dollar impact. We're taking 10 founding clients right now — full audit free, in exchange for an honest case study.
>
> Worth 15 minutes? {SITE}
>
> — Robert · [mailing address] · Reply "no thanks" and I won't email again.

### T2 — Podcast appearance / published content
**Subject:** `your [podcast] episode`
> Hi [First] — listened to your [podcast] conversation about [specific topic]. The point about [specific thing they said] stuck with me.
>
> It connects to what I do: [one-line bridge from their topic to revenue/pricing/retention analysis].
>
> {BRAND} turns a business's own sales history into a ranked what-to-fix-first list — arithmetic shown, no dashboards to learn. First 10 founding clients get the full audit free (case study in return).
>
> If knowing your own numbers that precisely sounds useful, it's a 30-minute lift on your side: {SITE}

### T3 — Expansion / new location / new hire
**Subject:** `the new [location/hire]`
> Hi [First] — saw [Company] is [opening X / brought on Y] ([source, month]). Growth mode is exactly when the numbers questions get expensive: what to charge the next tier of clients, which offerings actually carry margin, [for retail: how much stock the new location really needs].
>
> {BRAND} answers those from the sales history you already have — a ranked, plain-English fix list with the dollar impact of each move. Founding-client program: 10 businesses, full audit free, honest case study in return.
>
> 15 minutes to see if it fits? {SITE}

### T4 — Anniversary / longevity
**Subject:** `[N] years of [Company]`
> Hi [First] — [N] years in is genuinely rare in [industry]. Congrats.
>
> It also means you're sitting on [N] years of sales history — which almost certainly contains answers nobody's ever extracted: where you're underpriced, which customers quietly drift, what your best buyers would happily add.
>
> That extraction is literally what {BRAND} does. Plain-English report, ranked by dollar impact, ~30 minutes of your time total. We're giving the full audit free to 10 founding clients (case study in return).
>
> Curious what [N] years of your data says? {SITE}

### T5 — Retail: new location / season prep (inventory angle)
**Subject:** `stock planning for [location/season]`
> Hi [First] — saw [trigger: second location / holiday buying season / feature]. The hardest part of [trigger] is inventory math: how much cash to tie up, which lines earn their shelf space, what to reorder and when.
>
> {BRAND} runs the same statistical methods big-box replenishment teams use — sized for independent retail. Output: the cash trapped in slow stock, the best sellers you keep running out of, and exact reorder points. 5 of our 10 free founding-client audits are reserved for retailers.
>
> Worth a look before [season/opening]? {SITE}

### Follow-up cadence (all templates)
- **Day 4 — bump:** "Floating this up — one detail I didn't mention: [one new specific fact/benefit]. If it's a no, a one-word reply saves us both time."
- **Day 10 — breakup:** "Closing the loop — founding slots are going to [N remaining]. If the timing's wrong, no hard feelings; the free scorecard is there whenever: {SITE}/scorecard. I won't email again either way."
- Then stop. Two follow-ups max, forever.

## Upgrades available when Robert wants them

- **Licensed data providers** (Apollo, Clay, ZoomInfo connectors are installed but need authorization — claude.ai connector settings). These add lawful verified emails + org data at scale. The public-web engine works without them; they 10x the throughput.
- **Gmail drafts:** Claude can pre-load every drafted email into Gmail as drafts for one-click review-and-send (never auto-sent).
- **Post-rename:** dedicated sending domain + address before volume goes above ~20/day.

## KPI targets (engine health)

| Metric | Target |
|---|---|
| New verified leads/week | 20+ |
| Trigger-event coverage | ≥60% of drafted emails |
| Reply rate (personalized cold email) | ≥8% |
| Positive-reply → call rate | ≥50% |
| Founding cohort filled | 10 by end of month 1 |
