/*
6. Listar as 5 categorias
com a maior média de avaliações úteis positivas por produto.
 */
-- WITH avg_per_product AS (
--     SELECT p.pasin,
--            AVG(r.helpful) AS avg_helpful
--     FROM products p
--     JOIN reviews r ON p.pasin = r.pasin
--     GROUP BY p.pasin
-- ),
-- avg_per_category AS (
--     SELECT c.cid,
--            c.descr,
--            AVG(ap.avg_helpful) AS avg_helpful_per_product
--     FROM avg_per_product ap
--     JOIN products_categories pc ON ap.pasin = pc.pasin
--     JOIN categories c ON pc.cid = c.cid
--     GROUP BY c.cid, c.descr
-- )
-- SELECT cid, descr, avg_helpful_per_product
-- FROM avg_per_category
-- ORDER BY avg_helpful_per_product DESC
-- LIMIT 5;
-- ----------------------------------------------------------------------------
-- SELECT cid, descr
-- FROM categories
-- NATURAL JOIN products_categories
-- NATURAL JOIN reviews
-- WHERE votes > 0 AND rating > 3
-- GROUP BY cid, descr
-- ORDER BY AVG(CAST(helpful AS FLOAT) / votes) DESC, AVG(rating) DESC
-- LIMIT 5;
