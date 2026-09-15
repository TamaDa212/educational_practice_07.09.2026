# Написание DDL-скрипта (База данных в коде)

Скрипт `ddl.sql` описывает схему БД в коде: удаление таблиц, создание и ограничения целостности.

## Порядок DROP

Сначала зависимая таблица, потом справочники — иначе мешают внешние ключи:

1. `shipments`
2. `products`
3. `partners`

## Порядок CREATE

1. `partners` — партнёры
2. `products` — товары
3. `shipments` — история отгрузок

## Типы данных

| Поле | Тип | Зачем |
|---|---|---|
| названия, ИНН, email, телефон | `VARCHAR` | текстовые атрибуты |
| идентификаторы, количество | `INTEGER` / `INT` | целые числа |
| дата отгрузки | `DATE` | день без времени |
| дата создания записи | `TIMESTAMP` | дата и время |
| рейтинг, сумма отгрузки | `DECIMAL` | цены и дробные значения |

## Ограничения

**PRIMARY KEY**
- `partners.partner_id`
- `products.product_id`
- `shipments.sale_id`

**FOREIGN KEY**
- `shipments.partner_id` → `partners.partner_id`  
  `ON DELETE RESTRICT` — партнёра с отгрузками удалить нельзя  
  `ON UPDATE CASCADE` — смена `partner_id` уйдёт в отгрузки
- `shipments.product_id` → `products.product_id`  
  `ON DELETE RESTRICT` — товар из отгрузок удалить нельзя  
  `ON UPDATE CASCADE` — смена `product_id` уйдёт в отгрузки

## Запуск

```bash
sqlite3 mydb.db < ddl.sql
```
