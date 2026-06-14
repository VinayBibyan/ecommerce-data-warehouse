-- 1. MONTHLY REVENUE TRENDS
-- Purpose: Track gross sales revenue month-over-month to monitor business growth.
SELECT 
    d.year,
    d.month,
    ROUND(SUM(f.price)::numeric, 2) as total_revenue,
    COUNT(DISTINCT f.order_id) as total_orders
FROM fact_sales f
JOIN dim_dates d ON f.date_key = d.date_key
WHERE f.order_status = 'delivered'
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


-- 2. TOP 10 REVENUE-GENERATING PRODUCT CATEGORIES
-- Purpose: Identify high-value inventory segments driving the most revenue.
SELECT 
    p.product_category,
    COUNT(f.order_id) as total_items_sold,
    ROUND(SUM(f.price)::numeric, 2) as total_revenue
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
WHERE f.order_status = 'delivered'
GROUP BY p.product_category
ORDER BY total_revenue DESC
LIMIT 10;


-- 3. TOP STATES BY REVENUE
-- Purpose: Pinpoint primary geographical markets to optimize localized marketing and logistics.
SELECT 
    c.customer_state as state,
    COUNT(DISTINCT f.order_id) as total_orders,
    ROUND(SUM(f.price)::numeric, 2) as total_revenue
FROM fact_sales f
JOIN dim_customers c ON f.customer_id = c.customer_id
WHERE f.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY total_revenue DESC;


-- 4. REPEAT CUSTOMERS DETECTOR
-- Purpose: Measure customer loyalty and retention by tracking buyers who made multiple separate orders.
WITH customer_order_counts AS (
    SELECT 
        c.customer_unique_id,
        COUNT(DISTINCT f.order_id) as order_count,
        SUM(f.price) as total_spent
    FROM fact_sales f
    JOIN dim_customers c ON f.customer_id = c.customer_id
    GROUP BY c.customer_unique_id
)
SELECT 
    order_count as purchases_per_customer,
    COUNT(customer_unique_id) as customer_count,
    ROUND(SUM(total_spent)::numeric, 2) as total_revenue_contribution
FROM customer_order_counts
WHERE order_count > 1
GROUP BY order_count
ORDER BY purchases_per_customer DESC;


-- 5. TOP PRODUCTS RANKING BY CATEGORY (Window Function)
-- Purpose: Find the absolute best-selling individual product IDs inside every category.
WITH ranked_products AS (
    SELECT 
        p.product_category,
        f.product_id,
        COUNT(f.order_id) as total_sales_count,
        ROUND(SUM(f.price)::numeric, 2) as product_revenue,
        DENSE_RANK() OVER (PARTITION BY p.product_category ORDER BY COUNT(f.order_id) DESC) as sales_rank
    FROM fact_sales f
    JOIN dim_products p ON f.product_id = p.product_id
    WHERE f.order_status = 'delivered' AND p.product_category <> 'unknown'
    GROUP BY p.product_category, f.product_id
)
SELECT 
    product_category,
    product_id,
    total_sales_count,
    product_revenue,
    sales_rank
FROM ranked_products
WHERE sales_rank <= 3
ORDER BY product_category, sales_rank;