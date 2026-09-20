# squishy/ — store build and operations

Working files for the squishy-toy Shopify store described in `research/squishy-store/10-execution-plan.md`.

```
config/assortment.json        SKUs, costs (estimate vs quoted), bundle recipes, collections
config/legal_copy.md          choking warning, Prop 65, safety page, policy text
shopify/setup_store.py        builds pages, collections, products, bundles via Admin GraphQL (idempotent, --dry-run)
finance/bundle_margins.py     per-bundle contribution from assortment.json
suppliers/outreach.md         wholesale application copy and the six standard questions
ops/phase0_checklist.md       who does what, with status
ops/compliance_tracker.json   CPC / lab report / label tracking per SKU
reports/                      weekly analytics reports (Phase 1 onward)
```

Quick checks:

```
python3 squishy/finance/bundle_margins.py --cac 8
python3 squishy/shopify/setup_store.py --dry-run
```
