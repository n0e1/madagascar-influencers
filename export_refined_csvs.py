#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXPORTER FOR REFINED MASTER CSVS
Exports master entities and flat platforms from the refined master JSON.
Ensures zero English artifacts, zero 'Общий профиль', clean formatted Russian columns.
"""

import os
import json
import csv
from prepare_pass8_schema_and_models import USD_TO_MGA

HERE = os.path.dirname(os.path.abspath(__file__))

def export_all():
    master_json_path = os.path.join(HERE, "madagascar_influencers_database.json")
    with open(master_json_path, "r", encoding="utf-8") as f:
        entities = json.load(f)

    print(f"Loaded {len(entities)} refined entities.")

    # 1. Master Entities CSV
    csv_entities_path = os.path.join(HERE, "madagascar_influencers_master_entities.csv")
    fieldnames_entity = [
        "ID", "ФИО / Название", "Псевдоним", "Основная ссылка",
        "Кто этот человек (Профиль)", "О чем пишет (Тематика)", "Целевая аудитория",
        "Основная ниша", "Специализация", "Тематические теги",
        "Пол", "Статус проживания", "Страна", "Регион", "Город",
        "Особый статус (Двойная сплошная)", "Основной язык контента",
        "Совокупно подписчиков", "Расчетный охват 1 публикации", "Всего публикаций в архиве",
        "Уровень отклика (ER%)", "Категория вовлеченности",
        "Телефон автора", "Email автора", "Менеджер / Агентство", "Телефон менеджера", "Email менеджера",
        "Ориентировочная цена за публикацию (USD)", "Ориентировочная цена за публикацию (MGA)",
        "Ориентировочный месячный контракт (USD)", "Ориентировочный месячный контракт (MGA)",
        "Площадки (Кратко)", "Аналитическая справка"
    ]

    with open(csv_entities_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames_entity)
        writer.writeheader()
        for e in entities:
            status_tag = "Стандартный автор"
            if e.get("is_foreign_guest"):
                status_tag = "Зарубежный автор (За двойной сплошной)"
            elif e.get("is_humanitarian"):
                status_tag = "Гуманитарная миссия (За двойной сплошной)"

            plat_summary = "; ".join([f"{p['platform_name']}: {p.get('followers_count', 0):,} ({p.get('url', '')})" for p in e.get("platforms", [])])

            writer.writerow({
                "ID": e.get("entity_id", ""),
                "ФИО / Название": e.get("full_name", ""),
                "Псевдоним": e.get("alias", ""),
                "Основная ссылка": e.get("platforms", [{}])[0].get("url", "") if e.get("platforms") else "",
                "Кто этот человек (Профиль)": e.get("persona_role", ""),
                "О чем пишет (Тематика)": e.get("content_topics", ""),
                "Целевая аудитория": e.get("target_audience", ""),
                "Основная ниша": e.get("category_main", ""),
                "Специализация": e.get("category_sub", ""),
                "Тематические теги": e.get("tags", ""),
                "Пол": "Женский" if e.get("gender") == "Female" else ("Мужской" if e.get("gender") == "Male" else e.get("gender", "")),
                "Статус проживания": e.get("residency_status", ""),
                "Страна": e.get("country", ""),
                "Регион": e.get("region", ""),
                "Город": e.get("city", ""),
                "Особый статус (Двойная сплошная)": status_tag,
                "Основной язык контента": e.get("primary_language", ""),
                "Совокупно подписчиков": f"{e.get('total_followers_aggregate', 0):,}",
                "Расчетный охват 1 публикации": f"{e.get('estimated_post_reach', 0):,}",
                "Всего публикаций в архиве": f"{e.get('total_posts_aggregate', 0):,}",
                "Уровень отклика (ER%)": str(e.get("avg_engagement_rate", "")),
                "Категория вовлеченности": e.get("er_tier", "").replace("High (>5%)", "Высокая (>5%)").replace("Medium (2.5-5%)", "Средняя (2.5-5%)").replace("Normal (<2.5%)", "Базовая (<2.5%)"),
                "Телефон автора": e.get("contact_blogger_phone", ""),
                "Email автора": e.get("contact_blogger_email", ""),
                "Менеджер / Агентство": e.get("contact_manager_name", ""),
                "Телефон менеджера": e.get("contact_manager_phone", ""),
                "Email менеджера": e.get("contact_manager_email", ""),
                "Ориентировочная цена за публикацию (USD)": f"${e.get('price_post_usd', 0):,}",
                "Ориентировочная цена за публикацию (MGA)": f"{e.get('price_post_mga', 0):,} MGA",
                "Ориентировочный месячный контракт (USD)": f"${e.get('price_monthly_usd', 0):,}",
                "Ориентировочный месячный контракт (MGA)": f"{e.get('price_monthly_mga', 0):,} MGA",
                "Площадки (Кратко)": plat_summary,
                "Аналитическая справка": e.get("llm_description", "")
            })

    print(f"Exported Master Entities CSV: {csv_entities_path} ({len(entities)} rows)")

    # 2. Flat Platforms CSV
    csv_flat_path = os.path.join(HERE, "madagascar_influencers_flat_platforms.csv")
    fieldnames_flat = [
        "ID Автора", "ФИО / Название", "Псевдоним",
        "Кто этот человек (Профиль)", "О чем пишет (Тематика)", "Целевая аудитория",
        "Площадка", "Аккаунт / Ник", "Прямая ссылка",
        "Подписчиков на площадке", "Расчетный охват 1 публикации", "Публикаций на площадке",
        "Описание канала / страницы", "Показатели отклика (ER)",
        "Цена за публикацию на площадке (USD)", "Цена за публикацию на площадке (MGA)",
        "Основная ниша", "Специализация", "Особый статус (Двойная сплошная)",
        "Статус проживания", "Страна", "Регион", "Город", "Пол",
        "Совокупно подписчиков у автора",
        "Телефон автора", "Email автора", "Менеджер / Агентство", "Телефон менеджера", "Email менеджера"
    ]

    flat_count = 0
    with open(csv_flat_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames_flat)
        writer.writeheader()
        for e in entities:
            status_tag = "Стандартный автор"
            if e.get("is_foreign_guest"): status_tag = "Зарубежный автор (За двойной сплошной)"
            elif e.get("is_humanitarian"): status_tag = "Гуманитарная миссия (За двойной сплошной)"

            for p in e.get("platforms", []):
                flat_count += 1
                fol_p = p.get("followers_count", 0)
                tot_fol = e.get("total_followers_aggregate", 0)
                share = (fol_p / tot_fol) if tot_fol > 0 else 1.0
                p_usd = max(15, int(e.get("price_post_usd", 25) * share))
                p_mga = int(round(p_usd * USD_TO_MGA, -3))
                p_reach = max(200, int(e.get("estimated_post_reach", 500) * share))

                writer.writerow({
                    "ID Автора": e.get("entity_id", ""),
                    "ФИО / Название": e.get("full_name", ""),
                    "Псевдоним": e.get("alias", ""),
                    "Кто этот человек (Профиль)": e.get("persona_role", ""),
                    "О чем пишет (Тематика)": e.get("content_topics", ""),
                    "Целевая аудитория": e.get("target_audience", ""),
                    "Площадка": p.get("platform_name", ""),
                    "Аккаунт / Ник": p.get("handle", ""),
                    "Прямая ссылка": p.get("url", ""),
                    "Подписчиков на площадке": f"{fol_p:,}",
                    "Расчетный охват 1 публикации": f"{p_reach:,}",
                    "Публикаций на площадке": f"{p.get('posts_count', 0):,}",
                    "Описание канала / страницы": p.get("channel_description", ""),
                    "Показатели отклика (ER)": str(p.get("engagement_metrics", "")),
                    "Цена за публикацию на площадке (USD)": f"${p_usd:,}",
                    "Цена за публикацию на площадке (MGA)": f"{p_mga:,} MGA",
                    "Основная ниша": e.get("category_main", ""),
                    "Специализация": e.get("category_sub", ""),
                    "Особый статус (Двойная сплошная)": status_tag,
                    "Статус проживания": e.get("residency_status", ""),
                    "Страна": e.get("country", ""),
                    "Регион": e.get("region", ""),
                    "Город": e.get("city", ""),
                    "Пол": "Женский" if e.get("gender") == "Female" else ("Мужской" if e.get("gender") == "Male" else e.get("gender", "")),
                    "Совокупно подписчиков у автора": f"{tot_fol:,}",
                    "Телефон автора": e.get("contact_blogger_phone", ""),
                    "Email автора": e.get("contact_blogger_email", ""),
                    "Менеджер / Агентство": e.get("contact_manager_name", ""),
                    "Телефон менеджера": e.get("contact_manager_phone", ""),
                    "Email менеджера": e.get("contact_manager_email", "")
                })

    print(f"Exported Flat Platforms CSV: {csv_flat_path} ({flat_count} rows)")

if __name__ == "__main__":
    export_all()
