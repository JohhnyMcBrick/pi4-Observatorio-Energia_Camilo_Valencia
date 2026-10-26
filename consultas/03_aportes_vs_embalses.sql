-- Aportes hídricos (AporEner) frente al nivel de los embalses, por mes.
-- Los aportes bajos de forma sostenida anticipan embalses bajos y precio alto.
-- Los valores de bronce son TEXTO: se usa TRY_CAST.

WITH aportes_mes AS (
    SELECT strftime(CAST("Date" AS DATE), '%Y-%m')          AS mes,
           ROUND(AVG(TRY_CAST("Value" AS DOUBLE)), 0)       AS aporte_promedio_diario
    FROM read_parquet('data/bronze/xm_aportes_energia.parquet')
    GROUP BY mes
),
embalses_mes AS (
    SELECT strftime(CAST("Date" AS DATE), '%Y-%m')          AS mes,
           ROUND(AVG(TRY_CAST("Value" AS DOUBLE)) * 100, 1) AS embalses_pct
    FROM read_parquet('data/bronze/xm_embalses.parquet')
    GROUP BY mes
)
SELECT a.mes, a.aporte_promedio_diario, e.embalses_pct
FROM aportes_mes a
JOIN embalses_mes e USING (mes)
ORDER BY a.mes;
