#!/usr/bin/env python3
"""Per-bundle contribution from config/assortment.json.

Run: python3 bundle_margins.py [--cac 8]
Assumptions mirror research/squishy-store/unit_economics.py (USPS <1 lb $6.80,
packaging $0.35, Shopify Basic 2.9% + $0.30, 4% returns allowance).
"""
import argparse
import json
from pathlib import Path

A = json.loads((Path(__file__).resolve().parents[1] / "config" / "assortment.json").read_text())
USPS, PACK, PCT, FIXED_FEE, RETURNS = 6.80, 0.35, 0.029, 0.30, 0.04
by_sku = {s["sku"]: s for s in A["skus"]}


def contribution(price: float, cogs: float) -> float:
    return price - cogs - PACK - USPS - (price * PCT + FIXED_FEE) - price * RETURNS


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cac", type=float, default=8.0, help="blended acquisition cost per order")
    cac = ap.parse_args().cac
    est = any(s["quote_status"] != "quoted" for s in A["skus"])
    if est:
        print("NOTE: one or more unit costs are estimates, not quotes.\n")
    print(f"{'Bundle':22s} {'Price':>7s} {'COGS':>7s} {'COGS%':>6s} {'Wt oz':>6s} {'CM':>7s} {'CM%':>6s} {'after CAC':>10s} {'BE ROAS':>8s}")
    print("-" * 90)
    for b in A["bundles"]:
        cogs = sum(by_sku[c]["unit_cost"] for c in b["components"])
        wt = sum(by_sku[c]["weight_oz"] for c in b["components"])
        cm = contribution(b["price"], cogs)
        flag = " <1lb!" if wt >= 15.99 else ""
        be = f"{b['price']/cm:.2f}x" if cm > 0 else "n/a"
        print(f"{b['name']:22s} {b['price']:7.2f} {cogs:7.2f} {cogs/b['price']*100:5.0f}% {wt:6.1f}{flag} {cm:7.2f} {cm/b['price']*100:5.1f}% {cm-cac:10.2f} {be:>8s}")
    print("\nSingles as add-ons riding in an existing parcel (incremental cost = COGS + ~$0.70):")
    for s in A["skus"]:
        if s["format"] == "insert":
            continue
        inc = s["addon_price"] - s["unit_cost"] - 0.70 - s["addon_price"] * PCT
        print(f"  {s['sku']:16s} add-on ${s['addon_price']:5.2f}  incremental margin ${inc:5.2f} ({inc/s['addon_price']*100:.0f}%)")
    print("\nGate 0 target: every bundle >= $10 CM before CAC. Gate 1 target: blended CAC <= $10; Gate 2: <= $8.")


if __name__ == "__main__":
    main()
