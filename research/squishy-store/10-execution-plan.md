# Execution Plan: A Squishy Store Claude Code Can Build, Run and Make Profitable

Status: proposal, 20 Sept 2026. Numbers reference `04-unit-economics-and-supply-chain.md` and `unit_economics.py`.

## 0. Strategy in one paragraph

Launch a **kidult-leaning, safety-first curated squishy brand** (working positioning: "calm desk squishies for grown-ups and the kids who steal them"), selling **$25–40 curated bundles and mystery bags** rather than singles. Q4 2026 runs on **authorised US wholesale stock** (products that already carry a Children's Product Certificate), which removes lab-testing cost and import risk and gets the store live in weeks. Acquisition is **organic TikTok + TikTok Shop affiliates + email**, not Meta prospecting. If Q4 hits the gates below, 2027 moves to **own-brand imported taba-style capybara/food squishies plus a personalized pet-face line**, where contribution margin exceeds 50%.

## 1. Division of labour

Claude Code can build and operate almost everything digital. A human is required for money, legal identity, physical goods, and platform identity checks.

| Claude Code does (automated, in this repo) | Human does (cannot be automated) |
|---|---|
| Brand name and trademark clearance searches (TSDR + web) | Form LLC, EIN, business bank account, sales-tax registration |
| Build the Shopify store via Admin GraphQL (theme settings, pages, policies, collections, products, bundles, discounts, shipping profiles, Prop 65 and choking-hazard text on every listing) | Fix Shopify billing (the connected store currently returns "unavailable for API access"; likely a paused or unpaid plan), or claim a new store |
| Write and maintain the product catalogue from supplier CSVs; generate titles, descriptions, alt text, SEO | Open Faire / distributor wholesale accounts (needs business docs), approve samples |
| Unit-economics and pricing decisions from live quotes (`unit_economics.py`) | Pay for inventory, packaging, insurance, lab tests |
| Klaviyo flows: welcome, abandoned cart, post-purchase, win-back, restock | Pass Shopify Payments, TikTok Shop and Amazon identity/KYC checks |
| Daily TikTok content plan: hooks, scripts, captions, hashtags; AI-generated b-roll and voice via the Higgsfield/Krea connectors in this session; edit briefs for real footage | Shoot 10–20 minutes of real product footage per week (ASMR squeezes, unboxings, restocks); AI cannot fake tactile product credibly and TikTok Shop requires real product in affiliate videos |
| TikTok Shop affiliate outreach lists and message templates; creator sample-request triage rules | Pack and ship parcels (or approve 3PL at >500 orders/month); handle returns |
| Weekly analytics routine: ShopifyQL sales, CVR, AOV, CAC by channel, inventory days-of-cover, reorder alerts, written report committed to the repo | Read the weekly report; make the go/no-go calls at each gate |
| Trend monitor: weekly web search on squishy formats, Faire trend reports, CPSC recalls, competitor pricing | Sign supplier contracts, customs broker engagement, lab test submissions |
| Customer-service macros and first-response drafts (Shopify Inbox) | Final say on refunds and disputes |
| Compliance tracker: per-SKU CPC dates, test reports, label photos, retest reminders | Product-liability insurance, lawyer sign-off on age grading and Prop 65 wording |

## 2. Phases, timeline, gates

### Phase 0: Decide and set up (this week to 4 Oct)

1. Human: confirm entity, bank, and the Shopify store's billing status. Decision: revive the linked store or spin up a new one.
2. Claude: run brand-name clearance on 5 candidate names (no "mallow", "squishable", "pop it"; avoid "squishies" as a brand); pick one that is free on TSDR, .com, TikTok and Instagram.
3. Claude: build the store skeleton: theme, home, collections (Bundles, Mystery Bags, Desk Calm, Gifts under $30), policy pages, Prop 65 and 16 CFR 1500.19 choking warning blocks, shipping profile (free shipping at $29.99, flat $4.95 below).
4. Human: apply for Faire retailer account and, in parallel, contact ORB Toys (Tabalicious), Schylling (NeeDoh; distributors are being rationed, so may fail), RMS USA (Mystery Dumpling), Anboor, and TABASQUISHY B2B (MOQ 20/SKU, $500 minimum) for wholesale pricing and CPC copies.
5. Claude: build the Q4 assortment plan: 8–12 SKUs, three bundle recipes, one mystery bag, with per-bundle contribution computed from actual quotes. Target landed cost at or below 40% of price for wholesale stock (best achievable without importing).
6. Human: product-liability policy (~$500/yr), open TikTok Shop seller account, order $1,500–2,500 of stock and $300 of packaging.

**Gate 0 (go/no-go for Phase 1):** at least two wholesale sources with CPCs confirmed, a bundle that shows ≥ $10 contribution before acquisition cost at $34.99, and stock arriving by 25 Oct.

### Phase 1: Soft launch and validation (5 Oct to 15 Nov)

- Store live with 8–12 SKUs, 3 bundles, 1 mystery bag; bundle app configured for one-click add-ons (single squishies as $6–9 add-ons only ride inside an existing parcel, ~75% incremental margin).
- Content: 1–2 TikTok posts per day (Claude scripts and edits; human shoots product). Formats proven in 2026: ASMR squeeze, restock/haul, "dupe vs real" tests, mystery-bag opening, desk-setup.
- TikTok Shop: list bundles, open affiliate collaboration at 15% commission, send 20–30 free samples to nano/micro creators (Claude builds the list and messages). Note the calculator: on wholesale stock, TikTok Shop plus affiliate is roughly break-even; treat it as paid discovery, not profit, until own-brand margins.
- Email: Klaviyo flows live, pop-up with 10% first-order code.
- No Meta prospecting. Optional: $10/day Meta retargeting only once the site has 1,000+ visitors.
- Weekly report routine (Claude) every Monday: orders, revenue, CVR, AOV, blended CAC, contribution, best-performing content, inventory cover, reorder recommendation.

**Gate 1 (evaluated 15 Nov):** ≥ 100 orders, CVR ≥ 1.8%, AOV ≥ $32, blended CAC ≤ $10, at least one TikTok post over 100K views or one affiliate driving 20+ orders. If met, place a second stock order for BFCM. If not met, do not add stock; sell through and skip to Phase 3 decision.

### Phase 2: Q4 push (15 Nov to 31 Dec)

- Black Friday to Cyber Monday: bundle-only offers (free add-on at $50, not percentage discounts that kill margin).
- Gift guides, "ships by" dates on every page, holiday cut-off banner.
- Double content cadence in the 10 days before each shipping cut-off.
- Post-purchase flow asks for UGC and reviews (Judge.me) to build proof for 2027.
- Weekly report continues; inventory reorder recommendations move to twice weekly.

**Gate 2 (evaluated 5 Jan 2027):** Q4 cumulative ≥ 400 orders, blended CAC ≤ $8, contribution after CAC positive, repeat/email revenue ≥ 15% of total, no compliance incident. Base scenario in the calculator is 450 orders / +$1,156 after fixed costs; bull is 1,200 orders / +$5,900.

### Phase 3: Own-brand decision (Jan to Mar 2027)

Only if Gate 2 is met:

- Design 4–6 original taba-style or PU designs (capybara, food, calm/desk themes; no licensed characters, no Squishmallows trade-dress cues, no gel or water-bead fillers).
- Custom mold: $500–600 (PU) to $2,000–3,000 (TPR/silicone) per mold; MOQ 1,000–3,000; 60–90 days door to door.
- Lab testing at a CPSC-accepted lab: ASTM F963-23, lead, phthalates, small parts; budget $800–2,400 per SKU, less with component testing across shared materials. Issue CPCs, tracking labels, register for CPSC eFiling via broker.
- Personalized pet-face squishies as a made-to-order line ($29–45), started on Etsy-style workflow with a domestic print/paint partner before any OEM commitment.
- Target: $34.99 own-brand 3-pack at ~$6.50 landed, $18.62 contribution before CAC, break-even ROAS 1.9x, which makes Meta and TikTok paid ads viable for the first time.

Own-brand budget: $8,000–15,000 including tooling, testing, first production run, and freight. This is the real investment and it should not be made before Gate 2.

### Kill criteria (any phase)

- Blended CAC above $15 for three consecutive weeks with no content breakout.
- CVR below 1.0% after 2,000 sessions with fixed pricing and free-shipping threshold in place.
- Any IP notice or CPSC contact: stop selling the affected SKU immediately and escalate to a human.
- A category-wide fade signal in the weekly trend monitor (Faire squishy searches falling two months running, Google interest below 40% of peak) before own-brand tooling is paid: cancel Phase 3.

## 3. Budget

| Item | Phase 0–2 (Q4 2026) | Phase 3 (2027, conditional) |
|---|---|---|
| Shopify Basic + apps + domain | ~$100/month | ~$150/month |
| Inventory (wholesale, certified) | $1,500–2,500 initial, +$1,500 at Gate 1 | — |
| Packaging, inserts, labels | $300 | $500 (custom mailers at $0.35–0.44) |
| Creator samples (20–30 units) | ~$300 of stock | — |
| Product-liability insurance | ~$500/year | included |
| Meta retargeting (optional) | ≤ $300 | scaled to ROAS |
| LLC, sales-tax registration | $100–500 depending on state | — |
| Molds, lab tests, first run, freight, broker | — | $8,000–15,000 |
| **Total cash at risk** | **~$3,500–5,500** | **~$10,000–16,000** |

## 4. What Claude Code builds in this repo (proposed layout)

```
squishy/
  config/assortment.yaml        # SKUs, costs, bundle recipes, price points
  shopify/setup_store.py        # Admin GraphQL: pages, policies, collections, shipping, warnings
  shopify/sync_catalog.py       # supplier CSV -> products, variants, bundles, media
  shopify/discounts.py          # BFCM and threshold offers
  finance/unit_economics.py     # (moved from research/) margin + scenario calculator
  finance/weekly_report.py      # ShopifyQL -> markdown report, committed to reports/
  marketing/content_calendar.py # daily hooks/scripts/captions; briefs for human footage
  marketing/creator_outreach.py # affiliate shortlist + templates; sample tracker
  marketing/klaviyo_flows.md    # flow copy and triggers
  ops/inventory_alerts.py       # days-of-cover, reorder points, lead times
  ops/compliance_tracker.yaml   # per-SKU CPC dates, test reports, label photos
  ops/trend_monitor.py          # weekly search: formats, recalls, Faire trends, competitor prices
  reports/                      # weekly outputs
```

Runtime: the weekly report, inventory alerts and trend monitor run as scheduled Claude Code routines (this session can create them once the store is API-accessible). Everything writes back to the repo so the human reads one Monday report and makes the gate decisions.

## 5. Immediate next actions

1. Human: resolve the Shopify store's billing/plan so the API is reachable (or say "new store" and Claude will generate previews).
2. Human: confirm entity status and whether the Q4 cash budget (~$4–5K) is approved.
3. Claude (on go): brand clearance search, store skeleton build, Faire/distributor outreach drafts, assortment plan from first quotes.
