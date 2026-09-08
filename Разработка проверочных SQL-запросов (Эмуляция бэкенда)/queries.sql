-- Проверочные SQL-запросы (эмуляция бэкенда)
-- Таблицы: partners, products, shipments


-- 1. Список партнёров + сколько у каждого доставок
-- LEFT JOIN нужен, чтобы партнёры без отгрузок тоже попали в выборку (COUNT = 0)
SELECT
    p.company_name,
    COUNT(s.sale_id) AS deliveries_count
FROM partners AS p
LEFT JOIN shipments AS s ON s.partner_id = p.partner_id
GROUP BY p.partner_id, p.company_name
ORDER BY p.company_name;


-- 2. Транзакция: новый партнёр + его первая тестовая доставка
-- Если вторая вставка упадёт, откатятся оба изменения
BEGIN;

INSERT INTO partners (partner_id, company_name, inn, contact_email, phone, rating)
VALUES (10, 'ООО "СеверТорг"', '7709988776', 'north@severtorg.ru', '+7 (495) 100-20-30', 4.5);

INSERT INTO shipments (sale_id, partner_id, product_id, sale_date, quantity, total_amount)
VALUES (201, 10, 1, '2026-04-01', 25, 12500.00);

COMMIT;


-- 3. История отгрузок конкретного партнёра за период
-- Пример: partner_id = 1, март 2026
SELECT
    s.sale_date,
    pr.product_name,
    s.quantity,
    s.total_amount
FROM shipments AS s
JOIN products AS pr ON pr.product_id = s.product_id
WHERE s.partner_id = 1
  AND s.sale_date BETWEEN '2026-03-01' AND '2026-03-31'
ORDER BY s.sale_date;
