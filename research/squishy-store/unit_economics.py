#!/usr/bin/env python3
"""Unit economics for a squishy-toy Shopify store (US, Sept 2026 assumptions).

Run:  python3 unit_economics.py
Edit the ASSUMPTIONS block to re-run with your real quotes.
Sources for defaults: research/squishy-store/04-unit-economics-and-supply-chain.md
"""

from dataclasses import dataclass

# ---- ASSUMPTIONS (edit me) -------------------------------------------------
USPS_GROUND_ADVANTAGE_BLENDED = 6.80   # commercial, <1 lb, zone 4-5 blend (post Jul-2026 tier change)
PACKAGING = 0.35                       # poly mailer + insert card
SHOPIFY_CARD_PCT = 0.029               # Shopify Basic online rate
SHOPIFY_CARD_FIXED = 0.30
RETURNS_PCT = 0.04                     # damage / "not squishy enough" allowance
CHINA_DUTY_PCT = 0.20                  # Sec 301 7.5% + 12.5% forced-labor action (verify with broker)
AIR_DDP_FREIGHT_PER_UNIT = 0.50        # ~$6/kg DDP air, spread across light units
ENTRY_FIXED_PER_UNIT = 0.25            # $250 broker/entry amortised over ~1,000 units
FIXED_MONTHLY = 39 + 60 + 1.30         # Shopify Basic + app stack + domain
# ---------------------------------------------------------------------------


@dataclass
class Offer:
    name: str
    price: float
    cogs_landed: float          # per order, all units, landed in the US
    ship_cost: float = USPS_GROUND_ADVANTAGE_BLENDED
    shipping_charged: float = 0.0
    marketplace_pct: float = 0.0   # e.g. TikTok Shop 6% referral
    affiliate_pct: float = 0.0     # e.g. TikTok Shop affiliate 13%

    def contribution_before_cac(self) -> float:
        revenue = self.price + self.shipping_charged
        fees = revenue * SHOPIFY_CARD_PCT + SHOPIFY_CARD_FIXED
        fees += revenue * (self.marketplace_pct + self.affiliate_pct)
        returns = revenue * RETURNS_PCT
        return revenue - self.cogs_landed - PACKAGING - self.ship_cost - fees - returns

    def breakeven_roas(self) -> float:
        cm = self.contribution_before_cac()
        return float("inf") if cm <= 0 else self.price / cm


def landed_from_fob(fob: float) -> float:
    """China FOB -> landed in US (duty, freight, entry)."""
    return fob * (1 + CHINA_DUTY_PCT) + AIR_DDP_FREIGHT_PER_UNIT + ENTRY_FIXED_PER_UNIT


def main() -> None:
    offers = [
        # Phase 1 (Q4 2026): authorised US wholesale (Faire / distributor), no import, no lab testing.
        Offer("Phase 1: 3-pack curated bundle, US wholesale stock", price=34.99, cogs_landed=14.00),
        Offer("Phase 1: mystery bag (2 taba + 1 mini), US wholesale", price=24.99, cogs_landed=9.00),
        Offer("Phase 1: same 3-pack sold on TikTok Shop w/ affiliate", price=34.99, cogs_landed=14.00,
              marketplace_pct=0.06, affiliate_pct=0.13),
        # Phase 3 (2027): own-brand imported (FOB $4.80 per 3-pack, from research doc).
        Offer("Phase 3: own-brand 3-pack imported", price=29.99, cogs_landed=landed_from_fob(4.80)),
        Offer("Phase 3: own-brand 3-pack imported, $34.99", price=34.99, cogs_landed=landed_from_fob(4.80)),
        # The trap.
        Offer("TRAP: $12.99 single jumbo, free shipping", price=12.99, cogs_landed=landed_from_fob(2.00)),
        Offer("TRAP: $12.99 single + $4.95 shipping charged", price=12.99, cogs_landed=landed_from_fob(2.00),
              shipping_charged=4.95),
    ]

    print(f"{'Offer':58s} {'Price':>7s} {'COGS':>6s} {'CM/ord':>7s} {'CM%':>6s} {'BE-ROAS':>8s}")
    print("-" * 98)
    for o in offers:
        cm = o.contribution_before_cac()
        pct = cm / o.price * 100
        be = o.breakeven_roas()
        be_s = f"{be:6.2f}x" if be != float("inf") else "   n/a"
        print(f"{o.name:58s} {o.price:7.2f} {o.cogs_landed:6.2f} {cm:7.2f} {pct:5.1f}% {be_s:>8s}")

    print("\nContribution per order after blended CAC (organic/affiliate-heavy = $5, typical = $10, Meta-median = $15):")
    print(f"{'Offer':58s} {'CAC $5':>8s} {'CAC $10':>8s} {'CAC $15':>8s} {'orders to cover fixed @CAC10':>30s}")
    print("-" * 118)
    for o in offers:
        cm = o.contribution_before_cac()
        a, b, c = cm - 5, cm - 10, cm - 15
        n = "never" if b <= 0 else f"{FIXED_MONTHLY / b:.0f}"
        print(f"{o.name:58s} {a:8.2f} {b:8.2f} {c:8.2f} {n:>30s}")

    print("\nQ4 2026 scenario P&L (Phase 1 bundle, CM before CAC as above, 10-week window):")
    bundle = offers[0]
    cm = bundle.contribution_before_cac()
    for label, orders, cac in [("Bear", 150, 12.0), ("Base", 450, 8.0), ("Bull", 1200, 6.0)]:
        rev = orders * bundle.price
        profit = orders * (cm - cac) - FIXED_MONTHLY * 2.5
        print(f"  {label:4s}: {orders:5d} orders  revenue ${rev:9,.0f}  blended CAC ${cac:4.0f}  "
              f"contribution after CAC & fixed ${profit:8,.0f}")


if __name__ == "__main__":
    main()
