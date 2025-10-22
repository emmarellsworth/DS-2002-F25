#!/usr/bin/env python3
from __future__ import annotations
import os
import sys
import pandas as pd

def generate_summary(portfolio_file: str) -> None:
    if not os.path.exists(portfolio_file):
        print(f"[ERROR] File not found: {portfolio_file}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(portfolio_file)

    if df.empty:
        print("[INFO] Portfolio is empty. Nothing to report.")
        return

    if "card_market_value" not in df.columns:
        print("[ERROR] Missing required column 'card_market_value' in portfolio.", file=sys.stderr)
        sys.exit(1)

    total_portfolio_value = df["card_market_value"].fillna(0.0).sum()

    if df["card_market_value"].notna().any():
        idx = df["card_market_value"].idxmax()
        most_valuable_card = df.loc[idx]
    else:
        most_valuable_card = None

    print("=== Portfolio Summary ===")
    print(f"Total Portfolio Value: ${total_portfolio_value:,.2f}")

    if most_valuable_card is not None:
        name = str(most_valuable_card.get("card_name", "UNKNOWN"))
        cid = str(most_valuable_card.get("card_id", "UNKNOWN"))
        val = float(most_valuable_card.get("card_market_value", 0.0))
        print("Most Valuable Card:")
        print(f"  Name: {name}")
        print(f"  ID:   {cid}")
        print(f"  Value: ${val:,.2f}")
    else:
        print("Most Valuable Card: Not available (no values found)")

def main() -> None:
    generate_summary("card_portfolio.csv")

def test() -> None:
    generate_summary("test_card_portfolio.csv")

if __name__ == "__main__":
    test()
