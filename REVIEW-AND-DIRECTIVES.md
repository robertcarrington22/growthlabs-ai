# GrowthLabs AI — External Review & Improvement Directives

**Reviewer:** Independent review (Claude), July 8, 2026
**Scope reviewed:** `research/strategy-optimization.md`, `research/strategy-deep-dive.md`, all 14 `marketing/` docs + outreach tracker, `ai-engine/` (code, README, sample report), `site/` (all routes, styles, config)
**Purpose:** Hand-off document for the business-building agents. Each section lists FINDINGS (what's wrong or at risk, with severity) and DIRECTIVES (what to change, with acceptance criteria).

**Overriding strategic decision from the owner: GrowthLabs AI targets the UNITED STATES market, not Europe.** Several existing assets were built for Europe and must be rebuilt. This decision supersedes the geography assumptions in the marketing docs and target account list.

---

## Executive Summary — the 5 issues that gate everything else

| # | Issue | Severity | Owner |
|---|-------|----------|-------|
| 1 | GTM assets (target list, budgets, copy, events, calendar) were built for **Europe**; business targets the **US**. ~1/3 of marketing package is unusable as-is. | CRITICAL | Marketing agent |
| 2 | Website and marketing publish **unearned results claims** ("3× ROI average," "Real Results from Real Clients," "15–30% average revenue gap identified") with zero clients. Credibility + FTC substantiation risk. | CRITICAL | Web + Marketing agents |
| 3 | **Product–promise gap:** the site sells "10–20 revenue opportunities ranked by impact with estimated ROI"; the engine's actual output is 47 unranked warnings with no dollar quantification. First paid audit will disappoint → retainer conversion (the whole business) fails at step 1. | CRITICAL | AI-engine agent |
| 4 | Target account list violates the stated ICP: Tier 1 includes 500+ employee, nine-figure-revenue companies (DEPT, Media.Monks, Remote, Personio, Pleo). These buy via procurement and will never take a low-cost audit. | HIGH | Marketing agent |
| 5 | **Mobile navigation does not exist** — nav links are `hidden md:flex` with no hamburger menu. Most LinkedIn traffic is mobile; those visitors see only a logo and one button. | HIGH | Web agent |

---

## Section 1 — Strategic Direction: US Market (owner decision)

All agents must treat the following as fixed:

- **Geography:** United States primary. Europe is out of scope for GTM until further notice.
- **Currency:** USD everywhere — site, blog, budgets, outreach, lead magnet, proposals.
- **Time zones:** Content calendar and posting schedule anchored to US Eastern Time (not CET).
- **Compliance frame:** US, not EU. GDPR is no longer the blocking concern; instead:
  - FTC advertising substantiation rules — no performance claims without evidence (see Section 3).
  - CCPA/CPRA exposure if handling California businesses' customer-level data — needs a privacy policy and a plain-English data-handling statement ("where does my data go, who sees it, how is it deleted").
- **What survives unchanged:** The market-sizing in `strategy-optimization.md` is already US-based (SBA data, ~33M US businesses, $3B–$8B TAM). The strategy layer is fine; only the execution layer was pointed at the wrong continent.
- **New service line (owner decision, July 2026):** expand to **small US retail enterprises with an inventory-management service**, built exclusively on classical, tried-and-trusted statistical methods. Full specification in Section 7.

---

## Section 2 — Business Model & Pricing

### Findings

1. **$100 audit price is self-defeating.** (HIGH) The research itself flags it ("may be too low to be taken seriously," recommends testing $197/$297) but the site shipped at $100. At $100: attracts tire-kickers, anchors the brand cheap, cannot fund any human fulfillment time. US benchmark (from your own research): one-time business assessments sell for $500–$3,000.
2. **"Custom" retainer pricing on the site contradicts the research.** (HIGH) `pricing.tsx` shows "Custom — quoted after your audit." The strategy doc correctly says SMBs have "very high" preference for transparent tiers (SaaS-trained buyers). Opaque pricing reads as "expensive consulting" — the category we're positioned against.
3. **Performance bonus is publicly promised but operationally impossible today.** (MEDIUM) No attribution/measurement framework exists. It occupies a third of the pricing page. Attribution disputes are a known killer of performance-fee arrangements.
4. **Data access is the unowned bottleneck.** (HIGH) The model requires an SMB owner to hand over 3 years of transaction data. The research rates this risk "High likelihood" — and then no document assigns any work to it.

### Directives

- **D2.1 — Reprice the ladder:**
  - Free tier: Revenue Health Scorecard (lead magnet, already planned).
  - Audit: **$495–$995** (test within this band), positioned as "credited in full toward your first retainer month."
  - Retainer: publish the tiers — **$1,000 / $2,000 / $3,500 per month** by company size ($500K–$2M / $2M–$5M / $5M–$10M). Add the research's own recommendation: consider a $4,500–$5,000 tier for the $7.5M–$10M range.
  - Acceptance: pricing page shows three concrete numbers; no "Custom"; audit price ≥ $495.
- **D2.2 — Remove the Performance Bonus from the public site.** Keep it as an opt-in clause in retainer proposals once a written attribution framework exists (baseline period, attribution window, monthly cap = 100% of base retainer, as the research recommends). Acceptance: no public page mentions a revenue-share percentage.
- **D2.3 — Own the data-access problem.** Deliverables, in priority order:
  1. A "white-glove data pull" offer: 20-minute screen-share where we do the QuickBooks/Stripe export with the client. Zero client homework. Script it.
  2. QuickBooks Online connector (dominant US SMB accounting platform — one integration covers most of the funnel). Stripe second. Xero third.
  3. A one-page data-security explainer for prospects (what we receive, who sees it, retention, deletion on request).
  - Acceptance: the audit onboarding flow requires ≤ 30 minutes of client effort, matching the marketing promise.

---

## Section 3 — Claims, Evidence & Trust (applies to website AND marketing copy)

### Findings

1. **Unearned claims are published or drafted:** "Real Results from Real Clients" (case-studies page headline), "3× ROI — average return on audit investment," "15–30% average revenue gap identified," "4–6 weeks to first measurable impact." The company has zero clients. This is a credibility problem with data-literate founder buyers and an FTC substantiation problem in US advertising. (CRITICAL)
2. **Research case studies are partly unverifiable.** The "aggregated case studies" tables (35% agency revenue increase, law firm +28%/+40%, "FSR Group" and "Togetr" value-pricing examples, the churn-intervention table) cite "industry reports" and Wikipedia. Some appear non-verifiable. (HIGH if published externally; fine as internal hypotheses)

### Directives

- **D3.1 — Strip every quantified results claim from the site and outbound copy** until real client data exists. Allowed reframings:
  - "What our methodology targets" (aspirational, clearly labeled)
  - HubSpot/Salesforce case studies presented as *industry* examples, clearly attributed, not as our results
  - The founding-client offer (see D4.3) as the honest substitute for social proof
  - Acceptance: grep of site + marketing copy finds no unattributed %-improvement or ROI claim presented as GrowthLabs' track record.
- **D3.2 — Quarantine unverifiable research citations.** Mark the aggregated case-study tables in both research docs as INTERNAL — HYPOTHESIS, NOT FOR PUBLICATION. Anything published externally must trace to a named, checkable source.

---

## Section 4 — Go-to-Market Rebuild for the US (the requested GTM asset spec)

### Findings

1. **Entire 50-account target list is European** (Amsterdam, Berlin, London, Paris, Munich, Copenhagen, Helsinki). Week-1 account research (DEPT, Honeypot, u+i, Media.Monks, Achtung!), the connection-request templates personalized to those accounts, and the pre-populated outreach tracker are all unusable under US targeting. (CRITICAL)
2. **The list also violates the ICP on size:** DEPT, Media.Monks, Remote, Personio, Pleo are 500+ employees / nine-figure revenue, rationalized as "has divisions in range." Divisions buy through procurement. (HIGH)
3. **Six channels on ~$4.5K/month is too diffuse** for (apparently) one marketer: LinkedIn organic + paid + SEO + email + events + partnerships targeting 20+ leads/month. Events alone consume 25% of budget for 3–5 speculative leads. (HIGH)
4. **The best idea in the research — fractional-CFO/bookkeeper partnerships — is buried at P3.** It solves trust AND data access simultaneously (the CFO already has the books and the client's permission). (HIGH)
5. **The founding-client motion is recommended in research but never operationalized** ("first 10–20 audits free/discounted for case studies" appears in no marketing doc, calendar, or LinkedIn post). (HIGH)
6. **Euro/CET artifacts throughout:** €4K budget table, blog post titled "…Costing Your Service Business €50K+/Year," calendar times in CET. (HIGH)

### Directives — asset-by-asset rebuild spec

**D4.1 — New US target account list (replaces `05-target-account-list.md`)**
- ICP (hard filters — reject any account failing one):
  - US-headquartered, 10–50 employees (stretch to 75 max)
  - Estimated revenue $500K–$10M
  - Service business: digital/marketing agencies, B2B consultancies, professional services (law, accounting, engineering boutiques), IT services/MSPs, niche B2B SaaS
  - Growth signal: hiring, new service lines, or multi-tier pricing visible
  - Reachable decision maker: founder/CEO/COO active on LinkedIn
- Sourcing (agents should use these, not memory): Clutch.co and Agency Spotter directories (filter by size + US city), LinkedIn Sales Navigator (company size 11–50, US, Business Services / Marketing / IT Services), Inc. 5000 lower ranks (#2000–#5000 skew small), local Business Journals "fastest growing" lists, MSP 501 list for IT services.
- Structure: keep the 3-tier format (20 / 15 / 15). For each Tier-1 account: company, HQ city/state, size estimate, revenue estimate + basis, named decision maker, LinkedIn URL, one personalization hook.
- Acceptance: 50 accounts, all passing hard filters; no company over 100 employees; every Tier-1 row has a named person.

**D4.2 — Redenominate and re-anchor (edits across marketing docs)**
- All € → $ (budget tables, blog post title and body, scorecard copy, email templates).
- All CET → ET; posting windows: Mon/Wed/Fri 8:30–10:00 AM ET (catches both coasts' mornings).
- Replace the European events/communities list in `06-marketing-channels-plan.md`:
  - Communities: MicroConf Connect, Indie Hackers, EO (Entrepreneurs' Organization) chapters, Vistage groups, Bureau of Digital (agency owners), Agency Management Institute, r/agency and r/msp where appropriate.
  - Events (only after case studies exist — see D4.4): MicroConf US, SaaStr Annual, Bureau of Digital events, local 1 Million Cups / chamber SMB events for cheap early reps.
- Acceptance: grep of `marketing/` finds no "€" and no CET/European-venue references.

**D4.3 — Founding-client offer (new asset, becomes the week-1 motion)**
- Offer: "We're taking **10 US founding clients**. Full Discovery Audit **free** (normally $495+), in exchange for: (1) a case study with real numbers, anonymized if preferred, and (2) a testimonial if you're happy with the work."
- Deliverables: one LinkedIn post (this replaces the drafted thought-leadership post as post #1), one landing-page section or dedicated page, one outreach email variant, tracker column for founding-cohort status.
- Rationale to preserve in the doc: with zero clients, honesty outperforms manufactured authority; the cohort manufactures the case studies every other channel needs.
- Acceptance: post drafted, page live, first 10 outreach messages reference the offer.

**D4.4 — Channel focus for the first 90 days (rewrite of `06-marketing-channels-plan.md`)**
- Run exactly TWO motions until 2–3 real case studies exist:
  1. **US fractional-CFO / bookkeeper partner channel** (promote from P3 to P1). Targets: independent fractional CFOs, small CPA/bookkeeping firms serving 10–50-person businesses, Paro/B2B CFO network members. Hook: white-label Revenue Health Scorecard they can give clients + 15–20% referral share on audit and first retainer months (already in the plan). Goal: 5 active partners in 60 days.
  2. **Founding-client outreach** (D4.3) via LinkedIn + email to the new US Tier-1 list, 10–20 personalized touches/week.
- Explicitly PAUSED until case studies exist: LinkedIn paid, SEO/content spend beyond 2 posts/month, all paid events. Reallocate that budget to nothing — bank it; the constraint is proof, not reach.
- Acceptance: plan shows two active channels, a parked list with re-activation triggers ("resume paid when ≥2 published case studies").

**D4.5 — Rework dependent assets for US voice**
- `08-linkedin-week1-posts.md`, `10-content-calendar-week1.md`, `11-connection-requests-tier1.md`, `09-account-research-week1.md`: regenerate against the new US account list and founding-client offer. US business idiom, USD figures, ET times.
- `03-sample-blog-post.md`: retitle/rewrite in USD (e.g., "$75K+/Year"), keep structure — the post itself is good.
- `outreach-tracker.csv`: reset and repopulate from the new Tier 1.
- Acceptance: no message references a European company; every template's personalization slot maps to a field in the new tracker.

---

## Section 5 — AI Engine / Product (the existential gap)

### Findings

1. **Promise vs. output mismatch.** (CRITICAL) Site + audit sales copy: "10–20 revenue opportunities ranked by impact, with estimated ROI for each fix." Actual `sample_report.json`: 48 findings = **47 "warnings" + 0 "opportunities"**, descriptive statistics only (RFM segments, AOV trends, cohort retention, seasonality), no dollar quantification, no ranking, no recommendations tied to $ impact.
2. Descriptive analytics ≠ growth plan. A founder paying $495–$995 expects "do X, it's worth ~$Y/year." The retainer conversion — the entire business model — depends on audit #1 impressing.
3. Minor: sample data's first months show a synthetic ramp-up artifact (Jan 2024: 22 transactions vs steady-state ~180), so "growth trends" in demo reports are partly generator artifacts. Fine for dev; do not show demo trend charts to prospects as if meaningful.

### Directives

- **D5.1 — Build the recommendation layer.** For each detection pattern, emit: (a) plain-English finding, (b) recommended action, (c) **estimated annual $ impact with the arithmetic shown**, (d) confidence level (low/med/high), (e) effort level. Rank the report by expected $ impact. The research docs already contain the pattern library to implement (symptom→root-cause table, the 4 causal loops, industry-specific audit questions in §7 of strategy-optimization and Part I of the deep-dive) — wire those frameworks into code.
- **D5.2 — Human-in-the-loop is acceptable v1.** If full automation is too slow, the engine outputs candidate findings and a human writes the quantified recommendation layer for the first ~10 audits (they're free founding-cohort audits anyway — see D4.3). Codify the format so it's automatable later.
- **D5.3 — Fix the finding taxonomy.** "47 warnings / 0 opportunities" is a classification bug in spirit: most of those warnings ARE opportunities. Re-map so the executive summary leads with opportunities and their combined $ value.
- Acceptance: a sample report on synthetic data contains ≥10 ranked opportunities, each with a $ estimate and shown arithmetic; executive summary states total identified opportunity value.

---

## Section 6 — Website

### Findings

1. **No mobile navigation.** (HIGH) `src/routes/__root.tsx`: nav links are `hidden md:flex`; there is no hamburger menu. Mobile visitors (most of LinkedIn traffic) see logo + "Get Started" only.
2. **Unearned claims** on case-studies page and stats blocks (see Section 3). (CRITICAL)
3. **Competing CTAs on the hero.** Button: "Get Your Discovery Audit" → links to `/services` (not even `/contact`); caption beneath: "No commitment. No credit card. Just a 30-minute chat." Three different offers (free chat / free scorecard / paid audit) compete on one screen. (MEDIUM)
4. **Nav is overloaded:** 9 items, including a Case Studies page with no case studies; Services and Pricing substantially duplicate. (MEDIUM)
5. **Emoji icons** (💰📉🎯📈) on the problem grid undercut the analytical-rigor positioning. (LOW)
6. Google Fonts loaded from external CDN — minor performance/privacy nit; consider self-hosting Inter. (LOW)

### Directives

- **D6.1 — Add a mobile menu** (hamburger → slide-down panel with all nav links). Acceptance: all routes reachable on a 375px viewport.
- **D6.2 — Claims cleanup per D3.1.** Case-studies page: either remove from nav or convert honestly into a "Founding Clients" page carrying the D4.3 offer.
- **D6.3 — One primary CTA per page.** Site-wide primary = **Revenue Health Scorecard** (it's the lead capture). The audit becomes the CTA on the scorecard results screen and the pricing page. Fix the hero button to point where its caption promises. Acceptance: each page has exactly one visually-primary CTA; hero copy and destination agree.
- **D6.4 — Trim nav to ~5:** How It Works, Pricing, Scorecard, Blog, Get Started. (About/Services content folds into Home/How It Works; Case Studies returns when one exists.)
- **D6.5 — Replace emoji icons with line SVGs** consistent with the existing indigo system.
- **D6.6 — Publish pricing per D2.1** (three concrete tiers, no "Custom").
- **D6.7 — Add privacy policy + data-handling page** per Section 1 compliance frame (CCPA-aware, plain English). Link it from the audit/data-upload flow.

---

## Section 7 — New Service Line: Retail Inventory Analysis (owner decision)

**Mandate:** Expand service to small retail enterprises to help manage inventory. Analysis must use **classical statistical methods that inventory managers have trusted for decades** (OR/APICS-CPIM standard) — no ML/experimental models in v1. The methods themselves are the credibility asset: position as "the statistics behind big-box replenishment, sized for independent retail."

### 7.1 Fit & target segment

Same audit → retainer model, same engine architecture (CSV in → $-quantified findings out); inventory is a **module**, not a second product. For physical-goods retailers, inventory is the largest controllable profit lever: stockouts = lost sales, overstock = trapped cash + carrying cost + markdowns. Enterprise tools (Blue Yonder, NetSuite, Relex) are out of reach for this segment; spreadsheet-plus-gut is the incumbent.

ICP addendum: US independent retailers (1–10 locations), e-commerce brands, hybrid brick+click; $500K–$10M revenue; ~100–10,000 active SKUs; on any exportable POS/commerce platform (Shopify, Square, Lightspeed, Clover, Amazon). Buyer = owner/GM. Pain signals: cash tied up in stock, recurring stockouts of best sellers, seasonal guessing, markdowns eating margin.

### 7.2 Directive D7.1 — Service packaging

- **Inventory Health Audit**: new SKU at **$495–$995** (same band as D2.1), credited toward retainer; standalone or bundled with the revenue Discovery Audit at ~1.5×.
- **Inventory retainer module** folded into existing Growth Retainer tiers: monthly refreshed forecasts, updated reorder points before purchasing cycles, seasonal pre-buy recommendations, dead-stock/markdown watchlist, KPI dashboard. This gives the retainer a concrete recurring deliverable for retail clients.

### 7.3 Directive D7.2 — The required statistical toolkit (implement these and only these in v1)

**(a) ABC analysis (Pareto).** Rank SKUs by annual revenue/margin contribution: A = top ~80% cumulative (~20% of SKUs, tight control), B = next 15%, C = final 5% (~50% of SKUs, rationalization candidates).

**(b) XYZ analysis (demand variability).** Per-SKU coefficient of variation `CV = σ_demand / μ_demand`: X < 0.5 stable, Y 0.5–1.0 variable/seasonal, Z > 1.0 erratic. **The ABC-XYZ 9-cell matrix drives policy** (AX = automated statistical replenishment; AZ = buffers + human judgment; CZ = discontinue candidates) and is a headline visual in the report.

**(c) Demand forecasting — exponential smoothing family**, selected per SKU by data pattern:
- Simple Exponential Smoothing `F_{t+1} = α·D_t + (1−α)·F_t` for level-only demand
- Holt's linear method for trend; **Holt-Winters (triple exponential smoothing, multiplicative seasonality)** for retail seasonality when ≥2 full seasonal cycles of history exist
- **Croston's method** for intermittent/slow-moving SKUs (many zero periods)
- Model selection on a holdout (last 20% of periods) by MAE/MAPE; fall back to SES on short history. Use `statsmodels` — do not hand-roll, do not use ML. Report per-SKU forecast error honestly; it feeds safety stock.

**(d) Safety stock (service-level based).**
- Demand variability only: `SS = z × σ_d × √L`
- With lead-time variability (when PO history exists): `SS = z × √(L·σ_d² + d̄²·σ_L²)`
- z from cycle service level: 90%→1.28, 95%→1.65, 98%→2.05, 99%→2.33. **Differentiate targets by class** (A: 97–99%, B: 92–95%, C: 85–90%) — uniform service levels waste capital; the differentiation is where much of the freed cash comes from.

**(e) Reorder point.** `ROP = d̄ × L + SS` on inventory position (on hand + on order − backorders). For weekly-ordering retailers use the periodic-review order-up-to level: `S = d̄ × (R + L) + z × σ_d × √(R + L)`.

**(f) EOQ (Wilson formula).** `EOQ = √(2DS / H)`; default holding cost H = **25% of unit cost/year** when the client has no figure (state the assumption). Round to case packs/MOQs; skip for Z-class items.

**(g) Newsvendor model** for single-period seasonal/perishable buys: critical ratio `CR = C_u / (C_u + C_o)` (C_u = lost margin per unit understocked, C_o = cost − salvage per unit overstocked); order `Q* = F⁻¹(CR)` using forecast mean + error std dev (normal approximation). This answers "how much holiday stock should I buy?"

**(h) Retail KPI scorecard:** inventory turns (COGS / avg inventory at cost), DSI (365/turns), **GMROI** (gross margin $ / avg inventory cost; benchmark ≥ $2.0–$3.2), sell-through rate, weeks of cover per SKU, stockout rate (% SKU-days at zero on-hand; estimate from sales gaps if snapshots missing, flagged as estimate), dead stock (no sales in 90/180 days, aged buckets, valued at cost).

**(i) Dollar quantification (extends D5.1):** every finding carries checkable arithmetic —
- Cash locked in dead/excess stock = Σ dead-SKU on-hand cost + (on-hand − target weeks of cover) × unit cost
- Carrying cost avoided = excess value × 25%/yr (stated assumption)
- Lost stockout revenue = stockout days × avg daily demand × price × 50% recovery factor (stated assumption)
- Markdown exposure = dead stock value × historical markdown depth
- Executive summary leads with: "$X cash freeable, $Y/yr recoverable revenue, $Z/yr avoidable carrying cost."

### 7.4 Directive D7.3 — Data ingestion (extends D2.3)

New CSV schemas for `data_ingestion.py`:
- `sales.csv` (line items): date, sku, quantity, unit_price, [unit_cost, order_id, location]
- `inventory.csv` (snapshots, weekly history ideal, single current snapshot acceptable v1): date, sku, on_hand, [location]
- `products.csv`: sku, product_name, category, unit_cost, unit_price, [supplier, case_pack, moq]
- `purchase_orders.csv` (optional; unlocks lead-time statistics): po_id, sku, order_date, received_date, quantity

Minimum viable dataset: 12 months of sales + current on-hand + unit costs. Degrade gracefully: no seasonal history → skip Holt-Winters; no PO history → client-stated lead times; no costs → unit-based report, flagged. The white-glove screen-share export applies; **a Shopify connector is the retail equivalent of the QuickBooks connector** and shares its priority.

### 7.5 Directive D7.4 — Engine module & report

```
ai-engine/analysis/
  inventory_classification.py   # ABC, XYZ, ABC-XYZ matrix
  inventory_forecasting.py      # SES/Holt/Holt-Winters/Croston, per-SKU selection, error metrics
  inventory_policy.py           # safety stock, ROP, order-up-to, EOQ, newsvendor
  inventory_kpis.py             # turns, DSI, GMROI, sell-through, weeks of cover, stockouts, dead stock
```
Plus schema extensions, a synthetic retail dataset in `sample_data_generator.py` (seasonal + trend + intermittent SKUs so every code path is exercised), report section, API upload support.

Client-facing report, in order: (1) executive summary with the three headline $ figures; (2) KPI scorecard vs benchmark; (3) ABC-XYZ matrix with $ per cell; (4) top-20 action table (SKU, issue, action, $ impact, confidence); (5) reorder policy sheet for all A/B items — doubles as the retainer's living deliverable; (6) seasonal pre-buy (newsvendor) recommendations; (7) methodology appendix naming the methods in plain English — show the methods, they ARE the trust signal.

**Acceptance:** synthetic run yields ≥10 ranked $-quantified inventory findings with shown arithmetic; every SKU forecast logs holdout error; all assumptions (carrying rate, recovery factor, service targets) surfaced and overridable; classical `statsmodels` methods only, zero ML.

### 7.6 Directive D7.5 — GTM additions for retail

- Website: retail/inventory service page + retail block on Home; claims discipline (D3.1) applies — the methodology framing is the trust asset, not invented results.
- Lead magnet: "Retail Inventory Health Scorecard" variant (10 questions: turns, GMROI, dead-stock %, stockout frequency; same scoring pattern).
- Target list: extend the US Tier-1 rebuild (D4.1) with 10–15 retail accounts ($1M–$10M independent/e-commerce), sourced from Shopify/Square case directories and local Business Journal retail lists.
- Partner channel (extends D4.4): fractional CFOs see the trapped-cash problem on every retail balance sheet; add POS resellers/consultants (Lightspeed/Square partners) and retail-specialist bookkeepers.
- Founding cohort (D4.3): reserve 3–5 of the 10 slots for retailers so the inventory module gets real case studies.
- Content: "How much cash is trapped in your stockroom? (a GMROI walkthrough)" and "The safety-stock formula that ends both stockouts and overstock."

### 7.7 Risks & honesty notes

- **Data quality is the #1 failure mode** (shrinkage, untracked receipts, missing costs). Include a data-quality gate that reports what couldn't be computed and why — never silently produce garbage numbers.
- EOQ/newsvendor assumptions must be stated; recommendations must round to MOQ/case-pack reality.
- Don't market it as "AI inventory optimization" — classical statistics is the mandate and the more credible pitch to this buyer.
- Stockout-loss estimates are inherently soft (unobserved demand); always label the recovery-factor assumption.

---

## Section 8 — What's already good (keep, don't regress)

- The **Revenue Health Maturity Model, 4 causal loops, and symptom→root-cause diagnostic** are genuinely strong IP — both as the audit engine's brain and as content-marketing raw material. Keep them central.
- The **audit → retainer land-and-expand structure** is correct; only its price points and public presentation need work.
- The **white-label scorecard for partners** is an excellent hook — build it.
- The **website's visual system** (indigo palette, typography, layout discipline) is clean and consistent; the fixes above are surgical, not a redesign.
- The **US market sizing** in the research ($3B–$8B TAM, SAM/SOM logic) already supports the US decision — no rework needed there.

## Section 9 — Expanded Value Proposition & Approachability (owner decision, July 2026)

**Mandate:** Broaden the value proposition beyond "find revenue leaks," and make the site and mission approachable enough that a non-technical owner feels this was built for them.

### 9.1 The expanded value proposition — three pillars

GrowthLabs AI is no longer positioned as "an AI revenue audit." It is **the growth team small businesses don't have**. Three promises, in owner language:

1. **Make more money** — pricing, customer retention, upsells, and marketing that actually pays. (The revenue audit.)
2. **Free up cash** — for retailers and product businesses: cash trapped in slow stock, stockouts on best sellers, smarter ordering. (The inventory audit.)
3. **Know what to do next** — a short, plain-English list of what to fix first, refreshed monthly, with progress you can see. (Maturity model, scorecards, retainer dashboards — clarity as a product, not just findings.)

Rationale: owners don't wake up wanting "revenue analysis." They want to stop guessing. Pillar 3 is the emotional core; pillars 1–2 are the proof. All copy, decks, and outreach should ladder up to these three.

### 9.2 Directive D9.1 — Voice & approachability guide (applies to ALL public copy)

- Write to one owner, as "you." Founder-to-founder, warm, direct.
- **Lead with their questions, not our methods.** "Am I charging enough?" beats "pricing optimization."
- Banned on public pages: "revenue intelligence," "leakage," "optimization levers," "actionable insights," "synergy," and "AI-powered" as a badge or headline. AI is the how, mentioned in supporting copy — never the promise.
- Always state the cost in the owner's scarcest currency: **their time** ("about 30 minutes of yours, total").
- Every page answers within one scroll: who this is for, what they get, what it costs, what to click.
- Reduce perceived risk everywhere: free scorecard first, transparent prices, "no data science degree required," audit credited toward retainer.
- Mission statement (About page, decks): **"Every small business deserves the clarity big companies take for granted."**

### 9.3 Directive D9.2 — Site changes implementing the above

- Homepage hero: owner-outcome headline ("Know exactly what to fix next in your business"), scorecard as primary CTA with friction-reducers beneath.
- Problem section: reframe as the five questions owners actually ask (pricing, churn, marketing ROI, upsells, **inventory cash**) — inventory now appears on the homepage.
- Services section: three cards — Revenue Discovery Audit, Inventory Health Audit, Growth Retainer.
- Add a "who we help" section linking the existing industry pages (agencies, SaaS, retail/e-commerce, local services, manufacturing).
- About page: mission-led rewrite; REMOVE the "Performance-Aligned Pricing" card (violates D2.2 — the bonus is off the public site) and replace emoji icons with line SVGs (D6.5 applied only to Home).
- Meta title/description updated to the broader promise.
- Acceptance: no banned vocabulary on any public page; homepage mentions all three pillars; About contains the mission statement verbatim.

## Priority order (single merged list)

| Priority | Task | Directive |
|---|---|---|
| 1 | Mobile nav + strip unearned claims | D6.1, D6.2, D3.1 |
| 2 | Redenominate all assets to USD / ET | D4.2 |
| 3 | Pricing page rewrite (tiers, audit ≥$495, bonus removed) | D2.1, D2.2, D6.6 |
| 4 | Founding-client offer drafted + live | D4.3 |
| 5 | US target account list rebuilt | D4.1 |
| 6 | Fractional-CFO partner channel launched | D4.4 |
| 7 | Engine recommendation layer ($-quantified, ranked) | D5.1–D5.3 |
| 8 | **Inventory engine module** (classification, forecasting, policy, KPIs — build on the D5.1 skeleton) | D7.2–D7.4 |
| 9 | Data-access flow (white-glove script; QuickBooks + Shopify connectors) | D2.3, D7.3 |
| 10 | Rework LinkedIn/email/calendar assets for US (incl. retail accounts + retail founding-cohort slots) | D4.5, D7.5 |
| 11 | Retail service page, inventory scorecard variant, retail content posts | D7.5 |
| 12 | Privacy/data-handling page | D6.7 |

*End of review.*
