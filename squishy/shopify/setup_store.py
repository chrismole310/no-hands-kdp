#!/usr/bin/env python3
"""Build the store skeleton on a new Shopify store via the Admin GraphQL API.

Creates: collections, legal/safety pages, products (singles with add-on
metafield) and bundle products, with the choking warning and Prop 65 block on
every listing. Idempotent: re-running updates by handle instead of duplicating.

Usage:
  export SHOPIFY_STORE=your-store.myshopify.com
  export SHOPIFY_ADMIN_TOKEN=shpat_...      # custom app token, scopes:
                                            # write_products, write_content, read_publications
  python3 setup_store.py --dry-run          # print the plan, no API calls
  python3 setup_store.py all                # pages + collections + products + bundles
  python3 setup_store.py pages|collections|products|bundles

The Shopify MCP connector in a Claude Code session can run the same mutations
interactively; this script exists so the build is reproducible from the repo.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSORTMENT = json.loads((ROOT / "config" / "assortment.json").read_text())
LEGAL = (ROOT / "config" / "legal_copy.md").read_text()
API_VERSION = "2026-07"

CHOKING = ("<p><strong>WARNING: CHOKING HAZARD — Small parts. "
           "Not for children under 3 yrs.</strong> Age grade 6+.</p>")
PROP65 = ("<p><small>⚠ WARNING: Cancer and Reproductive Harm — "
          "{chemical} – www.P65Warnings.ca.gov</small></p>")
SAFETY_LINE = ("<p>Certified children's product: tested to ASTM F963-23, lead and "
               "phthalates by a CPSC-accepted lab. Certificate number available on request.</p>")


# ---------------------------------------------------------------- API client
class Shopify:
    def __init__(self, dry_run: bool):
        self.dry_run = dry_run
        self.store = os.environ.get("SHOPIFY_STORE", "")
        self.token = os.environ.get("SHOPIFY_ADMIN_TOKEN", "")
        if not dry_run and (not self.store or not self.token):
            sys.exit("Set SHOPIFY_STORE and SHOPIFY_ADMIN_TOKEN, or use --dry-run.")

    def gql(self, query: str, variables: dict | None = None) -> dict:
        if self.dry_run:
            m = re.search(r"\{\s*(\w+)", query)
            name = m.group(1) if m else query[:40]
            print(f"  [dry-run] {name} {json.dumps(variables or {}, ensure_ascii=False)[:160]}")
            return {}
        req = urllib.request.Request(
            f"https://{self.store}/admin/api/{API_VERSION}/graphql.json",
            data=json.dumps({"query": query, "variables": variables or {}}).encode(),
            headers={"Content-Type": "application/json", "X-Shopify-Access-Token": self.token},
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body = json.loads(r.read())
        except urllib.error.HTTPError as e:
            sys.exit(f"HTTP {e.code}: {e.read().decode()[:500]}")
        if body.get("errors"):
            sys.exit(f"GraphQL errors: {body['errors']}")
        data = body["data"]
        for v in data.values():
            if isinstance(v, dict) and v.get("userErrors"):
                sys.exit(f"userErrors: {v['userErrors']}")
        return data


# ---------------------------------------------------------------- helpers
def section(md: str, heading: str) -> str:
    """Return the body text under a '## heading' in legal_copy.md, as HTML paragraphs."""
    lines = md.splitlines()
    out, on = [], False
    for ln in lines:
        if ln.startswith("## "):
            on = ln[3:].strip().lower().startswith(heading.lower())
            continue
        if on and ln.strip() and not ln.startswith(">"):
            out.append(f"<p>{ln.strip()}</p>")
    return "\n".join(out)


def find_by_handle(api: Shopify, kind: str, handle: str) -> str | None:
    q = {
        "collection": "query($q:String){collections(first:1,query:$q){nodes{id handle}}}",
        "product": "query($q:String){products(first:1,query:$q){nodes{id handle}}}",
        "page": "query($q:String){pages(first:1,query:$q){nodes{id handle}}}",
    }[kind]
    data = api.gql(q, {"q": f"handle:{handle}"})
    if not data:
        return None
    nodes = next(iter(data.values()))["nodes"]
    return nodes[0]["id"] if nodes and nodes[0]["handle"] == handle else None


def listing_html(desc: str, chemical: str = "DEHP / Di(2-ethylhexyl)phthalate") -> str:
    return f"<p>{desc}</p>\n{SAFETY_LINE}\n{CHOKING}\n{PROP65.format(chemical=chemical)}"


# ---------------------------------------------------------------- builders
def build_pages(api: Shopify) -> None:
    pages = {
        "safety-testing": ("Safety & Testing", section(LEGAL, "Safety page")),
        "about": ("About", section(LEGAL, "Age and audience statement")),
        "shipping": ("Shipping", section(LEGAL, "Shipping policy summary")),
        "returns": ("Returns", section(LEGAL, "Returns policy summary")),
    }
    for handle, (title, body) in pages.items():
        print(f"page: {handle}")
        existing = find_by_handle(api, "page", handle)
        if existing:
            api.gql("mutation($id:ID!,$p:PageUpdateInput!){pageUpdate(id:$id,page:$p){page{id} userErrors{message}}}",
                    {"id": existing, "p": {"title": title, "body": body}})
        else:
            api.gql("mutation($p:PageCreateInput!){pageCreate(page:$p){page{id} userErrors{message}}}",
                    {"p": {"title": title, "handle": handle, "body": body, "isPublished": True}})


def build_collections(api: Shopify) -> dict[str, str]:
    ids: dict[str, str] = {}
    for c in ASSORTMENT["collections"]:
        print(f"collection: {c['handle']}")
        existing = find_by_handle(api, "collection", c["handle"])
        if existing:
            ids[c["handle"]] = existing
            continue
        data = api.gql(
            "mutation($c:CollectionInput!){collectionCreate(input:$c){collection{id} userErrors{message}}}",
            {"c": {"title": c["title"], "handle": c["handle"], "descriptionHtml": f"<p>{c['description']}</p>"}},
        )
        if data:
            ids[c["handle"]] = data["collectionCreate"]["collection"]["id"]
    return ids


def upsert_product(api: Shopify, handle: str, title: str, html: str, price: float,
                   sku: str, weight_oz: float, tags: list[str], collection_ids: list[str],
                   addon_price: float | None = None) -> None:
    existing = find_by_handle(api, "product", handle)
    product = {
        "title": title, "handle": handle, "descriptionHtml": html, "tags": tags,
        "status": "DRAFT", "productType": "Squishy toy", "vendor": ASSORTMENT.get("brand", ""),
        "collectionsToJoin": collection_ids,
    }
    if addon_price is not None:
        product["metafields"] = [{"namespace": "custom", "key": "addon_price", "type": "money",
                                  "value": json.dumps({"amount": f"{addon_price:.2f}", "currency_code": "USD"})}]
    if existing:
        product["id"] = existing
        api.gql("mutation($p:ProductUpdateInput!){productUpdate(product:$p){product{id} userErrors{message}}}",
                {"p": product})
        pid = existing
    else:
        data = api.gql("mutation($p:ProductCreateInput!){productCreate(product:$p){product{id variants(first:1){nodes{id}}} userErrors{message}}}",
                       {"p": product})
        pid = data["productCreate"]["product"]["id"] if data else "gid://dry-run"
    # Price/SKU/weight live on the default variant.
    if not api.dry_run:
        v = api.gql("query($id:ID!){product(id:$id){variants(first:1){nodes{id inventoryItem{id}}}}}", {"id": pid})
        node = v["product"]["variants"]["nodes"][0]
        api.gql(
            "mutation($pid:ID!,$v:[ProductVariantsBulkInput!]!){productVariantsBulkUpdate(productId:$pid,variants:$v){userErrors{message}}}",
            {"pid": pid, "v": [{"id": node["id"], "price": f"{price:.2f}",
                                "inventoryItem": {"sku": sku, "tracked": True,
                                                  "measurement": {"weight": {"unit": "OUNCES", "value": weight_oz}}}}]},
        )
    else:
        print(f"  [dry-run] variant price={price:.2f} sku={sku} weight={weight_oz}oz")


def build_products(api: Shopify, cols: dict[str, str]) -> None:
    for s in ASSORTMENT["skus"]:
        if s["format"] == "insert":
            continue
        print(f"product: {s['sku']} {s['name']}")
        html = listing_html(s.get("copy") or s["name"])
        upsert_product(api, handle=s["sku"].lower(), title=s["name"], html=html,
                       price=s["single_price"], sku=s["sku"], weight_oz=s["weight_oz"],
                       tags=["single", s["format"], "age-6plus"],
                       collection_ids=[cols[h] for h in ("add-ons",) if h in cols],
                       addon_price=s["addon_price"])


def build_bundles(api: Shopify, cols: dict[str, str]) -> None:
    by_sku = {s["sku"]: s for s in ASSORTMENT["skus"]}
    for b in ASSORTMENT["bundles"]:
        print(f"bundle: {b['sku']} {b['name']} ${b['price']}")
        parts = "".join(f"<li>{by_sku[c]['name']}</li>" for c in b["components"])
        html = listing_html(f"{b['positioning']}</p><p>Includes:<ul>{parts}</ul>")
        weight = sum(by_sku[c]["weight_oz"] for c in b["components"])
        if weight >= 15.99:
            print(f"  WARNING: bundle weight {weight}oz crosses the 1 lb USPS tier; re-spec it.")
        handle_map = {"Bundles": "bundles", "Mystery Bags": "mystery-bags", "Gifts under $30": "gifts-under-30"}
        col_ids = [cols[h] for h in (handle_map.get(b["collection"], ""), "desk-calm" if "DESK" in b["sku"] else "") if h in cols]
        upsert_product(api, handle=b["sku"].lower(), title=b["name"], html=html, price=b["price"],
                       sku=b["sku"], weight_oz=weight, tags=["bundle", "free-shipping"], collection_ids=col_ids)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("step", nargs="?", default="all", choices=["all", "pages", "collections", "products", "bundles"])
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    api = Shopify(a.dry_run)
    cols: dict[str, str] = {}
    if a.step in ("all", "pages"):
        build_pages(api)
    if a.step in ("all", "collections", "products", "bundles"):
        cols = build_collections(api)
    if a.step in ("all", "products"):
        build_products(api, cols)
    if a.step in ("all", "bundles"):
        build_bundles(api, cols)
    print("done" + (" (dry run)" if a.dry_run else ""))


if __name__ == "__main__":
    main()
