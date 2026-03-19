#!/usr/bin/env python3
"""Google Trends Scanner — monitors trend data for Recoveri keywords."""
import json, os, time
from datetime import datetime, timezone

OUTPUT_DIR = os.environ.get("TRENDS_OUTPUT_DIR", "/root/shared-repository/data/google-trends")

KEYWORD_GROUPS = {
    "STUDIOS": ["budget planner", "finance tracker", "google sheets template", "excel budget", "etsy digital download"],
    "TRADERS": ["crypto trading", "bitcoin price", "stock market today", "forex signals"],
    "CORE": ["ai automation", "saas startup", "no code tools", "ai agent"],
    "SOCIAL": ["faceless content", "social media automation", "tiktok growth"]
}

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    out_path = os.path.join(OUTPUT_DIR, "trends-" + date_str + ".jsonl")

    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl="en-GB", tz=0)
    except ImportError:
        print("pytrends not installed - skipping")
        return
    except Exception as e:
        print("pytrends init failed: " + str(e))
        return

    total = 0
    with open(out_path, "a") as f:
        for pillar, keywords in KEYWORD_GROUPS.items():
            try:
                pytrends.build_payload(keywords[:5], timeframe="now 7-d", geo="GB")
                interest = pytrends.interest_over_time()

                if interest.empty:
                    print("  [" + pillar + "] No data")
                    continue

                # Get latest values
                latest = interest.iloc[-1].to_dict()
                latest.pop("isPartial", None)

                entry = {
                    "scan_id": "GT-" + now.strftime("%Y%m%d") + "-" + str(total + 1).zfill(3),
                    "timestamp": now.isoformat(),
                    "pillar": pillar,
                    "keywords": keywords,
                    "latest_interest": {k: int(v) for k, v in latest.items()},
                    "source": "google_trends"
                }
                f.write(json.dumps(entry) + "\n")
                total += 1
                print("  [" + pillar + "] OK: " + str(len(latest)) + " keywords tracked")
                time.sleep(2)
            except Exception as e:
                print("  [" + pillar + "] FAIL: " + str(e))

    print("\nGoogle Trends: " + str(total) + " pillar scans -> " + out_path)

if __name__ == "__main__":
    print("Google Trends Scanner -- " + datetime.now(timezone.utc).isoformat())
    main()
