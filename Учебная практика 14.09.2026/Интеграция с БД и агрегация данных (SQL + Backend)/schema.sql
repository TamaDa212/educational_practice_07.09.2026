PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS sales_history;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS partners;

CREATE TABLE partners (
    partner_id    INTEGER      NOT NULL,
    company_name  VARCHAR(255) NOT NULL,
    inn           VARCHAR(12)  NOT NULL,
    contact_email VARCHAR(255) NOT NULL,
    phone         VARCHAR(50),
    rating        DECIMAL(3, 1),
    CONSTRAINT pk_partners PRIMARY KEY (partner_id)
);

CREATE TABLE products (
    product_id   INTEGER      NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    CONSTRAINT pk_products PRIMARY KEY (product_id)
);

CREATE TABLE sales_history (
    sale_id      INTEGER        NOT NULL,
    partner_id   INTEGER        NOT NULL,
    product_id   INTEGER        NOT NULL,
    sale_date    DATE           NOT NULL,
    quantity     INT            NOT NULL,
    total_amount DECIMAL(12, 2) NOT NULL,
    CONSTRAINT pk_sales_history PRIMARY KEY (sale_id),
    CONSTRAINT fk_sales_history_partner
        FOREIGN KEY (partner_id)
        REFERENCES partners (partner_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_sales_history_product
        FOREIGN KEY (product_id)
        REFERENCES products (product_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
