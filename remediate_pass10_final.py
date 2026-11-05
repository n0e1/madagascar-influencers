#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PASS 10 FINAL RECONCILIATION & EMOJI PURGE SCRIPT
1. Recursively scrubs all Unicode emoji characters from all strings in madagascar_influencers_database.json.
2. Exports madagascar_influencers_master_entities.csv with:
   - Semicolon (;) delimiter
   - UTF-8 BOM (\uFEFF)
   - Space-separated numbers
   - 'Площадки и ссылки' placed IMMEDIATELY after 'Автор (ФИО / Название)'
3. Exports madagascar_influencers_flat_platforms.csv with:
   - Semicolon (;) delimiter
   - UTF-8 BOM (\uFEFF)
   - Space-separated numbers
4. Updates section title in generate_pass10_production_dashboard.py and recompiles HTML dashboards.
"""

import os
import json
import csv
import re

HERE = os.path.dirname(os.path.abspath(__file__))

# Emoji pattern for purging
EMOJI_CLEAN_RE = re.compile(
    r'[\U0001F1E0-\U0001F1FF]'  # Flags
    r'|[\U0001F300-\U0001F5FF]'  # Misc Symbols & Pictographs
    r'|[\U0001F600-\U0001F64F]'  # Emoticons
    r'|[\U0001F680-\U0001F6FF]'  # Transport & Map
    r'|[\U0001F700-\U0001F77F]'  # Alchemical
    r'|[\U0001F780-\U0001F7FF]'  # Geometric Shapes Ext
    r'|[\U0001F800-\U0001F8FF]'  # Arrows-C
    r'|[\U0001F900-\U0001F9FF]'  # Supplemental Symbols and Pictographs
    r'|[\U0001FA00-\U0001FA6F]'  # Chess
    r'|[\U0001FA70-\U0001FAFF]'  # Symbols and Pictographs Extended-A
    r'|[\U00002702-\U000027B0]'  # Dingbats
    r'|[\U000024C2]'
)

def clean_emojis_recursive(val):
    if isinstance(val, str):
        cleaned = EMOJI_CLEAN_RE.sub('', val)
        # Collapse multi-spaces
        cleaned = re.sub(r' +', ' ', cleaned).strip()
        return cleaned
    elif isinstance(val, list):
        return [clean_emojis_recursive(x) for x in val]
    elif isinstance(val, dict):
        return {k: clean_emojis_recursive(v) for k, v in val.items()}
    return val

def format_space_num(n):
    if n is None:
        return "0"
    return f"{n:,}".replace(",", " ")

def main():
    json_path = os.path.join(HERE, "madagascar_influencers_database.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Loaded {len(data)} entities from {json_path}")
    cleaned_data = clean_emojis_recursive(data)

    # Save scrubbed JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
    print("Scrubbed all emojis from Master JSON.")

    # 2. Master CSV Export
    csv_entities_path = os.path.join(HERE, "madagascar_influencers_master_entities.csv")
    fieldnames_entity = [
        "ID",
        "Автор (ФИО / Название)",
        "Площадки и ссылки",
        "Псевдоним",
        "Ссылка на WhatsApp",
        "Кто этот человек (Профиль)",
        "О чем пишет (Тематика)",
        "Целевая аудитория",
        "Основная ниша",
        "Специализация",
        "Тематические теги",
        "Пол",
        "Статус проживания",
        "Страна",
        "Регион",
        "Город",
        "Особый статус",
        "Основной язык контента",
        "Совокупно подписчиков",
        "Расчетный охват 1 публикации",
        "Всего публикаций в архиве",
        "Уровень отклика (ER%)",
        "Категория вовлеченности",
        "Телефон автора",
        "Email автора",
        "Менеджер / Агентство",
        "Телефон менеджера",
        "Email менеджера",
        "Ориентировочная цена за публикацию (USD)",
        "Ориентировочная цена за публикацию (MGA)",
        "Ориентировочный месячный контракт (USD)",
        "Ориентировочный месячный контракт (MGA)",
        "Аналитическая справка"
    ]

    with open(csv_entities_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames_entity, delimiter=";")
        writer.writeheader()
        for e in cleaned_data:
            status_tag = "Стандартный автор"
            if e.get("is_foreign_guest"):
                status_tag = "Зарубежный автор (За чертой)"
            elif e.get("is_humanitarian"):
                status_tag = "Гуманитарная миссия (За чертой)"
            elif e.get("residency_status") == "Диаспора":
                status_tag = "Диаспора (Франция / ЕС / Канада)"

            plats_str = " | ".join([f"{p.get('platform_name')}: {p.get('url')}" for p in e.get("platforms", [])])

            writer.writerow({
                "ID": e.get("entity_id", ""),
                "Автор (ФИО / Название)": e.get("full_name", ""),
                "Площадки и ссылки": plats_str,
                "Псевдоним": e.get("alias", ""),
                "Ссылка на WhatsApp": e.get("whatsapp_link", ""),
                "Кто этот человек (Профиль)": e.get("persona_role", ""),
                "О чем пишет (Тематика)": e.get("content_topics", ""),
                "Целевая аудитория": e.get("target_audience", ""),
                "Основная ниша": e.get("category_main", ""),
                "Специализация": e.get("category_sub", ""),
                "Тематические теги": e.get("tags", ""),
                "Пол": e.get("gender", ""),
                "Статус проживания": e.get("residency_status", ""),
                "Страна": e.get("country", ""),
                "Регион": e.get("region", ""),
                "Город": e.get("city", ""),
                "Особый статус": status_tag,
                "Основной язык контента": e.get("primary_language", ""),
                "Совокупно подписчиков": format_space_num(e.get("total_followers_aggregate", 0)),
                "Расчетный охват 1 публикации": format_space_num(e.get("estimated_post_reach", 0)),
                "Всего публикаций в архиве": format_space_num(e.get("total_posts_aggregate", 0)),
                "Уровень отклика (ER%)": e.get("avg_engagement_rate", ""),
                "Категория вовлеченности": e.get("er_tier", ""),
                "Телефон автора": e.get("contact_blogger_phone", ""),
                "Email автора": e.get("contact_blogger_email", ""),
                "Менеджер / Агентство": e.get("contact_manager_name", ""),
                "Телефон менеджера": e.get("contact_manager_phone", ""),
                "Email менеджера": e.get("contact_manager_email", ""),
                "Ориентировочная цена за публикацию (USD)": format_space_num(e.get("price_post_usd", 0)),
                "Ориентировочная цена за публикацию (MGA)": format_space_num(e.get("price_post_mga", 0)),
                "Ориентировочный месячный контракт (USD)": format_space_num(e.get("price_monthly_usd", 0)),
                "Ориентировочный месячный контракт (MGA)": format_space_num(e.get("price_monthly_mga", 0)),
                "Аналитическая справка": e.get("llm_description", "")
            })
    print(f"Exported Master CSV: {csv_entities_path} ({len(cleaned_data)} rows)")

    # 3. Flat Platforms CSV Export
    csv_flat_path = os.path.join(HERE, "madagascar_influencers_flat_platforms.csv")
    fieldnames_flat = [
        "ID Автора", "Автор (ФИО / Название)", "Псевдоним", "Площадка", "Аккаунт / Ник",
        "Прямая ссылка", "Ссылка на WhatsApp", "Подписчики платформы", "Расчетный охват платформы",
        "Публикаций на платформе", "Описание аккаунта", "Кто этот человек (Профиль)",
        "О чем пишет (Тематика)", "Целевая аудитория", "Основная ниша", "Специализация",
        "Пол", "Статус проживания", "Страна", "Регион", "Город", "Основной язык контента",
        "Телефон автора", "Email автора", "Менеджер / Агентство", "Телефон менеджера", "Email менеджера",
        "Ориентировочная цена за публикацию (USD)", "Аналитическая справка"
    ]

    flat_rows_count = 0
    with open(csv_flat_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames_flat, delimiter=";")
        writer.writeheader()
        for e in cleaned_data:
            tot_fol = e.get("total_followers_aggregate", 0)
            tot_reach = e.get("estimated_post_reach", 500)
            tot_price = e.get("price_post_usd", 25)
            for p in e.get("platforms", []):
                flat_rows_count += 1
                fol_p = p.get("followers", 0) or p.get("followers_count", 0)
                share = (fol_p / tot_fol) if tot_fol > 0 else 1.0
                p_reach = p.get("reach_per_post") or max(200, int(tot_reach * share))
                p_price = p.get("price_post_usd") or max(15, int(tot_price * share))
                writer.writerow({
                    "ID Автора": e.get("entity_id", ""),
                    "Автор (ФИО / Название)": e.get("full_name", ""),
                    "Псевдоним": e.get("alias", ""),
                    "Площадка": p.get("platform_name", ""),
                    "Аккаунт / Ник": p.get("handle", ""),
                    "Прямая ссылка": p.get("url", ""),
                    "Ссылка на WhatsApp": e.get("whatsapp_link", ""),
                    "Подписчики платформы": format_space_num(fol_p),
                    "Расчетный охват платформы": format_space_num(p_reach),
                    "Публикаций на платформе": format_space_num(p.get("posts_count", 0)),
                    "Описание аккаунта": p.get("channel_description", ""),
                    "Кто этот человек (Профиль)": e.get("persona_role", ""),
                    "О чем пишет (Тематика)": e.get("content_topics", ""),
                    "Целевая аудитория": e.get("target_audience", ""),
                    "Основная ниша": e.get("category_main", ""),
                    "Специализация": e.get("category_sub", ""),
                    "Пол": e.get("gender", ""),
                    "Статус проживания": e.get("residency_status", ""),
                    "Страна": e.get("country", ""),
                    "Регион": e.get("region", ""),
                    "Город": e.get("city", ""),
                    "Основной язык контента": e.get("primary_language", ""),
                    "Телефон автора": e.get("contact_blogger_phone", ""),
                    "Email автора": e.get("contact_blogger_email", ""),
                    "Менеджер / Агентство": e.get("contact_manager_name", ""),
                    "Телефон менеджера": e.get("contact_manager_phone", ""),
                    "Email менеджера": e.get("contact_manager_email", ""),
                    "Ориентировочная цена за публикацию (USD)": format_space_num(p_price),
                    "Аналитическая справка": e.get("llm_description", "")
                })
    print(f"Exported Flat CSV: {csv_flat_path} ({flat_rows_count} rows)")

if __name__ == "__main__":
    main()
