-- SELECT pasin FROM products WHERE dl = 10 LIMIT 1;
-- SELECT * FROM reviews WHERE pasin = '0195110382';

/* 1. Dado um produto, listar os 5 comentários mais úteis e com maior avaliação
e os 5 comentários mais úteis e com menor avaliação.
 */
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

-------------------------------------------------------------------------------

-- SELECT DISTINCT p1.pasin
-- FROM similars s1
-- NATURAL JOIN products p1
-- JOIN products p2 ON s1.sim = p2.pasin
-- WHERE p1.srank < p2.srank
-- LIMIT 5;

/* 2. Dado um produto, listar os produtos similares com maiores vendas
(melhor srank) do que ele.
 */
-- SELECT p2.*
-- FROM similars s
-- NATURAL JOIN products p1
-- JOIN products p2 ON s.sim = p2.pasin
-- WHERE s.pasin = '0001053736' AND p1.srank < p2.srank;

-------------------------------------------------------------------------------

-- SELECT *
-- FROM products
-- -- WHERE pasin = '0807220280'
-- ORDER BY dl DESC NULLS LAST
-- LIMIT 1;

/* 3. Dado um produto, mostrar a evolução diária das médias de avaliação ao
longo do período coberto no arquivo.
 */
-- SELECT rdate, ROUND(AVG(rating), 2) AS avg_rating, COUNT(*) AS num_reviews
-- FROM reviews
-- WHERE pasin = '0807220280'
-- GROUP BY rdate;

-------------------------------------------------------------------------------

/* 4. Listar os 10 produtos líderes de venda em cada grupo de produtos. */
-- SELECT *
-- FROM products
-- WHERE srank IS NOT NULL
-- ORDER BY grp, srank
-- LIMIT 100;

-------------------------------------------------------------------------------

/* 5. Listar os 10 produtos com a maior média de avaliações úteis positivas
por produto.
 */
-- SELECT products.*
-- FROM products
-- NATURAL JOIN reviews
-- WHERE av_rt >= 4 AND votes > 0
-- ORDER BY helpful / votes DESC
-- LIMIT 10;

-------------------------------------------------------------------------------

/* 6. Listar as 5 categorias com a maior média de avaliações úteis positivas
por produto.
 */
SELECT pasin, AVG(positive) AS avg_positive
FROM reviews
GROUP BY pasin
ORDER BY avg_positive DESC
LIMIT 10;

-------------------------------------------------------------------------------

/* 7. Listar os 10 clientes que mais fizeram comentários por grupo de produto.
 */
-- SELECT p.grp, AVG(r.positive) AS avg_positive FROM reviews r
-- JOIN products p ON r.pasin = p.pasin
-- GROUP BY p.grp ORDER BY avg_positive DESC LIMIT 5;

-- SELECT r.userid, COUNT(*) AS num_reviews FROM reviews r
-- JOIN products p ON r.pasin = p.pasin
-- WHERE p.grp = 'Book'
-- GROUP BY r.userid ORDER BY num_reviews DESC LIMIT 10;
