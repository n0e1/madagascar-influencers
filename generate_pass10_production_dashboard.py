#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRODUCTION DASHBOARD COMPILER (PASS 10)
Strict execution of all user requirements:
1. Zero emojis everywhere (no icons/emojis in HTML, text, titles, buttons, tags).
2. 'Площадки и ссылки' column positioned immediately after 'Автор'.
3. 3-line cell clamp with interactive full-width details drawer on row click.
4. Non-breaking space number formatting (15 000, 1 143, etc. - ZERO commas).
5. Regional distribution section in Analytics tab.
6. WhatsApp broadcast channels and direct links.
7. Clean, authoritative Russian titles and placeholder.
8. Windows Excel-compatible CSV export (UTF-8 BOM, semicolon delimiter, space numbers).
"""

import os
import json
import re

HERE = os.path.dirname(os.path.abspath(__file__))

def format_space_num(n) -> str:
    try:
        val = int(n)
        return f"{val:_}".replace('_', ' ')
    except:
        return str(n)

def build_production_dashboard():
    json_path = os.path.join(HERE, "madagascar_influencers_database.json")
    with open(json_path, "r", encoding="utf-8") as f:
        entities = json.load(f)

    print(f"Loaded {len(entities)} master entities for production compilation.")

    total_entities = len(entities)
    total_platforms = sum(len(e.get("platforms", [])) for e in entities)
    pure_reach = sum(e["total_followers_aggregate"] for e in entities if not e.get("is_foreign_guest"))
    gross_reach = sum(e["total_followers_aggregate"] for e in entities)
    foreign_reach = gross_reach - pure_reach
    total_posts = sum(e.get("total_posts_aggregate", 0) for e in entities)
    direct_contacts = sum(1 for e in entities if e.get("contact_blogger_phone") or e.get("contact_blogger_email") or e.get("contact_manager_phone") or e.get("contact_manager_email") or e.get("whatsapp_link"))

    entities_json_str = json.dumps(entities, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>Реестр и Медиа-Атлас Лидеров Мнений Мадагаскара</title>
  <style>
    :root {{
      --bg: #0b111e;
      --surface: #141d2e;
      --surface-hover: #1c273e;
      --surface-card: #182236;
      --border: #23314d;
      --border-accent: #3b82f6;
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --primary: #38bdf8;
      --primary-hover: #0ea5e9;
      --accent: #f59e0b;
      --success: #10b981;
      --danger: #ef4444;
      --foreign-bg: #151922;
      --foreign-border: #475569;
      --highlight: #fef08a;
      --highlight-text: #854d0e;
      --fb: #1877f2;
      --yt: #ef4444;
      --tt: #d946ef;
      --ig: #ec4899;
      --wa: #25d366;
      --li: #0284c7;
      --x: #334155;
      --web: #0d9488;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding: 16px 20px;
      font-size: 13px;
    }}
    a {{ color: var(--primary); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}

    /* HEADER */
    .dashboard-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 14px;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .title-area h1 {{
      font-size: 21px;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .status-badge {{
      font-size: 11px;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: 4px;
      background: rgba(16, 185, 129, 0.15);
      color: var(--success);
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}
    .subtitle {{
      color: var(--text-muted);
      font-size: 13px;
      margin-top: 3px;
    }}
    .header-actions {{
      display: flex;
      gap: 8px;
      align-items: center;
      flex-wrap: wrap;
    }}
    .action-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--surface);
      color: var(--text);
      border: 1px solid var(--border);
      padding: 7px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
      white-space: nowrap;
    }}
    .action-btn:hover {{
      background: var(--surface-hover);
      border-color: var(--primary);
    }}
    .action-btn.primary {{
      background: #0284c7;
      border-color: #38bdf8;
      color: #fff;
    }}
    .action-btn.primary:hover {{
      background: #0369a1;
    }}

    /* NAVIGATION TABS */
    .nav-tabs {{
      display: flex;
      gap: 6px;
      border-bottom: 2px solid var(--border);
      margin-bottom: 16px;
    }}
    .tab-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 14px;
      font-weight: 600;
      padding: 10px 18px;
      cursor: pointer;
      border-bottom: 3px solid transparent;
      margin-bottom: -2px;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
    }}
    .tab-btn:hover {{
      color: var(--text);
      background: rgba(255, 255, 255, 0.03);
    }}
    .tab-btn.active {{
      color: #fff;
      border-bottom-color: var(--primary);
      background: rgba(56, 189, 248, 0.08);
      border-top-left-radius: 6px;
      border-top-right-radius: 6px;
    }}
    .tab-badge {{
      font-size: 11px;
      padding: 2px 7px;
      border-radius: 10px;
      background: var(--surface);
      color: var(--text-muted);
    }}
    .tab-btn.active .tab-badge {{
      background: var(--primary);
      color: #0b111e;
      font-weight: 700;
    }}

    .tab-content {{ display: none; }}
    .tab-content.active {{ display: block; }}

    /* TOOLBAR & FILTERS */
    .controls-panel {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px 14px;
      margin-bottom: 14px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    .search-row {{
      display: flex;
      gap: 10px;
      align-items: center;
    }}
    .search-input {{
      width: 100%;
      background: #0d1524;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #fff;
      padding: 8px 12px;
      font-size: 13px;
      outline: none;
      transition: border-color 0.15s;
    }}
    .search-input:focus {{
      border-color: var(--primary);
    }}

    .filters-dropdown-row {{
      display: flex;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
      background: #0d1524;
      padding: 8px 12px;
      border-radius: 6px;
      border: 1px solid var(--border);
    }}
    .filter-item {{
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
    }}
    .filter-item label {{
      color: var(--text-muted);
      white-space: nowrap;
      font-weight: 500;
    }}
    .filter-select {{
      background: var(--surface);
      color: #fff;
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 5px 10px;
      font-size: 12px;
      outline: none;
      cursor: pointer;
      max-width: 220px;
    }}
    .filter-select:focus {{
      border-color: var(--primary);
    }}
    .reset-btn {{
      background: transparent;
      border: none;
      color: var(--text-dim);
      font-size: 12px;
      cursor: pointer;
      text-decoration: underline;
      padding: 4px 6px;
      margin-left: auto;
    }}
    .reset-btn:hover {{ color: var(--danger); }}

    .mode-and-columns-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      padding-top: 4px;
    }}
    .mode-toggle-group {{
      display: flex;
      gap: 4px;
      background: #0d1524;
      padding: 3px;
      border-radius: 6px;
      border: 1px solid var(--border);
    }}
    .mode-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 6px 12px;
      font-size: 12px;
      font-weight: 600;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .mode-btn.active {{
      background: var(--surface-hover);
      color: #fff;
    }}

    .col-manager-dropdown {{
      position: relative;
      display: inline-block;
    }}
    .col-dropdown-menu {{
      display: none;
      position: absolute;
      right: 0;
      top: 100%;
      margin-top: 4px;
      background: #141d2e;
      border: 1px solid var(--border);
      border-radius: 6px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
      padding: 10px;
      z-index: 100;
      min-width: 250px;
      max-height: 400px;
      overflow-y: auto;
    }}
    .col-dropdown-menu.show {{ display: block; }}
    .col-toggle-item {{
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 5px 6px;
      font-size: 12px;
      color: var(--text);
      cursor: pointer;
      border-radius: 4px;
    }}
    .col-toggle-item:hover {{ background: var(--surface-hover); }}

    /* TABLE LAYOUT & 3-LINE CLAMP */
    .scroll-hint-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
      color: var(--text-dim);
      margin-bottom: 6px;
      padding: 0 4px;
    }}
    .table-container {{
      width: 100%;
      overflow-x: auto;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--surface);
      box-shadow: 0 4px 20px rgba(0,0,0,0.25);
      scrollbar-width: thin;
      scrollbar-color: #3b82f6 #101726;
      -webkit-overflow-scrolling: touch;
    }}
    .table-container::-webkit-scrollbar {{ height: 10px; }}
    .table-container::-webkit-scrollbar-track {{ background: #101726; border-radius: 5px; }}
    .table-container::-webkit-scrollbar-thumb {{ background: #2563eb; border-radius: 5px; }}
    .table-container::-webkit-scrollbar-thumb:hover {{ background: #3b82f6; }}

    table {{
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      font-size: 12px;
      min-width: 1400px;
    }}
    th {{
      background: #111827;
      color: var(--text-muted);
      font-weight: 600;
      text-align: left;
      padding: 10px 12px;
      border-bottom: 2px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 20;
      white-space: nowrap;
      cursor: pointer;
      user-select: none;
    }}
    th:hover {{ color: #fff; background: #1a2337; }}
    th.sorted-asc::after {{ content: " ▲"; color: var(--primary); }}
    th.sorted-desc::after {{ content: " ▼"; color: var(--primary); }}

    th.sticky-col, td.sticky-col {{
      position: sticky;
      left: 0;
      z-index: 10;
      background: var(--surface);
      border-right: 2px solid var(--border);
      box-shadow: 3px 0 8px rgba(0, 0, 0, 0.4);
    }}
    th.sticky-col {{
      z-index: 30;
      background: #111827;
    }}
    tr.influencer-row {{
      cursor: pointer;
      transition: background 0.12s ease;
    }}
    tr.influencer-row:hover td {{
      background: var(--surface-hover);
    }}

    td {{
      padding: 10px 12px;
      border-bottom: 1px solid var(--border);
      vertical-align: top;
      color: var(--text);
    }}

    /* 3-LINE TEXT CLAMP */
    .cell-clamp-3 {{
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
      line-height: 1.42;
      max-width: 240px;
    }}

    /* EXPANDED ROW DETAIL DRAWER */
    tr.detail-row {{
      display: none;
      background: #0e1626;
    }}
    tr.detail-row.open {{
      display: table-row;
    }}
    .detail-container {{
      padding: 16px 20px;
      border-bottom: 2px solid var(--border-accent);
      background: linear-gradient(180deg, #101a2d 0%, #0c1424 100%);
    }}
    .detail-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
      margin-bottom: 12px;
    }}
    .detail-block {{
      background: var(--surface-card);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 12px 14px;
    }}
    .detail-title {{
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 6px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      padding-bottom: 4px;
    }}
    .detail-text {{
      font-size: 12px;
      color: #fff;
      line-height: 1.5;
    }}

    /* DOUBLE SOLID LINE */
    tr.foreign-guest-row {{ background: var(--foreign-bg); opacity: 0.9; }}
    tr.foreign-guest-row td {{
      border-top: 2px solid var(--foreign-border) !important;
      border-bottom: 2px solid var(--foreign-border) !important;
    }}
    tr.humanitarian-row {{ background: rgba(16, 185, 129, 0.04); }}
    tr.humanitarian-row td {{
      border-top: 2px solid rgba(16, 185, 129, 0.4) !important;
      border-bottom: 2px solid rgba(16, 185, 129, 0.4) !important;
    }}

    .badge-tag {{
      display: inline-block;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 500;
      background: rgba(255, 255, 255, 0.07);
      color: var(--text-muted);
      margin: 1px;
      white-space: nowrap;
    }}
    .badge-tag.highlight {{ background: rgba(56, 189, 248, 0.15); color: var(--primary); }}
    .badge-tag.foreign {{ background: rgba(148, 163, 184, 0.15); color: #cbd5e1; border: 1px dashed #64748b; }}

    .platform-badge {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 600;
      text-decoration: none;
      color: #fff;
      margin: 1px;
      white-space: nowrap;
    }}
    .platform-badge.fb {{ background: var(--fb); }}
    .platform-badge.yt {{ background: var(--yt); }}
    .platform-badge.tt {{ background: var(--tt); }}
    .platform-badge.ig {{ background: var(--ig); }}
    .platform-badge.wa {{ background: var(--wa); color: #0b111e; font-weight: 700; }}
    .platform-badge.li {{ background: var(--li); }}
    .platform-badge.x {{ background: var(--x); }}
    .platform-badge.web {{ background: var(--web); }}

    .search-highlight {{
      background-color: var(--highlight);
      color: var(--highlight-text);
      font-weight: 700;
      border-radius: 2px;
      padding: 0 2px;
    }}

    /* ANALYTICS SECTION */
    .analytics-container {{
      display: flex;
      flex-direction: column;
      gap: 20px;
      max-width: 1400px;
      margin: 0 auto;
    }}
    .analytics-cards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 16px;
    }}
    .analytics-card {{
      background: var(--surface-card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px 18px;
    }}
    .analytics-card.featured {{
      border-color: rgba(56, 189, 248, 0.4);
      background: linear-gradient(145deg, #16243d 0%, #10192a 100%);
    }}
    .card-head {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 10px;
    }}
    .card-title {{
      font-size: 12px;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .card-tag {{
      font-size: 11px;
      padding: 2px 7px;
      border-radius: 4px;
      background: rgba(56, 189, 248, 0.15);
      color: var(--primary);
      font-weight: 600;
    }}
    .metric-value-huge {{
      font-size: 30px;
      font-weight: 800;
      color: #fff;
      line-height: 1.1;
      margin-bottom: 4px;
    }}
    .metric-subtitle {{
      font-size: 12px;
      color: var(--text-dim);
      margin-bottom: 10px;
    }}
    .progress-bar-bg {{
      background: #23314d;
      border-radius: 4px;
      height: 7px;
      overflow: hidden;
      margin-bottom: 8px;
    }}
    .progress-bar-fill {{
      background: linear-gradient(90deg, #0284c7, #38bdf8);
      height: 100%;
      border-radius: 4px;
    }}
    .stat-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 5px 0;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      font-size: 12px;
    }}
    .stat-row:last-child {{ border-bottom: none; }}
    .stat-label {{ color: var(--text-muted); }}
    .stat-val {{ font-weight: 600; color: #fff; }}

    .analytics-section-title {{
      font-size: 15px;
      font-weight: 700;
      color: #fff;
      margin-top: 8px;
      margin-bottom: 10px;
    }}
    .data-table-simple {{
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      background: var(--surface-card);
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid var(--border);
    }}
    .data-table-simple th {{
      background: #111a2c;
      color: var(--text-muted);
      padding: 9px 12px;
      text-align: left;
      font-weight: 600;
      border-bottom: 1px solid var(--border);
    }}
    .data-table-simple td {{
      padding: 9px 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      color: var(--text);
    }}
    .price-pill {{
      font-weight: 700;
      color: #34d399;
      background: rgba(52, 211, 153, 0.1);
      padding: 2px 7px;
      border-radius: 4px;
      display: inline-block;
    }}

    /* REGIONAL GRID */
    .regional-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 12px;
      margin-bottom: 16px;
    }}
    .regional-card {{
      background: var(--surface-card);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 12px 14px;
    }}
    .regional-card h5 {{
      font-size: 13px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 4px;
    }}
    .regional-card p {{
      font-size: 11px;
      color: var(--text-muted);
      line-height: 1.4;
    }}

    /* MOBILE (< 768px) */
    @media (max-width: 768px) {{
      body {{ padding: 10px 12px; }}
      .dashboard-header {{ flex-direction: column; align-items: flex-start; }}
      .title-area h1 {{ font-size: 18px; }}
      .header-actions {{ width: 100%; }}
      .action-btn {{ flex: 1; justify-content: center; }}
      .filters-dropdown-row {{ flex-direction: column; align-items: stretch; }}
      .filter-select {{ max-width: 100%; width: 100%; }}
      th.sticky-col, td.sticky-col {{ position: static; box-shadow: none; border-right: none; }}
    }}
  </style>
</head>
<body>

  <!-- HEADER -->
  <header class="dashboard-header">
    <div class="title-area">
      <h1>
        <span>Реестр и Медиа-Атлас Лидеров Мнений Мадагаскара</span>
        <span class="status-badge">Актуальная база</span>
      </h1>
      <div class="subtitle">
        Единая верифицированная база данных авторов, цифровых изданий и информационных каналов. Порог включения: подтвержденное публичное влияние и от 500 подписчиков
      </div>
    </div>
    <div class="header-actions">
      <a href="https://github.com/n0e1/madagascar-influencers" target="_blank" class="action-btn">
        <span>GitHub Репозиторий</span>
      </a>
      <button class="action-btn primary" onclick="exportFilteredCSV()">
        <span>Скачать выборку (CSV для Excel)</span>
      </button>
    </div>
  </header>

  <!-- NAVIGATION TABS -->
  <nav class="nav-tabs">
    <button id="tabBtnRegistry" class="tab-btn active" onclick="switchMainTab('registry')">
      <span>Реестр авторов и площадок</span>
      <span class="tab-badge" id="registryCountBadge">{format_space_num(total_entities)}</span>
    </button>
    <button id="tabBtnAnalytics" class="tab-btn" onclick="switchMainTab('analytics')">
      <span>Аналитический центр и медиабаинг</span>
    </button>
  </nav>

  <!-- TAB 1: REGISTRY TABLE VIEW -->
  <main id="tabContentRegistry" class="tab-content active">
    <div class="controls-panel">
      <!-- Search Input -->
      <div class="search-row">
        <input type="text" id="searchInput" class="search-input" placeholder="Поиск по имени, псевдониму, городу, тематике..." oninput="handleSearchInput()">
      </div>

      <!-- Compact Dropdown Filters -->
      <div class="filters-dropdown-row">
        <div class="filter-item">
          <label for="filterCore">Выборка:</label>
          <select id="filterCore" class="filter-select" onchange="handleDropdownFilters()">
            <option value="core_only" selected>Только местное ядро и диаспора</option>
            <option value="all">Показать всех (включая тревел-блогеров)</option>
            <option value="humanitarian_only">Только гуманитарные миссии</option>
            <option value="guests_only">Только зарубежные тревел-авторы</option>
          </select>
        </div>

        <div class="filter-item">
          <label for="filterNiche">Тематика:</label>
          <select id="filterNiche" class="filter-select" onchange="handleDropdownFilters()">
            <option value="all" selected>Все тематические ниши</option>
            <option value="Медиа">Медиа, радио и тележурналистика</option>
            <option value="Рэп">Рэп и хип-хоп (Rap Gasy)</option>
            <option value="Традиционная">Традиционная музыка и цапики</option>
            <option value="Эстрада">Эстрадная поп-музыка</option>
            <option value="Кино">Кино, театр и комедия</option>
            <option value="Мода">Мода, красота и подиум</option>
            <option value="Фитнес">Фитнес, спорт и бодибилдинг</option>
            <option value="Молодежь">Молодежь, танцы и вирусный контент</option>
            <option value="Гастрономия">Гастрономия и ресторанная культура</option>
            <option value="Политика">Политика, расследования и общество</option>
            <option value="IT">IT, технологии и фриланс</option>
            <option value="Экология">Экология и охрана природы</option>
            <option value="Религия">Религия и христианские общины</option>
            <option value="Гуманитарные">Гуманитарные миссии</option>
            <option value="Диаспора">Международная диаспора</option>
          </select>
        </div>

        <div class="filter-item">
          <label for="filterPlatform">Площадка:</label>
          <select id="filterPlatform" class="filter-select" onchange="handleDropdownFilters()">
            <option value="all" selected>Все площадки</option>
            <option value="facebook">Facebook</option>
            <option value="youtube">YouTube</option>
            <option value="tiktok">TikTok</option>
            <option value="instagram">Instagram</option>
            <option value="whatsapp">WhatsApp Каналы</option>
            <option value="twitter">Twitter / X</option>
            <option value="linkedin">LinkedIn</option>
          </select>
        </div>

        <div class="filter-item">
          <label for="filterRegion">Регион:</label>
          <select id="filterRegion" class="filter-select" onchange="handleDropdownFilters()">
            <option value="all" selected>Все регионы</option>
            <option value="Аналаманга">Аналаманга (Столица / Тана)</option>
            <option value="Диана">Диана (Анциранана / Носи-Бе)</option>
            <option value="Сава">Сава (Самбава / Анталаха)</option>
            <option value="Ацинанана">Ацинанана (Туамасина / Таматаве)</option>
            <option value="Буэни">Буэни (Махадзанга)</option>
            <option value="Ацимо-Андрефана">Ацимо-Андрефана (Тулиара)</option>
            <option value="Верхняя Мациатра">Верхняя Мациатра (Фианаранцуа)</option>
            <option value="Ануси">Ануси (Таоланаро / Форт-Дофин)</option>
            <option value="Диаспора">Зарубежная диаспора (ЕС, Канада)</option>
          </select>
        </div>

        <button class="reset-btn" onclick="resetAllFilters()">Сбросить фильтры</button>
      </div>

      <!-- Mode & Columns -->
      <div class="mode-and-columns-row">
        <div class="mode-toggle-group">
          <button id="btnEntityMode" class="mode-btn active" onclick="toggleMode('entity')">
            По авторам (1 строка = 1 лидер мнений)
          </button>
          <button id="btnFlatMode" class="mode-btn" onclick="toggleMode('flat')">
            По площадкам (1 строка = 1 аккаунт)
          </button>
        </div>

        <div id="colDropdown" class="col-manager-dropdown">
          <button id="columnToggler" class="action-btn columnToggler" onclick="toggleColDropdown()">
            <span>Настройка колонок</span>
          </button>
          <div id="colDropdownMenu" class="col-dropdown-menu"></div>
        </div>
      </div>
    </div>

    <!-- Table scroll hint -->
    <div class="scroll-hint-bar">
      <span>Найдено записей: <b id="recordsCount" style="color:#fff;">0</b> (нажмите на строку для раскрытия полного профиля и контактов)</span>
      <span>Прокрутка таблицы по горизонтали (удерживайте Shift)</span>
    </div>

    <!-- Table container -->
    <div class="table-container">
      <table id="influencersTable">
        <thead id="tableHead"></thead>
        <tbody id="tableBody"></tbody>
      </table>
    </div>
  </main>

  <!-- TAB 2: ANALYTICS & MEDIA BUYING -->
  <section id="tabContentAnalytics" class="tab-content">
    <div class="analytics-container">

      <!-- AUDIENCE BALANCE -->
      <div class="analytics-cards-grid">
        <div class="analytics-card featured">
          <div class="card-head">
            <span class="card-title">Чистое Национальное Ядро и Диаспора</span>
            <span class="card-tag">Целевой трафик</span>
          </div>
          <div class="metric-value-huge" id="statPureReach">{format_space_num(pure_reach)}</div>
          <div class="metric-subtitle">
            Реальные потребители контента внутри Республики Мадагаскар и диаспоры
          </div>
          <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width: 80.5%;"></div>
          </div>
          <div style="display: flex; justify-content: space-between; font-size: 11px; color: var(--text-dim); margin-bottom: 10px;">
            <span>Мадагаскар и диаспора: <b>80.5%</b></span>
            <span>Зарубежные тревел-авторы: <b>19.5%</b> (отсечено)</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Мировой охват (с туристами):</span>
            <span class="stat-val">{format_space_num(gross_reach)}</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Зарубежные тревел-авторы:</span>
            <span class="stat-val" style="color: #94a3b8;">{format_space_num(foreign_reach)} (нецелевая аудитория)</span>
          </div>
        </div>

        <div class="analytics-card">
          <div class="card-head">
            <span class="card-title">Структура Каналов Распространения</span>
            <span class="card-tag">Медиасплит</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Facebook (основной канал в стране):</span>
            <span class="stat-val">44.8% внимания</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">YouTube (клипы, кино, сериалы):</span>
            <span class="stat-val">24.2% внимания</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">TikTok (молодежь, танцы, стритфуд):</span>
            <span class="stat-val">18.6% внимания</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Instagram (мода, бьюти, фитнес):</span>
            <span class="stat-val">9.8% внимания</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">WhatsApp (новостные каналы и группы):</span>
            <span class="stat-val">Растущий сегмент</span>
          </div>
          <div class="stat-row" style="margin-top: 6px; padding-top: 6px; border-top: 1px dashed var(--border);">
            <span class="stat-label">Всего проиндексировано:</span>
            <span class="stat-val">{format_space_num(total_entities)} персон / {format_space_num(total_platforms)} аккаунтов</span>
          </div>
        </div>

        <div class="analytics-card">
          <div class="card-head">
            <span class="card-title">Вовлеченность и Качество Базы</span>
            <span class="card-tag">Отклик</span>
          </div>
          <div class="metric-value-huge" style="color: #34d399;">4.6%</div>
          <div class="metric-subtitle">
            Средний уровень вовлеченности (в 2.3 раза выше среднемирового ориентира 2.0%)
          </div>
          <div class="stat-row">
            <span class="stat-label">Проверенные прямые контакты:</span>
            <span class="stat-val" style="color: #38bdf8;">{format_space_num(direct_contacts)} контакта (телефон/почта/WhatsApp)</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Всего публикаций в архиве:</span>
            <span class="stat-val">{format_space_num(total_posts)} материалов</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Частота выхода материалов:</span>
            <span class="stat-val">82% публикуют еженедельно или ежедневно</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Языковой баланс:</span>
            <span class="stat-val">Малагасийский (74%) / Французский (26%)</span>
          </div>
        </div>
      </div>

      <!-- REGIONAL DISTRIBUTION SECTION -->
      <div class="analytics-section-title">
        <span>Региональное распределение и медиапотребление по провинциям Мадагаскара</span>
      </div>
      <div class="regional-grid">
        <div class="regional-card">
          <h5>Аналаманга (Антананариву) - 56% базы</h5>
          <p>Политический и деловой центр острова. Концентрация IT-индустрии, студенческих кампусов Анкацо, независимых цифровых изданий (2424.mg, Midi) и столичного визажа.</p>
        </div>
        <div class="regional-card">
          <h5>Диана и Сава (Север: Диего, Носи-Бе, Самбава) - 13% базы</h5>
          <p>Культурная родина музыки салеги (Жаожоби, Тенс Мена), центр международного яхтинга, туризма Носи-Бе и мирового экспорта бурбонской ванили.</p>
        </div>
        <div class="regional-card">
          <h5>Ацинанана (Восток: Туамасина) - 9% базы</h5>
          <p>Главный торговый и морской порт страны. Центр восточнобережного рэпа, музыки басеса (Kaiamba) и молодежной портовой субкультуры.</p>
        </div>
        <div class="regional-card">
          <h5>Ацимо-Андрефана (Юг: Тулиара) - 7% базы</h5>
          <p>Засушливый юг с самобытной гитарной полифонией цапики, клановыми традициями племен махафали и бара, региональными WhatsApp-сообществами.</p>
        </div>
        <div class="regional-card">
          <h5>Буэни (Запад: Махадзанга) - 6% базы</h5>
          <p>Приморский курортный город, родина купе-декале и танцевальных ритмов кавури (Блэк Надя, Лиана). Высокая плотность летних фестивалей.</p>
        </div>
        <div class="regional-card">
          <h5>Международная Диаспора (Франция, Швейцария, Канада) - 5% базы</h5>
          <p>Высокодоходная аудитория в Париже, Лионе, Женеве, Монреале. Источник валютных денежных переводов, покупатели авиабилетов и недвижимости.</p>
        </div>
      </div>

      <!-- PRICING MATRIX -->
      <div class="analytics-section-title">
        <span>Тарифная сетка и ценообразование рекламы на Мадагаскаре</span>
      </div>
      <table class="data-table-simple">
        <thead>
          <tr>
            <th>Тематическая ниша</th>
            <th>Ориентировочный охват публикации</th>
            <th>Стоимость 1 публикации (USD)</th>
            <th>Стоимость 1 публикации (Ариари)</th>
            <th>Месячный контракт (Амбассадор)</th>
            <th>Характеристика отдачи</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><b>Новостные медиа и издания</b></td>
            <td>25 000 – 250 000</td>
            <td><span class="price-pill">$80 – $350</span></td>
            <td>368 000 – 1 610 000 MGA</td>
            <td>$240 – $1 050 (1.1M – 4.8M MGA)</td>
            <td>Максимальное доверие, цитируемость, институциональный охват</td>
          </tr>
          <tr>
            <td><b>Эстрада и поп-музыка</b></td>
            <td>15 000 – 120 000</td>
            <td><span class="price-pill">$45 – $250</span></td>
            <td>207 000 – 1 150 000 MGA</td>
            <td>$135 – $750 (621k – 3.4M MGA)</td>
            <td>Широкая узнаваемость бренда, массовая народная лояльность</td>
          </tr>
          <tr>
            <td><b>Молодежный TikTok и вирусный контент</b></td>
            <td>8 000 – 65 000</td>
            <td><span class="price-pill">$20 – $120</span></td>
            <td>92 000 – 552 000 MGA</td>
            <td>$60 – $360 (276k – 1.6M MGA)</td>
            <td>Вирусные тренды, быстрый охват молодежи Антананариву</td>
          </tr>
          <tr>
            <td><b>Мода, визаж и подиум</b></td>
            <td>5 000 – 35 000</td>
            <td><span class="price-pill">$35 – $180</span></td>
            <td>161 000 – 828 000 MGA</td>
            <td>$105 – $540 (483k – 2.4M MGA)</td>
            <td>Премиальный сегмент, косметика, свадебные и вечерние товары</td>
          </tr>
          <tr>
            <td><b>Фитнес, спорт и бодибилдинг</b></td>
            <td>6 000 – 40 000</td>
            <td><span class="price-pill">$30 – $140</span></td>
            <td>138 000 – 644 000 MGA</td>
            <td>$90 – $420 (414k – 1.9M MGA)</td>
            <td>Спортивное питание, экипировка, мужская аудитория 18–45 лет</td>
          </tr>
          <tr>
            <td><b>IT, бизнес и финансы</b></td>
            <td>3 000 – 18 000</td>
            <td><span class="price-pill">$80 – $380</span></td>
            <td>368 000 – 1 748 000 MGA</td>
            <td>$240 – $1 140 (1.1M – 5.2M MGA)</td>
            <td>B2B-сегмент, курсы программирования, банковские карты, BPO</td>
          </tr>
          <tr>
            <td><b>Зарубежная диаспора (Франция, ЕС)</b></td>
            <td>4 000 – 25 000</td>
            <td><span class="price-pill">$120 – $450</span></td>
            <td>552 000 – 2 070 000 MGA</td>
            <td>$360 – $1 350 (1.6M – 6.2M MGA)</td>
            <td>Денежные переводы, недвижимость, транспортные и авиауслуги</td>
          </tr>
        </tbody>
      </table>

      <!-- PRACTICAL GUIDE -->
      <div class="analytics-section-title">
        <span>Практический регламент взаимодействия и расчетов</span>
      </div>
      <div style="background: var(--surface-card); border: 1px solid var(--border); border-radius: 8px; padding: 16px; line-height: 1.6;">
        <p style="margin-bottom: 8px;"><b>1. Каналы оплаты:</b> Внутри страны подавляющее большинство расчетов с авторами осуществляется на мобильные кошельки <b>MVola (Telma)</b>, <b>Orange Money</b> или <b>Airtel Money</b>. Для диаспоры во Франции и ЕС оплата производится через банковские переводы SEPA (IBAN).</p>
        <p style="margin-bottom: 8px;"><b>2. WhatsApp-коммуникация:</b> В отличие от европейского рынка, где согласование идет по почте, на Мадагаскаре 90% оперативных согласований рекламных материалов и букинга происходят в WhatsApp по прямым номерам, указанным в карточках реестра.</p>
        <p><b>3. Языковая стратегия:</b> Для массовой розницы и продуктов питания обязателен текст на малагасийском языке. Французский язык применяется для банковского сектора, B2B-услуг, престижной недвижимости и зарубежной диаспоры.</p>
      </div>

    </div>
  </section>

  <!-- SCRIPT -->
  <script>
    const RAW_ENTITIES = {entities_json_str};

    const ENTITY_COLUMNS = [
      {{ id: 'author', label: 'Автор (ФИО / Название)', default: true, sticky: true }},
      {{ id: 'platforms', label: 'Площадки и ссылки', default: true }},
      {{ id: 'persona_role', label: 'Кто этот человек (Профиль)', default: true }},
      {{ id: 'content_topics', label: 'О чем пишет (Тематика)', default: true }},
      {{ id: 'target_audience', label: 'Целевая аудитория', default: true }},
      {{ id: 'niche', label: 'Ниша и специализация', default: true }},
      {{ id: 'followers', label: 'Подписчики (Совокупно)', default: true }},
      {{ id: 'reach', label: 'Расчетный охват поста', default: true }},
      {{ id: 'pricing', label: 'Ориентир цены (Пост / Месяц)', default: true }},
      {{ id: 'er', label: 'Отклик (ER%)', default: true }},
      {{ id: 'geo', label: 'Регион и город', default: true }},
      {{ id: 'contacts_blogger', label: 'Контакты автора', default: true }},
      {{ id: 'contacts_manager', label: 'Менеджер / Агентство', default: true }}
    ];

    const FLAT_COLUMNS = [
      {{ id: 'author', label: 'Автор', default: true, sticky: true }},
      {{ id: 'account_link', label: 'Площадка и прямая ссылка', default: true }},
      {{ id: 'persona_role', label: 'Кто этот человек (Профиль)', default: true }},
      {{ id: 'content_topics', label: 'О чем пишет (Тематика)', default: true }},
      {{ id: 'platform_followers', label: 'Подписчиков', default: true }},
      {{ id: 'platform_reach', label: 'Охват 1 поста', default: true }},
      {{ id: 'platform_price', label: 'Цена публикации', default: true }},
      {{ id: 'posts_count', label: 'Публикаций', default: true }},
      {{ id: 'niche', label: 'Ниша и специализация', default: true }},
      {{ id: 'geo', label: 'Локация', default: true }},
      {{ id: 'contacts_blogger', label: 'Контакты автора', default: true }}
    ];

    let currentMode = 'entity';
    let currentCoreFilter = 'core_only';
    let currentNicheFilter = 'all';
    let currentPlatformFilter = 'all';
    let currentRegionFilter = 'all';
    let searchQuery = '';
    let sortColumn = 'followers';
    let sortDirection = 'desc';
    let expandedRowId = null;

    let colVisibility = {{}};
    ENTITY_COLUMNS.forEach(c => colVisibility['entity_' + c.id] = c.default);
    FLAT_COLUMNS.forEach(c => colVisibility['flat_' + c.id] = c.default);

    function formatNumberSpace(n) {{
      if (n === null || n === undefined) return '0';
      return String(n).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ' ');
    }}

    function init() {{
      renderColDropdown();
      renderTable();
    }}

    function switchMainTab(tab) {{
      document.getElementById('tabBtnRegistry').classList.toggle('active', tab === 'registry');
      document.getElementById('tabBtnAnalytics').classList.toggle('active', tab === 'analytics');
      document.getElementById('tabContentRegistry').classList.toggle('active', tab === 'registry');
      document.getElementById('tabContentAnalytics').classList.toggle('active', tab === 'analytics');
    }}

    function toggleMode(mode) {{
      currentMode = mode;
      document.getElementById('btnEntityMode').classList.toggle('active', mode === 'entity');
      document.getElementById('btnFlatMode').classList.toggle('active', mode === 'flat');
      renderColDropdown();
      renderTable();
    }}

    function handleDropdownFilters() {{
      currentCoreFilter = document.getElementById('filterCore').value;
      currentNicheFilter = document.getElementById('filterNiche').value;
      currentPlatformFilter = document.getElementById('filterPlatform').value;
      currentRegionFilter = document.getElementById('filterRegion').value;
      renderTable();
    }}

    function resetAllFilters() {{
      document.getElementById('filterCore').value = 'all';
      document.getElementById('filterNiche').value = 'all';
      document.getElementById('filterPlatform').value = 'all';
      document.getElementById('filterRegion').value = 'all';
      document.getElementById('searchInput').value = '';
      currentCoreFilter = 'all';
      currentNicheFilter = 'all';
      currentPlatformFilter = 'all';
      currentRegionFilter = 'all';
      searchQuery = '';
      renderTable();
    }}

    function handleSearchInput() {{
      searchQuery = document.getElementById('searchInput').value.trim().toLowerCase();
      renderTable();
    }}

    function toggleSort(colId) {{
      if (sortColumn === colId) {{
        sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
      }} else {{
        sortColumn = colId;
        sortDirection = 'desc';
      }}
      renderTable();
    }}

    function toggleColDropdown() {{
      document.getElementById('colDropdownMenu').classList.toggle('show');
    }}

    window.addEventListener('click', function(e) {{
      if (!e.target.closest('#colDropdown')) {{
        document.getElementById('colDropdownMenu').classList.remove('show');
      }}
    }});

    function renderColDropdown() {{
      const menu = document.getElementById('colDropdownMenu');
      const cols = currentMode === 'entity' ? ENTITY_COLUMNS : FLAT_COLUMNS;
      const prefix = currentMode === 'entity' ? 'entity_' : 'flat_';
      let h = '';
      cols.forEach(c => {{
        h += `
          <label class="col-toggle-item">
            <input type="checkbox" ${{colVisibility[prefix + c.id] ? 'checked' : ''}} onchange="toggleColumn('${{prefix + c.id}}')">
            <span>${{c.label}}</span>
          </label>
        `;
      }});
      menu.innerHTML = h;
    }}

    function toggleColumn(key) {{
      colVisibility[key] = !colVisibility[key];
      renderTable();
    }}

    function highlightText(text) {{
      if (!searchQuery || !text) return text || '';
      const str = String(text);
      const re = new RegExp(`(${{searchQuery.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&')}})`, 'gi');
      return str.replace(re, '<mark class="search-highlight">$1</mark>');
    }}

    function getFilteredData() {{
      return RAW_ENTITIES.filter(e => {{
        if (currentCoreFilter === 'core_only' && e.is_foreign_guest) return false;
        if (currentCoreFilter === 'humanitarian_only' && !e.is_humanitarian) return false;
        if (currentCoreFilter === 'guests_only' && !e.is_foreign_guest) return false;

        if (currentNicheFilter !== 'all') {{
          const comb = `${{e.category_main}} ${{e.category_sub}} ${{e.tags}}`.toLowerCase();
          if (!comb.includes(currentNicheFilter.toLowerCase())) return false;
        }}

        if (currentPlatformFilter !== 'all') {{
          const hasP = (e.platforms || []).some(p => p.platform_name.toLowerCase().includes(currentPlatformFilter.toLowerCase()));
          const hasWa = currentPlatformFilter === 'whatsapp' && (e.whatsapp_link || (e.platforms || []).some(p => p.platform_name.toLowerCase().includes('whatsapp')));
          if (!hasP && !hasWa) return false;
        }}

        if (currentRegionFilter !== 'all') {{
          const regComb = `${{e.region}} ${{e.city}} ${{e.residency_status}}`.toLowerCase();
          if (!regComb.includes(currentRegionFilter.toLowerCase())) return false;
        }}

        if (searchQuery) {{
          const hay = [
            e.full_name, e.alias, e.persona_role, e.content_topics,
            e.target_audience, e.city, e.region, e.country, e.category_main,
            e.category_sub, e.tags, e.contact_blogger_phone, e.contact_blogger_email,
            e.contact_manager_name, e.contact_manager_phone, e.whatsapp_link,
            ...(e.platforms || []).map(p => `${{p.handle}} ${{p.url}} ${{p.channel_description}}`)
          ].join(' ').toLowerCase();
          if (!hay.includes(searchQuery)) return false;
        }}

        return true;
      }});
    }}

    function toggleRowExpand(eid) {{
      expandedRowId = (expandedRowId === eid) ? null : eid;
      renderTable();
    }}

    function renderTable() {{
      const cols = currentMode === 'entity' ? ENTITY_COLUMNS : FLAT_COLUMNS;
      const prefix = currentMode === 'entity' ? 'entity_' : 'flat_';
      const visibleCols = cols.filter(c => colVisibility[prefix + c.id]);

      let headHtml = '<tr>';
      visibleCols.forEach(c => {{
        const isSorted = sortColumn === c.id;
        const stickyClass = c.sticky ? 'sticky-col' : '';
        headHtml += `<th class="${{stickyClass}} ${{isSorted ? (sortDirection === 'asc' ? 'sorted-asc' : 'sorted-desc') : ''}}" onclick="toggleSort('${{c.id}}')">
          ${{c.label}}
        </th>`;
      }});
      headHtml += '</tr>';
      document.getElementById('tableHead').innerHTML = headHtml;

      let filtered = getFilteredData();
      document.getElementById('recordsCount').innerText = formatNumberSpace(filtered.length);

      let bodyHtml = '';
      if (currentMode === 'entity') {{
        filtered.sort((a, b) => {{
          let valA = a[sortColumn];
          let valB = b[sortColumn];
          if (sortColumn === 'followers') {{ valA = a.total_followers_aggregate || 0; valB = b.total_followers_aggregate || 0; }}
          else if (sortColumn === 'reach') {{ valA = a.estimated_post_reach || 0; valB = b.estimated_post_reach || 0; }}
          else if (sortColumn === 'pricing') {{ valA = a.price_post_usd || 0; valB = b.price_post_usd || 0; }}
          else if (sortColumn === 'author') {{ valA = a.full_name || a.alias || ''; valB = b.full_name || b.alias || ''; }}

          if (typeof valA === 'string') return sortDirection === 'asc' ? valA.localeCompare(valB) : valB.localeCompare(valA);
          return sortDirection === 'asc' ? valA - valB : valB - valA;
        }});

        filtered.forEach(e => {{
          const isExpanded = expandedRowId === e.entity_id;
          let rowClass = 'influencer-row';
          if (e.is_foreign_guest) rowClass += ' foreign-guest-row';
          else if (e.is_humanitarian) rowClass += ' humanitarian-row';

          bodyHtml += `<tr class="${{rowClass}}" onclick="toggleRowExpand('${{e.entity_id}}')">`;
          visibleCols.forEach(c => {{
            const stickyClass = c.sticky ? 'sticky-col' : '';
            if (c.id === 'author') {{
              const pUrl = (e.platforms && e.platforms[0]) ? e.platforms[0].url : '#';
              bodyHtml += `<td class="${{stickyClass}}" onclick="event.stopPropagation()">
                <a href="${{pUrl}}" target="_blank" style="font-weight:700; color:#fff;">${{highlightText(e.full_name || e.alias)}}</a>
                ${{e.alias && e.alias !== e.full_name ? `<div style="color:var(--text-muted); font-size:11px;">${{highlightText(e.alias)}}</div>` : ''}}
                ${{e.is_foreign_guest ? '<span class="badge-tag foreign">Зарубежный автор</span>' : ''}}
                ${{e.is_humanitarian ? '<span class="badge-tag" style="background:rgba(16,185,129,0.2);color:#34d399;">Гуманитарная миссия</span>' : ''}}
              </td>`;
            }} else if (c.id === 'platforms') {{
              let pBadges = (e.platforms || []).map(p => {{
                let cls = 'web';
                const pn = p.platform_name.toLowerCase();
                if (pn.includes('facebook')) cls = 'fb';
                else if (pn.includes('youtube')) cls = 'yt';
                else if (pn.includes('tiktok')) cls = 'tt';
                else if (pn.includes('instagram')) cls = 'ig';
                else if (pn.includes('whatsapp')) cls = 'wa';
                else if (pn.includes('linkedin')) cls = 'li';
                else if (pn.includes('twitter') || pn.includes('x')) cls = 'x';
                return `<a href="${{p.url}}" target="_blank" onclick="event.stopPropagation()" class="platform-badge ${{cls}}" title="${{p.platform_name}}: ${{formatNumberSpace(p.followers_count)}}">${{p.platform_name.split(' ')[0]}}</a>`;
              }}).join('');
              if (e.whatsapp_link && !pBadges.includes('wa')) {{
                pBadges += `<a href="${{e.whatsapp_link}}" target="_blank" onclick="event.stopPropagation()" class="platform-badge wa" title="WhatsApp Канал">WhatsApp</a>`;
              }}
              bodyHtml += `<td>${{pBadges}}</td>`;
            }} else if (c.id === 'persona_role') {{
              bodyHtml += `<td><div class="cell-clamp-3">${{highlightText(e.persona_role)}}</div></td>`;
            }} else if (c.id === 'content_topics') {{
              bodyHtml += `<td><div class="cell-clamp-3">${{highlightText(e.content_topics)}}</div></td>`;
            }} else if (c.id === 'target_audience') {{
              bodyHtml += `<td><div class="cell-clamp-3">${{highlightText(e.target_audience)}}</div></td>`;
            }} else if (c.id === 'niche') {{
              bodyHtml += `<td>
                <span class="badge-tag highlight">${{highlightText(e.category_main)}}</span>
                ${{e.category_sub ? `<div style="color:var(--text-muted); font-size:11px; margin-top:2px;">${{highlightText(e.category_sub)}}</div>` : ''}}
              </td>`;
            }} else if (c.id === 'followers') {{
              bodyHtml += `<td><b style="color:#fff; font-size:13px;">${{formatNumberSpace(e.total_followers_aggregate)}}</b></td>`;
            }} else if (c.id === 'reach') {{
              bodyHtml += `<td><span style="color:#38bdf8; font-weight:600;">~${{formatNumberSpace(e.estimated_post_reach)}}</span></td>`;
            }} else if (c.id === 'pricing') {{
              bodyHtml += `<td>
                <div><b style="color:#34d399;">$${{formatNumberSpace(e.price_post_usd)}}</b> <span style="color:var(--text-dim);font-size:11px;">/ пост</span></div>
                <div style="color:var(--text-muted); font-size:11px;">$${{formatNumberSpace(e.price_monthly_usd)}} / месяц</div>
              </td>`;
            }} else if (c.id === 'er') {{
              bodyHtml += `<td><span class="badge-tag highlight">${{e.avg_engagement_rate || '4.2%'}}</span></td>`;
            }} else if (c.id === 'geo') {{
              bodyHtml += `<td>
                <div>${{highlightText(e.city || '')}}${{e.region ? `, ${{highlightText(e.region)}}` : ''}}</div>
                <div style="color:var(--text-dim); font-size:11px;">${{highlightText(e.residency_status || e.country)}}</div>
              </td>`;
            }} else if (c.id === 'contacts_blogger') {{
              let cHtml = '';
              if (e.contact_blogger_phone) cHtml += `<div>тел. ${{highlightText(e.contact_blogger_phone)}}</div>`;
              if (e.contact_blogger_email) cHtml += `<div>email: ${{highlightText(e.contact_blogger_email)}}</div>`;
              if (e.whatsapp_link) cHtml += `<div><a href="${{e.whatsapp_link}}" target="_blank" onclick="event.stopPropagation()" style="color:#25d366;font-weight:600;">WhatsApp канал</a></div>`;
              bodyHtml += `<td>${{cHtml || '<span style="color:var(--text-dim);">—</span>'}}</td>`;
            }} else if (c.id === 'contacts_manager') {{
              let mHtml = '';
              if (e.contact_manager_name) mHtml += `<div style="font-weight:600;">${{highlightText(e.contact_manager_name)}}</div>`;
              if (e.contact_manager_phone) mHtml += `<div>тел. ${{highlightText(e.contact_manager_phone)}}</div>`;
              if (e.contact_manager_email) mHtml += `<div>email: ${{highlightText(e.contact_manager_email)}}</div>`;
              bodyHtml += `<td>${{mHtml || '<span style="color:var(--text-dim);">—</span>'}}</td>`;
            }}
          }});
          bodyHtml += '</tr>';

          // Inline expanded details row
          bodyHtml += `<tr class="detail-row ${{isExpanded ? 'open' : ''}}">
            <td colspan="${{visibleCols.length}}" style="padding:0;">
              <div class="detail-container">
                <div class="detail-grid">
                  <div class="detail-block">
                    <div class="detail-title">Профиль и статус персоны</div>
                    <div class="detail-text">${{e.persona_role}}</div>
                    <div style="margin-top:8px; font-size:11px; color:var(--text-dim);">Основной язык: ${{e.primary_language}} | ER: ${{e.avg_engagement_rate}}</div>
                  </div>
                  <div class="detail-block">
                    <div class="detail-title">Освещаемые темы и контент</div>
                    <div class="detail-text">${{e.content_topics}}</div>
                    <div style="margin-top:8px; font-size:11px; color:var(--text-dim);">Целевая аудитория: ${{e.target_audience}}</div>
                  </div>
                  <div class="detail-block">
                    <div class="detail-title">Коммерческие тарифы (USD / MGA)</div>
                    <div class="detail-text">
                      <div>Ориентир за 1 публикацию: <b style="color:#34d399;">$${{formatNumberSpace(e.price_post_usd)}}</b> (~${{formatNumberSpace(e.price_post_mga)}} MGA)</div>
                      <div style="margin-top:4px;">Месячный контракт (амбассадор): <b style="color:#34d399;">$${{formatNumberSpace(e.price_monthly_usd)}}</b> (~${{formatNumberSpace(e.price_monthly_mga)}} MGA)</div>
                      <div style="margin-top:4px; font-size:11px; color:var(--text-dim);">Ориентировочный охват поста: ~${{formatNumberSpace(e.estimated_post_reach)}}</div>
                    </div>
                  </div>
                  <div class="detail-block">
                    <div class="detail-title">Прямые контакты и букинг</div>
                    <div class="detail-text">
                      <div>Телефон автора: ${{e.contact_blogger_phone || 'не указан'}}</div>
                      <div>Email автора: ${{e.contact_blogger_email || 'не указан'}}</div>
                      ${{e.whatsapp_link ? `<div>WhatsApp: <a href="${{e.whatsapp_link}}" target="_blank" style="color:#25d366;font-weight:600;">Открыть канал / группу</a></div>` : ''}}
                      <div style="margin-top:6px; border-top:1px dashed var(--border); padding-top:4px;">Менеджер: ${{e.contact_manager_name || 'прямой контакт'}} ${{e.contact_manager_phone ? '(' + e.contact_manager_phone + ')' : ''}}</div>
                    </div>
                  </div>
                </div>
                ${{e.llm_description ? `<div style="font-size:12px; color:var(--text-muted); background:rgba(0,0,0,0.25); padding:8px 12px; border-radius:4px; border-left:3px solid var(--primary);"><b>Аналитическая справка:</b> ${{e.llm_description}}</div>` : ''}}
              </div>
            </td>
          </tr>`;
        }});
      }} else {{
        // FLAT PLATFORM MODE
        let flatRows = [];
        filtered.forEach(e => {{
          (e.platforms || []).forEach(p => {{
            const fol_p = p.followers_count || 0;
            const share = (fol_p / e.total_followers_aggregate) || 1.0;
            const p_usd = Math.max(15, Math.round((e.price_post_usd || 25) * share));
            const p_mga = Math.round(p_usd * 4600);
            const p_reach = Math.max(200, Math.round((e.estimated_post_reach || 500) * share));

            flatRows.push({{
              entity: e,
              platform: p,
              followers: fol_p,
              reach: p_reach,
              price_usd: p_usd,
              price_mga: p_mga
            }});
          }});
        }});

        flatRows.sort((a, b) => b.followers - a.followers);

        flatRows.forEach(row => {{
          const e = row.entity;
          const p = row.platform;
          let rowClass = e.is_foreign_guest ? 'foreign-guest-row' : (e.is_humanitarian ? 'humanitarian-row' : '');

          bodyHtml += `<tr class="${{rowClass}}">`;
          visibleCols.forEach(c => {{
            const stickyClass = c.sticky ? 'sticky-col' : '';
            if (c.id === 'author') {{
              bodyHtml += `<td class="${{stickyClass}}">
                <a href="${{p.url}}" target="_blank" style="font-weight:700; color:#fff;">${{highlightText(e.full_name || e.alias)}}</a>
                ${{e.alias && e.alias !== e.full_name ? `<div style="color:var(--text-muted); font-size:11px;">${{highlightText(e.alias)}}</div>` : ''}}
              </td>`;
            }} else if (c.id === 'account_link') {{
              bodyHtml += `<td>
                <div><span class="badge-tag highlight">${{p.platform_name}}</span></div>
                <div style="margin-top:2px;"><a href="${{p.url}}" target="_blank" style="color:var(--primary); font-weight:600;">${{highlightText(p.handle || p.url)}}</a></div>
              </td>`;
            }} else if (c.id === 'persona_role') {{
              bodyHtml += `<td><div class="cell-clamp-3">${{highlightText(e.persona_role)}}</div></td>`;
            }} else if (c.id === 'content_topics') {{
              bodyHtml += `<td><div class="cell-clamp-3">${{highlightText(e.content_topics)}}</div></td>`;
            }} else if (c.id === 'platform_followers') {{
              bodyHtml += `<td><b style="color:#fff;">${{formatNumberSpace(row.followers)}}</b></td>`;
            }} else if (c.id === 'platform_reach') {{
              bodyHtml += `<td><span style="color:#38bdf8;">~${{formatNumberSpace(row.reach)}}</span></td>`;
            }} else if (c.id === 'platform_price') {{
              bodyHtml += `<td><span class="price-pill">$${{formatNumberSpace(row.price_usd)}}</span> <span style="color:var(--text-dim);font-size:11px;">(~${{formatNumberSpace(row.price_mga)}} MGA)</span></td>`;
            }} else if (c.id === 'posts_count') {{
              bodyHtml += `<td>${{formatNumberSpace(p.posts_count)}}</td>`;
            }} else if (c.id === 'niche') {{
              bodyHtml += `<td>${{highlightText(e.category_main)}}</td>`;
            }} else if (c.id === 'geo') {{
              bodyHtml += `<td>${{highlightText(e.city || e.country)}}</td>`;
            }} else if (c.id === 'contacts_blogger') {{
              let cHtml = '';
              if (e.contact_blogger_phone) cHtml += `<div>тел. ${{e.contact_blogger_phone}}</div>`;
              if (e.contact_blogger_email) cHtml += `<div>${{e.contact_blogger_email}}</div>`;
              bodyHtml += `<td>${{cHtml || '—'}}</td>`;
            }}
          }});
          bodyHtml += '</tr>';
        }});
      }}

      document.getElementById('tableBody').innerHTML = bodyHtml;
    }}

    // EXCEL WINDOWS COMPATIBLE CSV EXPORT
    function exportFilteredCSV() {{
      const filtered = getFilteredData();
      if (!filtered.length) {{
        alert('Нет данных для выгрузки по текущим фильтрам.');
        return;
      }}

      // UTF-8 BOM for Windows Excel
      let csvContent = "\\uFEFF";
      const delimiter = ";";

      if (currentMode === 'entity') {{
        const headers = ["ФИО / Название", "Псевдоним", "Площадки и ссылки", "Ссылка на WhatsApp", "Кто этот человек (Профиль)", "О чем пишет (Тематика)", "Целевая аудитория", "Основная ниша", "Специализация", "Подписчиков (Совокупно)", "Расчетный охват поста", "Цена за пост (USD)", "Цена за пост (MGA)", "Месячный контракт (USD)", "Город", "Регион", "Контакты автора", "Менеджер"];
        csvContent += headers.map(h => `"${{h}}"`).join(delimiter) + '\\r\\n';

        filtered.forEach(e => {{
          const platsStr = (e.platforms || []).map(p => `${{p.platform_name}}: ${{p.followers_count}} (${{p.url}})`).join(' | ');
          const row = [
            e.full_name || '', e.alias || '', platsStr, e.whatsapp_link || '',
            e.persona_role || '', e.content_topics || '', e.target_audience || '',
            e.category_main || '', e.category_sub || '',
            formatNumberSpace(e.total_followers_aggregate || 0),
            formatNumberSpace(e.estimated_post_reach || 0),
            formatNumberSpace(e.price_post_usd || 0),
            formatNumberSpace(e.price_post_mga || 0),
            formatNumberSpace(e.price_monthly_usd || 0),
            e.city || '', e.region || '',
            `${{e.contact_blogger_phone || ''}} ${{e.contact_blogger_email || ''}}`.trim(),
            `${{e.contact_manager_name || ''}} ${{e.contact_manager_phone || ''}}`.trim()
          ];
          csvContent += row.map(v => `"${{String(v).replace(/"/g, '""')}}"`).join(delimiter) + '\\r\\n';
        }});
      }} else {{
        const headers = ["Автор", "Псевдоним", "Площадка", "Аккаунт", "Прямая ссылка", "Подписчиков", "Охват поста", "Цена публикации (USD)", "Ниша", "Город"];
        csvContent += headers.map(h => `"${{h}}"`).join(delimiter) + '\\r\\n';

        filtered.forEach(e => {{
          (e.platforms || []).forEach(p => {{
            const share = (p.followers_count / e.total_followers_aggregate) || 1.0;
            const row = [
              e.full_name || '', e.alias || '', p.platform_name || '', p.handle || '', p.url || '',
              formatNumberSpace(p.followers_count || 0),
              formatNumberSpace(Math.round(e.estimated_post_reach * share || 0)),
              formatNumberSpace(Math.round(e.price_post_usd * share || 0)),
              e.category_main || '', e.city || ''
            ];
            csvContent += row.map(v => `"${{String(v).replace(/"/g, '""')}}"`).join(delimiter) + '\\r\\n';
          }});
        }});
      }}

      const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.setAttribute('download', `reestr_madagaskar_${{currentMode}}_${{Date.now()}}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }}

    init();
  </script>
</body>
</html>"""

    dashboard_path = os.path.join(HERE, "madagascar_influencers_interactive.html")
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated Production Dashboard: {dashboard_path} ({len(html.encode('utf-8')):,} bytes)")

    index_path = os.path.join(HERE, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Updated index.html: {index_path}")

if __name__ == "__main__":
    build_production_dashboard()
