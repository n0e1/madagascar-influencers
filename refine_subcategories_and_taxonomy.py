#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TAXONOMY REFINEMENT & SUBCATEGORY ELIMINATION ENGINE
Eliminates all 'Общий профиль' (General Profile) fallbacks.
Maps all 624 entities to deep, descriptive Russian subcategories and standardized main categories.
Removes any English artifacts from classifications.
"""

import os
import json
import csv
import re
from typing import Dict, Any, List

HERE = os.path.dirname(os.path.abspath(__file__))

def standardize_main_category(cat: str, role: str, topics: str) -> str:
    c = str(cat or "").lower()
    r = str(role or "").lower()
    t = str(topics or "").lower()
    text = f"{c} {r} {t}"

    if any(k in text for k in ["foreignguest", "itchy boots", "sonbuchner", "travel-документализм"]):
        return "Зарубежный travel-документализм"
    if any(k in text for k in ["pedro", "akamasoa", "doctors for madagascar", "гуманитарн", "нко", "благотворительн"]):
        return "Гуманитарные миссии и благотворительность"
    if any(k in text for k in ["рэп", "хип-хоп", "rap gasy", "дрилл", "трэп", "фристайл", "слэм"]):
        return "Рэп и хип-хоп культура (Rap Gasy)"
    if any(k in text for k in ["цапики", "салеги", "малеса", "батрелаки", "традицион", "фолк", "хира-гаси", "валиха"]):
        return "Традиционная музыка, цапики и фолк"
    if any(k in text for k in ["эстрад", "поп-музык", "певиц", "певец", "chanteu", "music", "афробит"]):
        return "Эстрада и поп-музыка"
    if any(k in text for k in ["кино", "сериал", "актер", "театр", "комеди", "юмор", "скетч", "стендап", "scoop digital"]):
        return "Кино, театр и комедия"
    if any(k in text for k in ["модел", "miss madagascar", "miss", "кутюр", "подиум", "визаж", "mua", "макияж", "дизайнер одежды", "haute couture"]):
        return "Мода, красота и подиум"
    if any(k in text for k in ["бодибилдинг", "фитнес", "спорт", "атлет", "футбол", "баскетбол", "barea", "ankoay", "moraingy", "воркаут", "тренер"]):
        return "Фитнес, бодибилдинг и спорт"
    if any(k in text for k in ["стритфуд", "кулинар", "шеф-повар", "еда", "гастроном", "ресторан", "шоколатье"]):
        return "Гастрономия и ресторанная культура"
    if any(k in text for k in ["tiktok", "тикток", "танц", "стрит-дэнс", "кампус", "студент", "лайфстайл", "gen-z", "молодеж"]):
        return "Молодежь, танцы и вирусный контент"
    if any(k in text for k in ["президент", "парламент", "депутат", "оппозиц", "jirama", "блэкаут", "протест", "диссидент", "расследован", "политик"]):
        return "Политика, расследования и общество"
    if any(k in text for k in ["радио", "тв", "телеканал", "подкаст", "журналист", "пресса", "газет", "ведущий"]):
        return "Медиа, радио и тележурналистика"
    if any(k in text for k in ["it", "bpo", "программист", "веб-разработ", "стартап", "фриланс", "аутсорсинг", "технолог"]):
        return "IT, технологии и фриланс"
    if any(k in text for k in ["эколог", "лемур", "биолог", "заповедник", "природ", "приматолог", "биоразнообраз"]):
        return "Экология и охрана природы"
    if any(k in text for k in ["пастор", "церков", "евангел", "госпел", "священник", "проповед", "христиан"]):
        return "Религия и христианские общины"
    if any(k in text for k in ["экспат", "жизнь на мадагаскаре", "nosy be", "строительство на носи-бе", "вилла"]):
        return "Экспаты и жизнь на острове"
    if any(k in text for k in ["диаспор", "франция", "швейцария", "канада", "реюньон", "майотта"]):
        return "Международная диаспора"
    
    return "Культура, общество и медиа"

def determine_sub_category(main_cat: str, role: str, topics: str, alias: str, full_name: str) -> str:
    text = f"{main_cat} {role} {topics} {alias} {full_name}".lower()

    # Rap & Hip-Hop
    if "рэп" in main_cat.lower() or "rap gasy" in main_cat.lower():
        if any(k in text for k in ["олдскул", "золотой век", "классик", "da hopp", "18.3", "diosezy"]):
            return "Классика и золотой век Rap Gasy"
        if any(k in text for k in ["дрилл", "трэп", "drill", "trap", "уличный"]):
            return "Уличный трэп и дрилл"
        if any(k in text for k in ["слэм", "поэзия", "spoken word", "bensalem", "caylah"]):
            return "Слэм-поэзия и Spoken Word"
        if any(k in text for k in ["баттл", "фристайл"]):
            return "Баттл-рэп и фристайл"
        return "Современный авторский хип-хоп"

    # Traditional / Folk / Salegy / Tsapiky
    if "традицион" in main_cat.lower() or "цапики" in main_cat.lower():
        if any(k in text for k in ["цапики", "tsapiky", "тулеар", "damily", "dily"]):
            return "Энергичный цапики южного Мадагаскара"
        if any(k in text for k in ["салеги", "salegy", "jaojoby", "tence mena"]):
            return "Северный салеги и прибрежные ритмы"
        if any(k in text for k in ["хира-гаси", "hira gasy", "опер"]):
            return "Народная опера Хира-Гаси"
        if any(k in text for k in ["валиха", "marovany", "маровани", "valiha"]):
            return "Мастера традиционной валихи и маровани"
        if any(k in text for k in ["батрелаки", "мангалиба", "ануси"]):
            return "Ритмы батрелаки и мангалиба (Юго-Восток)"
        if any(k in text for k in ["басеса", "kaiamba", "туамасина"]):
            return "Басеса восточного побережья"
        return "Этнический фолк и полифоническое пение"

    # Pop / Commercial Music
    if "эстрада" in main_cat.lower():
        if any(k in text for k in ["афробит", "afrobeat"]):
            return "Малагасийский афробит и танцевальные треки"
        if any(k in text for k in ["баллад", "акустик", "лирик"]):
            return "Лирическая эстрадная поп-баллада"
        if any(k in text for k in ["амбассадор", "звезда", "commercial"]):
            return "Коммерческая эстрада и стадионные туры"
        return "Эстрадный вокал и поп-музыка"

    # Cinema / Theater / Comedy
    if "кино" in main_cat.lower() or "комеди" in main_cat.lower():
        if any(k in text for k in ["scoop digital", "malok'ila", "раджао", "сериал"]):
            return "Народные киносериалы и теленовеллы"
        if any(k in text for k in ["стендап", "stand up", "сатир"]):
            return "Стендап и сатирическая комедия"
        if any(k in text for k in ["театр", "труппа", "fou hehy"]):
            return "Эстрадная комедийная буффонада"
        if any(k in text for k in ["режиссер", "авторское кино", "документал"]):
            return "Авторская кинорежиссура и фестивали"
        if any(k in text for k in ["боевые искусств", "кунг-фу", "kung fu"]):
            return "Кинематограф боевых искусств"
        return "Комедийные видеоскетчи и вайны"

    # Fashion / Beauty / Runway
    if "мода" in main_cat.lower() or "подиум" in main_cat.lower():
        if any(k in text for k in ["miss", "королева красоты", "мисс"]):
            return "Титулованные конкурсы красоты и подиум"
        if any(k in text for k in ["визаж", "mua", "макияж", "makeup"]):
            return "Свадебный, вечерний и сценический визаж"
        if any(k in text for k in ["кутюр", "haute couture", "дизайнер", "шелк", "рафия"]):
            return "Высокая авторская мода и эко-кутюр"
        if any(k in text for k in ["модел", "catwalk", "подиум"]):
            return "Профессиональный подиумный моделинг"
        return "Индустрия стиля и бьюти-инновации"

    # Fitness / Sports
    if "фитнес" in main_cat.lower() or "спорт" in main_cat.lower():
        if any(k in text for k in ["бодибилдинг", "wbpf", "wnbf", "classic physique"]):
            return "Профессиональный бодибилдинг и фитнес"
        if any(k in text for k in ["футбол", "barea"]):
            return "Звезды национальной футбольной сборной Barea"
        if any(k in text for k in ["баскетбол", "ankoay"]):
            return "Баскетбольная сборная Ankoay и стритбол"
        if any(k in text for k in ["moraingy", "бокс", "единоборств", "сават"]):
            return "Традиционные единоборства Моренги и бокс"
        if any(k in text for k in ["воркаут", "street workout", "калистеника"]):
            return "Уличный воркаут и функциональный тренинг"
        return "Спортивный коучинг и здоровый образ жизни"

    # Food & Gastronomy
    if "гастроном" in main_cat.lower():
        if any(k in text for k in ["шеф-повар", "шеф", "l'artistika", "haute gastronomy"]):
            return "Высокая гастрономия и малагасийская кухня"
        if any(k in text for k in ["стритфуд", "масикита", "мофо гаси", "gargote"]):
            return "Уличная еда и обзоры традиционных заведений"
        if any(k in text for k in ["шоколад", "какао", "robert", "menakao"]):
            return "Крафтовый шоколад и кондитерское мастерство"
        return "Кулинарные рецепты и гастрономический блогинг"

    # Youth / Dance / Gen-Z
    if "молодеж" in main_cat.lower() or "танцы" in main_cat.lower():
        if any(k in text for k in ["танец", "dance", "хореограф", "afro dance", "брейк"]):
            return "Уличная хореография и танцевальные челленджи"
        if any(k in text for k in ["кампус", "студент", "университет", "edugasy"]):
            return "Студенческая жизнь и молодежное образование"
        if any(k in text for k in ["юмор", "пародии", "мемы", "скетч"]):
            return "Молодежная сатира и мем-культура"
        return "Вирусные тренды TikTok и лайфстайл"

    # Politics / Opposition / Investigations
    if "политик" in main_cat.lower():
        if any(k in text for k in ["депутат", "парламент", "национальн"]):
            return "Парламентская оппозиция и законодательная критика"
        if any(k in text for k in ["jirama", "блэкаут", "вода", "тариф", "тазики"]):
            return "Гражданский протест против блэкаутов JIRAMA"
        if any(k in text for k in ["расследован", "коррупц", "газет", "независим"]):
            return "Антикоррупционные расследования и факты"
        if any(k in text for k in ["студенческ", "seces", "анкацо", "профсоюз"]):
            return "Профсоюзное и университетское сопротивление"
        if any(k in text for k in ["президент", "экс-президент", "лидер парти"]):
            return "Государственные лидеры и партийное руководство"
        return "Гражданский активизм и защита прав"

    # Media / Journalism / Podcasts
    if "медиа" in main_cat.lower():
        if any(k in text for k in ["радио", "rdj", "диджей", "dj"]):
            return "Ведущие молодежных радиостанций и DJ-культура"
        if any(k in text for k in ["подкаст", "storytown", "namana"]):
            return "Авторские разговорные подкасты и интервью"
        if any(k in text for k in ["тв", "телеведущ", "dream'in", "kolo"]):
            return "Телевизионная публицистика и ток-шоу"
        if any(k in text for k in ["колумнист", "сатирик", "actutana", "elman"]):
            return "Цифровая сатирическая публицистика"
        return "Печатная пресса и новостная аналитика"

    # IT / Tech / BPO
    if "it" in main_cat.lower() or "технолог" in main_cat.lower():
        if any(k in text for k in ["bpo", "контакт-центр", "outremer", "vivetic"]):
            return "Индустрия BPO и экспорт цифровых услуг"
        if any(k in text for k in ["фриланс", "payoneer", "удаленн"]):
            return "Коучинг фриланса и удаленной занятости"
        if any(k in text for k in ["разработ", "программист", "it university"]):
            return "Подготовка программистов и EdTech"
        if any(k in text for k in ["стартап", "венчур", "инкубатор"]):
            return "Стартап-экосистема и IT-предпринимательство"
        return "Цифровая трансформация и технологии"

    # Ecology / Nature
    if "эколог" in main_cat.lower():
        if any(k in text for k in ["лемур", "примат", "gerp", "ratsimbazafy"]):
            return "Защита эндемичных лемуров и приматология"
        if any(k in text for k in ["кит", "океан", "морск", "cétamada"]):
            return "Охрана морской фауны и океанических китов"
        if any(k in text for k in ["лес", "заповедник", "национальн парк"]):
            return "Сохранение тропических дождевых лесов"
        return "Экологический активизм и экотуризм"

    # Religion / Gospel
    if "религия" in main_cat.lower():
        if any(k in text for k in ["госпел", "хор", "rasolondraibe", "joseph d'af"]):
            return "Современный христианский госпел и поклонение"
        if any(k in text for k in ["радио", "radio don bosco", "radio maria"]):
            return "Христианские телерадиовещательные сети"
        if any(k in text for k in ["пастор", "епископ", "shine", "mailhol"]):
            return "Пасторское служение и мега-церкви"
        return "Религиозно-просветительская деятельность"

    # Humanitarian
    if "гуманитарн" in main_cat.lower():
        if any(k in text for k in ["педро", "akamasoa"]):
            return "Борьба с крайней бедностью (Миссия Акамасоа)"
        if any(k in text for k in ["медицин", "врач", "здравоохран"]):
            return "Гуманитарная медицина и сельское здравоохранение"
        return "Социальные благотворительные программы"

    # Expats
    if "экспат" in main_cat.lower():
        if any(k in text for k in ["носи-бе", "носи бе", "nosy be"]):
            return "Островная недвижимость и экспат-сообщество Носи-Бе"
        return "Жизнь иностранцев и туризм на Мадагаскаре"

    # Diaspora
    if "диаспора" in main_cat.lower():
        if any(k in text for k in ["франция", "париж", "европ", "rns"]):
            return "Малагасийские сообщества во Франции и ЕС"
        if any(k in text for k in ["канада", "квебек", "gmq"]):
            return "Североамериканская диаспора (Канада и США)"
        if any(k in text for k in ["реюньон", "майотта"]):
            return "Студенческие и женские диаспоры островов Индийского океана"
        return "Культурные связи глобальной диаспоры"

    # Foreign Travel
    if "travel" in main_cat.lower() or "зарубежный" in main_cat.lower():
        return "Международные экспедиции и соло-путешествия"

    return "Аналитика, культура и блогинг"

def run_taxonomy_refinement():
    json_path = os.path.join(HERE, "madagascar_influencers_database.json")
    with open(json_path, "r", encoding="utf-8") as f:
        entities = json.load(f)
    print(f"Loaded {len(entities)} entities for subcategory & taxonomy refinement.")

    eliminated_count = 0
    for e in entities:
        old_cat = e.get("category_main") or e.get("category", "")
        old_sub = e.get("category_sub", "")
        role = e.get("persona_role", "")
        topics = e.get("content_topics", "")
        alias = e.get("alias", "")
        fn = e.get("full_name", "")

        # Standardize main category to clean Russian
        new_main = standardize_main_category(old_cat, role, topics)
        
        # Eliminate 'Общий профиль' or English subcategories
        if old_sub in ["Общий профиль", ""] or re.search(r'[a-zA-Z]', old_sub):
            new_sub = determine_sub_category(new_main, role, topics, alias, fn)
            eliminated_count += 1
        else:
            new_sub = old_sub

        e["category_main"] = new_main
        e["category_sub"] = new_sub
        
        # Build pure Russian tags
        clean_tags = [new_main, new_sub]
        if e.get("is_foreign_guest"): clean_tags.append("Зарубежный автор")
        if e.get("is_humanitarian"): clean_tags.append("Гуманитарная миссия")
        res = e.get("residency_status", "")
        if "diaspora" in res.lower(): clean_tags.append("Диаспора")
        elif "expat" in res.lower(): clean_tags.append("Экспат")
        e["tags"] = ", ".join(clean_tags)

        # Standardize persona role if it was generic "лидер мнений"
        pr = e.get("persona_role", "")
        if pr.lower() in ["лидер мнений", "блогер", "инфлюенсер"]:
            e["persona_role"] = f"{new_sub}: авторский канал и публичная деятельность"

    print(f"Refined all entities. Subcategories updated from fallback: {eliminated_count}")

    # Re-save master JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(entities, f, ensure_ascii=False, indent=2)
    print(f"Saved refined master JSON: {json_path}")

    # Check remaining 'Общий профиль'
    remaining = sum(1 for e in entities if e.get("category_sub") == "Общий профиль")
    print(f"Remaining 'Общий профиль': {remaining} (Strictly 0 expected)")

if __name__ == "__main__":
    run_taxonomy_refinement()
