/* 4. Listar os 10 produtos líderes de venda em cada grupo de produtos.
 */

SELECT *
FROM (
    SELECT
        pasin,
        title,
        ROW_NUMBER() OVER (
            PARTITION BY grp
            ORDER BY srank
        ) AS rnk,
        grp,
        srank
    FROM products
    WHERE
        srank IS NOT NULL
        AND srank > 0
) ranked_products
WHERE rnk <= 10;
