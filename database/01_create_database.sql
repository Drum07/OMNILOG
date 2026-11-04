-- OMNILOG HUB | MySQL 8.0
-- Execute este script no MySQL Workbench com um usuário autorizado.

CREATE DATABASE IF NOT EXISTS omnilog_hub
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_0900_ai_ci;

USE omnilog_hub;

CREATE TABLE IF NOT EXISTS roles (
    role_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(60) NOT NULL UNIQUE,
    description VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(190) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_active (is_active)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS user_roles (
    user_id BIGINT UNSIGNED NOT NULL,
    role_id BIGINT UNSIGNED NOT NULL,
    assigned_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id),
    CONSTRAINT fk_user_roles_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_user_roles_role
        FOREIGN KEY (role_id) REFERENCES roles(role_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS customers (
    customer_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(190) NOT NULL UNIQUE,
    phone VARCHAR(30),
    document_hash VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_customers_name (full_name)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS customer_addresses (
    address_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT UNSIGNED NOT NULL,
    address_type ENUM('BILLING','SHIPPING','BOTH') NOT NULL DEFAULT 'BOTH',
    street VARCHAR(180) NOT NULL,
    number VARCHAR(20),
    complement VARCHAR(100),
    district VARCHAR(100),
    city VARCHAR(100) NOT NULL,
    state_code CHAR(2) NOT NULL,
    postal_code VARCHAR(12) NOT NULL,
    country_code CHAR(2) NOT NULL DEFAULT 'BR',
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT fk_addresses_customer
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    INDEX idx_addresses_customer (customer_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS categories (
    category_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    parent_category_id BIGINT UNSIGNED NULL,
    category_name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    CONSTRAINT uq_category_name_parent UNIQUE (parent_category_id, category_name),
    CONSTRAINT fk_categories_parent
        FOREIGN KEY (parent_category_id) REFERENCES categories(category_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS products (
    product_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    category_id BIGINT UNSIGNED NOT NULL,
    sku VARCHAR(60) NOT NULL UNIQUE,
    product_name VARCHAR(180) NOT NULL,
    description TEXT,
    unit_price DECIMAL(13,2) NOT NULL,
    unit_weight_kg DECIMAL(10,3) NOT NULL DEFAULT 0,
    is_hazardous BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_products_price CHECK (unit_price >= 0),
    CONSTRAINT chk_products_weight CHECK (unit_weight_kg >= 0),
    CONSTRAINT fk_products_category
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FULLTEXT INDEX ft_products_search (product_name, description),
    INDEX idx_products_category_active (category_id, is_active)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS warehouses (
    warehouse_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    warehouse_code VARCHAR(30) NOT NULL UNIQUE,
    warehouse_name VARCHAR(120) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state_code CHAR(2) NOT NULL,
    country_code CHAR(2) NOT NULL DEFAULT 'BR',
    is_active BOOLEAN NOT NULL DEFAULT TRUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS warehouse_locations (
    location_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    warehouse_id BIGINT UNSIGNED NOT NULL,
    aisle SMALLINT UNSIGNED NOT NULL,
    shelf SMALLINT UNSIGNED NOT NULL,
    level_no SMALLINT UNSIGNED NOT NULL,
    max_weight_kg DECIMAL(12,3) NOT NULL,
    hazardous_allowed BOOLEAN NOT NULL DEFAULT FALSE,
    location_status ENUM('AVAILABLE','OCCUPIED','BLOCKED') NOT NULL DEFAULT 'AVAILABLE',
    CONSTRAINT uq_warehouse_position UNIQUE (warehouse_id, aisle, shelf, level_no),
    CONSTRAINT chk_location_weight CHECK (max_weight_kg > 0),
    CONSTRAINT fk_locations_warehouse
        FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS inventory (
    inventory_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    product_id BIGINT UNSIGNED NOT NULL,
    warehouse_id BIGINT UNSIGNED NOT NULL,
    location_id BIGINT UNSIGNED NULL,
    quantity DECIMAL(14,3) NOT NULL DEFAULT 0,
    reserved_quantity DECIMAL(14,3) NOT NULL DEFAULT 0,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT uq_inventory_product_warehouse UNIQUE (product_id, warehouse_id),
    CONSTRAINT chk_inventory_quantity CHECK (quantity >= 0),
    CONSTRAINT chk_inventory_reserved CHECK (reserved_quantity >= 0 AND reserved_quantity <= quantity),
    CONSTRAINT fk_inventory_product
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_inventory_warehouse
        FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_inventory_location
        FOREIGN KEY (location_id) REFERENCES warehouse_locations(location_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS orders (
    order_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT UNSIGNED NOT NULL,
    order_number VARCHAR(40) NOT NULL UNIQUE,
    order_status ENUM('DRAFT','PLACED','PAID','PROCESSING','SHIPPED','DELIVERED','CANCELLED') NOT NULL DEFAULT 'DRAFT',
    subtotal DECIMAL(13,2) NOT NULL DEFAULT 0,
    shipping_amount DECIMAL(13,2) NOT NULL DEFAULT 0,
    total_amount DECIMAL(13,2) NOT NULL DEFAULT 0,
    placed_at DATETIME NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_orders_amounts CHECK (subtotal >= 0 AND shipping_amount >= 0 AND total_amount >= 0),
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    INDEX idx_orders_customer_date (customer_id, created_at),
    INDEX idx_orders_status_date (order_status, created_at)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT UNSIGNED NOT NULL,
    product_id BIGINT UNSIGNED NOT NULL,
    quantity DECIMAL(12,3) NOT NULL,
    unit_price DECIMAL(13,2) NOT NULL,
    line_total DECIMAL(13,2) NOT NULL,
    CONSTRAINT chk_order_item_values CHECK (quantity > 0 AND unit_price >= 0 AND line_total >= 0),
    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    INDEX idx_order_items_product (product_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS payments (
    payment_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT UNSIGNED NOT NULL,
    payment_reference VARCHAR(100) UNIQUE,
    payment_method ENUM('PIX','CREDIT_CARD','DEBIT_CARD','BOLETO','CASH','OTHER') NOT NULL,
    payment_status ENUM('PENDING','AUTHORIZED','PAID','REFUNDED','FAILED') NOT NULL DEFAULT 'PENDING',
    amount DECIMAL(13,2) NOT NULL,
    paid_at DATETIME NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_payment_amount CHECK (amount > 0),
    CONSTRAINT fk_payments_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    INDEX idx_payments_status_date (payment_status, created_at)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS drivers (
    driver_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    license_number_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(30),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    plate_hash VARCHAR(255) NOT NULL UNIQUE,
    vehicle_type VARCHAR(60) NOT NULL,
    capacity_kg DECIMAL(12,3) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT chk_vehicle_capacity CHECK (capacity_kg > 0)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS routes (
    route_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    route_code VARCHAR(40) NOT NULL UNIQUE,
    origin_warehouse_id BIGINT UNSIGNED NOT NULL,
    destination_description VARCHAR(180) NOT NULL,
    planned_distance_km DECIMAL(12,3) NOT NULL DEFAULT 0,
    estimated_cost DECIMAL(13,2) NOT NULL DEFAULT 0,
    route_status ENUM('PLANNED','IN_PROGRESS','COMPLETED','CANCELLED') NOT NULL DEFAULT 'PLANNED',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_route_distance CHECK (planned_distance_km >= 0),
    CONSTRAINT chk_route_cost CHECK (estimated_cost >= 0),
    CONSTRAINT fk_routes_warehouse
        FOREIGN KEY (origin_warehouse_id) REFERENCES warehouses(warehouse_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS deliveries (
    delivery_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT UNSIGNED NOT NULL,
    route_id BIGINT UNSIGNED NULL,
    vehicle_id BIGINT UNSIGNED NULL,
    driver_id BIGINT UNSIGNED NULL,
    tracking_code VARCHAR(60) NOT NULL UNIQUE,
    delivery_status ENUM('PENDING','PICKING','IN_TRANSIT','OUT_FOR_DELIVERY','DELIVERED','EXCEPTION') NOT NULL DEFAULT 'PENDING',
    shipped_at DATETIME NULL,
    delivered_at DATETIME NULL,
    CONSTRAINT uq_delivery_order UNIQUE (order_id),
    CONSTRAINT fk_deliveries_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_deliveries_route
        FOREIGN KEY (route_id) REFERENCES routes(route_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_deliveries_vehicle
        FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_deliveries_driver
        FOREIGN KEY (driver_id) REFERENCES drivers(driver_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    INDEX idx_deliveries_status (delivery_status)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS audit_logs (
    audit_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NULL,
    entity_name VARCHAR(100) NOT NULL,
    entity_id VARCHAR(80) NOT NULL,
    action_name ENUM('INSERT','UPDATE','DELETE','LOGIN','LOGOUT','OTHER') NOT NULL,
    details JSON NULL,
    ip_address VARBINARY(16) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_audit_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    INDEX idx_audit_entity (entity_name, entity_id),
    INDEX idx_audit_created (created_at)
) ENGINE=InnoDB;

INSERT IGNORE INTO roles (role_name, description) VALUES
('ADMIN', 'Administrador do sistema'),
('WAREHOUSE_OPERATOR', 'Operador de armazém'),
('LOGISTICS_MANAGER', 'Gerente logístico'),
('CUSTOMER', 'Cliente do portal');
