# Проектирование базы данных (3NF) и ER-диаграмма

## Назначение

Схема нужна для:
- просмотра партнёров
- редактирования данных партнёров
- просмотра истории отгрузок

## Сущности (3NF)

| Таблица | Назначение |
|---|---|
| `partners` | данные о партнёрах |
| `products` | справочник товаров |
| `shipments` | история отгрузок |

Связи:
- один партнёр → много отгрузок
- один товар → много отгрузок

## Почему это 3NF

1. **1NF** — все значения атомарные, нет повторяющихся групп  
2. **2NF** — нет частичной зависимости от составного ключа (ключи простые)  
3. **3NF** — нет транзитивных зависимостей: название товара и данные партнёра не хранятся внутри `shipments`, а вынесены в свои таблицы

## Ограничения целостности

**partners**
- PK: `partner_id`
- NOT NULL: `company_name`, `inn`, `contact_email`
- UNIQUE: `inn`, `contact_email`

**products**
- PK: `product_id`
- NOT NULL / UNIQUE: `product_name`

**shipments**
- PK: `sale_id`
- FK: `partner_id` → `partners.partner_id`
- FK: `product_id` → `products.product_id`
- NOT NULL: `partner_id`, `product_id`, `sale_date`, `quantity`, `total_amount`

## Именование

- `snake_case`
- таблицы во **множественном** числе: `partners`, `products`, `shipments`

## Файлы

- `schema.sql` — DDL-скрипт
- `er_diagram.pdf` — ER-диаграмма
