-- Drop tables if they exist to allow for clean pipeline reruns (Order matters due to Foreign Keys)
DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_payments;
DROP TABLE IF EXISTS dim_products;
DROP TABLE IF EXISTS dim_sellers;
DROP TABLE IF EXISTS dim_customers;
DROP TABLE IF EXISTS dim_dates;

-- 1. Create dim_dates
CREATE TABLE dim_dates (
    date_key DATE PRIMARY KEY,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    day_of_week VARCHAR(15) NOT NULL,
    quarter INT NOT NULL
);

-- 2. Create dim_customers
CREATE TABLE dim_customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50),
    zip_code INT,
    customer_city VARCHAR(100),
    customer_state VARCHAR(5)
);

-- 3. Create dim_sellers
CREATE TABLE dim_sellers (
    seller_id VARCHAR(50) PRIMARY KEY,
    zip_code INT,
    seller_city VARCHAR(100),
    seller_state VARCHAR(5)
);

-- 4. Create dim_products
CREATE TABLE dim_products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name_lenght FLOAT, -- kept original spellings from dataset
    product_description_lenght FLOAT,
    product_photos_qty FLOAT,
    product_weight_g FLOAT,
    product_length_cm FLOAT,
    product_height_cm FLOAT,
    product_width_cm FLOAT,
    product_category VARCHAR(100)
);

-- 5. Create dim_payments
CREATE TABLE dim_payments (
    order_id VARCHAR(50),
    payment_sequential INT,
    payment_type VARCHAR(50),
    payment_installments INT,
    payment_value FLOAT,
    PRIMARY KEY (order_id, payment_sequential)
);

-- 6. Create fact_sales
CREATE TABLE fact_sales (
    order_id VARCHAR(50),
    order_item_id INT,
    customer_id VARCHAR(50) REFERENCES dim_customers(customer_id),
    product_id VARCHAR(50) REFERENCES dim_products(product_id),
    seller_id VARCHAR(50) REFERENCES dim_sellers(seller_id),
    date_key DATE REFERENCES dim_dates(date_key),
    price FLOAT NOT NULL,
    freight_value FLOAT NOT NULL,
    order_status VARCHAR(30),
    order_delivered_customer_date TIMESTAMP,
    PRIMARY KEY (order_id, order_item_id, customer_id, product_id, seller_id)
);