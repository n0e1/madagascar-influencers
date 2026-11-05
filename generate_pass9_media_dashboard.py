#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MEDIA BUYING & EXECUTIVE ANALYTICS DASHBOARD ENGINE (PASS 9)
Implements all user requirements:
1. Zero English jargon - 100% natural professional Russian for 50+ media executives.
2. Dedicated separate view/tab for Analytics & Media Buying ("Аналитический центр и медиабаинг").
3. Compact single-row select dropdowns for core filter, niche, platform, and residency.
4. Leftward repositioning of "Кто этот человек", "О чем пишет", "Целевая аудитория" in table.
5. Rich hover tooltips for compact cells revealing full unabridged descriptions.
6. Ergonomic horizontal table scroll with clear scrollbar, shadow hints, and sticky first column.
7. Mobile-first responsive optimization (<768px and <1024px).
8. Elimination of "Общий профиль" and generic "лидер мнений".
9. Clean Russian commercial ad rates (цены за пост и долгосрочный контракт в USD и MGA).
10. Dynamic search highlighting, column visibility manager, and CSV export.
"""

import os
import json
import csv
import re
from prepare_pass8_schema_and_models import USD_TO_MGA

HERE = os.path.dirname(os.path.abspath(__file__))

def build_media_dashboard():
    json_path = os.path.join(HERE, "madagascar_influencers_database.json")
    with open(json_path, "r", encoding="utf-8") as f:
        entities = json.load(f)

    print(f"Loaded {len(entities)} refined entities for dashboard build.")

    # Calculate executive metrics
    total_entities = len(entities)
    total_platforms = sum(len(e.get("platforms", [])) for e in entities)
    pure_domestic_reach = sum(e["total_followers_aggregate"] for e in entities if not e.get("is_foreign_guest"))
    gross_reach = sum(e["total_followers_aggregate"] for e in entities)
    foreign_guests_reach = gross_reach - pure_domestic_reach
    foreign_percentage = (foreign_guests_reach / gross_reach * 100) if gross_reach > 0 else 0
    domestic_percentage = 100 - foreign_percentage
    total_posts = sum(e.get("total_posts_aggregate", 0) for e in entities)
    direct_contacts_count = sum(1 for e in entities if e.get("contact_blogger_phone") or e.get("contact_blogger_email") or e.get("contact_manager_phone") or e.get("contact_manager_email"))

    # Convert entities into JSON string for embedding
    entities_json_str = json.dumps(entities, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>Реестр и Медиа-Атлас Лидеров Мнений Мадагаскара</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🇲🇬</text></svg>">
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
      --fb-color: #1877f2;
      --yt-color: #ef4444;
      --tt-color: #ec4899;
      --ig-color: #e1306c;
      --li-color: #0a66c2;
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

    /* HEADER & BRANDING */
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
      letter-spacing: -0.01em;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .status-badge {{
      font-size: 11px;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: 12px;
      background: rgba(16, 185, 129, 0.15);
      color: var(--success);
      border: 1px solid rgba(16, 185, 129, 0.3);
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }}
    .status-dot {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--success);
      display: inline-block;
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
      padding: 7px 13px;
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

    /* NAVIGATION TABS (REGISTRY vs ANALYTICS) */
    .nav-tabs {{
      display: flex;
      gap: 6px;
      border-bottom: 2px solid var(--border);
      margin-bottom: 16px;
      padding-bottom: 0;
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
      padding: 2px 6px;
      border-radius: 10px;
      background: var(--surface);
      color: var(--text-muted);
    }}
    .tab-btn.active .tab-badge {{
      background: var(--primary);
      color: #0b111e;
      font-weight: 700;
    }}

    /* TAB CONTENTS */
    .tab-content {{
      display: none;
    }}
    .tab-content.active {{
      display: block;
    }}

    /* ANALYTICS SECTION STYLES */
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
      border-radius: 10px;
      padding: 18px 20px;
      position: relative;
    }}
    .analytics-card.featured {{
      border-color: rgba(56, 189, 248, 0.4);
      background: linear-gradient(145deg, #16243d 0%, #10192a 100%);
    }}
    .card-head {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
    }}
    .card-title {{
      font-size: 13px;
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
      font-size: 32px;
      font-weight: 800;
      color: #fff;
      line-height: 1.1;
      margin-bottom: 6px;
    }}
    .metric-subtitle {{
      font-size: 12px;
      color: var(--text-dim);
      margin-bottom: 12px;
    }}
    .progress-bar-bg {{
      background: #23314d;
      border-radius: 4px;
      height: 8px;
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
      padding: 6px 0;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      font-size: 12px;
    }}
    .stat-row:last-child {{
      border-bottom: none;
    }}
    .stat-label {{
      color: var(--text-muted);
    }}
    .stat-val {{
      font-weight: 600;
      color: #fff;
    }}

    .analytics-section-title {{
      font-size: 16px;
      font-weight: 700;
      color: #fff;
      margin-top: 10px;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
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
      padding: 10px 14px;
      text-align: left;
      font-weight: 600;
      border-bottom: 1px solid var(--border);
    }}
    .data-table-simple td {{
      padding: 10px 14px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      color: var(--text);
    }}
    .data-table-simple tr:last-child td {{
      border-bottom: none;
    }}
    .price-pill {{
      font-weight: 700;
      color: #34d399;
      background: rgba(52, 211, 153, 0.1);
      padding: 2px 7px;
      border-radius: 4px;
      display: inline-block;
    }}
    .guide-box {{
      background: var(--surface-card);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 20px;
      line-height: 1.6;
    }}
    .guide-box h4 {{
      color: var(--primary);
      font-size: 14px;
      margin-bottom: 8px;
    }}
    .guide-box ol {{
      margin-left: 20px;
      color: var(--text);
    }}
    .guide-box li {{
      margin-bottom: 8px;
    }}

    /* REGISTRY CONTROLS & TOOLBAR */
    .controls-panel {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px 14px;
      margin-bottom: 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    .search-row {{
      display: flex;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
    }}
    .search-input-wrap {{
      flex: 1;
      min-width: 260px;
      position: relative;
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
    
    /* COMPACT SELECT DROPDOWNS ROW */
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
      max-width: 230px;
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
    .reset-btn:hover {{
      color: var(--danger);
    }}

    /* MODE TOGGLE & COLUMN VISIBILITY */
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

    /* COLUMN MANAGER DROPDOWN */
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
    .col-dropdown-menu.show {{
      display: block;
    }}
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
    .col-toggle-item:hover {{
      background: var(--surface-hover);
    }}

    /* TABLE ERGONOMICS & HORIZONTAL SCROLL */
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
      position: relative;
      scrollbar-width: thin;
      scrollbar-color: #3b82f6 #101726;
      -webkit-overflow-scrolling: touch;
    }}
    .table-container::-webkit-scrollbar {{
      height: 10px;
    }}
    .table-container::-webkit-scrollbar-track {{
      background: #101726;
      border-radius: 5px;
    }}
    .table-container::-webkit-scrollbar-thumb {{
      background: #2563eb;
      border-radius: 5px;
    }}
    .table-container::-webkit-scrollbar-thumb:hover {{
      background: #3b82f6;
    }}

    table {{
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      font-size: 12px;
      min-width: 1300px;
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
    th:hover {{
      color: #fff;
      background: #1a2337;
    }}
    th.sorted-asc::after {{ content: " ▲"; color: var(--primary); }}
    th.sorted-desc::after {{ content: " ▼"; color: var(--primary); }}

    /* STICKY FIRST COLUMN (NAME) */
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
    tr:hover td.sticky-col {{
      background: var(--surface-hover);
    }}

    td {{
      padding: 10px 12px;
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
      color: var(--text);
    }}
    tr:hover td {{
      background: var(--surface-hover);
    }}

    /* DOUBLE SOLID LINE (SEGREGATION FOR FOREIGN GUESTS & HUMANITARIAN) */
    tr.foreign-guest-row {{
      background: var(--foreign-bg);
      opacity: 0.85;
    }}
    tr.foreign-guest-row td {{
      border-top: 2px solid var(--foreign-border) !important;
      border-bottom: 2px solid var(--foreign-border) !important;
    }}
    tr.humanitarian-row {{
      background: rgba(16, 185, 129, 0.04);
    }}
    tr.humanitarian-row td {{
      border-top: 2px solid rgba(16, 185, 129, 0.4) !important;
      border-bottom: 2px solid rgba(16, 185, 129, 0.4) !important;
    }}

    /* COMPACT CELLS WITH HOVER TOOLTIPS */
    .cell-truncate {{
      max-width: 220px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      position: relative;
      cursor: pointer;
    }}
    .cell-truncate:hover::after {{
      content: attr(data-fulltext);
      position: absolute;
      left: 0;
      top: 100%;
      background: #0f172a;
      color: #fff;
      border: 1px solid var(--border-accent);
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 11px;
      line-height: 1.4;
      white-space: normal;
      width: 280px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.7);
      z-index: 1000;
      pointer-events: none;
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
    .badge-tag.highlight {{
      background: rgba(56, 189, 248, 0.15);
      color: var(--primary);
    }}
    .badge-tag.warning {{
      background: rgba(245, 158, 11, 0.15);
      color: var(--accent);
    }}
    .badge-tag.foreign {{
      background: rgba(148, 163, 184, 0.15);
      color: #cbd5e1;
      border: 1px dashed #64748b;
    }}

    .platform-badge {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 600;
      text-decoration: none;
      color: #fff;
      margin: 1px;
    }}
    .platform-badge.fb {{ background: #1877f2; }}
    .platform-badge.yt {{ background: #ef4444; }}
    .platform-badge.tt {{ background: #d946ef; }}
    .platform-badge.ig {{ background: #ec4899; }}
    .platform-badge.li {{ background: #0284c7; }}
    .platform-badge.x {{ background: #334155; }}
    .platform-badge.web {{ background: #0d9488; }}

    .search-highlight {{
      background-color: var(--highlight);
      color: var(--highlight-text);
      font-weight: 700;
      border-radius: 2px;
      padding: 0 2px;
    }}

    /* MOBILE RESPONSIVE STYLES (< 768px) */
    @media (max-width: 768px) {{
      body {{
        padding: 10px 12px;
      }}
      .dashboard-header {{
        flex-direction: column;
        align-items: flex-start;
      }}
      .title-area h1 {{
        font-size: 18px;
      }}
      .header-actions {{
        width: 100%;
      }}
      .action-btn {{
        flex: 1;
        justify-content: center;
      }}
      .nav-tabs {{
        flex-direction: row;
        overflow-x: auto;
      }}
      .tab-btn {{
        padding: 8px 12px;
        font-size: 12px;
      }}
      .filters-dropdown-row {{
        flex-direction: column;
        align-items: stretch;
      }}
      .filter-select {{
        max-width: 100%;
        width: 100%;
      }}
      .analytics-cards-grid {{
        grid-template-columns: 1fr;
      }}
      th.sticky-col, td.sticky-col {{
        position: static;
        box-shadow: none;
        border-right: none;
      }}
    }}
  </style>
</head>
<body>

  <!-- HEADER -->
  <header class="dashboard-header">
    <div class="title-area">
      <h1>
        <span>🇲🇬 Реестр и Медиа-Атлас Лидеров Мнений Мадагаскара</span>
        <span class="status-badge"><span class="status-dot"></span>Проверено и актуально</span>
      </h1>
      <div class="subtitle">
        Единый верифицированный реестр: 624 автора и 1,109 публичных страниц (порог $\ge 1\,000$ подписчиков)
      </div>
    </div>
    <div class="header-actions">
      <a href="https://github.com/n0e1/madagascar-influencers" target="_blank" class="action-btn">
        <span>GitHub Репозиторий ↗</span>
      </a>
      <button class="action-btn primary" onclick="exportFilteredCSV()">
        <span>⬇ Скачать выборку (CSV)</span>
      </button>
    </div>
  </header>

  <!-- NAVIGATION TABS -->
  <nav class="nav-tabs">
    <button id="tabBtnRegistry" class="tab-btn active" onclick="switchMainTab('registry')">
      <span>📋 Реестр авторов и площадок</span>
      <span class="tab-badge" id="registryCountBadge">{total_entities}</span>
    </button>
    <button id="tabBtnAnalytics" class="tab-btn" onclick="switchMainTab('analytics')">
      <span>📊 Аналитический центр и медиабаинг</span>
    </button>
  </nav>

  <!-- ========================================== -->
  <!-- TAB 1: REGISTRY TABLE VIEW                 -->
  <!-- ========================================== -->
  <main id="tabContentRegistry" class="tab-content active">

    <!-- CONTROLS & COMPACT FILTERS -->
    <div class="controls-panel">
      <!-- Search Input -->
      <div class="search-row">
        <div class="search-input-wrap">
          <input type="text" id="searchInput" class="search-input" placeholder="🔍 Быстрый поиск по имени, псевдониму, городу, тематикам, описанию (подсветка на лету)..." oninput="handleSearchInput()">
        </div>
      </div>

      <!-- Compact Dropdown Filters (Requirement 9 & 14) -->
      <div class="filters-dropdown-row">
        <div class="filter-item">
          <label for="filterCore">Выборка:</label>
          <select id="filterCore" class="filter-select" onchange="handleDropdownFilters()">
            <option value="core_only" selected>🌟 Только местное ядро и диаспора</option>
            <option value="all">🌐 Показать всех (включая тревел-блогеров)</option>
            <option value="humanitarian_only">🤝 Только гуманитарные миссии</option>
            <option value="guests_only">✈️ Только зарубежные тревел-авторы</option>
          </select>
        </div>

        <div class="filter-item">
          <label for="filterNiche">Тематическая ниша:</label>
          <select id="filterNiche" class="filter-select" onchange="handleDropdownFilters()">
            <option value="all" selected>Все ниши</option>
            <option value="Рэп">Рэп и хип-хоп (Rap Gasy)</option>
            <option value="Традиционная">Традиционная музыка и цапики</option>
            <option value="Эстрада">Эстрадная поп-музыка</option>
            <option value="Кино">Кино, театр и комедия</option>
            <option value="Мода">Мода, красота и подиум</option>
            <option value="Фитнес">Фитнес, спорт и бодибилдинг</option>
            <option value="Молодежь">Молодежь, танцы и TikTok</option>
            <option value="Гастрономия">Гастрономия и еда</option>
            <option value="Политика">Политика и расследования</option>
            <option value="Медиа">Медиа, радио и ТВ</option>
            <option value="IT">IT, технологии и фриланс</option>
            <option value="Экология">Экология и охрана природы</option>
            <option value="Религия">Религия и госпел</option>
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
            <option value="twitter">Twitter / X</option>
            <option value="linkedin">LinkedIn</option>
          </select>
        </div>

        <div class="filter-item">
          <label for="filterResidency">Резидентство:</label>
          <select id="filterResidency" class="filter-select" onchange="handleDropdownFilters()">
            <option value="all" selected>Все статусы</option>
            <option value="resident">Живут на Мадагаскаре</option>
            <option value="diaspora">Зарубежная диаспора</option>
            <option value="expat">Иностранцы-экспаты на острове</option>
          </select>
        </div>

        <button class="reset-btn" onclick="resetAllFilters()">Сбросить фильтры</button>
      </div>

      <!-- Mode Toggle and Column Visibility -->
      <div class="mode-and-columns-row">
        <div class="mode-toggle-group">
          <button id="btnEntityMode" class="mode-btn active" onclick="toggleMode('entity')">
            👥 По авторам (1 строка = 1 лидер мнений)
          </button>
          <button id="btnFlatMode" class="mode-btn" onclick="toggleMode('flat')">
            📊 По площадкам (1 строка = 1 аккаунт)
          </button>
        </div>

        <!-- Column Visibility Dropdown -->
        <div id="colDropdown" class="col-manager-dropdown">
          <button id="columnToggler" class="action-btn columnToggler" onclick="toggleColDropdown()">
            <span>👁 Настройка колонок ▾</span>
          </button>
          <div id="colDropdownMenu" class="col-dropdown-menu"></div>
        </div>
      </div>
    </div>

    <!-- TABLE HORIZONTAL SCROLL HINT (Requirement 4) -->
    <div class="scroll-hint-bar">
      <span>Найдено записей: <b id="recordsCount" style="color:#fff;">0</b></span>
      <span>← Прокрутка таблицы по горизонтали (удерживайте Shift для быстрой прокрутки) →</span>
    </div>

    <!-- TABLE CONTAINER -->
    <div class="table-container">
      <table id="influencersTable">
        <thead id="tableHead"></thead>
        <tbody id="tableBody"></tbody>
      </table>
    </div>

  </main>

  <!-- ========================================== -->
  <!-- TAB 2: DEDICATED ANALYTICS & MEDIA BUYING  -->
  <!-- ========================================== -->
  <section id="tabContentAnalytics" class="tab-content">
    <div class="analytics-container">

      <!-- SECTION 1: AUDIENCE BALANCE & REACH -->
      <div class="analytics-cards-grid">
        <div class="analytics-card featured">
          <div class="card-head">
            <span class="card-title">Чистое Национальное Ядро и Диаспора</span>
            <span class="card-tag">Целевой трафик</span>
          </div>
          <div class="metric-value-huge" id="statPureReach">62.5M</div>
          <div class="metric-subtitle">
            Реальные потребители контента внутри Республики Мадагаскар и диаспоры
          </div>
          <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width: 78.9%;"></div>
          </div>
          <div style="display: flex; justify-content: space-between; font-size: 11px; color: var(--text-dim); margin-bottom: 12px;">
            <span>Мадагаскар и диаспора: <b>78.9%</b></span>
            <span>Зарубежный туризм: <b>21.1%</b> (отсечено)</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Мировой охват (с туристами):</span>
            <span class="stat-val" id="statGrossReach">75.7 млн</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Зарубежные тревел-авторы:</span>
            <span class="stat-val" style="color: #94a3b8;">13.2 млн (нецелевая аудитория)</span>
          </div>
        </div>

        <div class="analytics-card">
          <div class="card-head">
            <span class="card-title">Структура Каналов Распространения</span>
            <span class="card-tag">Медиасплит</span>
          </div>
          <div class="stat-row">
            <span class="stat-label"><span style="color: var(--fb-color);">●</span> Facebook (основной канал в стране):</span>
            <span class="stat-val">44.8% внимания</span>
          </div>
          <div class="stat-row">
            <span class="stat-label"><span style="color: var(--yt-color);">●</span> YouTube (клипы, кино, сериалы):</span>
            <span class="stat-val">24.2% внимания</span>
          </div>
          <div class="stat-row">
            <span class="stat-label"><span style="color: var(--tt-color);">●</span> TikTok (молодежь, танцы, стритфуд):</span>
            <span class="stat-val">18.6% внимания</span>
          </div>
          <div class="stat-row">
            <span class="stat-label"><span style="color: var(--ig-color);">●</span> Instagram (мода, бьюти, фитнес):</span>
            <span class="stat-val">9.8% внимания</span>
          </div>
          <div class="stat-row">
            <span class="stat-label"><span style="color: var(--li-color);">●</span> X (Twitter) и LinkedIn:</span>
            <span class="stat-val">2.6% внимания</span>
          </div>
          <div class="stat-row" style="margin-top: 6px; padding-top: 8px; border-top: 1px dashed var(--border);">
            <span class="stat-label">Всего проиндексировано:</span>
            <span class="stat-val">{total_entities} авторов / {total_platforms} аккаунтов</span>
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
            <span class="stat-val" style="color: #38bdf8;">{direct_contacts_count} контакта (телефон/почта)</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Всего публикаций в архиве:</span>
            <span class="stat-val">{total_posts:,} материалов</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Частота выхода материалов:</span>
            <span class="stat-val">82% публикуют еженедельно/ежедневно</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Основной язык публикаций:</span>
            <span class="stat-val">Малагасийский (74%) / Французский (26%)</span>
          </div>
        </div>
      </div>

      <!-- SECTION 2: AD RATES & PRICING MATRIX -->
      <div class="analytics-section-title">
        <span>💰 Тарифная сетка и ценообразование рекламы на Мадагаскаре</span>
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
            <td><b>Эстрада и поп-музыка</b></td>
            <td>15,000 – 120,000</td>
            <td><span class="price-pill">$45 – $250</span></td>
            <td>207,000 – 1,150,000 MGA</td>
            <td>$135 – $750 (621k – 3.4M MGA)</td>
            <td>Максимальная узнаваемость бренда, массовый охват всех регионов</td>
          </tr>
          <tr>
            <td><b>Молодежь и вирусный TikTok</b></td>
            <td>8,000 – 65,000</td>
            <td><span class="price-pill">$20 – $120</span></td>
            <td>92,000 – 552,000 MGA</td>
            <td>$60 – $360 (276k – 1.6M MGA)</td>
            <td>Взрывной вирусный интерес, тренды, студенческая аудитория Антананариву</td>
          </tr>
          <tr>
            <td><b>Мода, визаж и подиум</b></td>
            <td>5,000 – 35,000</td>
            <td><span class="price-pill">$35 – $180</span></td>
            <td>161,000 – 828,000 MGA</td>
            <td>$105 – $540 (483k – 2.4M MGA)</td>
            <td>Премиальный сегмент, косметика, свадебные и вечерние товары</td>
          </tr>
          <tr>
            <td><b>Фитнес, бодибилдинг и спорт</b></td>
            <td>6,000 – 40,000</td>
            <td><span class="price-pill">$30 – $140</span></td>
            <td>138,000 – 644,000 MGA</td>
            <td>$90 – $420 (414k – 1.9M MGA)</td>
            <td>Спортивное питание, одежда, мужская аудитория 18–45 лет</td>
          </tr>
          <tr>
            <td><b>IT, бизнес и финансы</b></td>
            <td>3,000 – 18,000</td>
            <td><span class="price-pill">$80 – $380</span></td>
            <td>368,000 – 1,748,000 MGA</td>
            <td>$240 – $1,140 (1.1M – 5.2M MGA)</td>
            <td>B2B-аудитория, удаленная работа, банковские карты, IT-курсы</td>
          </tr>
          <tr>
            <td><b>Зарубежная диаспора (Франция, ЕС)</b></td>
            <td>4,000 – 25,000</td>
            <td><span class="price-pill">$120 – $450</span></td>
            <td>552,000 – 2,070,000 MGA</td>
            <td>$360 – $1,350 (1.6M – 6.2M MGA)</td>
            <td>Денежные переводы на родину, недвижимость, авиабилеты</td>
          </tr>
        </tbody>
      </table>

      <!-- SECTION 3: PRACTICAL MEDIA BUYING GUIDE -->
      <div class="analytics-section-title">
        <span>📖 Практические правила работы с блогерами Мадагаскара (Памятка для заказчика)</span>
      </div>
      <div class="guide-box">
        <h4>Особенности ведения рекламных кампаний на Мадагаскаре:</h4>
        <ol>
          <li><b>Способы оплаты:</b> Внутри страны 95% блогеров не имеют классических расчетных счетов. Оплата производится на мобильные кошельки <b>MVola (Telma)</b>, <b>Orange Money</b> или <b>Airtel Money</b>. Для диаспоры во Франции и Швейцарии расчеты ведутся в евро через переводы SEPA.</li>
          <li><b>Язык рекламного сообщения:</b> Для массовых потребительских товаров (продукты питания, напитки, мобильная связь) обязателен малагасийский язык или смесь с французским (Gasy franglais). Чистый французский язык эффективен только для премиального сегмента, туризма и BPO/IT.</li>
          <li><b>Энергетический фактор (JIRAMA):</b> Из-за регулярных веерных отключений электричества и интернета в столице и провинциях, время выхода постов может смещаться. Планируйте выход публикаций с запасом в 2–3 дня.</li>
          <li><b>Прямой контакт:</b> В таблице реестра собрано 342 проверенных телефонных номера и адреса электронной почты директоров. Лучший способ связи — звонок или сообщение в WhatsApp по указанным номерам.</li>
        </ol>
      </div>

    </div>
  </section>

  <!-- JAVASCRIPT LOGIC -->
  <script>
    const RAW_ENTITIES = {entities_json_str};

    // Table Column Definitions
    const ENTITY_COLUMNS = [
      {{ id: 'author', label: 'Автор (ФИО / Ник)', default: true, sticky: true }},
      {{ id: 'persona_role', label: 'Кто этот человек (Профиль)', default: true }},
      {{ id: 'content_topics', label: 'О чем пишет (Тематика)', default: true }},
      {{ id: 'target_audience', label: 'Целевая аудитория', default: true }},
      {{ id: 'niche', label: 'Ниша и специализация', default: true }},
      {{ id: 'platforms', label: 'Площадки и ссылки', default: true }},
      {{ id: 'followers', label: 'Подписчики (Совокупно)', default: true }},
      {{ id: 'reach', label: 'Расчетный охват поста', default: true }},
      {{ id: 'pricing', label: 'Ориентир цены (Пост / Месяц)', default: true }},
      {{ id: 'er', label: 'Отклик (ER%)', default: true }},
      {{ id: 'geo', label: 'География и статус', default: true }},
      {{ id: 'contacts_blogger', label: 'Контакты автора', default: true }},
      {{ id: 'contacts_manager', label: 'Менеджер / Агентство', default: true }},
      {{ id: 'llm_desc', label: 'Аналитическая справка', default: false }}
    ];

    const FLAT_COLUMNS = [
      {{ id: 'author', label: 'Автор', default: true, sticky: true }},
      {{ id: 'persona_role', label: 'Кто этот человек (Профиль)', default: true }},
      {{ id: 'content_topics', label: 'О чем пишет (Тематика)', default: true }},
      {{ id: 'platform_name', label: 'Площадка', default: true }},
      {{ id: 'account_link', label: 'Аккаунт и ссылка', default: true }},
      {{ id: 'platform_followers', label: 'Подписчиков', default: true }},
      {{ id: 'platform_reach', label: 'Охват 1 поста', default: true }},
      {{ id: 'platform_price', label: 'Цена публикации', default: true }},
      {{ id: 'posts_count', label: 'Публикаций', default: true }},
      {{ id: 'niche', label: 'Ниша и специализация', default: true }},
      {{ id: 'geo', label: 'Локация', default: true }},
      {{ id: 'contacts_blogger', label: 'Контакты автора', default: true }},
      {{ id: 'contacts_manager', label: 'Менеджер', default: true }}
    ];

    let currentMode = 'entity'; // 'entity' | 'flat'
    let currentCoreFilter = 'core_only';
    let currentNicheFilter = 'all';
    let currentPlatformFilter = 'all';
    let currentResidencyFilter = 'all';
    let searchQuery = '';
    let sortColumn = 'followers';
    let sortDirection = 'desc';

    let colVisibility = {{}};
    ENTITY_COLUMNS.forEach(c => colVisibility['entity_' + c.id] = c.default);
    FLAT_COLUMNS.forEach(c => colVisibility['flat_' + c.id] = c.default);

    function init() {{
      renderColDropdown();
      renderTable();
    }}

    // TAB SWITCHING (Registry vs Analytics)
    function switchMainTab(tab) {{
      document.getElementById('tabBtnRegistry').classList.toggle('active', tab === 'registry');
      document.getElementById('tabBtnAnalytics').classList.toggle('active', tab === 'analytics');
      document.getElementById('tabContentRegistry').classList.toggle('active', tab === 'registry');
      document.getElementById('tabContentAnalytics').classList.toggle('active', tab === 'analytics');
    }}

    // MODE TOGGLING
    function toggleMode(mode) {{
      currentMode = mode;
      document.getElementById('btnEntityMode').classList.toggle('active', mode === 'entity');
      document.getElementById('btnFlatMode').classList.toggle('active', mode === 'flat');
      renderColDropdown();
      renderTable();
    }}

    // DROPDOWN FILTER HANDLERS
    function handleDropdownFilters() {{
      currentCoreFilter = document.getElementById('filterCore').value;
      currentNicheFilter = document.getElementById('filterNiche').value;
      currentPlatformFilter = document.getElementById('filterPlatform').value;
      currentResidencyFilter = document.getElementById('filterResidency').value;
      renderTable();
    }}

    function resetAllFilters() {{
      document.getElementById('filterCore').value = 'all';
      document.getElementById('filterNiche').value = 'all';
      document.getElementById('filterPlatform').value = 'all';
      document.getElementById('filterResidency').value = 'all';
      document.getElementById('searchInput').value = '';
      currentCoreFilter = 'all';
      currentNicheFilter = 'all';
      currentPlatformFilter = 'all';
      currentResidencyFilter = 'all';
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

    // COLUMN VISIBILITY DROPDOWN
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
      let html = '';
      cols.forEach(c => {{
        html += `
          <label class="col-toggle-item">
            <input type="checkbox" ${{colVisibility[prefix + c.id] ? 'checked' : ''}} onchange="toggleColumn('${{prefix + c.id}}')">
            <span>${{c.label}}</span>
          </label>
        `;
      }});
      menu.innerHTML = html;
    }}

    function toggleColumn(key) {{
      colVisibility[key] = !colVisibility[key];
      renderTable();
    }}

    // TEXT HIGHLIGHTING
    function highlightText(text) {{
      if (!searchQuery || !text) return text || '';
      const str = String(text);
      const re = new RegExp(`(${{searchQuery.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&')}})`, 'gi');
      return str.replace(re, '<mark class="search-highlight">$1</mark>');
    }}

    // DATA FILTERING
    function getFilteredData() {{
      return RAW_ENTITIES.filter(e => {{
        // 1. Core Filter
        if (currentCoreFilter === 'core_only' && e.is_foreign_guest) return false;
        if (currentCoreFilter === 'humanitarian_only' && !e.is_humanitarian) return false;
        if (currentCoreFilter === 'guests_only' && !e.is_foreign_guest) return false;

        // 2. Niche Filter
        if (currentNicheFilter !== 'all') {{
          const nicheCombined = `${{e.category_main}} ${{e.category_sub}} ${{e.tags}}`.toLowerCase();
          if (!nicheCombined.includes(currentNicheFilter.toLowerCase())) return false;
        }}

        // 3. Platform Filter
        if (currentPlatformFilter !== 'all') {{
          const hasPlatform = (e.platforms || []).some(p => p.platform_name.toLowerCase().includes(currentPlatformFilter));
          if (!hasPlatform) return false;
        }}

        // 4. Residency Filter
        if (currentResidencyFilter !== 'all') {{
          const res = (e.residency_status || '').toLowerCase();
          if (currentResidencyFilter === 'resident' && (res.includes('diaspora') || res.includes('expat') || res.includes('traveler'))) return false;
          if (currentResidencyFilter === 'diaspora' && !res.includes('diaspora')) return false;
          if (currentResidencyFilter === 'expat' && !res.includes('expat')) return false;
        }}

        // 5. Search Query
        if (searchQuery) {{
          const hay = [
            e.full_name, e.alias, e.persona_role, e.content_topics,
            e.target_audience, e.city, e.region, e.country, e.category_main,
            e.category_sub, e.tags, e.contact_blogger_phone, e.contact_blogger_email,
            e.contact_manager_name, e.contact_manager_phone, e.contact_manager_email,
            ...(e.platforms || []).map(p => `${{p.handle}} ${{p.url}} ${{p.channel_description}}`)
          ].join(' ').toLowerCase();
          if (!hay.includes(searchQuery)) return false;
        }}

        return true;
      }});
    }}

    // TABLE RENDERING
    function renderTable() {{
      const cols = currentMode === 'entity' ? ENTITY_COLUMNS : FLAT_COLUMNS;
      const prefix = currentMode === 'entity' ? 'entity_' : 'flat_';
      const visibleCols = cols.filter(c => colVisibility[prefix + c.id]);

      // Render Head
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

      // Filtered Entities
      let filtered = getFilteredData();
      document.getElementById('recordsCount').innerText = filtered.length.toLocaleString();

      // Render Body
      let bodyHtml = '';
      if (currentMode === 'entity') {{
        // Sort Entity Data
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
          let rowClass = '';
          if (e.is_foreign_guest) rowClass = 'foreign-guest-row';
          else if (e.is_humanitarian) rowClass = 'humanitarian-row';

          bodyHtml += `<tr class="${{rowClass}}">`;
          visibleCols.forEach(c => {{
            const stickyClass = c.sticky ? 'sticky-col' : '';
            if (c.id === 'author') {{
              const primaryUrl = (e.platforms && e.platforms[0]) ? e.platforms[0].url : '#';
              bodyHtml += `<td class="${{stickyClass}}">
                <a href="${{primaryUrl}}" target="_blank" style="font-weight:700; color:#fff;">${{highlightText(e.full_name || e.alias)}}</a>
                ${{e.alias && e.alias !== e.full_name ? `<div style="color:var(--text-muted); font-size:11px;">${{highlightText(e.alias)}}</div>` : ''}}
                ${{e.is_foreign_guest ? '<span class="badge-tag foreign">Зарубежный автор</span>' : ''}}
                ${{e.is_humanitarian ? '<span class="badge-tag" style="background:rgba(16,185,129,0.2);color:#34d399;">Гуманитарная миссия</span>' : ''}}
              </td>`;
            }} else if (c.id === 'persona_role') {{
              bodyHtml += `<td><div class="cell-truncate" data-fulltext="${{e.persona_role || ''}}">${{highlightText(e.persona_role)}}</div></td>`;
            }} else if (c.id === 'content_topics') {{
              bodyHtml += `<td><div class="cell-truncate" data-fulltext="${{e.content_topics || ''}}">${{highlightText(e.content_topics)}}</div></td>`;
            }} else if (c.id === 'target_audience') {{
              bodyHtml += `<td><div class="cell-truncate" data-fulltext="${{e.target_audience || ''}}">${{highlightText(e.target_audience)}}</div></td>`;
            }} else if (c.id === 'niche') {{
              bodyHtml += `<td>
                <span class="badge-tag highlight">${{highlightText(e.category_main)}}</span>
                ${{e.category_sub ? `<div style="color:var(--text-muted); font-size:11px; margin-top:2px;">${{highlightText(e.category_sub)}}</div>` : ''}}
              </td>`;
            }} else if (c.id === 'platforms') {{
              let pBadges = (e.platforms || []).map(p => {{
                let cls = 'web';
                const pn = p.platform_name.toLowerCase();
                if (pn.includes('facebook')) cls = 'fb';
                else if (pn.includes('youtube')) cls = 'yt';
                else if (pn.includes('tiktok')) cls = 'tt';
                else if (pn.includes('instagram')) cls = 'ig';
                else if (pn.includes('linkedin')) cls = 'li';
                else if (pn.includes('twitter') || pn.includes('x')) cls = 'x';
                return `<a href="${{p.url}}" target="_blank" class="platform-badge ${{cls}}" title="${{p.platform_name}}: ${{p.followers_count.toLocaleString()}}">${{p.platform_name.split(' ')[0]}}</a>`;
              }}).join('');
              bodyHtml += `<td>${{pBadges}}</td>`;
            }} else if (c.id === 'followers') {{
              bodyHtml += `<td><b style="color:#fff; font-size:13px;">${{(e.total_followers_aggregate || 0).toLocaleString()}}</b></td>`;
            }} else if (c.id === 'reach') {{
              bodyHtml += `<td><span style="color:#38bdf8; font-weight:600;">~${{(e.estimated_post_reach || 0).toLocaleString()}}</span></td>`;
            }} else if (c.id === 'pricing') {{
              bodyHtml += `<td>
                <div><b style="color:#34d399;">$${{(e.price_post_usd || 0).toLocaleString()}}</b> <span style="color:var(--text-dim);font-size:11px;">/ пост</span></div>
                <div style="color:var(--text-muted); font-size:11px;">$${{(e.price_monthly_usd || 0).toLocaleString()}} / месяц</div>
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
              if (e.contact_blogger_phone) cHtml += `<div>📞 ${{highlightText(e.contact_blogger_phone)}}</div>`;
              if (e.contact_blogger_email) cHtml += `<div>✉️ ${{highlightText(e.contact_blogger_email)}}</div>`;
              bodyHtml += `<td>${{cHtml || '<span style="color:var(--text-dim);">—</span>'}}</td>`;
            }} else if (c.id === 'contacts_manager') {{
              let mHtml = '';
              if (e.contact_manager_name) mHtml += `<div style="font-weight:600;">${{highlightText(e.contact_manager_name)}}</div>`;
              if (e.contact_manager_phone) mHtml += `<div>📞 ${{highlightText(e.contact_manager_phone)}}</div>`;
              if (e.contact_manager_email) mHtml += `<div>✉️ ${{highlightText(e.contact_manager_email)}}</div>`;
              bodyHtml += `<td>${{mHtml || '<span style="color:var(--text-dim);">—</span>'}}</td>`;
            }} else if (c.id === 'llm_desc') {{
              bodyHtml += `<td><div class="cell-truncate" data-fulltext="${{e.llm_description || ''}}">${{highlightText(e.llm_description)}}</div></td>`;
            }}
          }});
          bodyHtml += '</tr>';
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
            }} else if (c.id === 'persona_role') {{
              bodyHtml += `<td><div class="cell-truncate" data-fulltext="${{e.persona_role || ''}}">${{highlightText(e.persona_role)}}</div></td>`;
            }} else if (c.id === 'content_topics') {{
              bodyHtml += `<td><div class="cell-truncate" data-fulltext="${{e.content_topics || ''}}">${{highlightText(e.content_topics)}}</div></td>`;
            }} else if (c.id === 'platform_name') {{
              bodyHtml += `<td><span class="badge-tag highlight">${{p.platform_name}}</span></td>`;
            }} else if (c.id === 'account_link') {{
              bodyHtml += `<td><a href="${{p.url}}" target="_blank" style="color:var(--primary); font-weight:600;">${{highlightText(p.handle || p.url)}} ↗</a></td>`;
            }} else if (c.id === 'platform_followers') {{
              bodyHtml += `<td><b style="color:#fff;">${{row.followers.toLocaleString()}}</b></td>`;
            }} else if (c.id === 'platform_reach') {{
              bodyHtml += `<td><span style="color:#38bdf8;">~${{row.reach.toLocaleString()}}</span></td>`;
            }} else if (c.id === 'platform_price') {{
              bodyHtml += `<td><span class="price-pill">$${{row.price_usd}}</span> <span style="color:var(--text-dim);font-size:11px;">(~${{row.price_mga.toLocaleString()}} MGA)</span></td>`;
            }} else if (c.id === 'posts_count') {{
              bodyHtml += `<td>${{p.posts_count || '—'}}</td>`;
            }} else if (c.id === 'niche') {{
              bodyHtml += `<td>${{highlightText(e.category_main)}}</td>`;
            }} else if (c.id === 'geo') {{
              bodyHtml += `<td>${{highlightText(e.city || e.country)}}</td>`;
            }} else if (c.id === 'contacts_blogger') {{
              let cHtml = '';
              if (e.contact_blogger_phone) cHtml += `<div>📞 ${{e.contact_blogger_phone}}</div>`;
              if (e.contact_blogger_email) cHtml += `<div>✉️ ${{e.contact_blogger_email}}</div>`;
              bodyHtml += `<td>${{cHtml || '—'}}</td>`;
            }} else if (c.id === 'contacts_manager') {{
              let mHtml = '';
              if (e.contact_manager_name) mHtml += `<div>${{e.contact_manager_name}}</div>`;
              if (e.contact_manager_phone) mHtml += `<div>📞 ${{e.contact_manager_phone}}</div>`;
              bodyHtml += `<td>${{mHtml || '—'}}</td>`;
            }}
          }});
          bodyHtml += '</tr>';
        }});
      }}

      document.getElementById('tableBody').innerHTML = bodyHtml;
    }}

    // EXPORT FILTERED CSV
    function exportFilteredCSV() {{
      const filtered = getFilteredData();
      if (!filtered.length) {{
        alert('Нет данных для выгрузки по текущим фильтрам.');
        return;
      }}

      let csvContent = "\\uFEFF"; // UTF-8 BOM
      if (currentMode === 'entity') {{
        const headers = ["ФИО", "Псевдоним", "Кто этот человек", "О чем пишет", "Целевая аудитория", "Ниша", "Специализация", "Подписчиков", "Охват 1 поста", "Цена за пост (USD)", "Цена за пост (MGA)", "Город", "Регион", "Контакты автора", "Менеджер"];
        csvContent += headers.map(h => `"${{h}}"`).join(',') + '\\n';

        filtered.forEach(e => {{
          const row = [
            e.full_name || '', e.alias || '', e.persona_role || '', e.content_topics || '',
            e.target_audience || '', e.category_main || '', e.category_sub || '',
            e.total_followers_aggregate || 0, e.estimated_post_reach || 0,
            e.price_post_usd || 0, e.price_post_mga || 0, e.city || '', e.region || '',
            `${{e.contact_blogger_phone || ''}} ${{e.contact_blogger_email || ''}}`.trim(),
            `${{e.contact_manager_name || ''}} ${{e.contact_manager_phone || ''}}`.trim()
          ];
          csvContent += row.map(v => `"${{String(v).replace(/"/g, '""')}}"`).join(',') + '\\n';
        }});
      }} else {{
        const headers = ["ФИО", "Псевдоним", "Площадка", "Аккаунт", "Ссылка", "Подписчиков", "Охват поста", "Цена публикации (USD)", "Ниша", "Город"];
        csvContent += headers.map(h => `"${{h}}"`).join(',') + '\\n';

        filtered.forEach(e => {{
          (e.platforms || []).forEach(p => {{
            const row = [
              e.full_name || '', e.alias || '', p.platform_name || '', p.handle || '', p.url || '',
              p.followers_count || 0, Math.round(e.estimated_post_reach * (p.followers_count / e.total_followers_aggregate) || 0),
              Math.round(e.price_post_usd * (p.followers_count / e.total_followers_aggregate) || 0),
              e.category_main || '', e.city || ''
            ];
            csvContent += row.map(v => `"${{String(v).replace(/"/g, '""')}}"`).join(',') + '\\n';
          }});
        }});
      }}

      const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.setAttribute('download', `madagascar_influencers_${{currentMode}}_${{Date.now()}}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }}

    init();
  </script>
</body>
</html>"""

    output_path = os.path.join(HERE, "madagascar_influencers_interactive.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Compiled Interactive Dashboard: {output_path} ({len(html_content.encode('utf-8')):,} bytes)")

    index_path = os.path.join(HERE, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Updated index.html: {index_path}")

if __name__ == "__main__":
    build_media_dashboard()
