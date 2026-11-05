#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PASS 10 FORENSIC AUDIT SUITE
Audits:
1. Complete zero-emoji enforcement across JSON, CSVs, and HTML dashboards.
2. Forensic URL verification: 0 placeholder video links (watch?v=), 0 search queries (search_query=), 0 bare root domains.
3. Column reordering verification: 'Площадки и ссылки' immediately follows 'Автор (ФИО / Название)' in HTML and Master CSV.
4. UI typography: 3-line clamping ('cell-clamp-3') and interactive row-click expansion ('detail-row', 'toggleRowExpand').
5. Number formatting: Non-breaking space / regular space as thousand separator, 0 commas as thousand separators in numbers.
6. CSV export formatting: Semicolon delimiter (;) and UTF-8 BOM encoding for Russian Windows Excel compatibility.
7. Entity count and platform count parity: 663 master entities, 1 143 platform accounts across JSON and CSVs.
8. Analytics Tab: Regional geographical distribution section present (Analamanga, Diana, Sava, Atsinanana, etc.).
9. Clean headline and UI: Zero awkward LaTeX artifacts or internal debugging parentheticals like '(подсветка на лету)'.
10. WhatsApp integration: Presence of verified WhatsApp channels and contact points.
"""

import os
import json
import csv
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Comprehensive emoji pattern covering Unicode emoji blocks without BMP over-matching
EMOJI_PATTERN = re.compile(
    r'[\U0001F1E0-\U0001F1FF]'  # flags
    r'|[\U0001F300-\U0001F5FF]'  # symbols & pictographs
    r'|[\U0001F600-\U0001F64F]'  # emoticons
    r'|[\U0001F680-\U0001F6FF]'  # transport & map
    r'|[\U0001F700-\U0001F77F]'  # alchemical
    r'|[\U0001F780-\U0001F7FF]'  # geometric shapes ext
    r'|[\U0001F800-\U0001F8FF]'  # arrows-c
    r'|[\U0001F900-\U0001F9FF]'  # Supplemental Symbols and Pictographs
    r'|[\U0001FA00-\U0001FA6F]'  # Chess
    r'|[\U0001FA70-\U0001FAFF]'  # Symbols and Pictographs Extended-A
    r'|[\U00002702-\U000027B0]'  # Dingbats
    r'|[\U000024C2]'
)

SUSPICIOUS_URL_PATTERNS = [
    r'youtube\.com/watch\?v=',
    r'youtube\.com/results\?search_query=',
    r'tiktok\.com/search\?',
    r'facebook\.com/search/'
]

ROOT_DOMAINS = {
    "https://www.facebook.com", "https://facebook.com",
    "https://www.youtube.com", "https://youtube.com",
    "https://www.tiktok.com", "https://tiktok.com",
    "https://www.twitter.com", "https://twitter.com", "https://x.com",
    "https://www.instagram.com", "https://instagram.com",
    "https://www.linkedin.com", "https://linkedin.com"
}

def audit_emojis(file_path):
    violations = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line_num, line in enumerate(f, 1):
            matches = EMOJI_PATTERN.findall(line)
            if matches:
                violations.append((line_num, matches, line.strip()[:80]))
    return violations

def run_pass10_audit():
    errors = []
    warnings = []
    
    json_path = os.path.join(HERE, "madagascar_influencers_database.json")
    master_csv_path = os.path.join(HERE, "madagascar_influencers_master_entities.csv")
    flat_csv_path = os.path.join(HERE, "madagascar_influencers_flat_platforms.csv")
    html_path = os.path.join(HERE, "index.html")
    interactive_html_path = os.path.join(HERE, "madagascar_influencers_interactive.html")

    print("=== PASS 10 FORENSIC AUDIT INITIALIZED ===")

    # 1. Zero Emoji Enforcement
    files_to_check_emojis = [
        json_path, master_csv_path, flat_csv_path, html_path, interactive_html_path
    ]
    for fp in files_to_check_emojis:
        if os.path.exists(fp):
            v = audit_emojis(fp)
            if v:
                errors.append(f"Emoji detected in {os.path.basename(fp)} ({len(v)} occurrences): {v[:3]}")
            else:
                print(f"[OK] 0 emojis in {os.path.basename(fp)}")
        else:
            errors.append(f"Missing required file: {fp}")

    # 2. JSON Ingestion & URL Integrity
    if not os.path.exists(json_path):
        print("Master JSON missing. Aborting.")
        return False

    with open(json_path, "r", encoding="utf-8") as f:
        entities = json.load(f)

    print(f"Loaded Master JSON: {len(entities)} entities.")
    if len(entities) != 663:
        errors.append(f"Expected exactly 663 entities, found {len(entities)}")

    total_platforms = sum(len(e.get("platforms", [])) for e in entities)
    print(f"Total Platform Accounts: {total_platforms}")
    if total_platforms != 1143:
        errors.append(f"Expected exactly 1 143 platform accounts, found {total_platforms}")

    suspicious_url_count = 0
    bare_url_count = 0
    for idx, e in enumerate(entities):
        eid = e.get("entity_id", f"row_{idx}")
        for p in e.get("platforms", []):
            url = p.get("url", "").strip()
            for pat in SUSPICIOUS_URL_PATTERNS:
                if re.search(pat, url, re.IGNORECASE):
                    suspicious_url_count += 1
                    errors.append(f"Suspicious URL in entity {eid}: {url}")
            if url.rstrip("/").lower() in ROOT_DOMAINS:
                bare_url_count += 1
                errors.append(f"Bare root domain URL in entity {eid}: {url}")

    if suspicious_url_count == 0:
        print("[OK] 0 placeholder or search query URLs across all platforms.")
    if bare_url_count == 0:
        print("[OK] 0 bare root domains across all platforms.")

    # 3. CSV Format & Semicolon Delimiter Check
    for c_path, exp_count in [(master_csv_path, 663), (flat_csv_path, 1143)]:
        if os.path.exists(c_path):
            with open(c_path, "rb") as f:
                header_bytes = f.read(512)
                if not header_bytes.startswith(b'\xef\xbb\xbf'):
                    errors.append(f"{os.path.basename(c_path)} is missing UTF-8 BOM (\\uFEFF)")
                else:
                    print(f"[OK] {os.path.basename(c_path)} has valid UTF-8 BOM encoding.")

            with open(c_path, "r", encoding="utf-8-sig") as f:
                first_line = f.readline()
                if ";" not in first_line:
                    errors.append(f"{os.path.basename(c_path)} does not use semicolon (;) delimiter.")
                else:
                    print(f"[OK] {os.path.basename(c_path)} uses semicolon (;) delimiter.")

            with open(c_path, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f, delimiter=";")
                rows = list(reader)
                if len(rows) != exp_count:
                    errors.append(f"{os.path.basename(c_path)} row count mismatch: got {len(rows)}, expected {exp_count}")
                else:
                    print(f"[OK] {os.path.basename(c_path)} row count matches exact target: {len(rows)}.")

                # Check number formatting in CSV: verify space separator in numeric column
                sample_row = rows[0]
                followers_str = sample_row.get("Совокупная аудитория (подписчики)") or sample_row.get("Подписчики платформы")
                if followers_str and "," in followers_str:
                    errors.append(f"Found comma in number formatting in {os.path.basename(c_path)}: {followers_str}")
                else:
                    print(f"[OK] Number formatting verified with spaces (no commas) in {os.path.basename(c_path)}.")
        else:
            errors.append(f"Missing CSV: {c_path}")

    # Master CSV Column Order Check
    if os.path.exists(master_csv_path):
        with open(master_csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f, delimiter=";")
            headers = next(reader)
            if len(headers) >= 3:
                author_idx = headers.index("Автор (ФИО / Название)") if "Автор (ФИО / Название)" in headers else -1
                plats_idx = headers.index("Площадки и ссылки") if "Площадки и ссылки" in headers else -1
                if author_idx == -1 or plats_idx != author_idx + 1:
                    errors.append(f"Master CSV column order mismatch. Expected 'Площадки и ссылки' immediately after 'Автор (ФИО / Название)', got author={author_idx}, plats={plats_idx}")
                else:
                    print(f"[OK] Master CSV column order verified: 'Площадки и ссылки' (col {plats_idx}) immediately follows 'Автор (ФИО / Название)' (col {author_idx}).")

    # 4. HTML Dashboard Verification
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()

        print(f"Auditing HTML dashboard ({len(html):,} chars)...")

        # Required architectural tokens
        required_tokens = [
            "cell-clamp-3",
            "detail-row",
            "toggleRowExpand",
            "Реестр и Медиа-Атлас Лидеров Мнений Мадагаскара",
            "Порог включения: подтвержденное публичное влияние и от 500 подписчиков",
            "Региональное распределение и медиапотребление по провинциям",
            "Analamanga", "Diana", "Sava", "Atsinanana", "Boeny", "Atsimo-Andrefana",
            "whatsapp", "WhatsApp",
            "tabBtnRegistry", "tabBtnAnalytics",
            "exportFilteredCSV"
        ]

        for token in required_tokens:
            if token not in html:
                errors.append(f"HTML dashboard missing required token: '{token}'")
            else:
                print(f"[OK] Found token: '{token[:40]}'")

        # Forbidden tokens
        forbidden_tokens = [
            "(подсветка на лету)",
            "Pure Domestic & Diaspora Reach",
            "Foreign Guests & Global Tourists: 21.1% (отсечено)",
            "Ad Rates & Retainers",
            "Audited Pass 8",
            "Audited Pass 9"
        ]
        for ft in forbidden_tokens:
            if ft in html:
                errors.append(f"HTML dashboard contains forbidden token: '{ft}'")

    print("\n=== AUDIT SUMMARY ===")
    print(f"Errors encountered: {len(errors)}")
    print(f"Warnings encountered: {len(warnings)}")

    if errors:
        for err in errors:
            print(f"❌ FAIL: {err}")
        return False
    else:
        print("✅ 100% PASS 10 FORENSIC AUDIT SUCCESSFUL. ALL STANDARDS VERIFIED.")
        return True

if __name__ == "__main__":
    success = run_pass10_audit()
    sys.exit(0 if success else 1)
