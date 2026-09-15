-- =============================================
-- Подготовка данных и импорт (ETL)
-- =============================================
-- 1) Extract  — читаем import_partners.csv и import_sales.txt
-- 2) Transform — чистим данные (см. data/clean/)
-- 3) Load     — загружаем в БД этим скриптом
--
-- Правки при очистке:
-- * trim пробелов у company_name
-- * дата 15.03.2026 -> 2026-03-15
-- * пустые phone/rating -> NULL
-- * sale_id=104 пропускаем (partner_id=4 не существует)

INSERT INTO partners (partner_id, company_name, inn, contact_email, phone, rating) VALUES
(1, 'ООО "Логистик-Экспресс"', '7701234567', 'info@logex.ru', '+7 (999) 111-22-33', 4.8);

INSERT INTO partners (partner_id, company_name, inn, contact_email, phone, rating) VALUES
(2, 'ИП Петров А.В.', '5001098765', 'petrov_delivery@mail.ru', NULL, 4.2);

INSERT INTO partners (partner_id, company_name, inn, contact_email, phone, rating) VALUES
(3, 'ТК "Быстрый Путь"', '7812345678', 'speedway@yandex.ru', '+78125554433', NULL);


INSERT INTO products (product_id, product_name) VALUES
(1, 'Кондиционер для белья'),
(2, 'Мыло жидкое "Стандарт"'),
(3, 'Стиральный порошок "Альфа"');


-- отгрузки; строка 104 намеренно не включена
INSERT INTO shipments (sale_id, partner_id, product_id, sale_date, quantity, total_amount) VALUES
(101, 1, 3, '2026-03-01', 50, 25000.00),
(102, 2, 2, '2026-03-15', 200, 18000.50),
(103, 1, 1, '2026-03-20', 30, 10500.00),
(105, 3, 2, '2026-03-25', 150, 13500.00);
