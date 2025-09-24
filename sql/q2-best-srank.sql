/* 2. Dado um produto, listar os produtos similares com maiores vendas (melhor salesrank) do que ele.
 */
SELECT p2.pasin, p2.title, p2.srank
FROM products p1
NATURAL JOIN similars s
JOIN products p2 ON s.sim = p2.pasin
WHERE s.pasin = '0001053736' AND p1.srank > p2.srank;
