/* Dado um produto, listar os 5 comentários mais úteis e com maior avaliação e os 5 comentários mais úteis e com menor avaliação.
 */

(
    SELECT rid, rdate, usr_id, rating, helpful
    FROM reviews
    WHERE pasin = '0195110382'
    ORDER BY rating DESC, helpful DESC
    LIMIT 5
) UNION (
    SELECT
        NULL AS rid,
        NULL AS rdate,
        '----------' AS usr_id,
        NULL AS rating,
        NULL AS helpful
    FROM generate_series(1,1)
) UNION ALL (
    SELECT rid, rdate, usr_id, rating, helpful
    FROM reviews
    WHERE pasin = '0195110382'
    ORDER BY rating, helpful DESC
    LIMIT 5
);
