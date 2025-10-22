#!/usr/bin/env python3
from __future__ import annotations
import sys
import update_portfolio
import generate_summary

def run_production_pipeline() -> None:
    print("[PIPELINE] Starting production pipeline…", file=sys.stderr)
    print("[PIPELINE] ETL step: building portfolio CSV…", file=sys.stderr)
    update_portfolio.main()
    print("[PIPELINE] Reporting step: generating summary…", file=sys.stderr)
    generate_summary.main()
    print("[PIPELINE] Pipeline complete.", file=sys.stderr)

if __name__ == "__main__":
    run_production_pipeline()
