/* 1. Dado um produto, listar os 5 comentários mais úteis e com maior avaliação
e os 5 comentários mais úteis e com menor avaliação.
 */
-- SELECT pasin FROM products WHERE dl = 10 LIMIT 1;
-- SELECT * FROM reviews WHERE pasin = '0195110382';
-- ----------------------------------------------------------------------------
-- SELECT reviews.*
-- FROM reviews
-- NATURAL JOIN products
-- WHERE pasin = '0195110382'
-- ORDER BY rating DESC, helpful DESC
-- LIMIT 5;
-- SELECT reviews.*
-- FROM reviews
-- NATURAL JOIN products
-- WHERE pasin = '0195110382'
-- ORDER BY rating ASC, helpful DESC
-- LIMIT 5;
-- ############################################################################
/* 2. Dado um produto, listar os produtos similares com maiores vendas
(melhor srank) do que ele.
 */
-- SELECT DISTINCT p1.pasin
-- FROM similars s1
-- NATURAL JOIN products p1
-- JOIN products p2 ON s1.sim = p2.pasin
-- WHERE p1.srank < p2.srank
-- LIMIT 5;
-- ----------------------------------------------------------------------------
-- SELECT p2.*
-- FROM similars s
-- NATURAL JOIN products p1
-- JOIN products p2 ON s.sim = p2.pasin
-- WHERE s.pasin = '0001053736' AND p1.srank < p2.srank;
-- ############################################################################
/* 3. Dado um produto, mostrar a evolução diária das médias de avaliação ao
longo do período coberto no arquivo.
 */
-- SELECT *
-- FROM products
-- -- WHERE pasin = '0807220280'
-- ORDER BY dl DESC NULLS LAST
-- LIMIT 1;
-- ----------------------------------------------------------------------------
-- SELECT rdate, ROUND(AVG(rating), 2) AS avg_rating, COUNT(*) AS num_reviews
-- FROM reviews
-- WHERE pasin = '0807220280'
-- GROUP BY rdate;
-- ############################################################################
/* 4. Listar os 10 produtos líderes de venda em cada grupo de produtos.
 */
-- SELECT *
-- FROM
--     (SELECT *,
--             ROW_NUMBER() OVER (PARTITION BY grp
--                                ORDER BY srank DESC) AS rn
--      FROM products
--      WHERE srank IS NOT NULL ) ranked
-- WHERE rn <= 10;
-- ############################################################################
/*
5. Listar os 10 produtos
com a maior média de avaliações úteis positivas por produto.
 */
-- SELECT p.pasin,
--        p.title,
--        p.grp,
--        AVG(r.rating) AS avg_rating,
--        AVG(CAST(r.helpful AS FLOAT) / NULLIF(r.votes, 0)) AS avg_helpful_ratio,
--        COUNT(r.pasin) AS total_reviews,
--        COUNT(CASE
--                  WHEN r.rating >= 4 THEN 1
--              END) AS positive_reviews
-- FROM products p
-- JOIN reviews r ON p.pasin = r.pasin
-- WHERE
--     r.votes > 0
--     AND r.rating >= 4
-- GROUP BY p.pasin, p.title, p.grp
-- HAVING COUNT(r.pasin) >= 3 -- Pelo menos 3 reviews para ser considerado
-- ORDER BY
--     AVG(CAST(r.helpful AS FLOAT) / NULLIF(r.votes, 0)) DESC,
--     AVG(r.rating) DESC
-- LIMIT 10;
-- ############################################################################
/*
6. Listar as 5 categorias
com a maior média de avaliações úteis positivas por produto.
 */
-- SELECT c.descr AS categoria,
--        COUNT(DISTINCT p.pasin) AS total_produtos,
--        AVG(r.rating) AS media_rating,
--        AVG(CAST(r.helpful AS FLOAT) / NULLIF(r.votes, 0)) AS media_helpful_ratio,
--        COUNT(r.pasin) AS total_reviews_positivas
-- FROM categories c
-- JOIN products_categories pc ON c.cid = pc.cid
-- JOIN products p ON pc.pasin = p.pasin
-- JOIN reviews r ON p.pasin = r.pasin
-- WHERE r.rating >= 4
--     AND r.votes > 0
-- GROUP BY c.cid,
--          c.descr
-- HAVING COUNT(DISTINCT p.pasin) >= 5 -- Pelo menos 5 produtos na categoria
-- ORDER BY AVG(CAST(r.helpful AS FLOAT) / NULLIF(r.votes, 0)) DESC, AVG(r.rating) DESC
-- LIMIT 5;
-- ############################################################################
/* 7. Listar os 10 clientes que mais fizeram comentários por grupo de produto.
 */
-- SELECT p.grp, AVG(r.rating) AS avg_rating FROM reviews r
-- JOIN products p ON r.pasin = p.pasin
-- GROUP BY p.grp ORDER BY avg_rating DESC LIMIT 5;
-- SELECT r.userid, COUNT(*) AS num_reviews FROM reviews r
-- JOIN products p ON r.pasin = p.pasin
-- WHERE p.grp = 'Book'
-- GROUP BY r.userid ORDER BY num_reviews DESC LIMIT 10;
