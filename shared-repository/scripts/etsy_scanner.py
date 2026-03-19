#!/usr/bin/env python3
"""Etsy Market Scanner — monitors competitor listings and trends."""
import json, os, time, re
from datetime import datetime, timezone
from urllib.request import Request, urlopen

OUTPUT_DIR = os.environ.get("ETSY_OUTPUT_DIR", "/root/shared-repository/data/etsy-scanner")

SEARCH_QUERIES = [
    "budget planner google sheets",
    "finance tracker spreadsheet",
    "budget template excel",
    "digital planner 2026",
    "savings tracker spreadsheet",
]


def fetch_etsy_search(query, limit=12):
    """Fetch Etsy search results via HTML scraping (no API key needed)."""
    search_url = "https://www.etsy.com/search?q=" + query.replace(" ", "+")
    req = Request(search_url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-GB,en;q=0.9"
    })
    try:
        resp = urlopen(req, timeout=15)
        html = resp.read().decode("utf-8", errors="ignore")
        titles = re.findall(r'"title":"([^"]{10,100})"', html)[:limit]
        prices = re.findall(r'"price":\{"amount":(\d+)', html)[:limit]
        currencies = re.findall(r'"currency_code":"([A-Z]{3})"', html)[:limit]
        results = []
        for i, title in enumerate(titles):
            price = float(prices[i]) / 100 if i < len(prices) else None
            currency = currencies[i] if i < len(currencies) else "USD"
            results.append({
                "title": title,
                "price": price,
                "currency": currency,
                "source": "html_scrape"
            })
        return results
    except Exception as e:
        return [{"error": str(e), "source": "scrape_failed"}]


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    out_path = os.path.join(OUTPUT_DIR, f"etsy-{date_str}.jsonl")

    total = 0
    with open(out_path, "a") as f:
        for query in SEARCH_QUERIES:
            results = fetch_etsy_search(query)
            entry = {
                "scan_id": f"ETSY-{now.strftime('%Y%m%d')}-{total+1:03d}",
                "timestamp": now.isoformat(),
                "query": query,
                "results": results,
                "result_count": len(results),
                "pillar": "STUDIOS"
            }
            f.write(json.dumps(entry) + "\n")
            total += len(results)
            has_error = any("error" in r for r in results)
            status = "PARTIAL" if has_error else "OK"
            print(f"  [{query[:30]}] {status}: {len(results)} results")
            time.sleep(3)

    print(f"\nEtsy Scanner: {total} results -> {out_path}")


if __name__ == "__main__":
    print(f"Etsy Market Scanner -- {datetime.now(timezone.utc).isoformat()}")
    main()
