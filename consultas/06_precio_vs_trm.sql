-- Pregunta propia: ¿el precio de bolsa se mueve con el dólar?
-- Precio de bolsa promedio mensual (COP/kWh) frente a la TRM promedio del mes (COP/USD).

WITH precio_hora AS (
    UNPIVOT read_parquet('data/bronze/xm_precio_bolsa.parquet')
    ON COLUMNS('^Hour')
    INTO NAME hora VALUE precio
),
precio_mes AS (
    SELECT strftime(CAST("Date" AS DATE), '%Y-%m')          AS mes,
           ROUND(AVG(TRY_CAST(precio AS DOUBLE)), 0)        AS precio_bolsa_cop_kwh
    FROM precio_hora
    GROUP BY mes
),
trm_mes AS (
    SELECT strftime(CAST(vigenciadesde AS TIMESTAMP), '%Y-%m') AS mes,
           ROUND(AVG(TRY_CAST(valor AS DOUBLE)), 0)            AS trm_cop_usd
    FROM read_parquet('data/bronze/trm_diaria.parquet')
    GROUP BY mes
)
SELECT p.mes, p.precio_bolsa_cop_kwh, t.trm_cop_usd
FROM precio_mes p
JOIN trm_mes t USING (mes)
ORDER BY p.mes;
