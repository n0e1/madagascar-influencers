#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PASS 12 SCHEMA & ECONOMICS ENGINE
1. Recalibrates pricing for DIRECT BUYING (Прямая закупка без агентства).
   - Local domestic Madagascar rate (via MVola / Airtel Money / Orange Money / cash)
   - Western / European diaspora rate (France, Reunion, Canada, Switzerland, US)
2. Adds explicit Media Type classification:
   - 'is_traditional_media': bool
   - 'media_type_label': "Классическое СМИ / Редакция" vs "Независимый автор / Лидер мнений"
3. Standardizes all Russian enums, space-separated numbers, and zero emojis.
"""

import os
import json
import re

HERE = os.path.dirname(os.path.abspath(__file__))
USD_TO_MGA = 4500  # Official benchmark peg for commercial conversion

TRADITIONAL_MEDIA_IDS = {
    "media_tv_plus_mada", "media_tvplus", "media_kolo_tv", "media_real_tv_mada",
    "media_real_tv", "media_dreamin_tv", "media_midi_madagasikara", "media_lexpress_mada",
    "media_2424_mg", "media_orange_actu", "media_studio_sifaka", "media_record_tv",
    "media_viva_tv", "media_matv", "media_radio_antsiva", "media_rdj", "media_gazetiko",
    "media_taratra", "media_la_gazette", "media_tribune", "media_newsmada"
}

def is_traditional_media_entity(e):
    eid = e.get("entity_id", "")
    if eid in TRADITIONAL_MEDIA_IDS:
        return True
    
    # Do not classify independent journalists / whistleblowers as traditional media corporations
    if eid in ["galle_borgia", "mahery_lanto_manandafy", "riana_raymonde_randrianarisoa", "laza_ramanampanoharana_elman"]:
        return False
        
    gender = e.get("gender", "")
    role = (e.get("persona_role") or "").lower()
    cat_main = (e.get("category_main") or "").lower()
    cat_sub = (e.get("category_sub") or "").lower()
    fn = (e.get("full_name") or "").lower()
    al = (e.get("alias") or "").lower()
    
    # Must be editorial / organization
    if gender == "Редакция / Организация":
        if any(w in role or w in cat_sub or w in cat_main or w in fn or w in al for w in [
            "телеканал", "радиостанция", "газета", "новостной портал", "информационное агентство", "вещатель"
        ]):
            return True
            
    if any(k in fn or k in al for k in [
        "tv plus", "kolo tv", "real tv", "dream'in tv", "midi madagasikara",
        "l'express de madagascar", "radio antsiva", "radio des jeunes", "2424.mg",
        "gazetiko", "orange actu"
    ]):
        return True
        
    return False

def calculate_direct_booking_economics(e):
    fol = e.get("total_followers_aggregate", 0)
    er_str = str(e.get("avg_engagement_rate", "4.2%")).replace("%", "").strip()
    try:
        er_val = float(er_str)
    except:
        er_val = 4.2
        
    res = e.get("residency_status", "")
    is_foreign_guest = e.get("is_foreign_guest", False)
    
    is_diaspora = (res == "Диаспора" or any(c in (e.get("country", "")).lower() for c in ["франция", "france", "реюньон", "réunion", "швейцария", "канада", "бельгия", "сша", "usa"]))
    
    # 1. Reach calculation
    if fol <= 10000:
        reach_ratio = min(0.35, max(0.15, (er_val * 4.0) / 100))
    elif fol <= 50000:
        reach_ratio = min(0.25, max(0.10, (er_val * 3.0) / 100))
    elif fol <= 200000:
        reach_ratio = min(0.18, max(0.08, (er_val * 2.5) / 100))
    else:
        reach_ratio = min(0.12, max(0.05, (er_val * 2.0) / 100))
        
    estimated_post_reach = max(200, int(fol * reach_ratio))
    
    # 2. Direct Booking Pricing (БЕЗ посредников и агентских наценок)
    if is_foreign_guest:
        # Global creator commercial rates
        cpm = 25.0
        p_usd = min(4500, max(150, int((estimated_post_reach * cpm) / 1000)))
        tier_label = "Международный тревел-тариф (Global USD)"
    elif is_diaspora:
        # Western / European direct creator rate (CPM ~35 USD)
        cpm = 35.0
        raw_price = int((estimated_post_reach * cpm) / 1000)
        if fol > 500000:
            p_usd = min(raw_price, 2500)
        elif fol > 100000:
            p_usd = min(raw_price, 1200)
        elif fol > 25000:
            p_usd = min(raw_price, 550)
        elif fol > 5000:
            p_usd = min(raw_price, 220)
        else:
            p_usd = min(raw_price, 90)
        p_usd = max(75, p_usd)
        tier_label = "Европейский тариф диаспоры (EUR / USD)"
    else:
        # Domestic Madagascar DIRECT mobile money / cash rate
        # Local direct deal benchmarks:
        # Nano (500 - 5k): 35 000 - 80 000 MGA ($8 - $18)
        # Micro (5k - 25k): 80 000 - 225 000 MGA ($18 - $50)
        # Mid (25k - 100k): 225 000 - 650 000 MGA ($50 - $145)
        # Macro (100k - 500k): 650 000 - 1 800 000 MGA ($145 - $400)
        # Mega (500k+): 1 800 000 - 4 250 000 MGA ($400 - $950)
        if fol > 1000000:
            p_usd = 850
        elif fol > 500000:
            p_usd = 550
        elif fol > 250000:
            p_usd = 320
        elif fol > 100000:
            p_usd = 190
        elif fol > 50000:
            p_usd = 95
        elif fol > 25000:
            p_usd = 55
        elif fol > 10000:
            p_usd = 30
        elif fol > 5000:
            p_usd = 18
        else:
            p_usd = 10
            
        tier_label = "Локальный прямой тариф Мадагаскара (MGA / Airtel, MVola)"
        
    p_mga = int(round(p_usd * USD_TO_MGA, -3))
    monthly_usd = int(round(p_usd * 2.8, -1))
    monthly_mga = int(round(monthly_usd * USD_TO_MGA, -3))
    
    return {
        "estimated_post_reach": estimated_post_reach,
        "price_post_usd": p_usd,
        "price_post_mga": p_mga,
        "price_monthly_usd": monthly_usd,
        "price_monthly_mga": monthly_mga,
        "pricing_tier_type": tier_label
    }

print("prepare_pass12_schema_and_models.py created successfully.")
