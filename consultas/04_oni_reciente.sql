-- Índice ONI de NOAA desde 2023, con la fase de El Niño / La Niña.
-- SEAS es un trimestre móvil (DJF, JFM, ...): se ordena por su posición en el año.

SELECT SEAS                                         AS trimestre,
       CAST(YR AS INTEGER)                          AS anio,
       TRY_CAST(ANOM AS DOUBLE)                     AS anomalia,
       CASE WHEN TRY_CAST(ANOM AS DOUBLE) >=  0.5 THEN 'El Niño'
            WHEN TRY_CAST(ANOM AS DOUBLE) <= -0.5 THEN 'La Niña'
            ELSE 'Neutral' END                      AS fase
FROM read_parquet('data/bronze/noaa_oni.parquet')
WHERE CAST(YR AS INTEGER) >= 2023
ORDER BY anio,
         list_position(['DJF','JFM','FMA','MAM','AMJ','MJJ','JJA','JAS','ASO','SON','OND','NDJ'], SEAS);
