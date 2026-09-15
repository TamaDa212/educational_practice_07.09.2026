-- Написание DDL-скрипта (База данных в коде)
-- Таблицы: partners, products, shipments
--
-- DROP идёт от зависимых таблиц к справочникам.
-- CREATE — наоборот: сначала справочники, потом отгрузки.

PRAGMA foreign_keys = ON;


-- 1. Удаление таблиц (с учётом зависимостей)

DROP TABLE IF EXISTS shipments;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS partners;


-- 2. Создание таблиц


CREATE TABLE partners (
    partner_id    INTEGER      NOT NULL,
    company_name  VARCHAR(255) NOT NULL,
    inn           VARCHAR(12)  NOT NULL,
    contact_email VARCHAR(255) NOT NULL,
    phone         VARCHAR(50),
    rating        DECIMAL(3, 1),
    created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_partners PRIMARY KEY (partner_id),
    CONSTRAINT uq_partners_inn UNIQUE (inn),
    CONSTRAINT uq_partners_email UNIQUE (contact_email)
);


CREATE TABLE products (
    product_id   INTEGER      NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    created_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_products PRIMARY KEY (product_id),
    CONSTRAINT uq_products_name UNIQUE (product_name)
);


CREATE TABLE shipments (
    sale_id      INTEGER       NOT NULL,
    partner_id   INTEGER       NOT NULL,
    product_id   INTEGER       NOT NULL,
    sale_date    DATE          NOT NULL,
    quantity     INT           NOT NULL,
    total_amount DECIMAL(12, 2) NOT NULL,
    created_at   TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_shipments PRIMARY KEY (sale_id),
    CONSTRAINT fk_shipments_partner
        FOREIGN KEY (partner_id)
        REFERENCES partners (partner_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_shipments_product
        FOREIGN KEY (product_id)
        REFERENCES products (product_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
