PRAGMA foreign_keys = ON;

CREATE TABLE product_types (
    product_type_id INTEGER      NOT NULL,
    type_name       VARCHAR(255) NOT NULL,
    coefficient     DECIMAL(8, 3) NOT NULL,
    CONSTRAINT pk_product_types PRIMARY KEY (product_type_id)
);

CREATE TABLE material_types (
    material_type_id INTEGER      NOT NULL,
    type_name        VARCHAR(255) NOT NULL,
    defect_percent   DECIMAL(8, 3) NOT NULL,
    CONSTRAINT pk_material_types PRIMARY KEY (material_type_id)
);
