/*
6. Listar as 5 categorias
com a maior média de avaliações úteis positivas por produto.
 */

WITH A AS (
    SELECT cid, descr, COUNT(*) as n_products
    FROM categories
    NATURAL JOIN products_categories
    GROUP BY cid
),
B AS (
    SELECT cid, descr, COUNT(*) as n_pos_helpful
    FROM categories
    NATURAL JOIN products_categories
    NATURAL JOIN reviews
    WHERE helpful > 0 AND rating > 3
    GROUP BY cid
)
SELECT
    cid,
    descr,
    ROUND(CAST(n_pos_helpful AS NUMERIC) / n_products, 2) AS avg_pos_helpful,
    n_pos_helpful,
    n_products
FROM B
NATURAL JOIN A
ORDER BY avg_pos_helpful DESC
LIMIT 5;
