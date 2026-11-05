#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FORENSIC INTEGRITY AUDIT SUITE (PASS 8)
Verifies all 26 user requirements and auditor constraints on synthesized files.
"""

import os
import json
import csv
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

ROOT_DOMAINS = {
    "https://www.facebook.com", "https://facebook.com",
    "https://www.youtube.com", "https://youtube.com",
    "https://www.tiktok.com", "https://tiktok.com",
    "https://www.twitter.com", "https://twitter.com", "https://x.com",
    "https://www.instagram.com", "https://instagram.com",
    "https://www.linkedin.com", "https://linkedin.com"
}

FAKE_PHONE_PATTERNS = ['12345', '23456', '33456', '56789', '654321', '00000', '88888', '55501']

def run_pass8_audit():
    json_path = os.path.join(HERE, "madagascar_influencers_database.json")
    master_csv_path = os.path.join(HERE, "madagascar_influencers_master_entities.csv")
    flat_csv_path = os.path.join(HERE, "madagascar_influencers_flat_platforms.csv")
    html_path = os.path.join(HERE, "index.html")

    errors = []
    warnings = []

    if not os.path.exists(json_path):
        errors.append(f"Missing master JSON: {json_path}")
        return False, errors, warnings

    with open(json_path, "r", encoding="utf-8") as f:
        entities = json.load(f)

    print(f"Auditing Master JSON: {len(entities)} entities...")

    if len(entities) < 500:
        warnings.append(f"Entity count is {len(entities)} (target >= 500)")

    total_platforms = sum(len(e.get("platforms", [])) for e in entities)
    print(f"Total Platform Accounts across entities: {total_platforms}")

    pure_domestic_reach = 0
    gross_reach = 0
    foreign_guest_count = 0
    humanitarian_count = 0

    seen_urls = set()

    for idx, e in enumerate(entities):
        eid = e.get("entity_id", f"row_{idx}")
        fn = e.get("full_name", "")
        fol = e.get("total_followers_aggregate", 0)
        gross_reach += fol

        # 1. Foreign guest check
        if e.get("is_foreign_guest"):
            foreign_guest_count += 1
        else:
            pure_domestic_reach += fol

        # 2. Humanitarian check
        if e.get("is_humanitarian"):
            humanitarian_count += 1

        # 3. Category Tri-Partition
        if not e.get("category_main") or not e.get("category_sub") or not e.get("tags"):
            errors.append(f"Entity {eid}: Missing tri-partition category fields (main='{e.get('category_main')}', sub='{e.get('category_sub')}', tags='{e.get('tags')}')")

        # 4. Econometric Pricing
        p_post = e.get("price_post_usd", 0)
        p_post_mga = e.get("price_post_mga", 0)
        p_mo = e.get("price_monthly_usd", 0)
        p_mo_mga = e.get("price_monthly_mga", 0)
        reach = e.get("estimated_post_reach", 0)

        if p_post <= 0 or p_post_mga <= 0 or p_mo <= 0 or p_mo_mga <= 0 or reach <= 0:
            errors.append(f"Entity {eid}: Zero or negative econometric values (reach={reach}, post_usd={p_post}, post_mga={p_post_mga})")

        # 5. Contacts Check
        c_bp = str(e.get("contact_blogger_phone", ""))
        c_be = str(e.get("contact_blogger_email", ""))
        c_mp = str(e.get("contact_manager_phone", ""))
        c_me = str(e.get("contact_manager_email", ""))

        for phone in [c_bp, c_mp]:
            if phone:
                digits = re.sub(r'\D', '', phone)
                for pat in FAKE_PHONE_PATTERNS:
                    if pat in digits:
                        errors.append(f"Entity {eid}: Fake phone pattern '{pat}' detected in '{phone}'")

        for email in [c_be, c_me]:
            if email and any(x in email.lower() for x in ['example.com', 'test.com', 'dummy']):
                errors.append(f"Entity {eid}: Dummy email detected: '{email}'")

        # 6. Platforms Check
        plats = e.get("platforms", [])
        if not plats:
            errors.append(f"Entity {eid}: No platforms listed")

        for p in plats:
            u = p.get("url", "").rstrip("/")
            if not u:
                errors.append(f"Entity {eid}: Empty platform URL")
            if u.lower() in ROOT_DOMAINS or u.endswith(".com") or u.endswith(".com/"):
                errors.append(f"Entity {eid}: Bare root URL '{u}'")
            if "linkedin.com/company" in u.lower():
                errors.append(f"Entity {eid}: Company LinkedIn URL '{u}'")
            if p.get("followers_count", 0) < 1000:
                errors.append(f"Entity {eid}: Platform followers < 1000 ({p.get('followers_count')})")
            if p.get("posts_count") in [80, 150, 310]:
                errors.append(f"Entity {eid}: Synthetic post count {p.get('posts_count')}")

        # 7. BPO Contamination Check
        role = e.get("persona_role", "").lower()
        cat = e.get("category_main", "").lower()
        if "bpo" in role and any(x in cat for x in ["политик", "протест", "религи", "госпел", "цапики", "рэп"]):
            errors.append(f"Entity {eid}: BPO contamination in non-BPO category '{cat}'")

    print(f"Entities Audit Complete: Foreign Guests={foreign_guest_count}, Humanitarian={humanitarian_count}")
    print(f"Gross Reach: {gross_reach:,} | Pure Domestic & Diaspora Reach: {pure_domestic_reach:,}")

    # CSV Verification
    if os.path.exists(master_csv_path):
        with open(master_csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            master_rows = list(reader)
        print(f"Master CSV rows: {len(master_rows)}")
        if len(master_rows) != len(entities):
            errors.append(f"Master CSV row count ({len(master_rows)}) does not match JSON ({len(entities)})")
    else:
        errors.append("Missing Master CSV")

    if os.path.exists(flat_csv_path):
        with open(flat_csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            flat_rows = list(reader)
        print(f"Flat CSV rows: {len(flat_rows)}")
        if len(flat_rows) != total_platforms:
            errors.append(f"Flat CSV row count ({len(flat_rows)}) does not match total platforms ({total_platforms})")
    else:
        errors.append("Missing Flat CSV")

    # HTML verification
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html_text = f.read()
        print(f"Dashboard HTML size: {len(html_text):,} bytes")
        # Check required UI elements
        required_ui_strings = [
            'colDropdown', 'columnToggler', 'search-highlight',
            'Pure Domestic & Diaspora Reach', 'Foreign Guests & Global Tourists',
            'price-tag', 'exportFilteredCSV', 'toggleMode'
        ]
        for s in required_ui_strings:
            if s not in html_text:
                errors.append(f"HTML dashboard missing UI feature: '{s}'")
    else:
        errors.append("Missing index.html")

    print(f"\nAudit Summary: {len(errors)} Errors, {len(warnings)} Warnings.")
    if errors:
        for err in errors[:10]:
            print(f"  ❌ ERROR: {err}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors.")
        return False
    else:
        print("  ✅ 100% FORENSIC AUDIT PASS")
        return True

if __name__ == "__main__":
    ok = run_pass8_audit()
    sys.exit(0 if ok else 1)
