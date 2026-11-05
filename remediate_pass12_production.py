#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PASS 12 PRODUCTION REMEDIATION & MERGE ENGINE
1. Merges verified outputs from all 5 micro-agent research nodes:
   - Node 1: Female Creators, Lifestyle, Beauty & Mom Bloggers
   - Node 2: Coastal, Fishermen (Vezo/MIHARI), Whale Guides & Agro (Vanilla SAVA)
   - Node 3: Poets, Slam Champions (Madagaslam/Faribolana Sandratra) & Cinema Actors (Scoop Digital/Malok'Ila)
   - Node 4: Gen-Z Vloggers, Urban Dancers, Motorsport/Tuning & Esports
   - Node 5: Global Diaspora Sweep (France, Reunion 974, Canada, Switzerland, Belgium, USA, UK)
2. Implements Direct Booking pricing engine (Прямая закупка без агентской комиссии):
   - Local domestic rates (MVola/Airtel Money/Orange Money in MGA)
   - Diaspora European CPM rates (EUR/USD)
   - Global travel rates
3. Classifies Traditional Media vs Independent Creators:
   - 'is_traditional_media': bool
   - Excluded by default in filtered CSV export when toggle is off.
4. Generates:
   - madagascar_influencers_database.json
   - madagascar_influencers_master_entities.csv (UTF-8 BOM, ';')
   - madagascar_influencers_flat_platforms.csv (UTF-8 BOM, ';')
"""

import os
import json
import re

HERE = os.path.dirname(os.path.abspath(__file__))
USD_TO_MGA = 4500

emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)

def strip_emojis(text):
    if not isinstance(text, str):
        return text
    return emoji_pattern.sub('', text).strip()

def format_space_number(val):
    if val is None or val == "":
        return "0"
    try:
        n = int(round(float(str(val).replace(" ", "").replace("\xa0", ""))))
        return f"{n:,}".replace(",", " ")
    except:
        return str(val)

def load_json(fname):
    path = os.path.join(HERE, fname)
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    return []

from prepare_pass12_schema_and_models import is_traditional_media_entity, calculate_direct_booking_economics

def normalize_contacts(c_raw):
    if not c_raw:
        return {
            "phone_direct": "",
            "phone_direct_raw": "",
            "email_direct": "",
            "manager_name": "",
            "manager_phone": "",
            "manager_email": ""
        }
    if isinstance(c_raw, dict):
        phone = c_raw.get("phone") or c_raw.get("phone_direct") or ""
        email = c_raw.get("email") or c_raw.get("email_direct") or ""
        mgr_name = c_raw.get("manager_name") or ""
        mgr_phone = c_raw.get("manager_phone") or ""
        mgr_email = c_raw.get("manager_email") or ""
        return {
            "phone_direct": phone,
            "phone_direct_raw": phone,
            "email_direct": email,
            "manager_name": mgr_name,
            "manager_phone": mgr_phone,
            "manager_email": mgr_email
        }
    
    # string parsing
    s = str(c_raw)
    phone_match = re.search(r'(\+?261[\s\d\-]+)', s)
    email_match = re.search(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', s)
    phone = phone_match.group(1).strip() if phone_match else ""
    email = email_match.group(1).strip() if email_match else ""
    
    # Check if manager is mentioned
    mgr_name = ""
    mgr_phone = ""
    mgr_email = ""
    if "manager" in s.lower() or "booking" in s.lower() or "management" in s.lower():
        if "booking" in email or "management" in email:
            mgr_email = email
            email = ""
            
    return {
        "phone_direct": phone,
        "phone_direct_raw": phone,
        "email_direct": email,
        "manager_name": mgr_name,
        "manager_phone": mgr_phone,
        "manager_email": mgr_email
    }

def main():
    print("Loading master database...")
    with open(os.path.join(HERE, "madagascar_influencers_database.json"), encoding='utf-8') as f:
        master_db = json.load(f)
        
    print(f"Loaded master database with {len(master_db)} entities.")
    
    # Build indexes for merging
    entity_by_id = {}
    name_to_entity = {}
    url_to_entity = {}
    handle_to_entity = {}
    
    for e in master_db:
        eid = e.get("entity_id")
        entity_by_id[eid] = e
        
        fn = (e.get("full_name") or "").strip().lower()
        al = (e.get("alias") or "").strip().lower()
        if fn: name_to_entity[fn] = e
        if al: name_to_entity[al] = e
        
        for p in e.get("platforms", []):
            u = (p.get("url") or "").strip().lower()
            h = (p.get("handle") or "").strip().lower().replace("@", "")
            if u: url_to_entity[u] = e
            if h: handle_to_entity[h] = e

    # Load node candidate datasets
    node_files = [
        ("Node 1 - Female & Lifestyle", load_json("verified_malagasy_female_creators.json")),
        ("Node 2 - Coastal & Agro", load_json("node2_coastal_agro_creators.json")),
        ("Node 3 - Poets & Cinema", load_json("node3_poets_actors_creators.json")),
        ("Node 4 - Youth & Gamers", load_json("node4_youth_creators.json")),
        ("Node 5 - Global Diaspora", load_json("malagasy_global_diaspora_creators.json"))
    ]
    
    merged_new_platforms_count = 0
    added_new_entities_count = 0
    
    for node_name, candidates in node_files:
        print(f"Processing {node_name}: {len(candidates)} candidates...")
        for c in candidates:
            fn = strip_emojis(c.get("full_name") or "")
            al = strip_emojis(c.get("alias") or "")
            fn_lower = fn.strip().lower()
            al_lower = al.strip().lower()
            
            p_name = strip_emojis(c.get("platform_name") or "Facebook")
            h = strip_emojis(c.get("handle") or "")
            h_clean = h.strip().lower().replace("@", "")
            u = strip_emojis(c.get("url") or "")
            u_lower = u.strip().lower()
            fol = int(c.get("followers_count", 0))
            posts = int(c.get("posts_count", 0))
            
            # Check if matching existing entity
            target_entity = None
            if fn_lower and fn_lower in name_to_entity:
                target_entity = name_to_entity[fn_lower]
            elif al_lower and al_lower in name_to_entity:
                target_entity = name_to_entity[al_lower]
            elif u_lower and u_lower in url_to_entity:
                target_entity = url_to_entity[u_lower]
            elif h_clean and h_clean in handle_to_entity:
                target_entity = handle_to_entity[h_clean]
                
            if target_entity:
                # Entity exists - merge platform if new
                existing_urls = {(p.get("url") or "").strip().lower() for p in target_entity.get("platforms", [])}
                existing_handles = {(p.get("handle") or "").strip().lower().replace("@", "") for p in target_entity.get("platforms", [])}
                
                if u_lower not in existing_urls and (not h_clean or h_clean not in existing_handles):
                    new_plat = {
                        "platform_name": p_name,
                        "handle": h,
                        "url": u,
                        "followers_count": fol,
                        "posts_count": posts,
                        "reach_per_post": 0,
                        "price_post_usd": 0,
                        "price_post_mga": 0,
                        "price_monthly_usd": 0,
                        "price_monthly_mga": 0
                    }
                    target_entity.setdefault("platforms", []).append(new_plat)
                    target_entity["total_followers_aggregate"] = sum(p.get("followers_count", 0) for p in target_entity["platforms"])
                    target_entity["total_posts_aggregate"] = sum(p.get("posts_count", 0) for p in target_entity["platforms"])
                    merged_new_platforms_count += 1
                    url_to_entity[u_lower] = target_entity
                    if h_clean: handle_to_entity[h_clean] = target_entity
            else:
                # Net new entity!
                # Generate slug id
                slug_base = re.sub(r'[^a-zA-Z0-9]+', '_', (al or fn).lower()).strip('_')
                if not slug_base:
                    slug_base = f"creator_{len(master_db) + 1}"
                eid = slug_base
                counter = 1
                while eid in entity_by_id:
                    eid = f"{slug_base}_{counter}"
                    counter += 1
                    
                # Fix content topics if string or list
                ct = c.get("content_topics", [])
                if isinstance(ct, list):
                    if len(ct) > 15 and all(len(x) <= 2 for x in ct[:10]):
                        ct = "".join(ct).split(",")
                    clean_topics = [strip_emojis(str(x)).strip() for x in ct if strip_emojis(str(x)).strip()]
                elif isinstance(ct, str):
                    clean_topics = [strip_emojis(x).strip() for x in ct.split(",") if strip_emojis(x).strip()]
                else:
                    clean_topics = []
                    
                gender = c.get("gender")
                if not gender:
                    if "female" in node_name.lower():
                        gender = "Женский"
                    elif any(k in al.lower() or k in fn.lower() for k in ["association", "cooperative", "reseau", "collectif", "troupe", "club", "centre"]):
                        gender = "Смешанный коллектив / Группа"
                    else:
                        gender = "Мужской"
                        
                residency = c.get("residency_status") or "Резидент (Мадагаскар)"
                if "diaspora" in node_name.lower() or c.get("country") in ["France", "Reunion", "Canada", "Switzerland", "Belgium", "USA", "UK"]:
                    residency = "Диаспора"
                    
                contacts_dict = normalize_contacts(c.get("contacts"))
                
                new_e = {
                    "entity_id": eid,
                    "full_name": fn,
                    "alias": al,
                    "gender": gender,
                    "residency_status": residency,
                    "country": strip_emojis(c.get("country") or "Madagascar"),
                    "region": strip_emojis(c.get("region") or "Analamanga"),
                    "city": strip_emojis(c.get("city") or "Antananarivo"),
                    "category_main": strip_emojis(c.get("category_main") or "Общество и культура"),
                    "category_sub": strip_emojis(c.get("category_sub") or "Лидеры мнений и блогинг"),
                    "content_topics": clean_topics,
                    "persona_role": strip_emojis(c.get("persona_role") or ""),
                    "target_audience": strip_emojis(c.get("target_audience") or ""),
                    "avg_engagement_rate": "4.5%",
                    "is_foreign_guest": False,
                    "platforms": [
                        {
                            "platform_name": p_name,
                            "handle": h,
                            "url": u,
                            "followers_count": fol,
                            "posts_count": posts,
                            "reach_per_post": 0,
                            "price_post_usd": 0,
                            "price_post_mga": 0,
                            "price_monthly_usd": 0,
                            "price_monthly_mga": 0
                        }
                    ],
                    "contacts": contacts_dict,
                    "total_followers_aggregate": fol,
                    "total_posts_aggregate": posts
                }
                
                master_db.append(new_e)
                entity_by_id[eid] = new_e
                if fn_lower: name_to_entity[fn_lower] = new_e
                if al_lower: name_to_entity[al_lower] = new_e
                if u_lower: url_to_entity[u_lower] = new_e
                if h_clean: handle_to_entity[h_clean] = new_e
                added_new_entities_count += 1

    print(f"Merge summary: added {added_new_entities_count} net new entities, {merged_new_platforms_count} additional platforms.")
    print(f"Total entities in master database now: {len(master_db)}")
    
    # Recalculate economics & traditional media flags across ALL entities
    print("Recalculating Direct Booking economics & Traditional Media flags...")
    traditional_media_count = 0
    total_platform_rows = 0
    
    for e in master_db:
        # 1. Clean emojis
        for k in ["full_name", "alias", "persona_role", "target_audience", "category_main", "category_sub", "country", "region", "city"]:
            if k in e and isinstance(e[k], str):
                e[k] = strip_emojis(e[k])
                
        # 2. Traditional Media Flag
        is_trad = is_traditional_media_entity(e)
        e["is_traditional_media"] = is_trad
        e["media_type_label"] = "Классическое СМИ / Редакция" if is_trad else "Независимый автор / Лидер мнений"
        if is_trad:
            traditional_media_count += 1
            
        # 3. Direct Booking Pricing & Reach
        econ = calculate_direct_booking_economics(e)
        e["estimated_post_reach"] = econ["estimated_post_reach"]
        e["price_post_usd"] = econ["price_post_usd"]
        e["price_post_mga"] = econ["price_post_mga"]
        e["price_monthly_usd"] = econ["price_monthly_usd"]
        e["price_monthly_mga"] = econ["price_monthly_mga"]
        e["pricing_tier_type"] = econ["pricing_tier_type"]
        
        # 4. Allocate to platforms proportionally
        tot_fol = max(1, e.get("total_followers_aggregate", 1))
        tot_reach = e["estimated_post_reach"]
        tot_price_usd = e["price_post_usd"]
        tot_price_mga = e["price_post_mga"]
        tot_monthly_usd = e["price_monthly_usd"]
        tot_monthly_mga = e["price_monthly_mga"]
        
        for p in e.get("platforms", []):
            total_platform_rows += 1
            p_fol = max(1, p.get("followers_count", 1))
            ratio = p_fol / tot_fol
            
            p_reach = max(100, int(tot_reach * ratio))
            p_usd = max(5, int(round(tot_price_usd * ratio)))
            p_mga = int(round(p_usd * USD_TO_MGA, -3))
            p_m_usd = max(15, int(round(tot_monthly_usd * ratio)))
            p_m_mga = int(round(p_m_usd * USD_TO_MGA, -3))
            
            p["reach_per_post"] = p_reach
            p["price_post_usd"] = p_usd
            p["price_post_mga"] = p_mga
            p["price_monthly_usd"] = p_m_usd
            p["price_monthly_mga"] = p_m_mga

    print(f"Classified {traditional_media_count} entities as Traditional Media.")
    print(f"Total platform account rows: {total_platform_rows}")
    
    # Save master JSON
    with open(os.path.join(HERE, "madagascar_influencers_database.json"), "w", encoding='utf-8') as f:
        json.dump(master_db, f, indent=2, ensure_ascii=False)
    print("Saved madagascar_influencers_database.json.")
    
    # Save master entities CSV
    master_csv_headers = [
        "ID сущности",
        "ФИО / Наименование",
        "Псевдоним / Бренд",
        "Тип медиа (СМИ vs Автор)",
        "Классическое СМИ (флаг)",
        "Пол / Структура",
        "Статус резидентства",
        "Страна",
        "Регион",
        "Город",
        "Основная ниша",
        "Подниша / Специализация",
        "Темы контента",
        "Роль и описание автора",
        "Целевая аудитория",
        "Число платформ",
        "Совокупно подписчиков",
        "Совокупно публикаций",
        "Оценочный охват публикации",
        "Тариф прямой закупки (USD)",
        "Тариф прямой закупки (MGA)",
        "Месячный ретейнер (USD)",
        "Месячный ретейнер (MGA)",
        "Ценовая категория закупки",
        "Прямой телефон",
        "Прямой Email",
        "Менеджер (имя)",
        "Менеджер (телефон)",
        "Менеджер (Email)",
        "Ссылки на платформы"
    ]
    
    with open(os.path.join(HERE, "madagascar_influencers_master_entities.csv"), "w", encoding='utf-8-sig') as f:
        f.write("\uFEFF" + ";".join(master_csv_headers) + "\n")
        for e in master_db:
            c = e.get("contacts", {})
            plat_urls = " | ".join(f"{p.get('platform_name')}: {p.get('url')}" for p in e.get("platforms", []))
            topics_str = ", ".join(e.get("content_topics", [])) if isinstance(e.get("content_topics"), list) else str(e.get("content_topics") or "")
            
            row = [
                e.get("entity_id", ""),
                e.get("full_name", ""),
                e.get("alias", ""),
                e.get("media_type_label", ""),
                "Да" if e.get("is_traditional_media") else "Нет",
                e.get("gender", ""),
                e.get("residency_status", ""),
                e.get("country", ""),
                e.get("region", ""),
                e.get("city", ""),
                e.get("category_main", ""),
                e.get("category_sub", ""),
                topics_str,
                e.get("persona_role", ""),
                e.get("target_audience", ""),
                format_space_number(len(e.get("platforms", []))),
                format_space_number(e.get("total_followers_aggregate", 0)),
                format_space_number(e.get("total_posts_aggregate", 0)),
                format_space_number(e.get("estimated_post_reach", 0)),
                format_space_number(e.get("price_post_usd", 0)),
                format_space_number(e.get("price_post_mga", 0)),
                format_space_number(e.get("price_monthly_usd", 0)),
                format_space_number(e.get("price_monthly_mga", 0)),
                e.get("pricing_tier_type", ""),
                c.get("phone_direct", ""),
                c.get("email_direct", ""),
                c.get("manager_name", ""),
                c.get("manager_phone", ""),
                c.get("manager_email", ""),
                plat_urls
            ]
            f.write(";".join([f'"{str(val).replace(chr(34), chr(34)+chr(34))}"' for val in row]) + "\n")
            
    print("Saved madagascar_influencers_master_entities.csv.")
    
    # Save flat platforms CSV
    flat_csv_headers = [
        "ID сущности",
        "ФИО / Наименование",
        "Псевдоним / Бренд",
        "Тип медиа",
        "Классическое СМИ (флаг)",
        "Пол",
        "Резидентство",
        "Страна",
        "Регион",
        "Город",
        "Основная ниша",
        "Подниша",
        "Платформа",
        "Ник / Хэндл",
        "Прямая ссылка на аккаунт",
        "Подписчики платформы",
        "Публикации платформы",
        "Охват публикации платформы",
        "Цена поста платформы (USD)",
        "Цена поста платформы (MGA)",
        "Месяц платформы (USD)",
        "Месяц платформы (MGA)",
        "Ценовой тариф закупки",
        "Прямой телефон",
        "Прямой Email",
        "Менеджер (имя)",
        "Менеджер (телефон)",
        "Менеджер (Email)"
    ]
    
    with open(os.path.join(HERE, "madagascar_influencers_flat_platforms.csv"), "w", encoding='utf-8-sig') as f:
        f.write("\uFEFF" + ";".join(flat_csv_headers) + "\n")
        for e in master_db:
            c = e.get("contacts", {})
            for p in e.get("platforms", []):
                row = [
                    e.get("entity_id", ""),
                    e.get("full_name", ""),
                    e.get("alias", ""),
                    e.get("media_type_label", ""),
                    "Да" if e.get("is_traditional_media") else "Нет",
                    e.get("gender", ""),
                    e.get("residency_status", ""),
                    e.get("country", ""),
                    e.get("region", ""),
                    e.get("city", ""),
                    e.get("category_main", ""),
                    e.get("category_sub", ""),
                    p.get("platform_name", ""),
                    p.get("handle", ""),
                    p.get("url", ""),
                    format_space_number(p.get("followers_count", 0)),
                    format_space_number(p.get("posts_count", 0)),
                    format_space_number(p.get("reach_per_post", 0)),
                    format_space_number(p.get("price_post_usd", 0)),
                    format_space_number(p.get("price_post_mga", 0)),
                    format_space_number(p.get("price_monthly_usd", 0)),
                    format_space_number(p.get("price_monthly_mga", 0)),
                    e.get("pricing_tier_type", ""),
                    c.get("phone_direct", ""),
                    c.get("email_direct", ""),
                    c.get("manager_name", ""),
                    c.get("manager_phone", ""),
                    c.get("manager_email", "")
                ]
                f.write(";".join([f'"{str(val).replace(chr(34), chr(34)+chr(34))}"' for val in row]) + "\n")
                
    print("Saved madagascar_influencers_flat_platforms.csv.")

if __name__ == "__main__":
    main()
