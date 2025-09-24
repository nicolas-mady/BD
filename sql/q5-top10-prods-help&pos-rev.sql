/* 5. Listar os 10 produtos com a maior média de avaliações úteis positivas por produto.
 */

SELECT pasin,
       title,
       ROUND(AVG(helpful), 2) AS avg_helpful_positive
FROM products
NATURAL JOIN reviews
WHERE rating > 3 AND helpful > 0
GROUP BY pasin, title
ORDER BY avg_helpful_positive DESC
LIMIT 10;
