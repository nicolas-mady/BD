/*
6. Listar as 5 categorias
com a maior média de avaliações úteis positivas por produto.
 */

SELECT cid, descr, AVG(helpful) AS avg_helpful, COUNT(*) as n_products
FROM categories
NATURAL JOIN products_categories
NATURAL JOIN reviews
WHERE helpful > 0 AND rating > 3
GROUP BY cid, descr
ORDER BY avg_helpful DESC
;