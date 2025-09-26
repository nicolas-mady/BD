/* 2. Dado um produto, listar os produtos similares com maiores vendas (melhor salesrank) do que ele.
 */

SELECT pasin, title, srank
FROM products
WHERE pasin = '0807220280' 
UNION (
    SELECT p2.pasin, p2.title, p2.srank
    FROM products p1
    NATURAL JOIN similars s
    JOIN products p2 ON s.sim = p2.pasin
    WHERE s.pasin = '0807220280' AND p1.srank > p2.srank
)
ORDER BY srank;
