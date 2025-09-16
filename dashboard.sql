-- SELECT pasin FROM products WHERE dl = 10 LIMIT 1;
-- SELECT * FROM reviews WHERE pasin = '0195110382';

/* 1. Dado um produto, listar os 5 comentários mais úteis e com maior avaliação e os 5 comentários mais úteis e com menor avaliação. */

-- SELECT reviews.* FROM reviews NATURAL JOIN products WHERE pasin = '0195110382' ORDER BY rating DESC, helpful DESC LIMIT 5;
-- SELECT reviews.* FROM reviews NATURAL JOIN products WHERE pasin = '0195110382' ORDER BY rating ASC, helpful DESC LIMIT 5;


-- SELECT DISTINCT p1.pasin
-- FROM similars s1
-- NATURAL JOIN products p1
-- JOIN products p2 ON s1.sim = p2.pasin
-- WHERE p1.srank < p2.srank
-- LIMIT 5;

/* 2. Dado um produto, listar os produtos similares com maiores vendas (melhor srank) do que ele. */

-- SELECT p2.*
-- FROM similars s
-- NATURAL JOIN products p1
-- JOIN products p2 ON s.sim = p2.pasin
-- WHERE s.pasin = '0001053736' AND p1.srank < p2.srank;

-- SELECT *
-- FROM products
-- WHERE srank < (
--     SELECT srank
--     FROM products
--     WHERE pasin = '0001053736'
-- ) LIMIT 5;
/* 3. Dado um produto, mostrar a evolução diária das médias de avaliação ao longo do período coberto no arquivo. */
-- SELECT date, AVG(rating) FROM reviews WHERE pid = 'B00004S1RH' GROUP BY date ORDER BY date;


/* 4. Listar os 10 produtos líderes de venda em cada grupo de produtos. */
-- SELECT p1.asin, p1.title, p1.srank FROM products p1
-- JOIN products p2 ON p1.group = p2.group
-- WHERE p2.asin = 'B00004S1RH' AND p1.srank < p2.srank
-- ORDER BY p1.srank LIMIT 5;


/* 5. Listar os 10 produtos com a maior média de avaliações úteis positivas por produto. */
-- SELECT asin, title, srank FROM products WHERE group = 'Book' ORDER BY srank LIMIT 10;


/* 6. Listar as 5 categorias com a maior média de avaliações úteis positivas por produto. */
-- SELECT pid, AVG(positive) AS avg_positive FROM reviews GROUP BY pid ORDER BY avg_positive DESC LIMIT 10;


/* 7. Listar os 10 clientes que mais fizeram comentários por grupo de produto. */
-- SELECT p.group, AVG(r.positive) AS avg_positive FROM reviews r
-- JOIN products p ON r.pid = p.asin
-- GROUP BY p.group ORDER BY avg_positive DESC LIMIT 5;

-- SELECT r.userid, COUNT(*) AS num_reviews FROM reviews r
-- JOIN products p ON r.pid = p.asin
-- WHERE p.group = 'Book'
-- GROUP BY r.userid ORDER BY num_reviews DESC LIMIT 10;
