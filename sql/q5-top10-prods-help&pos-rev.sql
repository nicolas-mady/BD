/* 5. Listar os 10 produtos com a maior média de avaliações úteis positivas por produto.
 */
SELECT p.pasin,
       p.title,
       ROUND(AVG(r.helpful), 2) AS avg_helpful_positive
FROM products p
JOIN reviews r ON p.pasin = r.pasin
WHERE r.rating >= 4 AND r.helpful > 0
GROUP BY p.pasin, p.title
ORDER BY avg_helpful_positive DESC
LIMIT 10;
