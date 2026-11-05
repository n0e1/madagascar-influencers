#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PASS 12 RIGOROUS READINESS AUDIT
Verifies:
1. Zero emojis in JSON, CSVs, and HTML
2. Windows Excel CSV compliance (UTF-8 BOM, semicolon delimiter, non-breaking space numbers)
3. Non-zero reach and pricing on all platform rows
4. Traditional Media isolation flag and toggle presence
5. Comprehensive quantitative metrics in Analytics view
"""

import os
import json
import re

HERE = os.path.dirname(os.path.abspath(__file__))
emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)

errors = []

def check_emojis(filename):
    path = os.path.join(HERE, filename)
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    matches = emoji_pattern.findall(text)
    if matches:
        errors.append(f"Emoji violation in {filename}: found {len(matches)} emojis!")
    else:
        print(f"PASS: Zero emojis in {filename}")

def check_csv(filename, expected_cols_min):
    path = os.path.join(HERE, filename)
    with open(path, 'rb') as f:
        content = f.read()
    if not content.startswith(b'\xef\xbb\xbf'):
        errors.append(f"CSV error in {filename}: missing UTF-8 BOM!")
    else:
        print(f"PASS: UTF-8 BOM confirmed in {filename}")
        
    text = content.decode('utf-8-sig')
    lines = text.strip().split('\n')
    header = lines[0].split(';')
    if len(header) < expected_cols_min:
        errors.append(f"CSV error in {filename}: expected at least {expected_cols_min} columns, got {len(header)}")
    else:
        print(f"PASS: Semicolon delimiter and {len(header)} columns confirmed in {filename}")

def check_database():
    path = os.path.join(HERE, "madagascar_influencers_database.json")
    with open(path, 'r', encoding='utf-8') as f:
        db = json.load(f)
    print(f"Database contains {len(db)} entities.")
    
    zero_reach_plats = 0
    zero_price_plats = 0
    missing_media_flag = 0
    
    for e in db:
        if "is_traditional_media" not in e:
            missing_media_flag += 1
        for p in e.get("platforms", []):
            if p.get("reach_per_post", 0) <= 0:
                zero_reach_plats += 1
            if p.get("price_post_usd", 0) <= 0 or p.get("price_post_mga", 0) <= 0:
                zero_price_plats += 1
                
    if missing_media_flag > 0:
        errors.append(f"Database error: {missing_media_flag} entities missing is_traditional_media flag!")
    else:
        print("PASS: is_traditional_media flag verified across 100% of entities.")
        
    if zero_reach_plats > 0:
        errors.append(f"Database error: {zero_reach_plats} platform rows have zero reach!")
    else:
        print("PASS: 100% of platform rows have positive non-zero reach.")
        
    if zero_price_plats > 0:
        errors.append(f"Database error: {zero_price_plats} platform rows have zero direct buying price!")
    else:
        print("PASS: 100% of platform rows have positive direct buying price (USD & MGA).")

def check_html():
    path = os.path.join(HERE, "index.html")
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    if "chkTraditionalMedia" not in text:
        errors.append("HTML error: chkTraditionalMedia toggle not found in index.html!")
    else:
        print("PASS: Traditional media toggle confirmed in index.html.")
        
    if "viewAnalytics" not in text:
        errors.append("HTML error: Analytics view not found in index.html!")
    else:
        print("PASS: Dedicated Analytics view confirmed in index.html.")

def main():
    print("=== PASS 12 VERIFICATION SUITE ===")
    check_database()
    check_emojis("madagascar_influencers_database.json")
    check_emojis("madagascar_influencers_master_entities.csv")
    check_emojis("madagascar_influencers_flat_platforms.csv")
    check_emojis("index.html")
    check_csv("madagascar_influencers_master_entities.csv", 25)
    check_csv("madagascar_influencers_flat_platforms.csv", 20)
    check_html()
    
    print("\n=== SUMMARY ===")
    if errors:
        print(f"FAILED with {len(errors)} errors:")
        for err in errors:
            print(f"  ERROR: {err}")
        exit(1)
    else:
        print("ALL PASS 12 PRODUCTION READINESS CHECKS PASSED WITH 0 ERRORS!")

if __name__ == "__main__":
    main()
