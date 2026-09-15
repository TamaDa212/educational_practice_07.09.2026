INSERT INTO partners (partner_id, company_name, inn, contact_email, phone, rating) VALUES
(1, 'ООО "Логистик-Экспресс"', '7701234567', 'info@logex.ru', '+7 (999) 111-22-33', 4.8);

INSERT INTO partners (partner_id, company_name, inn, contact_email, phone, rating) VALUES
(2, 'ИП Петров А.В.', '5001098765', 'petrov_delivery@mail.ru', NULL, 4.2);

INSERT INTO partners (partner_id, company_name, inn, contact_email, phone, rating) VALUES
(3, 'ТК "Быстрый Путь"', '7812345678', 'speedway@yandex.ru', '+78125554433', NULL);

INSERT INTO partners (partner_id, company_name, inn, contact_email, phone, rating) VALUES
(4, 'ООО "Новый Контур"', '7705554433', 'hello@newcontour.ru', '+7 (495) 222-33-44', 4.0);

INSERT INTO partners (partner_id, company_name, inn, contact_email, phone, rating) VALUES
(5, 'ТД "ОптМаркет"', '7809988776', 'opt@optmarket.ru', '+7 (812) 300-40-50', 4.6);

INSERT INTO products (product_id, product_name) VALUES
(1, 'Кондиционер для белья'),
(2, 'Мыло жидкое "Стандарт"'),
(3, 'Стиральный порошок "Альфа"');

INSERT INTO sales_history (sale_id, partner_id, product_id, sale_date, quantity, total_amount) VALUES
(101, 1, 3, '2026-03-01', 50, 25000.00),
(102, 2, 2, '2026-03-15', 200, 18000.50),
(103, 1, 1, '2026-03-20', 30, 10500.00),
(105, 3, 2, '2026-03-25', 150, 13500.00),
(106, 5, 3, '2026-04-01', 10000, 500000.00);
