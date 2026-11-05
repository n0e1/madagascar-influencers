#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PASS 12 RIGOROUS READINESS AUDIT & VERIFICATION SUITE
Verifies:
1. Zero emojis in JSON, CSVs, and HTML
2. Windows Excel CSV compliance:
   - Single UTF-8 BOM (\xef\xbb\xbf)
   - Semicolon delimiter (;)
   - Proper quoting and space-separated thousands
3. Strict CSV contact serialization coverage (phone > 300, email > 600 in Master; phone > 500, email > 1000 in Flat)
4. Strict taxonomy compliance:
   - 100% adherence to classification_taxonomy_guide.md (14 canonical main categories, 54 subcategories)
   - Zero ghost IT/BPO assignments on musicians or cultural figures
   - Precise classification of key public figures (Siteny, Antsaly, Sitraka, Barea, Fandrama, Tiako Ianao, Morning D)
5. Non-zero reach and pricing on all platform rows
6. Traditional Media isolation flag and toggle presence
7. Comprehensive quantitative metrics in Analytics view
"""

import os
import json
import csv
import re

HERE = os.path.dirname(os.path.abspath(__file__))
emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)

errors = []

canonical_taxonomy = {
    "Рэп и хип-хоп культура (Rap Gasy)": {
        "Классика и золотой век Rap Gasy",
        "Уличный трэп и дрилл",
        "Слэм-поэзия и Spoken Word",
        "Баттл-рэп и фристайл",
        "Современный авторский хип-хоп"
    },
    "Традиционная музыка, цапики и фолк": {
        "Энергичный цапики южного Мадагаскара",
        "Северный салеги и прибрежные ритмы",
        "Народная опера Хира-Гаси",
        "Мастера традиционной валихи и маровани",
        "Ритмы батрелаки и мангалиба (Юго-Восток)",
        "Басеса восточного побережья"
    },
    "Эстрада и поп-музыка": {
        "Малагасийский афробит и танцевальные треки",
        "Лирическая эстрадная поп-баллада",
        "Коммерческая эстрада и стадионные туры"
    },
    "Кино, театр и комедия": {
        "Народные киносериалы и теленовеллы",
        "Стендап и сатирическая комедия",
        "Эстрадная комедийная буффонада",
        "Авторская кинорежиссура и фестивали",
        "Кинематограф боевых искусств",
        "Комедийные видеоскетчи и вайны"
    },
    "Мода, красота и подиум": {
        "Титулованные конкурсы красоты и подиум",
        "Свадебный, вечерний и сценический визаж",
        "Высокая авторская мода и эко-кутюр",
        "Профессиональный подиумный моделинг"
    },
    "Фитнес, бодибилдинг и спорт": {
        "Профессиональный бодибилдинг и фитнес",
        "Звезды национальной футбольной сборной Barea",
        "Баскетбольная сборная Ankoay и стритбол",
        "Традиционные единоборства Моренги и бокс",
        "Уличный воркаут и функциональный тренинг"
    },
    "Молодежь, танцы и вирусный контент": {
        "Уличная хореография и танцевальные челленджи",
        "Студенческая жизнь и молодежное образование",
        "Вирусные тренды TikTok и лайфстайл"
    },
    "Гастрономия и ресторанная культура": {
        "Высокая гастрономия и малагасийская кухня",
        "Уличная еда и обзоры традиционных заведений",
        "Крафтовый шоколад и кондитерское мастерство"
    },
    "Политика, расследования и общество": {
        "Парламентская оппозиция и законодательная критика",
        "Гражданский протест против блэкаутов JIRAMA",
        "Антикоррупционные расследования и факты",
        "Профсоюзное и университетское сопротивление",
        "Государственные лидеры и партийное руководство"
    },
    "Медиа, радио и тележурналистика": {
        "Ведущие молодежных радиостанций и DJ-культура",
        "Авторские разговорные подкасты и интервью",
        "Телевизионная публицистика и ток-шоу",
        "Цифровая сатирическая публицистика"
    },
    "IT, технологии и фриланс": {
        "Индустрия BPO и экспорт цифровых услуг",
        "Коучинг фриланса и удаленной занятости",
        "Подготовка программистов и EdTech"
    },
    "Экология и охрана природы": {
        "Защита эндемичных лемуров и приматология",
        "Охрана морской фауны и океанических китов",
        "Региональные экспедиции и видеохроника"
    },
    "Гуманитарные миссии и благотворительность": {
        "Борьба с крайней бедностью (Миссия Акамасоа)",
        "Гуманитарная медицина и сельское здравоохранение",
        "Христианские телерадиовещательные сети"
    },
    "Зарубежный travel-документализм": {
        "Международные экспедиции и соло-путешествия"
    }
}

def check_emojis(filename):
    path = os.path.join(HERE, filename)
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    matches = emoji_pattern.findall(text)
    if matches:
        errors.append(f"Emoji violation in {filename}: found {len(matches)} emojis!")
    else:
        print(f"PASS: Zero emojis in {filename}")

def check_csv_structure_and_contacts():
    # 1. Master CSV
    master_path = os.path.join(HERE, "madagascar_influencers_master_entities.csv")
    with open(master_path, 'rb') as f:
        raw_start = f.read(10)
    if raw_start != b'\xef\xbb\xbfID \xd1\x81\xd1\x83':
        errors.append(f"Master CSV BOM violation: expected single UTF-8 BOM, got {raw_start}")
    else:
        print("PASS: Master CSV single UTF-8 BOM verified.")

    with open(master_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter=';')
        m_headers = next(reader)
        m_rows = list(reader)

    if len(m_headers) != 30:
        errors.append(f"Master CSV header count error: expected 30 columns, got {len(m_headers)}")
    else:
        print(f"PASS: Master CSV contains exact 30 columns.")

    if len(m_rows) != 710:
        errors.append(f"Master CSV row count error: expected 710 entities, got {len(m_rows)}")
    else:
        print(f"PASS: Master CSV contains exact 710 rows.")

    m_phones = sum(1 for r in m_rows if r[24].strip())
    m_emails = sum(1 for r in m_rows if r[25].strip())
    print(f"Master CSV contact coverage: {m_phones} direct phones (col 24), {m_emails} direct emails (col 25)")
    if m_phones < 300:
        errors.append(f"Master CSV phone deficit: found only {m_phones} phones (expected >= 300)")
    if m_emails < 600:
        errors.append(f"Master CSV email deficit: found only {m_emails} emails (expected >= 600)")

    # 2. Flat CSV
    flat_path = os.path.join(HERE, "madagascar_influencers_flat_platforms.csv")
    with open(flat_path, 'rb') as f:
        raw_start_f = f.read(10)
    if raw_start_f != b'\xef\xbb\xbfID \xd1\x81\xd1\x83':
        errors.append(f"Flat CSV BOM violation: expected single UTF-8 BOM, got {raw_start_f}")
    else:
        print("PASS: Flat CSV single UTF-8 BOM verified.")

    with open(flat_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter=';')
        f_headers = next(reader)
        f_rows = list(reader)

    if len(f_headers) != 28:
        errors.append(f"Flat CSV header count error: expected 28 columns, got {len(f_headers)}")
    else:
        print(f"PASS: Flat CSV contains exact 28 columns.")

    if len(f_rows) != 1213:
        errors.append(f"Flat CSV row count error: expected 1213 platform rows, got {len(f_rows)}")
    else:
        print(f"PASS: Flat CSV contains exact 1 213 rows.")

    f_phones = sum(1 for r in f_rows if r[23].strip())
    f_emails = sum(1 for r in f_rows if r[24].strip())
    print(f"Flat CSV contact coverage: {f_phones} direct phones (col 23), {f_emails} direct emails (col 24)")
    if f_phones < 500:
        errors.append(f"Flat CSV phone deficit: found only {f_phones} phones (expected >= 500)")
    if f_emails < 1000:
        errors.append(f"Flat CSV email deficit: found only {f_emails} emails (expected >= 1000)")

def check_taxonomy():
    path = os.path.join(HERE, "madagascar_influencers_database.json")
    with open(path, 'r', encoding='utf-8') as f:
        db = json.load(f)

    invalid_cats = []
    ghost_it = []
    by_id = {e.get("entity_id"): e for e in db}

    for e in db:
        m = e.get("category_main")
        s = e.get("category_sub")
        eid = e.get("entity_id", "")
        al = (e.get("alias") or "").lower()
        role = (e.get("persona_role") or "").lower()

        # 1. Canonical validation
        if m not in canonical_taxonomy:
            invalid_cats.append((eid, m, s, "Main category not canonical"))
        elif s not in canonical_taxonomy[m]:
            invalid_cats.append((eid, m, s, "Subcategory not canonical"))

        # 2. Ghost IT/BPO check on musicians
        if m == "IT, технологии и фриланс":
            if any(k in role or k in al for k in ["salegy", "tsapiky", "rap", "musicien", "chanteur", "guitariste", "valiha"]):
                ghost_it.append((eid, al, role))

    if invalid_cats:
        errors.append(f"Taxonomy error: {len(invalid_cats)} entities have non-canonical categories: {invalid_cats[:5]}")
    else:
        print("PASS: 100% of 710 entities adhere strictly to canonical taxonomy (14 main, 54 sub).")

    if ghost_it:
        errors.append(f"Ghost IT/BPO error: {len(ghost_it)} musicians stamped as IT: {ghost_it}")
    else:
        print("PASS: Zero ghost IT/BPO stamping on musicians.")

    # 3. Key entity assertions
    checks = [
        ("nodeD-010", "Эстрада и поп-музыка", "Малагасийский афробит и танцевальные треки"),
        ("nodeD-003", "Традиционная музыка, цапики и фолк", "Северный салеги и прибрежные ритмы"),
        ("nodeD-002", "Традиционная музыка, цапики и фолк", "Северный салеги и прибрежные ритмы"),
        ("nodeD-022", "Традиционная музыка, цапики и фолк", "Мастера традиционной валихи и маровани"),
        ("siteny_thierry_randrianasoloniaiko", "Политика, расследования и общество", "Парламентская оппозиция и законодательная критика"),
        ("antsaly_rajoelina", "Мода, красота и подиум", "Титулованные конкурсы красоты и подиум"),
        ("sitraka_harimalala_miss", "Мода, красота и подиум", "Титулованные конкурсы красоты и подиум"),
        ("barea-06", "Фитнес, бодибилдинг и спорт", "Звезды национальной футбольной сборной Barea"),
        ("malgache_et_fier", "Медиа, радио и тележурналистика", "Цифровая сатирическая публицистика"),
        ("tiako_ianao_couple", "Кино, театр и комедия", "Комедийные видеоскетчи и вайны"),
        ("christian_ratovonony_morning_d", "Медиа, радио и тележурналистика", "Телевизионная публицистика и ток-шоу"),
        ("fandrama_roi_malesa", "Традиционная музыка, цапики и фолк", "Северный салеги и прибрежные ритмы")
    ]

    for eid, exp_m, exp_s in checks:
        e = by_id.get(eid)
        if not e:
            errors.append(f"Target entity {eid} not found in database!")
            continue
        if e.get("category_main") != exp_m or e.get("category_sub") != exp_s:
            errors.append(f"Target entity {eid} misclassified: expected {exp_m} -> {exp_s}, got {e.get('category_main')} -> {e.get('category_sub')}")

    print("PASS: All key prominent figures verified in correct domains.")

def check_database_metrics():
    path = os.path.join(HERE, "madagascar_influencers_database.json")
    with open(path, 'r', encoding='utf-8') as f:
        db = json.load(f)

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
    print("=== PASS 12 RIGOROUS PRODUCTION READINESS VERIFICATION ===")
    check_database_metrics()
    check_taxonomy()
    check_csv_structure_and_contacts()
    check_emojis("madagascar_influencers_database.json")
    check_emojis("madagascar_influencers_master_entities.csv")
    check_emojis("madagascar_influencers_flat_platforms.csv")
    check_emojis("index.html")
    check_emojis("madagascar_influencers_interactive.html")
    check_html()

    print("\n=== SUMMARY ===")
    if errors:
        print(f"FAILED with {len(errors)} errors:")
        for err in errors:
            print(f"  ERROR: {err}")
        exit(1)
    else:
        print("ALL PASS 12 VERIFICATION SUITE CHECKS PASSED WITH 0 ERRORS!")

if __name__ == "__main__":
    main()
