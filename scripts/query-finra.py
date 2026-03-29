#!/usr/bin/env python3
"""Query FINRA BrokerCheck for registration and disciplinary data.

Usage:
    python scripts/query-finra.py --crd 123456 --output workspace/finra-123456.json
    python scripts/query-finra.py --search "firm name" --output workspace/finra-search.json

Output: JSON with BrokerCheck data including registration status, disclosures, etc.
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

BROKERCHECK_BASE = "https://api.brokercheck.finra.org"
HEADERS = {
    "User-Agent": "AllocatorStack/0.1 (institutional research)",
    "Accept": "application/json",
}
RATE_LIMIT_DELAY = 0.2


def search_firms(query: str) -> dict:
    """Search for firms by name in FINRA BrokerCheck."""
    url = f"{BROKERCHECK_BASE}/search/firm?query={query}"
    time.sleep(RATE_LIMIT_DELAY)
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_firm_by_crd(crd: str) -> dict:
    """Pull BrokerCheck data for a firm by CRD number."""
    url = f"{BROKERCHECK_BASE}/firm/summary/{crd}"
    time.sleep(RATE_LIMIT_DELAY)
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json()


def main():
    parser = argparse.ArgumentParser(description="Query FINRA BrokerCheck")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--crd", type=str, help="CRD number of the firm")
    group.add_argument("--search", type=str, help="Search by firm name")
    parser.add_argument("--output", "-o", type=Path, required=True, help="Output JSON file")
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)

    try:
        if args.crd:
            result = get_firm_by_crd(args.crd)
        else:
            result = search_firms(args.search)

        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Results written to {args.output}")

    except requests.RequestException as e:
        error = {"error": str(e), "source": "finra_brokercheck"}
        with open(args.output, "w") as f:
            json.dump(error, f, indent=2)
        print(f"FINRA BrokerCheck query failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
