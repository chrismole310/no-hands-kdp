# Phase 0 checklist (target: complete by 4 Oct 2026)

Gate 0 to pass before ordering stock: two wholesale sources with CPCs confirmed; at least one bundle at >= $10 contribution before acquisition cost at ~$35; stock able to arrive by 25 Oct.

| # | Task | Owner | Status | Notes |
|---|---|---|---|---|
| 1 | Confirm entity, EIN, business bank | Human | open | Needed before Faire and TikTok Shop applications |
| 2 | Brand name: shortlist and clearance search | Claude | done | `ops/brand-name-clearance.md`: top 3 are Deskloaf, Doughlet, Fidgetnook |
| 3 | Brand name: final pick, buy .com, claim TikTok/Instagram handles | Human | open | Do not buy until item 2 is reviewed |
| 4 | New Shopify store: generate previews, pick theme, sign up | Human | previews ready | Generated 20 Sept via the Shopify connector; sign up through the chosen preview's link |
| 5 | Connect the new store to this session (switch-shop) or create a custom-app Admin token | Human | open | Token scopes: write_products, write_content, read_publications |
| 6 | Build store skeleton: pages, collections, products, bundles | Claude | ready | `python3 squishy/shopify/setup_store.py --dry-run` passes; run for real after item 5 |
| 7 | Shipping profile: free at $35, $4.95 below; USPS Ground Advantage via Shopify Shipping | Claude/Human | open | Set in Shopify admin (delivery profiles); Claude can do it via GraphQL once connected |
| 8 | Apply to Faire as retailer | Human | open | Copy in `suppliers/outreach.md` |
| 9 | Email ORB, TABASQUISHY, RMS USA, Anboor, Schylling | Human (send) / Claude (drafted) | drafted | `suppliers/outreach.md` |
| 10 | Enter quotes and CPC data as they arrive | Claude | waiting | `config/assortment.json`, `ops/compliance_tracker.json` |
| 11 | Re-run margins with real quotes; confirm Gate 0 | Claude | waiting | `python3 squishy/finance/bundle_margins.py` |
| 12 | Product-liability insurance (~$1M) | Human | open | ~$500/yr; needed before first sale |
| 13 | TikTok Shop seller account; upload CPCs to Toys & Hobby category | Human (KYC) / Claude (docs) | open | |
| 14 | Order first stock ($1,500–2,500) and packaging ($300) | Human | blocked by Gate 0 | |
| 15 | Klaviyo account + connect; Claude loads flow copy | Human (account) / Claude (flows) | open | Flow copy to be added at `marketing/klaviyo_flows.md` in Phase 1 |
| 16 | Weekly report routine scheduled (Mondays) | Claude | blocked by item 5 | ShopifyQL via connector |
