#!/usr/bin/env python3
"""
Market Data Poller — Phase 1 (Swarm 1 prep)
Polls free-tier market APIs for crypto, stocks, and market movers.
Outputs raw JSONL to /root/shared-repository/data/market-intel/raw/

Runs every 4 hours via cron. Qwen 2 processes results downstream.
All output validated by gatekeeper before logging.

Sprint 9 | Session 12 | 19 March 2026
"""

import json
import os
import sys
import time
import hashlib
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# ============================================================
# CONFIG — from environment variables (Golden Rule 1)
# ============================================================

COINGECKO_API_KEY = os.environ.get("COINGECKO_API_KEY", "")
ALPHAVANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY", "")
FINNHUB_API_KEY = os.environ.get("FINNHUB_API_KEY", "")

OUTPUT_DIR = os.environ.get("MARKET_DATA_DIR", "/root/shared-repository/data/market-intel/raw")
LOG_FILE = os.environ.get("MARKET_LOG", "/root/shared-repository/data/market-intel/poll-log.jsonl")

# ============================================================
# HTTP HELPERS
# ============================================================

def fetch_json(url, headers=None, timeout=30):
    """Fetch JSON from URL with error handling."""
    try:
        req = Request(url)
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8")), None
    except HTTPError as e:
        return None, f"HTTP {e.code}: {e.reason}"
    except URLError as e:
        return None, f"URL error: {e.reason}"
    except Exception as e:
        return None, str(e)


# ============================================================
# DATA SOURCES
# ============================================================

def poll_coingecko():
    """Top 20 crypto by market cap from CoinGecko."""
    if not COINGECKO_API_KEY:
        return None, "COINGECKO_API_KEY not set"

    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&page=1&sparkline=false"
    headers = {"x-cg-demo-api-key": COINGECKO_API_KEY}
    data, err = fetch_json(url, headers)
    if err:
        return None, f"CoinGecko error: {err}"

    results = []
    for coin in data:
        results.append({
            "symbol": coin.get("symbol", "").upper(),
            "name": coin.get("name"),
            "price_usd": coin.get("current_price"),
            "market_cap": coin.get("market_cap"),
            "volume_24h": coin.get("total_volume"),
            "change_24h_pct": coin.get("price_change_percentage_24h"),
            "rank": coin.get("market_cap_rank"),
        })
    return results, None


def poll_alphavantage():
    """Major stock indices / top stocks from Alpha Vantage."""
    if not ALPHAVANTAGE_API_KEY:
        return None, "ALPHAVANTAGE_API_KEY not set"

    # Top gainers and losers (free endpoint)
    url = f"https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={ALPHAVANTAGE_API_KEY}"
    data, err = fetch_json(url)
    if err:
        return None, f"AlphaVantage error: {err}"

    results = []

    for category in ["top_gainers", "top_losers", "most_actively_traded"]:
        items = data.get(category, [])[:5]
        for item in items:
            results.append({
                "category": category,
                "ticker": item.get("ticker"),
                "price": item.get("price"),
                "change_amount": item.get("change_amount"),
                "change_pct": item.get("change_percentage"),
                "volume": item.get("volume"),
            })

    return results, None


def poll_finnhub():
    """US market movers from Finnhub."""
    if not FINNHUB_API_KEY:
        return None, "FINNHUB_API_KEY not set"

    # Market news (general)
    url = f"https://finnhub.io/api/v1/news?category=general&token={FINNHUB_API_KEY}"
    data, err = fetch_json(url)
    if err:
        return None, f"Finnhub error: {err}"

    results = []
    for article in (data or [])[:10]:
        results.append({
            "headline": article.get("headline"),
            "source": article.get("source"),
            "url": article.get("url"),
            "category": article.get("category"),
            "timestamp": article.get("datetime"),
            "summary": (article.get("summary") or "")[:200],
        })

    return results, None


# ============================================================
# MAIN POLLER
# ============================================================

def run_poll():
    """Execute all polls and write results."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    ts = now.isoformat()
    poll_id = f"POLL-{now.strftime('%Y%m%d-%H%M%S')}"

    sources = [
        ("coingecko", "crypto", poll_coingecko),
        ("alphavantage", "stocks", poll_alphavantage),
        ("finnhub", "news", poll_finnhub),
    ]

    results_summary = {
        "poll_id": poll_id,
        "timestamp": ts,
        "sources": {},
    }

    total_records = 0

    for source_name, data_type, poll_fn in sources:
        start = time.time()
        data, error = poll_fn()
        duration = round(time.time() - start, 2)

        if error:
            results_summary["sources"][source_name] = {
                "status": "ERROR",
                "error": error,
                "records": 0,
                "duration_seconds": duration,
            }
            print(f"  [{source_name}] ERROR: {error}")
            continue

        # Write raw data to JSONL
        output_file = os.path.join(OUTPUT_DIR, f"{source_name}-{date_str}.jsonl")
        with open(output_file, "a") as f:
            entry = {
                "poll_id": poll_id,
                "timestamp": ts,
                "source": source_name,
                "data_type": data_type,
                "record_count": len(data),
                "data": data,
            }
            f.write(json.dumps(entry, default=str) + "\n")

        results_summary["sources"][source_name] = {
            "status": "OK",
            "records": len(data),
            "duration_seconds": duration,
            "output_file": output_file,
        }
        total_records += len(data)
        print(f"  [{source_name}] OK: {len(data)} records in {duration}s")

    results_summary["total_records"] = total_records
    results_summary["overall"] = "OK" if total_records > 0 else "EMPTY"

    # Log poll result
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(results_summary, default=str) + "\n")

    return results_summary


if __name__ == "__main__":
    print(f"\n{'='*50}")
    print(f"MARKET DATA POLLER — {datetime.now(timezone.utc).isoformat()}")
    print(f"{'='*50}")

    # Check which keys are configured
    keys = {
        "CoinGecko": bool(COINGECKO_API_KEY),
        "AlphaVantage": bool(ALPHAVANTAGE_API_KEY),
        "Finnhub": bool(FINNHUB_API_KEY),
    }
    print(f"\nAPI Keys: {sum(keys.values())}/3 configured")
    for name, ok in keys.items():
        print(f"  {'✓' if ok else '✗'} {name}")

    if not any(keys.values()):
        print("\nNo API keys configured. Set COINGECKO_API_KEY, ALPHAVANTAGE_API_KEY, FINNHUB_API_KEY in /root/.env")
        sys.exit(1)

    print(f"\nPolling...\n")
    summary = run_poll()

    print(f"\n{'='*50}")
    print(f"COMPLETE: {summary['total_records']} records from {sum(1 for s in summary['sources'].values() if s['status']=='OK')}/{len(summary['sources'])} sources")
    print(f"Log: {LOG_FILE}")
    print(f"{'='*50}\n")

    sys.exit(0 if summary["overall"] == "OK" else 1)
