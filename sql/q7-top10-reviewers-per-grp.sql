/* 7. Listar os 10 clientes que mais fizeram comentários por grupo de produto.
 */

SELECT *
FROM (
    SELECT
        usr_id,
        ROW_NUMBER() OVER (
            PARTITION BY grp
            ORDER BY COUNT(*) DESC
        ) AS rnk,
        grp,
        COUNT(*) AS num_reviews
    FROM reviews
    NATURAL JOIN products
    GROUP BY usr_id, grp
)
WHERE rnk <= 10;
