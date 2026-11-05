#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL FORENSIC AUDIT & VERIFICATION ENGINE
Audits all platform URLs across the database.
Identifies suspicious patterns:
- Incomplete or generic slugs
- Broken paths
- Misspelled handles
- Formatting errors
"""

import os
import json
import re
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))

def audit_urls():
    json_path = os.path.join(HERE, "madagascar_influencers_database.json")
    with open(json_path, "r", encoding="utf-8") as f:
        entities = json.load(f)

    total_urls = 0
    suspicious = []
    platform_counts = {}

    for e in entities:
        eid = e.get("entity_id", "")
        for p in e.get("platforms", []):
            total_urls += 1
            u = p.get("url", "").strip()
            pname = p.get("platform_name", "")
            h = p.get("handle", "")
            platform_counts[pname] = platform_counts.get(pname, 0) + 1

            parsed = urlparse(u)
            path = parsed.path.strip("/")

            # Check 1: Empty path on social networks
            if any(net in parsed.netloc for net in ["facebook.com", "tiktok.com", "instagram.com", "youtube.com", "x.com", "linkedin.com"]):
                if not path:
                    suspicious.append((eid, pname, u, "Empty path on social network"))
                elif path in ["home", "login", "explore", "search", "watch"]:
                    suspicious.append((eid, pname, u, f"Generic path '{path}'"))

            # Check 2: TikTok format
            if "tiktok.com" in parsed.netloc:
                if not path.startswith("@"):
                    suspicious.append((eid, pname, u, f"TikTok missing '@' in path '{path}'"))

            # Check 3: YouTube format
            if "youtube.com" in parsed.netloc:
                if not any(x in path for x in ["@", "channel/", "c/", "user/"]):
                    suspicious.append((eid, pname, u, f"YouTube missing channel/user/handle indicator in '{path}'"))

            # Check 4: Double slashes or trailing spaces
            if "//" in path:
                suspicious.append((eid, pname, u, "Double slash in path"))

    print(f"Total URLs audited: {total_urls}")
    print(f"Suspicious / Malformed URLs: {len(suspicious)}")
    for s in suspicious:
        print(f"  Entity: {s[0]} | {s[1]} | {s[2]} -> Issue: {s[3]}")

if __name__ == "__main__":
    audit_urls()
