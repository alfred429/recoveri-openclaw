#!/usr/bin/env python3
"""RSS News Aggregator — Cron 6. Monitors curated feeds across all pillars."""
import json, os, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError

RSS_FEEDS = {
    "CORE": [
        "https://techcrunch.com/feed/",
        "https://www.indiehackers.com/feed.xml",
    ],
    "STUDIOS": [
        "https://blog.etsy.com/en/feed/",
    ],
    "SOCIAL": [
        "https://blog.hootsuite.com/feed/",
    ],
    "TRADERS": [
        "https://cointelegraph.com/rss",
    ]
}

OUTPUT_DIR = os.environ.get("RSS_OUTPUT_DIR", "/root/shared-repository/data/rss-news")

def fetch_feed(url, timeout=15):
    req = Request(url, headers={"User-Agent": "Recoveri Research Bot 1.0"})
    try:
        resp = urlopen(req, timeout=timeout)
        return ET.fromstring(resp.read())
    except Exception as e:
        return None

def parse_rss(root):
    articles = []
    for item in root.findall(".//item")[:10]:
        title = item.findtext("title", "")
        link = item.findtext("link", "")
        pub = item.findtext("pubDate", "")
        desc = item.findtext("description", "")
        if desc and len(desc) > 200:
            desc = desc[:200] + "..."
        articles.append({"title": title, "url": link, "published": pub, "summary": desc})
    return articles

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    out_path = os.path.join(OUTPUT_DIR, f"rss-{date_str}.jsonl")
    total = 0
    
    with open(out_path, "a") as f:
        for pillar, feeds in RSS_FEEDS.items():
            for feed_url in feeds:
                domain = feed_url.split("/")[2]
                root = fetch_feed(feed_url)
                if root is None:
                    print(f"  [{domain}] FAIL")
                    continue
                articles = parse_rss(root)
                entry = {
                    "scan_id": f"RSS-{now.strftime('%Y%m%d')}-{total+1:03d}",
                    "timestamp": now.isoformat(),
                    "feed": domain,
                    "pillar": pillar,
                    "articles": articles,
                    "article_count": len(articles)
                }
                f.write(json.dumps(entry) + "\n")
                total += len(articles)
                print(f"  [{domain}] OK: {len(articles)} articles")
    
    print(f"\nRSS total: {total} articles -> {out_path}")

if __name__ == "__main__":
    print(f"RSS Monitor — {datetime.now(timezone.utc).isoformat()}")
    main()
