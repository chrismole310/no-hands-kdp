# Faire retailer application (paste-ready answers)

Apply at https://www.faire.com/signup ("Sign up to buy"). Use deskloaf@gmail.com. Faire verifies after the first order and may ask for documentation; the resale certificate (NY Certificate of Authority, item 21 on the checklist) is the document they most often request, so start that application the same day.

## Form answers

| Field | Answer |
|---|---|
| Store name | Deskloaf |
| Website | https://deskloaf.co |
| Business type | Online store |
| Legal entity | MoleHole, Inc. (New York corporation) |
| Store category | Toys & Games; Gifts; Stationery & Desk |
| Where you sell | Online only (own Shopify store and TikTok Shop) |
| Years in business | New store; parent company since 2023 |
| Business address | [MoleHole, Inc. registered address, New York] |
| Phone | [business phone] |
| Instagram | @deskloaf |
| Number of locations | 0 physical; 1 online |
| Annual revenue | Under $100K (new) |

## Store description (150 words)

Deskloaf is a US online boutique launching in October 2026 that sells curated squishy bundles to adults and gift buyers: silicone taba squishies, jumbo slow-rise pastries and desk fidgets, packed in three-piece sets at $30 to $37 and shipped free. Our customers are women in their twenties and thirties buying for their own desks, plus parents buying gifts for 7-to-12-year-olds. We only stock items with a current Children's Product Certificate and lab reports, and we market them on TikTok and Instagram with daily short-form content. We're looking for brands with certified, well-made squishies and sensory items in capybara, food and pastel styles, and we expect to reorder monthly through the holiday season.

## What to say if Faire asks "why do you want to buy wholesale"

Opening orders for a Q4 launch: 8 to 12 SKUs, 20 to 50 units each, from certified brands. We plan to reorder through December and build a curated assortment rather than a general store.

## First brands to search once approved

| Brand on Faire | Why | Ask for |
|---|---|---|
| ORB Toys (Tabalicious) | Hero taba line; on Faire at faire.com/brand/b_4m8pbfzvxk | CPC + lab reports per SKU; note the May 2026 Orb Funkee recall and ask what changed in QA |
| Showcase (authorised RMS / Crazy Fun distributor) | Mystery Dumpling and food squishies | Fill material confirmation (no water beads), CPC |
| Schylling (via distributors) | Genuine NeeDoh if any allocation exists | Availability only; don't build around it |
| Toysmith, Top Trenz, Iscream, Kawaii Company | Certified squishy/fidget lines common at independent toy stores | Capybara, pastel, food designs; CPCs |

Use Faire's "first order free returns" and net-60 terms on each new brand; it turns the opening order into a low-risk sample run.

## After approval
1. Message each brand through Faire with the six standard questions (`outreach.md`).
2. Download each brand's compliance documents from the product pages or by request; log them in `ops/compliance_tracker.json`.
3. Enter real unit costs in `config/assortment.json` (`quote_status: "quoted"`) and run `python3 squishy/finance/bundle_margins.py`.
