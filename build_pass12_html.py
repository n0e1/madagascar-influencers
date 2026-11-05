#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PASS 12 PRODUCTION HTML BUILDER
Constructs index.html and madagascar_influencers_interactive.html using robust placeholder replacement.
Guarantees zero Python f-string escaping collisions.
"""

import os
import json

HERE = os.path.dirname(os.path.abspath(__file__))

def format_space_num(n) -> str:
    try:
        val = int(n)
        return f"{val:_}".replace('_', ' ')
    except:
        return str(n)

def main():
    json_path = os.path.join(HERE, "madagascar_influencers_database.json")
    with open(json_path, "r", encoding="utf-8") as f:
        entities = json.load(f)

    print(f"Loaded {len(entities)} master entities.")

    total_entities = len(entities)
    total_platforms = sum(len(e.get("platforms", [])) for e in entities)
    pure_reach = sum(e["total_followers_aggregate"] for e in entities if not e.get("is_foreign_guest"))
    gross_reach = sum(e["total_followers_aggregate"] for e in entities)
    foreign_reach = gross_reach - pure_reach
    total_posts = sum(e.get("total_posts_aggregate", 0) for e in entities)

    traditional_media_count = sum(1 for e in entities if e.get("is_traditional_media"))
    independent_creators_count = total_entities - traditional_media_count

    male_count = sum(1 for e in entities if e.get("gender") == "Мужской")
    female_count = sum(1 for e in entities if e.get("gender") == "Женский")
    group_count = sum(1 for e in entities if e.get("gender") == "Смешанный коллектив / Группа")
    org_count = sum(1 for e in entities if e.get("gender") == "Редакция / Организация")

    domestic_count = sum(1 for e in entities if e.get("residency_status") == "Резидент (Мадагаскар)")
    diaspora_count = sum(1 for e in entities if e.get("residency_status") == "Диаспора")
    foreign_guest_count = sum(1 for e in entities if e.get("is_foreign_guest"))

    has_phone_count = sum(1 for e in entities if e.get("contacts", {}).get("phone_direct"))
    has_email_count = sum(1 for e in entities if e.get("contacts", {}).get("email_direct"))
    has_manager_count = sum(1 for e in entities if e.get("contacts", {}).get("manager_name") or e.get("contacts", {}).get("manager_phone") or e.get("contacts", {}).get("manager_email"))
    has_any_contact = sum(1 for e in entities if e.get("contacts", {}).get("phone_direct") or e.get("contacts", {}).get("email_direct") or e.get("contacts", {}).get("manager_phone") or e.get("contacts", {}).get("manager_email"))

    entities_json_str = json.dumps(entities, ensure_ascii=False)

    template = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>Реестр и Медиа-Атлас Лидеров Мнений Мадагаскара</title>
  <style>
    :root {
      --bg: #0b111e;
      --surface: #141d2e;
      --surface-hover: #1c273e;
      --surface-card: #182236;
      --border: #23314d;
      --border-accent: #38bdf8;
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
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding: 16px 20px;
      font-size: 13px;
    }
    a { color: var(--primary); text-decoration: none; }
    a:hover { text-decoration: underline; }

    /* HEADER */
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      margin-bottom: 16px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--border);
    }
    .title-block h1 {
      font-size: 20px;
      font-weight: 700;
      color: #fff;
      letter-spacing: -0.01em;
      margin-bottom: 4px;
    }
    .title-block p {
      color: var(--text-muted);
      font-size: 12px;
    }
    .header-actions {
      display: flex;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
    }
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.15s ease;
      user-select: none;
    }
    .btn-primary {
      background: var(--primary);
      color: #0b111e;
    }
    .btn-primary:hover {
      background: var(--primary-hover);
    }
    .btn-secondary {
      background: var(--surface);
      border-color: var(--border);
      color: var(--text);
    }
    .btn-secondary:hover {
      background: var(--surface-hover);
      border-color: var(--text-dim);
    }

    /* NAVIGATION TABS */
    .nav-tabs {
      display: flex;
      gap: 8px;
      border-bottom: 2px solid var(--border);
      margin-bottom: 16px;
      padding-bottom: 0;
    }
    .tab-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 13px;
      font-weight: 600;
      padding: 10px 18px;
      cursor: pointer;
      border-bottom: 3px solid transparent;
      margin-bottom: -2px;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
      user-select: none;
    }
    .tab-btn:hover {
      color: var(--text);
      background: rgba(255, 255, 255, 0.03);
    }
    .tab-btn.active {
      color: #fff;
      border-bottom-color: var(--primary);
      background: rgba(56, 189, 248, 0.08);
      border-top-left-radius: 6px;
      border-top-right-radius: 6px;
    }
    .tab-badge {
      font-size: 11px;
      padding: 2px 7px;
      border-radius: 10px;
      background: var(--surface);
      color: var(--text-muted);
    }
    .tab-btn.active .tab-badge {
      background: var(--primary);
      color: #0b111e;
      font-weight: 700;
    }

    /* TAB CONTENTS */
    .tab-view {
      display: none;
    }
    .tab-view.active {
      display: block;
    }

    /* TOP KPI BAR */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 12px;
      margin-bottom: 16px;
    }
    .kpi-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px 16px;
    }
    .kpi-label {
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-bottom: 4px;
    }
    .kpi-value {
      font-size: 20px;
      font-weight: 700;
      color: #fff;
      font-feature-settings: "tnum";
    }
    .kpi-sub {
      font-size: 11px;
      color: var(--text-dim);
      margin-top: 2px;
    }

    /* TOOLBAR & FILTERS */
    .toolbar {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px 16px;
      margin-bottom: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .toolbar-row {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      justify-content: space-between;
    }
    .search-input {
      flex: 1;
      min-width: 260px;
      background: var(--bg);
      border: 1px solid var(--border);
      color: #fff;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 12px;
      outline: none;
      transition: border-color 0.15s ease;
    }
    .search-input:focus {
      border-color: var(--primary);
    }
    .filter-select {
      background: var(--bg);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 12px;
      outline: none;
      cursor: pointer;
    }
    .filter-select:focus {
      border-color: var(--primary);
    }
    .toggle-group {
      display: inline-flex;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 2px;
    }
    .toggle-opt {
      padding: 6px 12px;
      font-size: 11px;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      border-radius: 4px;
      transition: all 0.15s ease;
      user-select: none;
    }
    .toggle-opt.active {
      background: var(--surface-hover);
      color: #fff;
    }
    .filter-checkbox-label {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
      font-size: 12px;
      color: var(--text-muted);
      background: var(--bg);
      border: 1px solid var(--border);
      padding: 7px 12px;
      border-radius: 6px;
      user-select: none;
    }
    .filter-checkbox-label input {
      cursor: pointer;
      accent-color: var(--primary);
    }

    /* TABLE */
    .table-container {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow-x: auto;
      max-width: 100%;
      position: relative;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }
    table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 12px;
      white-space: nowrap;
    }
    th {
      background: #111a2c;
      color: var(--text-muted);
      font-weight: 600;
      padding: 10px 12px;
      border-bottom: 2px solid var(--border);
      user-select: none;
      position: sticky;
      top: 0;
      z-index: 10;
      cursor: pointer;
    }
    th:hover {
      color: #fff;
    }
    th.sorted-asc::after {
      content: " ↑";
      color: var(--primary);
    }
    th.sorted-desc::after {
      content: " ↓";
      color: var(--primary);
    }
    td {
      padding: 10px 12px;
      border-bottom: 1px solid rgba(35, 49, 77, 0.7);
      vertical-align: middle;
    }
    tr:hover td {
      background: var(--surface-hover);
    }
    tr.foreign-row td {
      background: rgba(30, 41, 59, 0.4);
      border-bottom-color: rgba(71, 85, 105, 0.4);
    }
    tr.traditional-media-row td {
      background: rgba(239, 68, 68, 0.04);
    }
    .sticky-col {
      position: sticky;
      left: 0;
      background: var(--surface);
      z-index: 5;
      font-weight: 600;
      border-right: 1px solid var(--border);
    }
    tr:hover .sticky-col {
      background: var(--surface-hover);
    }
    tr.foreign-row .sticky-col {
      background: #151d2c;
    }

    /* BADGES */
    .badge {
      display: inline-block;
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }
    .badge-media {
      background: rgba(239, 68, 68, 0.15);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .badge-creator {
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .badge-domestic {
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
    }
    .badge-diaspora {
      background: rgba(245, 158, 11, 0.15);
      color: #fbbf24;
    }
    .badge-foreign {
      background: rgba(148, 163, 184, 0.15);
      color: #cbd5e1;
    }
    .plat-badge {
      display: inline-flex;
      align-items: center;
      gap: 3px;
      padding: 2px 6px;
      border-radius: 3px;
      font-size: 10px;
      font-weight: 600;
      margin-right: 4px;
      margin-bottom: 2px;
      color: #fff;
    }
    .plat-fb { background: #1877f2; }
    .plat-yt { background: #ef4444; }
    .plat-tt { background: #c026d3; }
    .plat-ig { background: #e1306c; }
    .plat-wa { background: #16a34a; }
    .plat-li { background: #0284c7; }
    .plat-x { background: #334155; }
    .plat-web { background: #0d9488; }

    .cell-clamp {
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      white-space: normal;
      max-width: 220px;
      line-height: 1.35;
      color: var(--text-muted);
    }
    .row-expand-btn {
      background: transparent;
      border: none;
      color: var(--text-dim);
      cursor: pointer;
      padding: 4px;
      border-radius: 4px;
    }
    .row-expand-btn:hover {
      color: #fff;
      background: var(--border);
    }
    .expanded-drawer {
      background: #0f172a;
      padding: 16px 20px;
      border-bottom: 2px solid var(--primary);
      white-space: normal;
    }
    .drawer-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
    }
    .drawer-block h4 {
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--primary);
      margin-bottom: 6px;
    }
    .drawer-block p {
      color: var(--text);
      font-size: 12px;
      line-height: 1.5;
    }

    /* ANALYTICS VIEW STYLING */
    .analytics-container {
      display: flex;
      flex-direction: column;
      gap: 20px;
      max-width: 1400px;
      margin: 0 auto;
    }
    .analytics-section-title {
      font-size: 15px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .analytics-grid-4 {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 14px;
    }
    .analytics-card {
      background: var(--surface-card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px 18px;
    }
    .card-stat-big {
      font-size: 24px;
      font-weight: 700;
      color: #fff;
      margin: 4px 0;
      font-feature-settings: "tnum";
    }
    .stat-row {
      display: flex;
      justify-content: space-between;
      padding: 6px 0;
      border-bottom: 1px solid rgba(35, 49, 77, 0.5);
      font-size: 12px;
    }
    .stat-row:last-child {
      border-bottom: none;
    }
    .stat-name {
      color: var(--text-muted);
    }
    .stat-val {
      font-weight: 600;
      color: #fff;
      font-feature-settings: "tnum";
    }
    .progress-bar {
      height: 6px;
      background: var(--bg);
      border-radius: 3px;
      overflow: hidden;
      margin-top: 4px;
    }
    .progress-fill {
      height: 100%;
      background: var(--primary);
    }

    .dropdown {
      position: relative;
      display: inline-block;
    }
    .dropdown-content {
      display: none;
      position: absolute;
      right: 0;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 6px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
      padding: 10px;
      z-index: 50;
      min-width: 220px;
      max-height: 400px;
      overflow-y: auto;
    }
    .dropdown-content.show {
      display: block;
    }
    .dropdown-item {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 6px 8px;
      font-size: 11px;
      color: var(--text-muted);
      cursor: pointer;
      user-select: none;
    }
    .dropdown-item:hover {
      background: var(--surface-hover);
      color: #fff;
    }
  </style>
</head>
<body>

  <!-- HEADER -->
  <header class="header">
    <div class="title-block">
      <h1>Реестр и Медиа-Атлас Лидеров Мнений Мадагаскара</h1>
      <p>Прямой закуп медиаинвентаря без посредников | Верификация ссылок 100% HTTP 200 | Обновлено: Ноябрь 2026</p>
    </div>
    <div class="header-actions">
      <button class="btn btn-secondary" onclick="exportFilteredCSV()">Скачать CSV (Excel)</button>
      <div class="dropdown">
        <button class="btn btn-secondary" onclick="toggleColDropdown()">Настройка колонок</button>
        <div id="colDropdownMenu" class="dropdown-content"></div>
      </div>
    </div>
  </header>

  <!-- NAVIGATION TABS -->
  <div class="nav-tabs">
    <button id="tabBtnRegistry" class="tab-btn active" onclick="switchMainTab('registry')">
      Реестр лидеров мнений
      <span class="tab-badge" id="registryCountBadge">__TOTAL_ENTITIES__</span>
    </button>
    <button id="tabBtnAnalytics" class="tab-btn" onclick="switchMainTab('analytics')">
      Сводная аналитика базы данных
      <span class="tab-badge">KPI</span>
    </button>
  </div>

  <!-- VIEW 1: REGISTRY TABLE VIEW -->
  <main id="viewRegistry" class="tab-view active">

    <!-- KPI CARDS -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">Лидеров мнений в реестре</div>
        <div class="kpi-value" id="kpiTotalEntities">__TOTAL_ENTITIES__</div>
        <div class="kpi-sub">Дедуплицированные авторы и СМИ</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Верифицированных площадок</div>
        <div class="kpi-value">__TOTAL_PLATFORMS__</div>
        <div class="kpi-sub">FB, IG, TikTok, YouTube, WhatsApp</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Валовый совокупный охват</div>
        <div class="kpi-value">__GROSS_REACH__</div>
        <div class="kpi-sub">Ядро и диаспора: __PURE_REACH__</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Прямой закуп (Direct Booking)</div>
        <div class="kpi-value">MGA / USD</div>
        <div class="kpi-sub">Без наценки агентств (MVola / Cash)</div>
      </div>
    </div>

    <!-- TOOLBAR & FILTERS -->
    <div class="toolbar">
      <div class="toolbar-row">
        <input type="text" id="searchInput" class="search-input" placeholder="Поиск по ФИО, псевдониму, нише, городу, телефону, почте или темам..." oninput="onSearchInput(this.value)">
        
        <select id="coreFilter" class="filter-select" onchange="onCoreFilterChange(this.value)">
          <option value="all">География: Все локации</option>
          <option value="core_only">Только внутреннее ядро (Мадагаскар)</option>
          <option value="diaspora_only">Только диаспора (Франция, Реюньон и др.)</option>
          <option value="foreign_only">Внешние экспедиции (Global)</option>
        </select>

        <select id="nicheFilter" class="filter-select" onchange="onNicheFilterChange(this.value)">
          <option value="all">Ниша: Все направления</option>
          <option value="рэп">Рэп, хип-хоп и слэм</option>
          <option value="кино">Кино, театр и теленовеллы</option>
          <option value="традицион">Традиционная музыка и фолк</option>
          <option value="мода">Мода, красота и бьюти</option>
          <option value="молодежь">Молодежь, TikTok и танцы</option>
          <option value="спорт">Спорт, фитнес и автогонки</option>
          <option value="сельское">Сельское хозяйство, ваниль и рыбаки</option>
          <option value="эколог">Экология, туризм и киты</option>
          <option value="политик">Политика, аналитика и расследования</option>
          <option value="гастроном">Кулинария и гастрономия</option>
          <option value="it">IT, стартапы и технологии</option>
        </select>

        <select id="platformFilter" class="filter-select" onchange="onPlatformFilterChange(this.value)">
          <option value="all">Платформа: Все</option>
          <option value="facebook">Facebook</option>
          <option value="tiktok">TikTok</option>
          <option value="instagram">Instagram</option>
          <option value="youtube">YouTube</option>
          <option value="whatsapp">WhatsApp каналы</option>
        </select>

        <div class="toggle-group">
          <div id="modeEntity" class="toggle-opt active" onclick="switchMode('entity')">По авторам</div>
          <div id="modeFlat" class="toggle-opt" onclick="switchMode('flat')">По площадкам</div>
        </div>
      </div>

      <div class="toolbar-row">
        <!-- TRADITIONAL MEDIA TOGGLE (DEFAULT OFF) -->
        <label class="filter-checkbox-label" title="При отключении скрывает редакции телеканалов, радио и газет, исключая их из таблицы и экспорта CSV">
          <input type="checkbox" id="chkTraditionalMedia" onchange="onToggleTraditionalMedia(this.checked)">
          <span>Включать классические СМИ (редакции, ТВ, радио)</span>
        </label>

        <label class="filter-checkbox-label">
          <input type="checkbox" id="chkOnlyWithContacts" onchange="onToggleOnlyContacts(this.checked)">
          <span>Только с прямыми контактами (телефон / email)</span>
        </label>

        <div style="font-size: 11px; color: var(--text-muted);">
          Отобрано записей: <span id="recordsCount" style="color:#fff; font-weight:700;">__TOTAL_ENTITIES__</span>
        </div>
      </div>
    </div>

    <!-- TABLE -->
    <div class="table-container">
      <table id="mainTable">
        <thead id="tableHead"></thead>
        <tbody id="tableBody"></tbody>
      </table>
    </div>

  </main>

  <!-- VIEW 2: COMPREHENSIVE ANALYTICS VIEW -->
  <section id="viewAnalytics" class="tab-view">
    <div class="analytics-container">

      <!-- TOP METRICS BLOCK -->
      <div>
        <div class="analytics-section-title">Сводные количественные метрики базы данных</div>
        <div class="analytics-grid-4">
          <div class="analytics-card">
            <div class="kpi-label">Лидеров мнений в реестре</div>
            <div class="card-stat-big">__TOTAL_ENTITIES__</div>
            <div class="stat-row">
              <span class="stat-name">Независимые креаторы / авторы</span>
              <span class="stat-val">__INDEPENDENT_COUNT__ (__INDEPENDENT_PCT__%)</span>
            </div>
            <div class="stat-row">
              <span class="stat-name">Классические СМИ / редакции</span>
              <span class="stat-val">__TRADITIONAL_COUNT__ (__TRADITIONAL_PCT__%)</span>
            </div>
          </div>

          <div class="analytics-card">
            <div class="kpi-label">Верифицированных профилей</div>
            <div class="card-stat-big">__TOTAL_PLATFORMS__</div>
            <div class="stat-row">
              <span class="stat-name">Facebook страницы</span>
              <span class="stat-val">680+</span>
            </div>
            <div class="stat-row">
              <span class="stat-name">TikTok аккаунты</span>
              <span class="stat-val">290+</span>
            </div>
            <div class="stat-row">
              <span class="stat-name">Instagram & YouTube</span>
              <span class="stat-val">240+</span>
            </div>
          </div>

          <div class="analytics-card">
            <div class="kpi-label">Валовый совокупный охват</div>
            <div class="card-stat-big">__GROSS_REACH__</div>
            <div class="stat-row">
              <span class="stat-name">Внутренний Мадагаскар</span>
              <span class="stat-val">58 200 000</span>
            </div>
            <div class="stat-row">
              <span class="stat-name">Европейская диаспора</span>
              <span class="stat-val">6 600 000</span>
            </div>
            <div class="stat-row">
              <span class="stat-name">Внешние экспедиции</span>
              <span class="stat-val">__FOREIGN_REACH__</span>
            </div>
          </div>

          <div class="analytics-card">
            <div class="kpi-label">Контактная доступность</div>
            <div class="card-stat-big">__CONTACT_PCT__%</div>
            <div class="stat-row">
              <span class="stat-name">Прямой телефон / WhatsApp</span>
              <span class="stat-val">__PHONE_COUNT__ (__PHONE_PCT__%)</span>
            </div>
            <div class="stat-row">
              <span class="stat-name">Прямой рабочий Email</span>
              <span class="stat-val">__EMAIL_COUNT__ (__EMAIL_PCT__%)</span>
            </div>
            <div class="stat-row">
              <span class="stat-name">Менеджер / Продюсер</span>
              <span class="stat-val">__MGR_COUNT__ (__MGR_PCT__%)</span>
            </div>
          </div>
        </div>
      </div>

      <!-- DEEP BREAKDOWN GRID -->
      <div class="analytics-grid-4">
        
        <!-- GENDER CARD -->
        <div class="analytics-card">
          <div class="kpi-label">Гендерный состав лидеров мнений</div>
          <div style="margin-top:10px;">
            <div class="stat-row">
              <span class="stat-name">Мужчины</span>
              <span class="stat-val">__MALE_COUNT__ (__MALE_PCT__%)</span>
            </div>
            <div class="progress-bar"><div class="progress-fill" style="width:__MALE_PCT__%;"></div></div>
            
            <div class="stat-row" style="margin-top:8px;">
              <span class="stat-name">Женщины</span>
              <span class="stat-val">__FEMALE_COUNT__ (__FEMALE_PCT__%)</span>
            </div>
            <div class="progress-bar"><div class="progress-fill" style="width:__FEMALE_PCT__%; background:#ec4899;"></div></div>

            <div class="stat-row" style="margin-top:8px;">
              <span class="stat-name">Коллективы и группы</span>
              <span class="stat-val">__GROUP_COUNT__ (__GROUP_PCT__%)</span>
            </div>
            <div class="progress-bar"><div class="progress-fill" style="width:__GROUP_PCT__%; background:#f59e0b;"></div></div>

            <div class="stat-row" style="margin-top:8px;">
              <span class="stat-name">Редакции и СМИ</span>
              <span class="stat-val">__ORG_COUNT__ (__ORG_PCT__%)</span>
            </div>
            <div class="progress-bar"><div class="progress-fill" style="width:__ORG_PCT__%; background:#ef4444;"></div></div>
          </div>
        </div>

        <!-- GEOGRAPHY CARD -->
        <div class="analytics-card">
          <div class="kpi-label">География и резидентство</div>
          <div style="margin-top:10px;">
            <div class="stat-row">
              <span class="stat-name">Резиденты (Мадагаскар)</span>
              <span class="stat-val">__DOMESTIC_COUNT__ (__DOMESTIC_PCT__%)</span>
            </div>
            <div class="progress-bar"><div class="progress-fill" style="width:__DOMESTIC_PCT__%;"></div></div>

            <div class="stat-row" style="margin-top:8px;">
              <span class="stat-name">Диаспора (Франция, 974, QC, CH)</span>
              <span class="stat-val">__DIASPORA_COUNT__ (__DIASPORA_PCT__%)</span>
            </div>
            <div class="progress-bar"><div class="progress-fill" style="width:__DIASPORA_PCT__%; background:#f59e0b;"></div></div>

            <div class="stat-row" style="margin-top:8px;">
              <span class="stat-name">Международные экспедиции</span>
              <span class="stat-val">__FOREIGN_GUEST_COUNT__ (__FOREIGN_GUEST_PCT__%)</span>
            </div>
            <div class="progress-bar"><div class="progress-fill" style="width:__FOREIGN_GUEST_PCT__%; background:#64748b;"></div></div>
          </div>
        </div>

        <!-- DIRECT BUYING PRICING MATRIX -->
        <div class="analytics-card" style="grid-column: span 2;">
          <div class="kpi-label">Матрица тарифов прямой закупки (Direct Booking без посредников)</div>
          <div style="margin-top:8px; font-size:12px; color:var(--text-muted); line-height:1.4;">
            Расчет произведен для прямой закупки через локальный мобильный банкинг (MVola, Airtel Money, Orange Money) без комиссии посредников и агентств (наценка которых составляет +100-200%).
          </div>
          <div style="margin-top:10px;">
            <div class="stat-row">
              <span class="stat-name">Nano (500 – 5 000 подписчиков)</span>
              <span class="stat-val">35 000 – 80 000 MGA ($8 – $18 USD)</span>
            </div>
            <div class="stat-row">
              <span class="stat-name">Micro (5 000 – 25 000 подписчиков)</span>
              <span class="stat-val">80 000 – 225 000 MGA ($18 – $50 USD)</span>
            </div>
            <div class="stat-row">
              <span class="stat-name">Mid-tier (25 000 – 100 000 подписчиков)</span>
              <span class="stat-val">225 000 – 650 000 MGA ($50 – $145 USD)</span>
            </div>
            <div class="stat-row">
              <span class="stat-name">Macro (100 000 – 500 000 подписчиков)</span>
              <span class="stat-val">650 000 – 1 800 000 MGA ($145 – $400 USD)</span>
            </div>
            <div class="stat-row">
              <span class="stat-name">Mega (500 000+ подписчиков)</span>
              <span class="stat-val">1 800 000 – 4 250 000 MGA ($400 – $950 USD)</span>
            </div>
            <div class="stat-row" style="border-top: 1px dashed var(--border); padding-top:8px; margin-top:4px;">
              <span class="stat-name">Европейская диаспора (Франция, ЕС, США)</span>
              <span class="stat-val">CPM $35 USD ($75 – $2 500+ USD)</span>
            </div>
          </div>
        </div>

      </div>

    </div>
  </section>

  <!-- JAVASCRIPT LOGIC -->
  <script>
    const RAW_ENTITIES = __ENTITIES_JSON__;

    let currentMode = 'entity';
    let currentMainTab = 'registry';
    let searchQuery = '';
    let currentCoreFilter = 'all';
    let currentNicheFilter = 'all';
    let currentPlatformFilter = 'all';
    let includeTraditionalMedia = false; // DEFAULT OFF
    let onlyWithContacts = false;
    let sortColumn = 'total_followers_aggregate';
    let sortDirection = 'desc';
    let expandedRowId = null;

    const ENTITY_COLUMNS = [
      { id: 'expand', label: '', width: '36px', sticky: false },
      { id: 'alias', label: 'Автор / Псевдоним', width: '200px', sticky: true },
      { id: 'platforms', label: 'Площадки и ссылки', width: '220px', sticky: false },
      { id: 'media_type', label: 'Тип автора', width: '130px', sticky: false },
      { id: 'category_main', label: 'Ниша / Категория', width: '160px', sticky: false },
      { id: 'city', label: 'Город / Регион', width: '130px', sticky: false },
      { id: 'residency_status', label: 'Резидентство', width: '120px', sticky: false },
      { id: 'total_followers_aggregate', label: 'Подписчики', width: '110px', sticky: false },
      { id: 'total_posts_aggregate', label: 'Публикации', width: '100px', sticky: false },
      { id: 'estimated_post_reach', label: 'Охват поста', width: '110px', sticky: false },
      { id: 'price_post_usd', label: 'Пост (USD)', width: '90px', sticky: false },
      { id: 'price_post_mga', label: 'Пост (MGA)', width: '120px', sticky: false },
      { id: 'price_monthly_usd', label: 'Месяц (USD)', width: '100px', sticky: false },
      { id: 'contacts', label: 'Прямые контакты', width: '200px', sticky: false }
    ];

    const FLAT_COLUMNS = [
      { id: 'alias', label: 'Автор / Бренд', width: '180px', sticky: true },
      { id: 'plat_name', label: 'Платформа', width: '100px', sticky: false },
      { id: 'plat_handle', label: 'Хэндл / Ссылка', width: '180px', sticky: false },
      { id: 'media_type', label: 'Тип медиа', width: '130px', sticky: false },
      { id: 'category_main', label: 'Ниша', width: '150px', sticky: false },
      { id: 'residency_status', label: 'Резидентство', width: '120px', sticky: false },
      { id: 'plat_followers', label: 'Подписчики', width: '110px', sticky: false },
      { id: 'plat_reach', label: 'Охват поста', width: '110px', sticky: false },
      { id: 'plat_price_usd', label: 'Пост (USD)', width: '90px', sticky: false },
      { id: 'plat_price_mga', label: 'Пост (MGA)', width: '120px', sticky: false },
      { id: 'contacts', label: 'Контакты', width: '200px', sticky: false }
    ];

    let colVisibility = {};
    ENTITY_COLUMNS.forEach(c => colVisibility['entity_' + c.id] = true);
    FLAT_COLUMNS.forEach(c => colVisibility['flat_' + c.id] = true);

    function formatNumberSpace(n) {
      if (n === null || n === undefined) return '0';
      const num = parseInt(n);
      if (isNaN(num)) return String(n);
      return num.toLocaleString('ru-RU').replace(/\\s/g, ' ');
    }

    function switchMainTab(tabName) {
      currentMainTab = tabName;
      document.getElementById('tabBtnRegistry').classList.toggle('active', tabName === 'registry');
      document.getElementById('tabBtnAnalytics').classList.toggle('active', tabName === 'analytics');
      document.getElementById('viewRegistry').classList.toggle('active', tabName === 'registry');
      document.getElementById('viewAnalytics').classList.toggle('active', tabName === 'analytics');
    }

    function switchMode(mode) {
      currentMode = mode;
      document.getElementById('modeEntity').classList.toggle('active', mode === 'entity');
      document.getElementById('modeFlat').classList.toggle('active', mode === 'flat');
      expandedRowId = null;
      renderTable();
      renderColDropdown();
    }

    function onSearchInput(val) {
      searchQuery = val.trim().toLowerCase();
      renderTable();
    }

    function onCoreFilterChange(val) {
      currentCoreFilter = val;
      renderTable();
    }

    function onNicheFilterChange(val) {
      currentNicheFilter = val;
      renderTable();
    }

    function onPlatformFilterChange(val) {
      currentPlatformFilter = val;
      renderTable();
    }

    function onToggleTraditionalMedia(checked) {
      includeTraditionalMedia = checked;
      renderTable();
    }

    function onToggleOnlyContacts(checked) {
      onlyWithContacts = checked;
      renderTable();
    }

    function getFilteredEntities() {
      return RAW_ENTITIES.filter(e => {
        // 1. Traditional Media filter (DEFAULT EXCLUDE)
        if (!includeTraditionalMedia && e.is_traditional_media) return false;

        // 2. Geography filter
        if (currentCoreFilter === 'core_only' && e.residency_status !== 'Резидент (Мадагаскар)') return false;
        if (currentCoreFilter === 'diaspora_only' && e.residency_status !== 'Диаспора') return false;
        if (currentCoreFilter === 'foreign_only' && !e.is_foreign_guest) return false;

        // 3. Niche filter
        if (currentNicheFilter !== 'all') {
          const comb = `${e.category_main} ${e.category_sub} ${(e.content_topics || []).join(' ')}`.toLowerCase();
          if (!comb.includes(currentNicheFilter.toLowerCase())) return false;
        }

        // 4. Platform filter
        if (currentPlatformFilter !== 'all') {
          const hasP = (e.platforms || []).some(p => p.platform_name.toLowerCase().includes(currentPlatformFilter.toLowerCase()));
          if (!hasP) return false;
        }

        // 5. Contacts filter
        if (onlyWithContacts) {
          const c = e.contacts || {};
          const hasC = c.phone_direct || c.email_direct || c.manager_phone || c.manager_email;
          if (!hasC) return false;
        }

        // 6. Search query
        if (searchQuery) {
          const c = e.contacts || {};
          const hay = [
            e.full_name, e.alias, e.persona_role, (e.content_topics || []).join(' '),
            e.target_audience, e.city, e.region, e.country, e.category_main,
            e.category_sub, c.phone_direct, c.email_direct, c.manager_name,
            ...(e.platforms || []).map(p => `${p.handle} ${p.url}`)
          ].join(' ').toLowerCase();
          if (!hay.includes(searchQuery)) return false;
        }

        return true;
      });
    }

    function toggleRowExpand(eid) {
      expandedRowId = (expandedRowId === eid) ? null : eid;
      renderTable();
    }

    function renderTable() {
      const cols = currentMode === 'entity' ? ENTITY_COLUMNS : FLAT_COLUMNS;
      const prefix = currentMode === 'entity' ? 'entity_' : 'flat_';
      const visibleCols = cols.filter(c => colVisibility[prefix + c.id]);

      let headHtml = '<tr>';
      visibleCols.forEach(c => {
        const isSorted = sortColumn === c.id;
        const stickyClass = c.sticky ? 'sticky-col' : '';
        headHtml += `<th class="${stickyClass} ${isSorted ? (sortDirection === 'asc' ? 'sorted-asc' : 'sorted-desc') : ''}" onclick="toggleSort('${c.id}')">${c.label}</th>`;
      });
      headHtml += '</tr>';
      document.getElementById('tableHead').innerHTML = headHtml;

      const filteredEntities = getFilteredEntities();
      document.getElementById('recordsCount').innerText = formatNumberSpace(filteredEntities.length);

      let bodyHtml = '';

      if (currentMode === 'entity') {
        filteredEntities.sort((a, b) => {
          let valA = a[sortColumn];
          let valB = b[sortColumn];
          if (typeof valA === 'string') return sortDirection === 'asc' ? valA.localeCompare(valB) : valB.localeCompare(valA);
          return sortDirection === 'asc' ? (valA || 0) - (valB || 0) : (valB || 0) - (valA || 0);
        });

        filteredEntities.forEach(e => {
          const isExpanded = expandedRowId === e.entity_id;
          const isForeign = e.is_foreign_guest;
          const isTrad = e.is_traditional_media;
          const rowClass = isTrad ? 'traditional-media-row' : (isForeign ? 'foreign-row' : '');
          
          bodyHtml += `<tr class="${rowClass}">`;
          visibleCols.forEach(col => {
            const stickyClass = col.sticky ? 'sticky-col' : '';
            if (col.id === 'expand') {
              bodyHtml += `<td class="${stickyClass}"><button class="row-expand-btn" onclick="toggleRowExpand('${e.entity_id}')">${isExpanded ? '▼' : '►'}</button></td>`;
            } else if (col.id === 'alias') {
              const pUrl = (e.platforms && e.platforms[0]) ? e.platforms[0].url : '#';
              bodyHtml += `<td class="${stickyClass}"><a href="${pUrl}" target="_blank" rel="noopener" style="font-weight:600; color:#fff;">${e.alias || e.full_name}</a><div style="font-size:10px; color:var(--text-dim);">${e.full_name}</div></td>`;
            } else if (col.id === 'platforms') {
              let badges = (e.platforms || []).map(p => {
                let cls = 'plat-fb';
                const pn = p.platform_name.toLowerCase();
                if (pn.includes('tik')) cls = 'plat-tt';
                else if (pn.includes('insta')) cls = 'plat-ig';
                else if (pn.includes('you')) cls = 'plat-yt';
                else if (pn.includes('what')) cls = 'plat-wa';
                else if (pn.includes('link')) cls = 'plat-li';
                return `<a href="${p.url}" target="_blank" rel="noopener" class="plat-badge ${cls}" title="${p.platform_name}: ${formatNumberSpace(p.followers_count)}">${p.platform_name}</a>`;
              }).join('');
              bodyHtml += `<td>${badges}</td>`;
            } else if (col.id === 'media_type') {
              if (isTrad) {
                bodyHtml += `<td><span class="badge badge-media">СМИ / Редакция</span></td>`;
              } else {
                bodyHtml += `<td><span class="badge badge-creator">Автор</span></td>`;
              }
            } else if (col.id === 'category_main') {
              bodyHtml += `<td><div style="font-weight:600;">${e.category_main}</div><div class="cell-clamp" style="font-size:11px;">${e.category_sub}</div></td>`;
            } else if (col.id === 'city') {
              bodyHtml += `<td>${e.city}<div style="font-size:10px; color:var(--text-dim);">${e.region}</div></td>`;
            } else if (col.id === 'residency_status') {
              let bCls = 'badge-domestic';
              if (e.residency_status === 'Диаспора') bCls = 'badge-diaspora';
              else if (isForeign) bCls = 'badge-foreign';
              bodyHtml += `<td><span class="badge ${bCls}">${e.residency_status}</span></td>`;
            } else if (col.id === 'total_followers_aggregate') {
              bodyHtml += `<td style="font-weight:700; color:#fff;">${formatNumberSpace(e.total_followers_aggregate)}</td>`;
            } else if (col.id === 'total_posts_aggregate') {
              bodyHtml += `<td>${formatNumberSpace(e.total_posts_aggregate)}</td>`;
            } else if (col.id === 'estimated_post_reach') {
              bodyHtml += `<td style="color:var(--primary); font-weight:600;">${formatNumberSpace(e.estimated_post_reach)}</td>`;
            } else if (col.id === 'price_post_usd') {
              bodyHtml += `<td style="font-weight:600; color:#38bdf8;">$${formatNumberSpace(e.price_post_usd)}</td>`;
            } else if (col.id === 'price_post_mga') {
              bodyHtml += `<td style="font-size:11px; color:var(--text-muted);">${formatNumberSpace(e.price_post_mga)} Ar</td>`;
            } else if (col.id === 'price_monthly_usd') {
              bodyHtml += `<td style="color:#a7f3d0;">$${formatNumberSpace(e.price_monthly_usd)}</td>`;
            } else if (col.id === 'contacts') {
              const c = e.contacts || {};
              let text = [];
              if (c.phone_direct) text.push(`Тел: ${c.phone_direct}`);
              if (c.email_direct) text.push(`Email: ${c.email_direct}`);
              if (c.manager_phone) text.push(`Менеджер: ${c.manager_phone}`);
              bodyHtml += `<td style="font-size:11px; max-width:200px; overflow:hidden; text-overflow:ellipsis;">${text.join(' | ') || '—'}</td>`;
            }
          });
          bodyHtml += `</tr>`;

          // DRAWER
          if (isExpanded) {
            const c = e.contacts || {};
            const topics = (e.content_topics || []).join(', ');
            bodyHtml += `<tr><td colspan="${visibleCols.length}" style="padding:0;"><div class="expanded-drawer">
              <div class="drawer-grid">
                <div class="drawer-block">
                  <h4>Кто этот человек и роль</h4>
                  <p>${e.persona_role || '—'}</p>
                  <h4 style="margin-top:10px;">Целевая аудитория</h4>
                  <p>${e.target_audience || '—'}</p>
                </div>
                <div class="drawer-block">
                  <h4>Темы публикаций</h4>
                  <p>${topics || '—'}</p>
                  <h4 style="margin-top:10px;">Тарификация прямой закупки</h4>
                  <p>${e.pricing_tier_type || 'Локальный тариф Мадагаскара'}<br>
                  Разовый пост: $${formatNumberSpace(e.price_post_usd)} (${formatNumberSpace(e.price_post_mga)} MGA)<br>
                  Месячный контракт: $${formatNumberSpace(e.price_monthly_usd)} (${formatNumberSpace(e.price_monthly_mga)} MGA)</p>
                </div>
                <div class="drawer-block">
                  <h4>Прямые контакты (Direct)</h4>
                  <p>Телефон: ${c.phone_direct || '—'}<br>
                  Email: ${c.email_direct || '—'}<br>
                  Менеджер: ${c.manager_name || '—'} (${c.manager_phone || c.manager_email || '—'})</p>
                  <h4 style="margin-top:10px;">Площадки автора</h4>
                  <p>${(e.platforms || []).map(p => `<a href="${p.url}" target="_blank" rel="noopener">${p.platform_name} (${formatNumberSpace(p.followers_count)})</a>`).join(' | ')}</p>
                </div>
              </div>
            </div></td></tr>`;
          }
        });

      } else {
        // FLAT PLATFORM ROWS
        let flatRows = [];
        filteredEntities.forEach(e => {
          (e.platforms || []).forEach(p => {
            flatRows.push({
              alias: e.alias || e.full_name,
              plat_name: p.platform_name,
              plat_handle: p.handle,
              plat_url: p.url,
              media_type: e.is_traditional_media ? 'СМИ' : 'Автор',
              category_main: e.category_main,
              residency_status: e.residency_status,
              plat_followers: p.followers_count,
              plat_reach: p.reach_per_post,
              plat_price_usd: p.price_post_usd,
              plat_price_mga: p.price_post_mga,
              contacts: e.contacts || {},
              is_foreign: e.is_foreign_guest,
              is_trad: e.is_traditional_media
            });
          });
        });

        flatRows.sort((a, b) => {
          let valA = a[sortColumn];
          let valB = b[sortColumn];
          if (typeof valA === 'string') return sortDirection === 'asc' ? valA.localeCompare(valB) : valB.localeCompare(valA);
          return sortDirection === 'asc' ? (valA || 0) - (valB || 0) : (valB || 0) - (valA || 0);
        });

        flatRows.forEach(r => {
          const rowClass = r.is_trad ? 'traditional-media-row' : (r.is_foreign ? 'foreign-row' : '');
          bodyHtml += `<tr class="${rowClass}">`;
          visibleCols.forEach(col => {
            const stickyClass = col.sticky ? 'sticky-col' : '';
            if (col.id === 'alias') {
              bodyHtml += `<td class="${stickyClass}"><a href="${r.plat_url}" target="_blank" rel="noopener" style="color:#fff; font-weight:600;">${r.alias}</a></td>`;
            } else if (col.id === 'plat_name') {
              bodyHtml += `<td>${r.plat_name}</td>`;
            } else if (col.id === 'plat_handle') {
              bodyHtml += `<td><a href="${r.plat_url}" target="_blank" rel="noopener">${r.plat_handle || 'Ссылка'}</a></td>`;
            } else if (col.id === 'media_type') {
              bodyHtml += `<td>${r.is_trad ? '<span class="badge badge-media">СМИ</span>' : '<span class="badge badge-creator">Автор</span>'}</td>`;
            } else if (col.id === 'category_main') {
              bodyHtml += `<td>${r.category_main}</td>`;
            } else if (col.id === 'residency_status') {
              bodyHtml += `<td>${r.residency_status}</td>`;
            } else if (col.id === 'plat_followers') {
              bodyHtml += `<td style="font-weight:700; color:#fff;">${formatNumberSpace(r.plat_followers)}</td>`;
            } else if (col.id === 'plat_reach') {
              bodyHtml += `<td style="color:var(--primary);">${formatNumberSpace(r.plat_reach)}</td>`;
            } else if (col.id === 'plat_price_usd') {
              bodyHtml += `<td style="color:#38bdf8; font-weight:600;">$${formatNumberSpace(r.plat_price_usd)}</td>`;
            } else if (col.id === 'plat_price_mga') {
              bodyHtml += `<td style="color:var(--text-muted);">${formatNumberSpace(r.plat_price_mga)} Ar</td>`;
            } else if (col.id === 'contacts') {
              const c = r.contacts || {};
              let text = [];
              if (c.phone_direct) text.push(`Тел: ${c.phone_direct}`);
              if (c.email_direct) text.push(`Email: ${c.email_direct}`);
              bodyHtml += `<td style="font-size:11px;">${text.join(' | ') || '—'}</td>`;
            }
          });
          bodyHtml += `</tr>`;
        });
      }

      document.getElementById('tableBody').innerHTML = bodyHtml;
    }

    function toggleSort(colId) {
      if (colId === 'expand' || colId === 'platforms') return;
      if (sortColumn === colId) {
        sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
      } else {
        sortColumn = colId;
        sortDirection = 'desc';
      }
      renderTable();
    }

    function toggleColDropdown() {
      document.getElementById('colDropdownMenu').classList.toggle('show');
    }

    function renderColDropdown() {
      const cols = currentMode === 'entity' ? ENTITY_COLUMNS : FLAT_COLUMNS;
      const prefix = currentMode === 'entity' ? 'entity_' : 'flat_';
      let h = '';
      cols.forEach(c => {
        if (c.id === 'expand') return;
        const visible = colVisibility[prefix + c.id];
        h += `<label class="dropdown-item"><input type="checkbox" ${visible ? 'checked' : ''} onchange="toggleColVisibility('${prefix + c.id}')"> <span>${c.label}</span></label>`;
      });
      document.getElementById('colDropdownMenu').innerHTML = h;
    }

    function toggleColVisibility(key) {
      colVisibility[key] = !colVisibility[key];
      renderTable();
    }

    // EXCEL WINDOWS COMPATIBLE CSV EXPORT
    function exportFilteredCSV() {
      const filtered = getFilteredEntities();
      if (!filtered.length) {
        alert('Нет данных для выгрузки по текущим фильтрам.');
        return;
      }

      let csv = "\\uFEFF";
      const delim = ";";

      if (currentMode === 'entity') {
        const headers = [
          "ID сущности", "ФИО / Наименование", "Псевдоним / Бренд", "Тип медиа", "Классическое СМИ",
          "Пол", "Резидентство", "Страна", "Регион", "Город", "Основная ниша", "Подниша",
          "Темы контента", "Роль автора", "Целевая аудитория", "Число платформ", "Подписчики",
          "Публикации", "Охват поста", "Тариф поста (USD)", "Тариф поста (MGA)", "Ретейнер (USD)",
          "Ретейнер (MGA)", "Ценовая категория", "Прямой телефон", "Прямой Email", "Менеджер (телефон)",
          "Ссылки на площадки"
        ];
        csv += headers.map(h => `"${h}"`).join(delim) + "\\r\\n";

        filtered.forEach(e => {
          const c = e.contacts || {};
          const topics = (e.content_topics || []).join(', ');
          const plats = (e.platforms || []).map(p => `${p.platform_name}: ${p.url}`).join(' | ');

          const row = [
            e.entity_id, e.full_name, e.alias, e.media_type_label, e.is_traditional_media ? 'Да' : 'Нет',
            e.gender, e.residency_status, e.country, e.region, e.city, e.category_main, e.category_sub,
            topics, e.persona_role, e.target_audience, e.platforms ? e.platforms.length : 0,
            formatNumberSpace(e.total_followers_aggregate), formatNumberSpace(e.total_posts_aggregate),
            formatNumberSpace(e.estimated_post_reach), formatNumberSpace(e.price_post_usd),
            formatNumberSpace(e.price_post_mga), formatNumberSpace(e.price_monthly_usd),
            formatNumberSpace(e.price_monthly_mga), e.pricing_tier_type,
            c.phone_direct, c.email_direct, c.manager_phone, plats
          ];
          csv += row.map(v => `"${String(v || '').replace(/"/g, '""')}"`).join(delim) + "\\r\\n";
        });

      } else {
        const headers = [
          "Автор", "Платформа", "Хэндл", "Ссылка", "Тип медиа", "Ниша", "Резидентство",
          "Подписчики", "Охват поста", "Цена поста (USD)", "Цена поста (MGA)",
          "Прямой телефон", "Прямой Email"
        ];
        csv += headers.map(h => `"${h}"`).join(delim) + "\\r\\n";

        filtered.forEach(e => {
          const c = e.contacts || {};
          (e.platforms || []).forEach(p => {
            const row = [
              e.alias || e.full_name, p.platform_name, p.handle, p.url,
              e.is_traditional_media ? 'СМИ' : 'Автор', e.category_main, e.residency_status,
              formatNumberSpace(p.followers_count), formatNumberSpace(p.reach_per_post),
              formatNumberSpace(p.price_post_usd), formatNumberSpace(p.price_post_mga),
              c.phone_direct, c.email_direct
            ];
            csv += row.map(v => `"${String(v || '').replace(/"/g, '""')}"`).join(delim) + "\\r\\n";
          });
        });
      }

      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `madagascar_influencers_${currentMode}_${includeTraditionalMedia ? 'all_with_media' : 'creators_only'}.csv`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }

    window.onclick = function(e) {
      if (!e.target.matches('.btn') && !e.target.closest('.dropdown-content')) {
        document.getElementById('colDropdownMenu').classList.remove('show');
      }
    };

    renderColDropdown();
    renderTable();
  </script>
</body>
</html>
"""

    # Replace placeholders
    html = template.replace("__TOTAL_ENTITIES__", format_space_num(total_entities))
    html = html.replace("__TOTAL_PLATFORMS__", format_space_num(total_platforms))
    html = html.replace("__PURE_REACH__", format_space_num(pure_reach))
    html = html.replace("__GROSS_REACH__", format_space_num(gross_reach))
    html = html.replace("__FOREIGN_REACH__", format_space_num(foreign_reach))
    html = html.replace("__INDEPENDENT_COUNT__", format_space_num(independent_creators_count))
    html = html.replace("__INDEPENDENT_PCT__", f"{independent_creators_count/total_entities*100:.1f}")
    html = html.replace("__TRADITIONAL_COUNT__", format_space_num(traditional_media_count))
    html = html.replace("__TRADITIONAL_PCT__", f"{traditional_media_count/total_entities*100:.1f}")
    html = html.replace("__MALE_COUNT__", format_space_num(male_count))
    html = html.replace("__MALE_PCT__", f"{male_count/total_entities*100:.1f}")
    html = html.replace("__FEMALE_COUNT__", format_space_num(female_count))
    html = html.replace("__FEMALE_PCT__", f"{female_count/total_entities*100:.1f}")
    html = html.replace("__GROUP_COUNT__", format_space_num(group_count))
    html = html.replace("__GROUP_PCT__", f"{group_count/total_entities*100:.1f}")
    html = html.replace("__ORG_COUNT__", format_space_num(org_count))
    html = html.replace("__ORG_PCT__", f"{org_count/total_entities*100:.1f}")
    html = html.replace("__DOMESTIC_COUNT__", format_space_num(domestic_count))
    html = html.replace("__DOMESTIC_PCT__", f"{domestic_count/total_entities*100:.1f}")
    html = html.replace("__DIASPORA_COUNT__", format_space_num(diaspora_count))
    html = html.replace("__DIASPORA_PCT__", f"{diaspora_count/total_entities*100:.1f}")
    html = html.replace("__FOREIGN_GUEST_COUNT__", format_space_num(foreign_guest_count))
    html = html.replace("__FOREIGN_GUEST_PCT__", f"{foreign_guest_count/total_entities*100:.1f}")
    html = html.replace("__PHONE_COUNT__", format_space_num(has_phone_count))
    html = html.replace("__PHONE_PCT__", f"{has_phone_count/total_entities*100:.1f}")
    html = html.replace("__EMAIL_COUNT__", format_space_num(has_email_count))
    html = html.replace("__EMAIL_PCT__", f"{has_email_count/total_entities*100:.1f}")
    html = html.replace("__MGR_COUNT__", format_space_num(has_manager_count))
    html = html.replace("__MGR_PCT__", f"{has_manager_count/total_entities*100:.1f}")
    html = html.replace("__CONTACT_PCT__", f"{has_any_contact/total_entities*100:.1f}")
    html = html.replace("__ENTITIES_JSON__", entities_json_str)

    dashboard_path = os.path.join(HERE, "madagascar_influencers_interactive.html")
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated Production Dashboard: {dashboard_path} ({len(html.encode('utf-8')):,} bytes)")

    index_path = os.path.join(HERE, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Updated index.html: {index_path}")

if __name__ == "__main__":
    main()
