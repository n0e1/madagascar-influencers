#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FAST URL AUDIT & PRE-FLIGHT VERIFIER
Performs asynchronous HTTP checks across all 1 103 unique URLs in the database.
Classifies URLs into:
- 200 OK (Clean)
- 404 / Dead (Definite Broken)
- Login Wall / Blocked (Needs Browser / Headless confirmation)
- Malformed / Suspicious
"""

import os
import json
import urllib.request
import urllib.error
import ssl
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5"
}

def check_url(item):
    eid, name, plat, url = item
    res = {
        "entity_id": eid,
        "name": name,
        "platform": plat,
        "url": url,
        "status": None,
        "final_url": None,
        "error": None,
        "content_length": 0,
        "title": ""
    }
    
    # Clean url
    u = url.strip()
    if not u.startswith("http"):
        res["status"] = "INVALID_URL"
        res["error"] = "Missing protocol"
        return res

    req = urllib.request.Request(u, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
            res["status"] = resp.status
            res["final_url"] = resp.geturl()
            raw = resp.read(50000)
            res["content_length"] = len(raw)
            raw_str = raw.decode("utf-8", errors="ignore")
            
            # Simple title extraction
            import re
            m = re.search(r'<title>(.*?)</title>', raw_str, re.IGNORECASE | re.DOTALL)
            if m:
                res["title"] = m.group(1).strip()
    except urllib.error.HTTPError as e:
        res["status"] = e.code
        res["error"] = str(e.reason)
    except urllib.error.URLError as e:
        res["status"] = "CONN_ERR"
        res["error"] = str(e.reason)
    except Exception as e:
        res["status"] = "ERR"
        res["error"] = str(e)
        
    return res

def main():
    json_path = os.path.join(HERE, "madagascar_influencers_database.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = []
    seen = set()
    for e in data:
        for p in e.get("platforms", []):
            u = p.get("url", "").strip()
            if u and u not in seen:
                seen.add(u)
                items.append((e["entity_id"], e["full_name"], p.get("platform_name"), u))

    print(f"Total unique URLs to pre-screen: {len(items)}")

    results = []
    start_t = time.time()
    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = {executor.submit(check_url, it): it for it in items}
        for idx, fut in enumerate(as_completed(futures), 1):
            res = fut.result()
            results.append(res)
            if idx % 100 == 0 or idx == len(items):
                print(f"Processed {idx}/{len(items)} URLs ({time.time() - start_t:.1f}s)...")

    # Analyze statuses
    status_counts = {}
    dead_or_err = []
    for r in results:
        st = r["status"]
        status_counts[st] = status_counts.get(st, 0) + 1
        if st in [404, 410, "CONN_ERR", "INVALID_URL", 500, 502, 503]:
            dead_or_err.append(r)

    print("\n--- STATUS SUMMARY ---")
    for s, c in sorted(status_counts.items(), key=lambda x: str(x[0])):
        print(f"  Status {s}: {c}")

    print(f"\nPotential dead/error URLs: {len(dead_or_err)}")
    
    out_path = os.path.join(HERE, "url_audit_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Saved complete audit log to {out_path}")

    dead_path = os.path.join(HERE, "url_dead_candidates.json")
    with open(dead_path, "w", encoding="utf-8") as f:
        json.dump(dead_or_err, f, ensure_ascii=False, indent=2)
    print(f"Saved dead/broken candidates to {dead_path}")

if __name__ == "__main__":
    main()
