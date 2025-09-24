/* 3. Dado um produto, mostrar a evolução diária das médias de avaliação ao longo do período coberto no arquivo.
 */
WITH date_range AS ( -- datas de início e fim do produto
    SELECT
        MIN(rdate) AS start_date,
        MAX(rdate) AS end_date
    FROM reviews
    WHERE pasin = '0807220280'
),
all_dates AS ( -- gera todas as datas no intervalo
    SELECT generate_series(
               (SELECT start_date FROM date_range),
               (SELECT end_date FROM date_range),
               interval '1 day'
           )::date AS rdate
),
prod_dates AS ( -- média diária real (somente dias com review)
    SELECT rdate,
           SUM(rating) AS sum_rating,
           COUNT(*) AS num_reviews
    FROM reviews
    WHERE pasin = '0807220280'
    GROUP BY rdate
),
joined AS ( -- preenche valores faltantes com zero
    SELECT
        rdate,
        COALESCE(sum_rating, 0) AS sum_rating,
        COALESCE(num_reviews, 0) AS num_reviews
    FROM all_dates
    NATURAL LEFT JOIN prod_dates
),
accumulated AS (
    SELECT
        rdate,
        SUM(sum_rating) OVER (ORDER BY rdate) AS acc_rating,
        SUM(num_reviews) OVER (ORDER BY rdate) AS acc_reviews
    FROM joined
)
SELECT
    rdate,
    ROUND(acc_rating / NULLIF(acc_reviews, 0), 2) AS avg_rating,
    acc_reviews
FROM accumulated
ORDER BY rdate;
