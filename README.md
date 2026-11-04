# Madagascar Influencers Intelligence System (Реестр лидеров мнений Мадагаскара)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fn0e1%2Fmadagascar-influencers)
[![GitHub Pages](https://img.shields.io/badge/Live_Dashboard-GitHub_Pages-success?style=flat&logo=github)](https://n0e1.github.io/madagascar-influencers/)

> **Live Production Dashboard**: [https://n0e1.github.io/madagascar-influencers/](https://n0e1.github.io/madagascar-influencers/)  
> **1-Click Deploy to Vercel**: [Deploy to Vercel](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fn0e1%2Fmadagascar-influencers)

---

## 1. Обзор проекта

Исчерпывающий, дедуплицированный и аналитически верифицированный реестр лидеров мнений, блоггеров, общественных деятелей, музыкантов, спортсменов, ученых и предпринимателей, связанных с Республикой Мадагаскар (с фильтрацией $\ge 1\,000$ подписчиков).

### Сводные метрики базы данных
- **Всего уникальных сущностей (Entity Count)**: `411`
- **Верифицированных платформенных аккаунтов**: `789`
- **Совокупный валовый охват аудитории (Gross Reach)**: `62,705,816`
- **Проиндексировано публикаций**: `217,395`
- **Верифицированных прямых контактов (Email / Phone)**: `294`
- **Охват каналов**: Facebook, YouTube, TikTok, Instagram, LinkedIn, X (Twitter), Подкасты, Независимые блоги

---

## 2. Структура репозитория

| Файл | Описание | Формат |
|---|---|:---:|
| **`index.html`** | Интерактивный веб-дашборд с мгновенным поиском, фасетными фильтрами по 14 нишам и переключателем режимов *Entity View* / *Flat Platform View* | HTML / JS / CSS (2.12 MB) |
| **`madagascar_influencers_database.json`** | Каноническая реляционная база данных со всеми вложенными платформами, метриками и контактами | JSON (411 сущностей) |
| **`madagascar_influencers_master_entities.csv`** | Сводная таблица сущностей (1 строка = 1 блоггер, 19 колонок) | CSV (UTF-8-BOM) |
| **`madagascar_influencers_flat_platforms.csv`** | Поплатформенная плоская таблица (1 строка = 1 платформенный аккаунт, 21 колонка) | CSV (UTF-8-BOM) |
| **`vercel.json`** | Конфигурационный файл для нулевой настройки деплоя на Vercel | JSON |

---

## 3. Деплой и развертывание

### Быстрый деплой на Vercel
Нажмите кнопку ниже для мгновенного развертывания проекта на платформе Vercel в собственном аккаунте:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fn0e1%2Fmadagascar-influencers)

### Локальный запуск
Для локального запуска интерактивного дашборда достаточно открыть `index.html` в любом браузере либо запустить встроенный веб-сервер:
```bash
python3 -m http.server 8000
# Открыть в браузере: http://localhost:8000
```
