#!/usr/bin/env python3
"""Query SEC EDGAR for ADV filing data.

Usage:
    python scripts/query-edgar.py --crd 123456 --output workspace/edgar-123456.json
    python scripts/query-edgar.py --search "firm name" --output workspace/edgar-search.json

Output: JSON with ADV filing data including AUM, employees, disciplinary history, etc.
"""
import argparse
import json
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("requests required: pip install requests", file=sys.stderr)
    sys.exit(1)

# SEC EDGAR requires a User-Agent header identifying the requester
EDGAR_BASE = "https://efts.sec.gov/LATEST"
IAPD_BASE = "https://api.adviserinfo.sec.gov/IAPD/content/search"  # SEC IAPD API
HEADERS = {
    "User-Agent": "AllocatorStack/0.1 (institutional research)",
    "Accept": "application/json",
}
# Rate limit: SEC asks for max 10 requests/second
RATE_LIMIT_DELAY = 0.1


def search_firms(query: str) -> list[dict]:
    """Search for firms by name in SEC EDGAR."""
    url = f"{EDGAR_BASE}/search-index?q={query}&dateRange=custom&startdt=2020-01-01&forms=ADV"
    time.sleep(RATE_LIMIT_DELAY)
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json().get("hits", {}).get("hits", [])


def get_adv_by_crd(crd: str) -> dict:
    """Pull ADV filing data for a firm by CRD number from SEC IAPD."""
    # SEC IAPD API: SearchType=12 searches by CRD number
    url = f"{IAPD_BASE}/genericsearch/firm?SearchValue={crd}&SearchType=12"
    time.sleep(RATE_LIMIT_DELAY)
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json()


def main():
    parser = argparse.ArgumentParser(description="Query SEC EDGAR for ADV data")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--crd", type=str, help="CRD number of the firm")
    group.add_argument("--search", type=str, help="Search by firm name")
    parser.add_argument("--output", "-o", type=Path, required=True, help="Output JSON file")
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)

    try:
        if args.crd:
            result = get_adv_by_crd(args.crd)
        else:
            result = search_firms(args.search)

        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Results written to {args.output}")

    except requests.RequestException as e:
        error = {"error": str(e), "source": "sec_edgar"}
        with open(args.output, "w") as f:
            json.dump(error, f, indent=2)
        print(f"SEC EDGAR query failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
