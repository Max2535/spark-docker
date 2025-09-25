CREATE DATABASE IF NOT EXISTS sales_db;
USE sales_db;

DROP TABLE IF EXISTS sales;

CREATE TABLE sales (
    id INT,
    product STRING,
    amount DOUBLE
)
USING csv
OPTIONS (
    path 'file:///data/sales.csv',
    header 'true',
    inferSchema 'true'
);

-- query ตัวอย่าง
SELECT product, SUM(amount) AS total_sales
FROM sales
GROUP BY product
ORDER BY total_sales DESC;


CREATE TABLE products (
    id INT,
    category STRING
)
USING csv
OPTIONS (
    path 'file:///data/products.csv',
    header 'true',
    inferSchema 'true'
);

SELECT s.product, p.category, SUM(s.amount) AS total_sales
FROM sales s
JOIN products p ON s.id = p.id
GROUP BY s.product, p.category;
