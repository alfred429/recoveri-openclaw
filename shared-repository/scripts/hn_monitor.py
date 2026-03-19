#!/usr/bin/env python3
"""Hacker News Monitor — Cron 3. Tracks AI/SaaS/startup trends."""
import json, os, time
from datetime import datetime, timezone
from urllib.request import urlopen

OUTPUT_DIR = os.environ.get("HN_OUTPUT_DIR", "/root/shared-repository/data/hackernews")
RELEVANT_KW = ["ai", "saas", "automation", "startup", "digital", "no-code", "agent", "llm",
               "product", "autonomous", "gpt", "claude", "open source", "api", "machine learning"]

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    out_path = os.path.join(OUTPUT_DIR, f"hn-{date_str}.jsonl")

    top = json.loads(urlopen("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10).read())[:30]
    stories = []
    relevant = []

    for sid in top:
        try:
            s = json.loads(urlopen(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=10).read())
            title = s.get("title", "")
            story = {
                "title": title,
                "url": s.get("url", f"https://news.ycombinator.com/item?id={sid}"),
                "score": s.get("score", 0),
                "comments": s.get("descendants", 0),
                "by": s.get("by", ""),
            }
            stories.append(story)
            kw_match = [k for k in RELEVANT_KW if k in title.lower()]
            if kw_match:
                story["relevance_keywords"] = kw_match
                relevant.append(story)
            time.sleep(0.1)
        except:
            continue

    entry = {
        "scan_id": f"HN-{now.strftime('%Y%m%d')}-001",
        "timestamp": now.isoformat(),
        "source": "hackernews",
        "stories": relevant,
        "total_scanned": len(stories),
        "relevant_found": len(relevant),
        "pillar": "CORE"
    }

    with open(out_path, "a") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"HN Monitor: {len(relevant)}/{len(stories)} relevant stories -> {out_path}")
    for s in relevant[:5]:
        print(f"  [{s['score']:>4}] {s['title'][:70]}")

if __name__ == "__main__":
    print(f"HN Monitor — {datetime.now(timezone.utc).isoformat()}")
    main()
