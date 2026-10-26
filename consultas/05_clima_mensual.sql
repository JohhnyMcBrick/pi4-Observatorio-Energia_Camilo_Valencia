-- Lluvia y temperatura mensuales en Antioquia (promedio de las estaciones del IDEAM).
-- Ya vienen agregadas por día y estación desde el servidor (SoQL).

WITH lluvia AS (
    SELECT strftime(CAST(fecha AS TIMESTAMP), '%Y-%m')             AS mes,
           ROUND(AVG(TRY_CAST(precipitacion_mm AS DOUBLE)), 2)     AS lluvia_mm_dia_estacion
    FROM read_parquet('data/bronze/ideam_precipitacion_diaria.parquet')
    GROUP BY mes
),
temperatura AS (
    SELECT strftime(CAST(fecha AS TIMESTAMP), '%Y-%m')             AS mes,
           ROUND(AVG(TRY_CAST(temp_media_c AS DOUBLE)), 1)         AS temp_media_c,
           ROUND(MIN(TRY_CAST(temp_min_c AS DOUBLE)), 1)           AS temp_min_c,
           ROUND(MAX(TRY_CAST(temp_max_c AS DOUBLE)), 1)           AS temp_max_c
    FROM read_parquet('data/bronze/ideam_temperatura_diaria.parquet')
    GROUP BY mes
)
SELECT mes, l.lluvia_mm_dia_estacion, t.temp_media_c, t.temp_min_c, t.temp_max_c
FROM lluvia l
JOIN temperatura t USING (mes)
ORDER BY mes;
