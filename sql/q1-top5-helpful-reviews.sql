/* Dado um produto, listar os 5 comentários mais úteis e com maior avaliação e os 5 comentários mais úteis e com menor avaliação.
 */

SELECT *
FROM reviews
WHERE pasin = '0195110382'
ORDER BY rating DESC, helpful DESC
LIMIT 5;

SELECT *
FROM reviews
WHERE pasin = '0195110382'
ORDER BY rating, helpful DESC
LIMIT 5;
