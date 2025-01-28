-- Query 1: Product Sales Summary
CREATE TABLE product_sales_summary AS
SELECT 
    p.product_id,
    p.name AS product_name,
    SUM(oi.quantity * p.price) AS total_sales,
    SUM(oi.quantity) AS total_units_sold,
    SUM(oi.quantity * p.price) / NULLIF(SUM(oi.quantity), 0) AS avg_revenue_per_unit,
    SUM(oi.quantity * (p.price - p.manufacturing_cost)) AS total_profit,
    CASE 
        WHEN SUM(oi.quantity * p.price) > 0 
        THEN SUM(oi.quantity * (p.price - p.manufacturing_cost)) / SUM(oi.quantity * p.price)
        ELSE 0
    END AS profit_margin
FROM 
    products p
JOIN 
    order_items oi ON p.product_id = oi.product_id
GROUP BY 
    p.product_id, p.name;

-- Query 2: Customer Orders Summary
CREATE TABLE customer_orders_summary AS
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_spent,
    AVG(o.total_amount) AS avg_order_value
FROM 
    customers c
JOIN 
    orders o ON c.customer_id = o.customer_id
GROUP BY 
    c.customer_id, c.first_name, c.last_name;
