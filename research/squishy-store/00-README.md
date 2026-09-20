# Squishy Shopify Store: Research Summary and Verdict (20 Sept 2026)

This folder is the research package for launching a squishy-toy Shopify store. Five research tracks ran in parallel (about 170 web searches); each has its own file with tables and source URLs. This README answers the four questions asked and points to the plan.

| File | What it covers |
|---|---|
| `01-demand-and-trends.md` | Market size, Circana POS data, search and social trends, seasonality, who buys |
| `02-competition-and-saturation.md` | 17 existing DTC stores, Amazon/Temu/TikTok Shop pricing, ad costs, gaps |
| `03-new-products-and-trends.md` | 18 product formats ranked by trend direction, top 5 bets for Q4 2026 |
| `04-unit-economics-and-supply-chain.md` | Sourcing costs, tariffs, shipping, platform fees, worked P&L |
| `05-legal-safety-and-platform-risk.md` | Trademarks, CPSC/CPSIA testing, recalls, customs, platform gating |
| `10-execution-plan.md` | The phased plan Claude Code can build and run, with gates and budget |
| `unit_economics.py` | Reproducible margin calculator behind the plan's numbers |

**Caveat on data quality.** The sandbox blocked full-page fetches for most sources, so figures come from search-result snapshots. Circana point-of-sale numbers and CPSC/SEC filings are high confidence; syndicated "market size" vendor reports and Alibaba price snippets are low confidence and labelled as such in each file.

---

## 1. Is it oversaturated?

**Generic squishies: yes, completely. Curated and own-brand: no.**

- Amazon has 1,258 listings in the $10–20 band for "squishy fidget toys" alone. The top 30-pack mochi listing sells ~40,000 units a month, and 26-packs have hit $5.99 (about $0.23 per squishy).
- Temu, Shein and AliExpress sell the same product at factory cost (under $1 per unit) with free shipping.
- ShopifySpy counts 82 Shopify stores in the "squishy toys" niche. Several of the mid-tier ones are dying or dead (Squishy Plushies defunct, Bunny's Cafe SF shops closed, Squishmania and Squishyshop.com with non-delivery complaints). The dropship-a-single-squishy model has an 80–90% failure rate and the Trustpilot record to prove it.
- Meta's median ecommerce ROAS is about 1.9–2.2x; a $13 squishy with a 50% margin cannot survive a $40 CPA.

What is **not** saturated: authentic premium/licensed (Creamiicandy is the only Western specialist, 293K Instagram followers), safety-certified "parent-safe" branding, adult "desk calm" positioning (adults drove 35% of 2026 toy growth), personalized squishies (Etsy only), and curated subscriptions (one active squishy-specific box, SomaSquish at $35/month).

## 2. Are there new products?

**Yes. The category re-invented itself in 2025–26 and the new formats are not the 2018 formats.**

| Format | Direction (Sept 2026) | Retail | Wholesale |
|---|---|---|---|
| Silicone "taba" squishies (sticky, slow rebound) | Rising; "Top Cozy Sensory Toy" at Toy Fair 2026; ORB Tabalicious now in Walmart | $5–20 | $0.20–2.00 (custom mold MOQ 1,000+) |
| Food squishies (dumpling, butter, bao, cheese) | At peak; RMS "Mystery Dumpling" sell-out streak | $8–13 blind box | $0.80–3 |
| NeeDoh / gel "dough" squishies | Peaked; class action filed July 2026; CPSC burn alerts | $3–15 | avoid unbranded |
| Jumbo/giant food squishies | Rising as content prop; scarce at big box | $20–77 | $2–8 |
| Capybara anything | Still rising; top mini-figure ASIN >5,000/month | $7–65 | $0.50–6 |
| Squishy bag charms / keychains | Rising as a use case post-Labubu | $6–15 | $0.40–1.50 |
| Personalized pet-face / name squishies | White space; Etsy only | $25–45 | $3–6 |
| Mochi mini packs | Declining commodity | $0.50/unit | $0.10–0.24 |
| Pop-its, slow-rise kawaii singles | Flat/filler | | |

## 3. Have we missed the rush?

**No, but the window is Q4 2026, and the rush will probably fade in 2027.**

- Circana: US squishy-toy sales hit ~$297M in H1 2026, roughly 4x H1 2025, on 58.6M units. Sensory toys posted triple-digit growth. This is the biggest toy craze of the year (CNBC, 27 Aug 2026).
- Faire wholesale searches for "squishy" are up 18,000% year over year; independent-retailer plush/squishy orders were up 628% in Q2.
- Toy Insider's Holiday 2026 hot lists (out 23 Sept) feature NeeDoh and "toys that squish". Q4 will be the largest squishy holiday ever; toys do 36–65% of annual sales in the Oct–Dec window.
- The cautionary pattern: the 2017–18 squishy craze crossed $100M US sales, then collapsed in 2019 under knockoffs and chemical-safety scrutiny. Labubu went from peak to "cooled" in 12–18 months. Squishmallows-led plush peaked in 2024 and Jazwares revenue fell 38.5% in H1 2025.
- Meaning: buy inventory for Q4 sell-through, not for a 12-month runway, and treat any 2027 own-brand investment as conditional on Q4 results.

## 4. Can this be profitable?

**Yes, narrowly, and only under four conditions.** (Full math in `04-…` and `unit_economics.py`.)

1. **Bundles, never singles.** A $12.99 single squishy with free shipping nets $1.49 per order before any ad spend. USPS's July 2026 rate change means every sub-1 lb parcel costs ~$6.80 commercial. A $30–35 three-pack nets $11–19 before ad spend.
2. **Landed cost at or below 25% of price.** That means bulk import (tariff stack on China toys is ~20% as of July 2026) or US wholesale from a brand that already holds safety certificates. Per-order dropshipping is dead since de minimis ended in Aug 2025.
3. **Blended customer acquisition cost under ~$8.** Meta prospecting at its 2x median ROAS loses money on every order. The channel that fits is organic TikTok plus TikTok Shop affiliates, where commission is only paid on conversion.
4. **Compliance done once, properly.** Squishies are children's products: CPSC-accepted lab testing ($800–2,400 per SKU), a Children's Product Certificate, tracking labels, choking warnings, Prop 65 warnings. CPSC stopped 355,683 counterfeit squishies at ports in 2026 and there were two water-bead recalls in September. "Ages 14+" labelling does not escape this. Selling unlicensed Sanrio/Pokémon/Stitch designs gets funds frozen under Schedule A lawsuits.

**What the calculator says (per order, before acquisition cost):**

| Offer | Price | Contribution | Break-even ROAS |
|---|---|---|---|
| Q4 2026 curated 3-pack from US wholesale stock | $34.99 | $11.13 | 3.1x |
| 2027 own-brand imported 3-pack | $34.99 | $18.62 | 1.9x |
| $12.99 single, free shipping | $12.99 | $1.49 | 8.7x |

**Q4 2026 scenarios (10-week window, wholesale stock, after acquisition cost and fixed costs):** bear 150 orders / −$382; base 450 orders / +$1,156; bull 1,200 orders / +$5,900. In other words, the Q4 launch is a paid-for validation experiment, not a payday. The profit case is 2027 own-brand at 50%+ contribution margin, which only makes sense if Q4 proves the store can acquire customers for under $8.

## Verdict

Build it, but as a **two-stage bet**: a low-capital, compliance-safe Q4 2026 launch on certified wholesale stock to prove acquisition cost, then a conditional own-brand (taba-style capybara/food line plus personalized squishies) for 2027 only if the gates in `10-execution-plan.md` are met. Do not build a generic squishy dropshipping store; the data says that model is already dead.
