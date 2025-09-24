/* 5. Listar os 10 produtos com a maior média de avaliações úteis positivas por produto.
 */
-- SELECT p.pasin,
--        p.title,
--        ROUND(AVG(r.helpful), 2) AS avg_helpful
-- FROM products p
-- JOIN reviews r ON p.pasin = r.pasin
-- GROUP BY p.pasin, p.title
-- ORDER BY avg_helpful DESC
-- LIMIT 10;

SELECT p.pasin,
       p.title,
       AVG(r.rating) AS avg_rating,
       AVG(CAST(r.helpful AS FLOAT) / NULLIF(r.votes, 0)) AS avg_helpful_ratio,
       COUNT(r.pasin) AS total_reviews,
       COUNT(CASE
                 WHEN r.rating > 3 THEN 1
             END) AS positive_reviews
FROM products p
JOIN reviews r ON p.pasin = r.pasin
WHERE
    r.votes > 0
    AND r.rating > 3
GROUP BY p.pasin, p.title, p.grp
-- HAVING COUNT(r.pasin) >= 3 -- Pelo menos 3 reviews para ser considerado
ORDER BY
    AVG(CAST(r.helpful AS FLOAT) / NULLIF(r.votes, 0)) DESC,
    AVG(r.rating) DESC
LIMIT 10;

-- SELECT pasin, title
-- FROM reviews
-- NATURAL JOIN products
-- WHERE votes > 0 AND rating > 3
-- GROUP BY pasin, title, helpful, votes
-- ORDER BY helpful / votes DESC, AVG(rating) DESC
-- LIMIT 10;
