# Deskloaf handoff (state as of 20 Sept 2026, 10:30 UTC)

Read this first when continuing the Deskloaf project in a new Claude Code session. Everything below is committed on branch `claude/squishy-shopify-research-9hwl25`.

## What Deskloaf is
A US Shopify store selling curated squishy-toy bundles ($30–37) to adults and gift buyers, positioned "Squishies for grown-up desks". Q4 2026 launch on certified US-wholesale stock as a validation run; own-brand imports in 2027 only if Q4 gates pass. Full plan: `research/squishy-store/10-execution-plan.md`. Research: `research/squishy-store/00-README.md`.

## Accounts and identifiers
- Shopify: `nzkkpf-7r.myshopify.com`, trial plan, still named "My Store" in admin. All GIDs in `squishy/ops/store_ids.json`.
- Domain: deskloaf.co bought on Namecheap; DNS to be moved to Cloudflare (CNAME @ and www → shops.myshopify.com, DNS only), then connected in Shopify.
- Social: Instagram, Facebook Page, TikTok all created 20 Sept. Bios in `squishy/marketing/brand_copy.md`. Avatar options: `squishy/marketing/brand-assets/README.md`.
- Business email: deskloaf@gmail.com (new; connectors in the web session were still on chrismole@gmail.com). Two supplier drafts (TABASQUISHY, Anboor) were created in chrismole@gmail.com on 20 Sept; recreate from deskloaf@gmail.com if preferred.
- Google Calendar (chrismole@gmail.com): 7 Deskloaf events incl. admin block 21 Sept 2pm ET, weekly Tue footage shoot, Gate 0 (4 Oct), stock deadline (25 Oct), Gate 1 (15 Nov), BFCM (27 Nov), Gate 2 (5 Jan 2027).
- Cloud routine: "Deskloaf Monday ops report" (trig_01LVPHa9zNDrnyHs5dXcJoJD) fires Mondays 13:00 UTC into the original web session; may lack connector tools. Delete or recreate locally if a local weekly run is preferred.

## Store state
- 5 smart collections (tags: bundle, mystery, desk-calm, gift-under-30, single).
- 13 DRAFT products (9 singles, 4 bundles) with safety/choking/Prop 65 copy, weights, costs, HS 950300. SKUs in `squishy/config/assortment.json` (costs are estimates until quotes arrive).
- Pages: Safety & Testing, About, Shipping, Returns. Menus wired.
- Shipping: $4.95 under $29.99, free at $29.99+. Discount LOAF10 (10%, all customers).
- Theme: unpublished duplicate "Horizon - Deskloaf copy (Claude edits)" has hero, value props, product grids, announcement bar and password page copy. Human previews and publishes. Source: `squishy/shopify/theme/`.

## Human tasks outstanding (in priority order)
1. Shopify: rename store to Deskloaf; choose Basic plan; paste policies (`squishy/config/policies.md`); Shopify Payments; set contact email to deskloaf@gmail.com.
2. Cloudflare DNS for deskloaf.co → connect in Shopify → set primary.
3. Send supplier emails (TABASQUISHY, Anboor); submit ORB and RMS web forms (`squishy/suppliers/contacts.md`); sign up at faire.com/signup.
4. TikTok Shop seller application. Product-liability insurance. Confirm LLC + bank.
5. Buy 4 sample items (~$43, links in `suppliers/contacts.md`); shoot footage bank (`marketing/content_calendar.md`).
6. Publish the duplicated theme after preview.

## Claude tasks queued
- When quotes/CPCs arrive: update `config/assortment.json` (unit_cost, quote_status) and `ops/compliance_tracker.json`; run `python3 squishy/finance/bundle_margins.py`; call Gate 0.
- Weekly: Monday ops report into `squishy/reports/`; Sunday content refresh (7 hooks) from performance data.
- On launch (~25 Oct): set products ACTIVE, remove password, load Klaviyo flows (`marketing/klaviyo_flows.md`), turn on pop-up.
- Not yet built: `shopify/setup_store.py` was written for an Admin token but the store was built via the connector; keep it as the reproducible fallback.

## Guardrails
- Never use the words in `marketing/brand_copy.md` "Words we do not use". No licensed characters, no water-bead or unbranded gel items, no "non-toxic" claims without a report. Ads target 18+ only.
- Products stay DRAFT until CPCs are on file for each SKU.
