import re

def extract_column_names(sql_query):
    # Regular expression to capture SELECT fields
    select_pattern = re.compile(r"SELECT\s+(.*?)\s+FROM", re.DOTALL | re.IGNORECASE)
    
    # Extract the SELECT clause
    select_match = select_pattern.search(sql_query)
    if not select_match:
        return []

    select_clause = select_match.group(1)

    # Split columns by commas, ignoring nested functions and cases
    columns = re.split(r",\s*(?![^()]*\))", select_clause)

    # Extract column aliases or names
    column_names = []
    for col in columns:
        col = col.strip()
        # Match "AS alias" or just column names
        alias_match = re.search(r"(?:AS\s+)?(\w+)$", col, re.IGNORECASE)
        if alias_match:
            column_names.append(alias_match.group(1))

    return column_names

# Sample SQL queries
query_1 = """
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
"""

query_2 = """
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
"""

# Extract and print column names
columns_query_1 = extract_column_names(query_1)
columns_query_2 = extract_column_names(query_2)

print("Columns for Query 1:", columns_query_1)
print("Columns for Query 2:", columns_query_2)
