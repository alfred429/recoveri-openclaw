#!/usr/bin/env python3
"""AI Trends Monitor — Cron 7. Tracks arXiv, HuggingFace trending, GitHub AI repos."""
import json, os, time, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from urllib.request import Request, urlopen

OUTPUT_DIR = os.environ.get("AI_OUTPUT_DIR", "/root/shared-repository/data/ai-trends")
RELEVANCE_KW = ["agent", "autonomous", "multi-agent", "orchestrat", "constitutional", "llm",
                "retrieval", "rag", "fine-tun", "instruct", "tool-use", "function-call",
                "code-gen", "digital product", "e-commerce", "saas"]

def fetch_json(url, headers=None, timeout=15):
    req = Request(url, headers=headers or {"User-Agent": "Recoveri Research Bot 1.0"})
    return json.loads(urlopen(req, timeout=timeout).read())

def fetch_arxiv():
    url = "http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.CL&sortBy=submittedDate&sortOrder=descending&max_results=20"
    req = Request(url, headers={"User-Agent": "Recoveri Research Bot 1.0"})
    root = ET.fromstring(urlopen(req, timeout=20).read())
    ns = {"a": "http://www.w3.org/2005/Atom"}
    items = []
    for entry in root.findall("a:entry", ns)[:20]:
        title = entry.findtext("a:title", "", ns).strip().replace("\n", " ")
        summary = entry.findtext("a:summary", "", ns).strip()[:200]
        link = entry.findtext("a:id", "", ns)
        pub = entry.findtext("a:published", "", ns)[:10]
        items.append({"title": title, "url": link, "published": pub, "summary": summary, "source": "arxiv"})
    return items

def fetch_github():
    url = "https://api.github.com/search/repositories?q=topic:llm+topic:ai-agent&sort=stars&order=desc&per_page=15"
    try:
        data = fetch_json(url)
        items = []
        for r in data.get("items", [])[:15]:
            items.append({
                "title": r["full_name"], "url": r["html_url"],
                "stars": r["stargazers_count"], "language": r.get("language", ""),
                "description": (r.get("description") or "")[:150], "source": "github"
            })
        return items
    except:
        return []

def tag_relevance(title, summary=""):
    text = (title + " " + summary).lower()
    matched = [k for k in RELEVANCE_KW if k in text]
    if not matched:
        return "GENERAL", [], ""
    if any(k in text for k in ["competitor", "replac", "threat"]):
        return "COMPETITIVE_INTEL", matched, "Potential competitive relevance"
    if any(k in text for k in ["new model", "release", "open source", "framework"]):
        return "OPPORTUNITY", matched, "Potential tool/model opportunity"
    return "RELEVANT", matched, "Relevant to Recoveri operations"

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    out_path = os.path.join(OUTPUT_DIR, f"ai-{date_str}.jsonl")

    all_items = []
    print("  [arxiv]", end=" ", flush=True)
    try:
        arxiv = fetch_arxiv()
        all_items.extend(arxiv)
        print(f"OK: {len(arxiv)} papers")
    except Exception as e:
        print(f"FAIL: {e}")

    time.sleep(1)
    print("  [github]", end=" ", flush=True)
    try:
        gh = fetch_github()
        all_items.extend(gh)
        print(f"OK: {len(gh)} repos")
    except Exception as e:
        print(f"FAIL: {e}")

    relevant = 0
    competitive = 0
    opportunities = 0
    for item in all_items:
        tag, kw, reason = tag_relevance(item["title"], item.get("summary", item.get("description", "")))
        item["relevance_tag"] = tag
        item["relevance_keywords"] = kw
        item["relevance_reason"] = reason
        if tag == "RELEVANT": relevant += 1
        elif tag == "COMPETITIVE_INTEL": competitive += 1
        elif tag == "OPPORTUNITY": opportunities += 1

    entry = {
        "scan_id": f"AI-{now.strftime('%Y%m%d')}-001",
        "timestamp": now.isoformat(),
        "items": all_items,
        "total_scanned": len(all_items),
        "relevant_found": relevant,
        "competitive_intel": competitive,
        "opportunities": opportunities,
        "pillar": "CORE"
    }

    with open(out_path, "a") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"\nAI Trends: {len(all_items)} items, {relevant} relevant, {competitive} competitive, {opportunities} opportunities")

if __name__ == "__main__":
    print(f"AI Trends Monitor — {datetime.now(timezone.utc).isoformat()}")
    main()
