# Phase 0 checklist (target: complete by 4 Oct 2026)

Gate 0 to pass before ordering stock: two wholesale sources with CPCs confirmed; at least one bundle at >= $10 contribution before acquisition cost at ~$35; stock able to arrive by 25 Oct.

| # | Task | Owner | Status | Notes |
|---|---|---|---|---|
| 1 | Confirm entity, EIN, business bank | Human | open | Needed before Faire and TikTok Shop applications |
| 2 | Brand name: shortlist and clearance search | Claude | done | `ops/brand-name-clearance.md`: top 3 are Deskloaf, Doughlet, Fidgetnook |
| 3 | Brand name: final pick, domain, handles | Human | mostly done | Deskloaf chosen; deskloaf.co bought (Namecheap, DNS via Cloudflare pending); Instagram, Facebook Page and TikTok all created 20 Sept |
| 4 | New Shopify store created | Human | done | nzkkpf-7r.myshopify.com, trial plan; rename to Deskloaf in Settings > General; pick Basic plan |
| 5 | Connect the new store to this session | Human | done | Connected via Shopify connector 20 Sept |
| 6 | Build store skeleton: pages, collections, products, bundles, menus, weights, LOAF10 code | Claude | done | Built 20 Sept via connector; IDs in `ops/store_ids.json`; products are DRAFT |
| 7 | Shipping rates: free at $29.99, $4.95 below | Claude | done | Default profile updated; Express and $8 default rates removed |
| 8 | Apply to Faire as retailer | Human | open | Copy in `suppliers/outreach.md` |
| 9 | Supplier outreach | Claude (drafts) / Human (send + forms) | drafts in Gmail | TABASQUISHY and Anboor drafts in Gmail (review, add state, send). ORB and RMS via web forms, text in `suppliers/contacts.md`. Schylling paused new accounts. |
| 10 | Enter quotes and CPC data as they arrive | Claude | waiting | `config/assortment.json`, `ops/compliance_tracker.json` |
| 11 | Re-run margins with real quotes; confirm Gate 0 | Claude | waiting | `python3 squishy/finance/bundle_margins.py` |
| 12 | Product-liability insurance (~$1M) | Human | open | ~$500/yr; needed before first sale |
| 13 | TikTok Shop seller account; upload CPCs to Toys & Hobby category | Human (KYC) / Claude (docs) | open | |
| 14 | Order first stock ($1,500–2,500) and packaging ($300) | Human | blocked by Gate 0 | |
| 15 | Klaviyo account + connect; Claude loads flow copy | Human (account) / Claude (flows) | open | Flow copy to be added at `marketing/klaviyo_flows.md` in Phase 1 |
| 16 | Weekly report routine scheduled (Mondays) | Claude | blocked by item 5 | ShopifyQL via connector |

| 17 | Paste store policies (refund, shipping, privacy, terms) | Human | open | `config/policies.md`; connector lacks the legal-policies scope |
| 18 | Set store name to Deskloaf, store email, address, Shopify Payments | Human | open | Settings > General / Payments |
| 19 | Home page theme copy | Claude (edit) / Human (publish) | edited on copy | Unpublished theme "Horizon - Deskloaf copy (Claude edits)": preview in Online Store > Themes, then Publish |
| 20 | Monday ops routine + calendar deadlines | Claude | done | Routine trig_01LVPHa9zNDrnyHs5dXcJoJD; 7 Google Calendar events incl. gates |
