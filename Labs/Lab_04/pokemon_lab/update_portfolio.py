#!/usr/bin/env python3
from __future__ import annotations
import os
import sys
import glob
import json
import pandas as pd

def _load_lookup_data(lookup_dir: str) -> pd.DataFrame:
    all_lookup_df: list[pd.DataFrame] = []
    json_files = sorted(glob.glob(os.path.join(lookup_dir, "*.json")))
    for path in json_files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[WARN] Skipping unreadable JSON: {path} ({e})", file=sys.stderr)
            continue
        if not isinstance(data, dict) or "data" not in data or not isinstance(data["data"], list):
            print(f"[WARN] JSON missing 'data' array: {path}", file=sys.stderr)
            continue
        df = pd.json_normalize(data["data"])
        if df.empty:
            continue
        holo = df.get("tcgplayer.prices.holofoil.market")
        normal = df.get("tcgplayer.prices.normal.market")
        df["card_market_value"] = (
            (holo if holo is not None else pd.Series([pd.NA] * len(df)))
            .fillna(normal if normal is not None else pd.Series([pd.NA] * len(df)))
        )
        df["card_market_value"] = df["card_market_value"].fillna(0.0).astype(float)
        df = df.rename(
            columns={
                "id": "card_id",
                "name": "card_name",
                "number": "card_number",
                "set.id": "set_id",
                "set.name": "set_name",
            }
        )
        required_cols = [
            "card_id",
            "card_name",
            "card_number",
            "set_id",
            "set_name",
            "card_market_value",
        ]
        for col in required_cols:
            if col not in df.columns:
                df[col] = "" if col not in ("card_market_value",) else 0.0
        all_lookup_df.append(df[required_cols].copy())
    if not all_lookup_df:
        return pd.DataFrame(
            columns=[
                "card_id",
                "card_name",
                "card_number",
                "set_id",
                "set_name",
                "card_market_value",
            ]
        )
    lookup_df = pd.concat(all_lookup_df, ignore_index=True)
    lookup_df = lookup_df.sort_values(
        by=["card_market_value", "card_id"], ascending=[False, True]
    ).drop_duplicates(subset=["card_id"], keep="first")
    lookup_df["card_number"] = lookup_df["card_number"].astype(str)
    lookup_df["set_id"] = lookup_df["set_id"].astype(str)
    return lookup_df.reset_index(drop=True)

def _load_inventory_data(inventory_dir: str) -> pd.DataFrame:
    inventory_data: list[pd.DataFrame] = []
    csv_files = sorted(glob.glob(os.path.join(inventory_dir, "*.csv")))
    for path in csv_files:
        try:
            df = pd.read_csv(path)
            inventory_data.append(df)
        except Exception as e:
            print(f"[WARN] Skipping unreadable CSV: {path} ({e})", file=sys.stderr)
    if not inventory_data:
        return pd.DataFrame(
            columns=[
                "card_name",
                "set_id",
                "card_number",
                "binder_name",
                "page_number",
                "slot_number",
                "card_id",
            ]
        )
    inventory_df = pd.concat(inventory_data, ignore_index=True)
    needed = ["set_id", "card_number"]
    for col in needed:
        if col not in inventory_df.columns:
            inventory_df[col] = ""
    inventory_df["set_id"] = inventory_df["set_id"].astype(str)
    inventory_df["card_number"] = inventory_df["card_number"].astype(str)
    inventory_df["card_id"] = inventory_df["set_id"].str.cat(
        inventory_df["card_number"], sep="-"
    )
    return inventory_df

def update_portfolio(inventory_dir: str, lookup_dir: str, output_file: str) -> None:
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)
    final_cols = [
        "index",
        "binder_name",
        "page_number",
        "slot_number",
        "card_id",
        "card_name",
        "card_number",
        "set_id",
        "set_name",
        "card_market_value",
    ]
    if inventory_df.empty:
        print("[ERROR] Inventory is empty; writing empty portfolio CSV.", file=sys.stderr)
        pd.DataFrame(columns=final_cols).to_csv(output_file, index=False)
        return
    lookup_needed = [
        "card_id",
        "card_name",
        "card_number",
        "set_id",
        "set_name",
        "card_market_value",
    ]
    if not lookup_df.empty:
        lookup_df = lookup_df[lookup_needed].copy()
    else:
        lookup_df = pd.DataFrame(columns=lookup_needed)
    merged = pd.merge(
        inventory_df,
        lookup_df,
        on="card_id",
        how="left",
        suffixes=("", "_lookup"),
    )
    merged["card_market_value"] = merged["card_market_value"].fillna(0.0).astype(float)
    merged["set_name"] = merged["set_name"].fillna("NOT_FOUND")
    for col in ("binder_name", "page_number", "slot_number"):
        if col not in merged.columns:
            merged[col] = ""
    merged["index"] = (
        merged["binder_name"].astype(str)
        + "-"
        + merged["page_number"].astype(str)
        + "-"
        + merged["slot_number"].astype(str)
    )
    for col in final_cols:
        if col not in merged.columns:
            merged[col] = ""
    merged = merged[final_cols]
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    merged.to_csv(output_file, index=False)
    print(f"[OK] Wrote portfolio to: {output_file}")

def main() -> None:
    update_portfolio(
        inventory_dir="./card_inventory/",
        lookup_dir="./card_set_lookup/",
        output_file="card_portfolio.csv",
    )

def test() -> None:
    update_portfolio(
        inventory_dir="./card_inventory_test/",
        lookup_dir="./card_set_lookup_test/",
        output_file="test_card_portfolio.csv",
    )

if __name__ == "__main__":
    print("[INFO] Running update_portfolio.py in Test Mode…", file=sys.stderr)
    test()
