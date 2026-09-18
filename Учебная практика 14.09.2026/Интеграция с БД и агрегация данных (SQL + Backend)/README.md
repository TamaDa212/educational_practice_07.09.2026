# Интеграция с БД и агрегация данных (SQL + Backend)

Подключение SQLite к коду, суммарный объём продаж партнёра и расчёт скидки из подзадания 1.

## Как устроено

1. Native-драйвер `sqlite3` — тот же движок, что в практике 07.09.2026.
2. SQL с `LEFT JOIN` и `SUM(quantity)` по таблице `sales_history`.
3. Результат дополняется `discount_percent` через `calculate_partner_discount`.

`LEFT JOIN` нужен, чтобы партнёр без продаж всё равно вернулся: объём `0`, скидка `0%`.

Список всех партнёров: `list_partners_with_discount(connection)` — тот же расчёт по каждому `partner_id`. Если `SUM(quantity)` равен `NULL` или `0`, скидка `0%`.

## Выход функции

```python
{
    "partner_id": 1,
    "company_name": 'ООО "Логистик-Экспресс"',
    "inn": "7701234567",
    "contact_email": "info@logex.ru",
    "phone": "+7 (999) 111-22-33",
    "rating": 4.8,
    "total_quantity": 80,
    "discount_percent": 0,
}
```

## Запуск демо

```bash
cd "Учебная практика 14.09.2026/Интеграция с БД и агрегация данных (SQL + Backend)"
python3 demo.py
```

## Тесты

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```
