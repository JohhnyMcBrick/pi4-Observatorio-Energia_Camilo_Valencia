# Perfilamiento de la capa bronce

> Generado automáticamente con `python -m src.perfilar` el 2026-10-25 23:36 UTC. No editar a mano: se regenera completo (las notas del equipo van en `docs/notas_perfilamiento.md`).

## Resumen

| Archivo | Filas | Columnas | Duplicadas | Rango de fechas |
|---|---:|---:|---:|---|
| `enerandes_ventas_2023` | 1,114 | 10 | 32 | n/a: fechas como texto en formatos mixtos (se normalizan en plata) |
| `enerandes_ventas_2024` | 1,114 | 11 | 32 | n/a: fechas como texto en formatos mixtos (se normalizan en plata) |
| `enerandes_ventas_2025` | 1,117 | 10 | 32 | n/a: fechas como texto en formatos mixtos (se normalizan en plata) |
| `enerandes_ventas_2026` | 839 | 10 | 24 | n/a: fechas como texto en formatos mixtos (se normalizan en plata) |
| `ideam_precipitacion_diaria` | 29,804 | 12 | 0 | 2025-01-01 a 2026-07-24 |
| `ideam_temperatura_diaria` | 17,349 | 14 | 0 | 2025-01-01 a 2026-07-24 |
| `noaa_oni` | 920 | 7 | 0 | 1950 a 2026 (años) |
| `trm_diaria` | 652 | 7 | 0 | 2023-12-27 a 2026-09-30 |
| `xm_aportes_energia` | 1,004 | 6 | 0 | 2024-01-01 a 2026-09-30 |
| `xm_demanda` | 1,004 | 30 | 0 | 2024-01-01 a 2026-09-30 |
| `xm_embalses` | 1,004 | 6 | 0 | 2024-01-01 a 2026-09-30 |
| `xm_generacion_recurso` | 350,361 | 30 | 0 | 2024-01-01 a 2026-09-30 |
| `xm_listado_recursos` | 2,493 | 13 | 2 | n/a (sin columna de fecha) |
| `xm_precio_bolsa` | 1,004 | 30 | 0 | 2024-01-01 a 2026-09-30 |

## Tablas por archivo

### `enerandes_ventas_2023.parquet`

| Métrica | Valor |
|---|---|
| Filas | 1,114 |
| Columnas | 10 |
| Filas duplicadas (exactas, sin columnas de linaje) | 32 (2.9 %) |
| Rango de fechas | n/a: fechas como texto en formatos mixtos (se normalizan en plata) |

| Columna | Tipo | Nulos | % nulos | Vacíos ('') |
|---|---|---:|---:|---:|
| `col_0` | texto | 0 | 0.0 % | 0 |
| `col_1` | texto | 1 | 0.1 % | 0 |
| `col_2` | texto | 16 | 1.4 % | 0 |
| `col_3` | texto | 1 | 0.1 % | 0 |
| `col_4` | texto | 10 | 0.9 % | 0 |
| `col_5` | texto | 8 | 0.7 % | 0 |
| `col_6` | texto | 1 | 0.1 % | 0 |
| `_fuente` | texto | 0 | 0.0 % | 0 |
| `_origen` | texto | 0 | 0.0 % | 0 |
| `_extraido_en` | texto | 0 | 0.0 % | 0 |

### `enerandes_ventas_2024.parquet`

| Métrica | Valor |
|---|---|
| Filas | 1,114 |
| Columnas | 11 |
| Filas duplicadas (exactas, sin columnas de linaje) | 32 (2.9 %) |
| Rango de fechas | n/a: fechas como texto en formatos mixtos (se normalizan en plata) |

| Columna | Tipo | Nulos | % nulos | Vacíos ('') |
|---|---|---:|---:|---:|
| `col_0` | texto | 0 | 0.0 % | 0 |
| `col_1` | texto | 1 | 0.1 % | 0 |
| `col_2` | texto | 4 | 0.4 % | 0 |
| `col_3` | texto | 1 | 0.1 % | 0 |
| `col_4` | texto | 8 | 0.7 % | 0 |
| `col_5` | texto | 1 | 0.1 % | 0 |
| `col_6` | texto | 12 | 1.1 % | 0 |
| `col_7` | texto | 1 | 0.1 % | 0 |
| `_fuente` | texto | 0 | 0.0 % | 0 |
| `_origen` | texto | 0 | 0.0 % | 0 |
| `_extraido_en` | texto | 0 | 0.0 % | 0 |

### `enerandes_ventas_2025.parquet`

| Métrica | Valor |
|---|---|
| Filas | 1,117 |
| Columnas | 10 |
| Filas duplicadas (exactas, sin columnas de linaje) | 32 (2.9 %) |
| Rango de fechas | n/a: fechas como texto en formatos mixtos (se normalizan en plata) |

| Columna | Tipo | Nulos | % nulos | Vacíos ('') |
|---|---|---:|---:|---:|
| `col_0` | texto | 1 | 0.1 % | 0 |
| `col_1` | texto | 4 | 0.4 % | 0 |
| `col_2` | texto | 10 | 0.9 % | 0 |
| `col_3` | texto | 4 | 0.4 % | 0 |
| `col_4` | texto | 10 | 0.9 % | 0 |
| `col_5` | texto | 8 | 0.7 % | 0 |
| `col_6` | texto | 4 | 0.4 % | 0 |
| `_fuente` | texto | 0 | 0.0 % | 0 |
| `_origen` | texto | 0 | 0.0 % | 0 |
| `_extraido_en` | texto | 0 | 0.0 % | 0 |

### `enerandes_ventas_2026.parquet`

| Métrica | Valor |
|---|---|
| Filas | 839 |
| Columnas | 10 |
| Filas duplicadas (exactas, sin columnas de linaje) | 24 (2.9 %) |
| Rango de fechas | n/a: fechas como texto en formatos mixtos (se normalizan en plata) |

| Columna | Tipo | Nulos | % nulos | Vacíos ('') |
|---|---|---:|---:|---:|
| `col_0` | texto | 1 | 0.1 % | 0 |
| `col_1` | texto | 4 | 0.5 % | 0 |
| `col_2` | texto | 9 | 1.1 % | 0 |
| `col_3` | texto | 4 | 0.5 % | 0 |
| `col_4` | texto | 9 | 1.1 % | 0 |
| `col_5` | texto | 11 | 1.3 % | 0 |
| `col_6` | texto | 4 | 0.5 % | 0 |
| `_fuente` | texto | 0 | 0.0 % | 0 |
| `_origen` | texto | 0 | 0.0 % | 0 |
| `_extraido_en` | texto | 0 | 0.0 % | 0 |

### `ideam_precipitacion_diaria.parquet`

| Métrica | Valor |
|---|---|
| Filas | 29,804 |
| Columnas | 12 |
| Filas duplicadas (exactas, sin columnas de linaje) | 0 (0.0 %) |
| Rango de fechas | 2025-01-01 a 2026-07-24 |

| Columna | Tipo | Nulos | % nulos | Vacíos ('') |
|---|---|---:|---:|---:|
| `codigoestacion` | texto | 0 | 0.0 % | 0 |
| `nombreestacion` | texto | 0 | 0.0 % | 0 |
| `municipio` | texto | 0 | 0.0 % | 0 |
| `zonahidrografica` | texto | 0 | 0.0 % | 0 |
| `latitud` | texto | 0 | 0.0 % | 0 |
| `longitud` | texto | 0 | 0.0 % | 0 |
| `fecha` | texto | 0 | 0.0 % | 0 |
| `precipitacion_mm` | texto | 0 | 0.0 % | 0 |
| `n_obs` | texto | 0 | 0.0 % | 0 |
| `_fuente` | texto | 0 | 0.0 % | 0 |
| `_origen` | texto | 0 | 0.0 % | 0 |
| `_extraido_en` | texto | 0 | 0.0 % | 0 |

### `ideam_temperatura_diaria.parquet`

| Métrica | Valor |
|---|---|
| Filas | 17,349 |
| Columnas | 14 |
| Filas duplicadas (exactas, sin columnas de linaje) | 0 (0.0 %) |
| Rango de fechas | 2025-01-01 a 2026-07-24 |

| Columna | Tipo | Nulos | % nulos | Vacíos ('') |
|---|---|---:|---:|---:|
| `codigoestacion` | texto | 0 | 0.0 % | 0 |
| `nombreestacion` | texto | 0 | 0.0 % | 0 |
| `municipio` | texto | 0 | 0.0 % | 0 |
| `zonahidrografica` | texto | 0 | 0.0 % | 0 |
| `latitud` | texto | 0 | 0.0 % | 0 |
| `longitud` | texto | 0 | 0.0 % | 0 |
| `fecha` | texto | 0 | 0.0 % | 0 |
| `temp_media_c` | texto | 0 | 0.0 % | 0 |
| `temp_min_c` | texto | 0 | 0.0 % | 0 |
| `temp_max_c` | texto | 0 | 0.0 % | 0 |
| `n_obs` | texto | 0 | 0.0 % | 0 |
| `_fuente` | texto | 0 | 0.0 % | 0 |
| `_origen` | texto | 0 | 0.0 % | 0 |
| `_extraido_en` | texto | 0 | 0.0 % | 0 |

### `noaa_oni.parquet`

| Métrica | Valor |
|---|---|
| Filas | 920 |
| Columnas | 7 |
| Filas duplicadas (exactas, sin columnas de linaje) | 0 (0.0 %) |
| Rango de fechas | 1950 a 2026 (años) |

| Columna | Tipo | Nulos | % nulos | Vacíos ('') |
|---|---|---:|---:|---:|
| `SEAS` | texto | 0 | 0.0 % | 0 |
| `YR` | texto | 0 | 0.0 % | 0 |
| `TOTAL` | texto | 0 | 0.0 % | 0 |
| `ANOM` | texto | 0 | 0.0 % | 0 |
| `_fuente` | texto | 0 | 0.0 % | 0 |
| `_origen` | texto | 0 | 0.0 % | 0 |
| `_extraido_en` | texto | 0 | 0.0 % | 0 |

### `trm_diaria.parquet`

| Métrica | Valor |
|---|---|
| Filas | 652 |
| Columnas | 7 |
| Filas duplicadas (exactas, sin columnas de linaje) | 0 (0.0 %) |
| Rango de fechas | 2023-12-27 a 2026-09-30 |

| Columna | Tipo | Nulos | % nulos | Vacíos ('') |
|---|---|---:|---:|---:|
| `valor` | texto | 0 | 0.0 % | 0 |
| `unidad` | texto | 0 | 0.0 % | 0 |
| `vigenciadesde` | texto | 0 | 0.0 % | 0 |
| `vigenciahasta` | texto | 0 | 0.0 % | 0 |
| `_fuente` | texto | 0 | 0.0 % | 0 |
| `_origen` | texto | 0 | 0.0 % | 0 |
| `_extraido_en` | texto | 0 | 0.0 % | 0 |

### `xm_aportes_energia.parquet`

| Métrica | Valor |
|---|---|
| Filas | 1,004 |
| Columnas | 6 |
| Filas duplicadas (exactas, sin columnas de linaje) | 0 (0.0 %) |
| Rango de fechas | 2024-01-01 a 2026-09-30 |

| Columna | Tipo | Nulos | % nulos | Vacíos ('') |
|---|---|---:|---:|---:|
| `Date` | texto | 0 | 0.0 % | 0 |
| `Id` | texto | 0 | 0.0 % | 0 |
| `Value` | texto | 0 | 0.0 % | 0 |
| `_fuente` | texto | 0 | 0.0 % | 0 |
| `_origen` | texto | 0 | 0.0 % | 0 |
| `_extraido_en` | texto | 0 | 0.0 % | 0 |

### `xm_demanda.parquet`

| Métrica | Valor |
|---|---|
| Filas | 1,004 |
| Columnas | 30 |
| Filas duplicadas (exactas, sin columnas de linaje) | 0 (0.0 %) |
| Rango de fechas | 2024-01-01 a 2026-09-30 |

| Columna | Tipo | Nulos | % nulos | Vacíos ('') |
|---|---|---:|---:|---:|
| `Date` | texto | 0 | 0.0 % | 0 |
| `Id` | texto | 0 | 0.0 % | 0 |
| `code` | texto | 0 | 0.0 % | 0 |
| `Hour01` | texto | 0 | 0.0 % | 0 |
| `Hour02` | texto | 0 | 0.0 % | 0 |
| `Hour03` | texto | 0 | 0.0 % | 0 |
| `Hour04` | texto | 0 | 0.0 % | 0 |
| `Hour05` | texto | 0 | 0.0 % | 0 |
| `Hour06` | texto | 0 | 0.0 % | 0 |
| `Hour07` | texto | 0 | 0.0 % | 0 |
| `Hour08` | texto | 0 | 0.0 % | 0 |
| `Hour09` | texto | 0 | 0.0 % | 0 |
| `Hour10` | texto | 0 | 0.0 % | 0 |
| `Hour11` | texto | 0 | 0.0 % | 0 |
| `Hour12` | texto | 0 | 0.0 % | 0 |
| `Hour13` | texto | 0 | 0.0 % | 0 |
| `Hour14` | texto | 0 | 0.0 % | 0 |
| `Hour15` | texto | 0 | 0.0 % | 0 |
| `Hour16` | texto | 0 | 0.0 % | 0 |
| `Hour17` | texto | 0 | 0.0 % | 0 |
| `Hour18` | texto | 0 | 0.0 % | 0 |
| `Hour19` | texto | 0 | 0.0 % | 0 |
| `Hour20` | texto | 0 | 0.0 % | 0 |
| `Hour21` | texto | 0 | 0.0 % | 0 |
| `Hour22` | texto | 0 | 0.0 % | 0 |
| `Hour23` | texto | 0 | 0.0 % | 0 |
| `Hour24` | texto | 0 | 0.0 % | 0 |
| `_fuente` | texto | 0 | 0.0 % | 0 |
| `_origen` | texto | 0 | 0.0 % | 0 |
| `_extraido_en` | texto | 0 | 0.0 % | 0 |

### `xm_embalses.parquet`

| Métrica | Valor |
|---|---|
| Filas | 1,004 |
| Columnas | 6 |
| Filas duplicadas (exactas, sin columnas de linaje) | 0 (0.0 %) |
| Rango de fechas | 2024-01-01 a 2026-09-30 |

| Columna | Tipo | Nulos | % nulos | Vacíos ('') |
|---|---|---:|---:|---:|
| `Date` | texto | 0 | 0.0 % | 0 |
| `Id` | texto | 0 | 0.0 % | 0 |
| `Value` | texto | 0 | 0.0 % | 0 |
| `_fuente` | texto | 0 | 0.0 % | 0 |
| `_origen` | texto | 0 | 0.0 % | 0 |
| `_extraido_en` | texto | 0 | 0.0 % | 0 |

### `xm_generacion_recurso.parquet`

| Métrica | Valor |
|---|---|
| Filas | 350,361 |
| Columnas | 30 |
| Filas duplicadas (exactas, sin columnas de linaje) | 0 (0.0 %) |
| Rango de fechas | 2024-01-01 a 2026-09-30 |

| Columna | Tipo | Nulos | % nulos | Vacíos ('') |
|---|---|---:|---:|---:|
| `Date` | texto | 0 | 0.0 % | 0 |
| `Id` | texto | 0 | 0.0 % | 0 |
| `code` | texto | 0 | 0.0 % | 0 |
| `Hour01` | texto | 0 | 0.0 % | 182,025 |
| `Hour02` | texto | 0 | 0.0 % | 184,023 |
| `Hour03` | texto | 0 | 0.0 % | 184,632 |
| `Hour04` | texto | 0 | 0.0 % | 184,818 |
| `Hour05` | texto | 0 | 0.0 % | 183,644 |
| `Hour06` | texto | 0 | 0.0 % | 156,067 |
| `Hour07` | texto | 0 | 0.0 % | 52,273 |
| `Hour08` | texto | 0 | 0.0 % | 37,162 |
| `Hour09` | texto | 0 | 0.0 % | 30,427 |
| `Hour10` | texto | 0 | 0.0 % | 26,803 |
| `Hour11` | texto | 0 | 0.0 % | 24,801 |
| `Hour12` | texto | 0 | 0.0 % | 24,116 |
| `Hour13` | texto | 0 | 0.0 % | 24,048 |
| `Hour14` | texto | 0 | 0.0 % | 23,722 |
| `Hour15` | texto | 0 | 0.0 % | 24,072 |
| `Hour16` | texto | 0 | 0.0 % | 26,508 |
| `Hour17` | texto | 0 | 0.0 % | 31,434 |
| `Hour18` | texto | 0 | 0.0 % | 40,140 |
| `Hour19` | texto | 0 | 0.0 % | 141,440 |
| `Hour20` | texto | 0 | 0.0 % | 175,967 |
| `Hour21` | texto | 0 | 0.0 % | 177,096 |
| `Hour22` | texto | 0 | 0.0 % | 177,907 |
| `Hour23` | texto | 0 | 0.0 % | 179,809 |
| `Hour24` | texto | 0 | 0.0 % | 180,281 |
| `_fuente` | texto | 0 | 0.0 % | 0 |
| `_origen` | texto | 0 | 0.0 % | 0 |
| `_extraido_en` | texto | 0 | 0.0 % | 0 |

### `xm_listado_recursos.parquet`

| Métrica | Valor |
|---|---|
| Filas | 2,493 |
| Columnas | 13 |
| Filas duplicadas (exactas, sin columnas de linaje) | 2 (0.1 %) |
| Rango de fechas | n/a (sin columna de fecha) |

| Columna | Tipo | Nulos | % nulos | Vacíos ('') |
|---|---|---:|---:|---:|
| `Id` | texto | 0 | 0.0 % | 0 |
| `Code` | texto | 0 | 0.0 % | 0 |
| `Name` | texto | 0 | 0.0 % | 0 |
| `Type` | texto | 0 | 0.0 % | 0 |
| `Disp` | texto | 0 | 0.0 % | 0 |
| `RecType` | texto | 0 | 0.0 % | 0 |
| `CompanyCode` | texto | 0 | 0.0 % | 0 |
| `EnerSource` | texto | 0 | 0.0 % | 0 |
| `OperStartdate` | texto | 0 | 0.0 % | 0 |
| `State` | texto | 0 | 0.0 % | 0 |
| `_fuente` | texto | 0 | 0.0 % | 0 |
| `_origen` | texto | 0 | 0.0 % | 0 |
| `_extraido_en` | texto | 0 | 0.0 % | 0 |

### `xm_precio_bolsa.parquet`

| Métrica | Valor |
|---|---|
| Filas | 1,004 |
| Columnas | 30 |
| Filas duplicadas (exactas, sin columnas de linaje) | 0 (0.0 %) |
| Rango de fechas | 2024-01-01 a 2026-09-30 |

| Columna | Tipo | Nulos | % nulos | Vacíos ('') |
|---|---|---:|---:|---:|
| `Date` | texto | 0 | 0.0 % | 0 |
| `Id` | texto | 0 | 0.0 % | 0 |
| `code` | texto | 0 | 0.0 % | 0 |
| `Hour01` | texto | 0 | 0.0 % | 0 |
| `Hour02` | texto | 0 | 0.0 % | 0 |
| `Hour03` | texto | 0 | 0.0 % | 0 |
| `Hour04` | texto | 0 | 0.0 % | 0 |
| `Hour05` | texto | 0 | 0.0 % | 0 |
| `Hour06` | texto | 0 | 0.0 % | 0 |
| `Hour07` | texto | 0 | 0.0 % | 0 |
| `Hour08` | texto | 0 | 0.0 % | 0 |
| `Hour09` | texto | 0 | 0.0 % | 0 |
| `Hour10` | texto | 0 | 0.0 % | 0 |
| `Hour11` | texto | 0 | 0.0 % | 0 |
| `Hour12` | texto | 0 | 0.0 % | 0 |
| `Hour13` | texto | 0 | 0.0 % | 0 |
| `Hour14` | texto | 0 | 0.0 % | 0 |
| `Hour15` | texto | 0 | 0.0 % | 0 |
| `Hour16` | texto | 0 | 0.0 % | 0 |
| `Hour17` | texto | 0 | 0.0 % | 0 |
| `Hour18` | texto | 0 | 0.0 % | 0 |
| `Hour19` | texto | 0 | 0.0 % | 0 |
| `Hour20` | texto | 0 | 0.0 % | 0 |
| `Hour21` | texto | 0 | 0.0 % | 0 |
| `Hour22` | texto | 0 | 0.0 % | 0 |
| `Hour23` | texto | 0 | 0.0 % | 0 |
| `Hour24` | texto | 0 | 0.0 % | 0 |
| `_fuente` | texto | 0 | 0.0 % | 0 |
| `_origen` | texto | 0 | 0.0 % | 0 |
| `_extraido_en` | texto | 0 | 0.0 % | 0 |

## Hallazgos de calidad (19)

### H1. Cada hoja anual tiene encabezados distintos y algunas traen título encima

- **Archivo(s):** `enerandes_ventas_2023, enerandes_ventas_2024, enerandes_ventas_2025, enerandes_ventas_2026`
- **Evidencia:** 4 encabezados distintos en 4 hojas; 2 hojas con filas de título previas (2025: 3 filas, 2026: 3 filas); la hoja 2024 tiene además columna UNIDAD (8 columnas vs 7).
- **Qué haremos en plata:** Mapear cada hoja a un esquema común y saltar las filas de título.

### H2. Fila 'TOTAL' mezclada con los datos

- **Archivo(s):** `enerandes_ventas_2023, enerandes_ventas_2024, enerandes_ventas_2025, enerandes_ventas_2026`
- **Evidencia:** 4 filas TOTAL (una por hoja) que sumarían doble.
- **Qué haremos en plata:** Excluir filas TOTAL antes de agregar.

### H3. Fechas en formatos mixtos

- **Archivo(s):** `enerandes_ventas_2023, enerandes_ventas_2024, enerandes_ventas_2025, enerandes_ventas_2026`
- **Evidencia:** 4 formatos: MM/AAAA: 1,500 filas; AAAA-MM: 1,466 filas; DD/MM/AAAA: 834 filas; mmm-AA: 370 filas. En la hoja 2024 conviven 3 formatos: MM/AAAA=388, mmm-AA=370, AAAA-MM=354.
- **Qué haremos en plata:** Parser por formato hacia fecha de primer día de mes (DATE).

### H4. Registros duplicados exactos

- **Archivo(s):** `enerandes_ventas_2023, enerandes_ventas_2024, enerandes_ventas_2025, enerandes_ventas_2026`
- **Evidencia:** 120 duplicados sobre 4,170 filas de datos (2.9 %); por hoja: 2023=32, 2024=32, 2025=32, 2026=24
- **Qué haremos en plata:** Deduplicar por (mes, municipio, segmento, tipo de compra).

### H5. Municipios mal escritos (tildes, mayúsculas, espacios, abreviaturas)

- **Archivo(s):** `enerandes_ventas_2023, enerandes_ventas_2024, enerandes_ventas_2025, enerandes_ventas_2026`
- **Evidencia:** 32 escrituras distintas para ~20 nombres tras quitar tildes/mayúsculas/espacios; Medellín aparece de 6 formas: 'MEDELLÍN', 'Medellin', 'Medellín', 'Medellín ', 'Medellín D.E.', 'medellin'. Siguen quedando variantes como 'Rio Negro'/'Rionegro', 'Sta Fe de Antioquia'.
- **Qué haremos en plata:** Normalizar contra el catálogo DIVIPOLA con tabla de equivalencias.

### H6. Unidades mezcladas (kWh y MWh) en la misma columna

- **Archivo(s):** `enerandes_ventas_2024`
- **Evidencia:** 765 filas en kWh y 347 en MWh (31.2 %); mediana kWh = 296,851 vs mediana MWh = 301.7: sumarlas sin convertir subestima el consumo ~1000 veces.
- **Qué haremos en plata:** Convertir todo a kWh (MWh × 1000) usando la columna UNIDAD.

### H7. Tipo de compra con escrituras inconsistentes

- **Archivo(s):** `enerandes_ventas_2023, enerandes_ventas_2024, enerandes_ventas_2025, enerandes_ventas_2026`
- **Evidencia:** 4 valores para 2 categorías reales: 'Bolsa'=1,975, 'Contrato'=1,974, 'CONTRATOS'=117, 'bolsa'=104
- **Qué haremos en plata:** Mapear a {Contrato, Bolsa}.

### H8. Celdas vacías y valores negativos imposibles en energía

- **Archivo(s):** `enerandes_ventas_2023, enerandes_ventas_2024, enerandes_ventas_2025, enerandes_ventas_2026`
- **Evidencia:** 27 celdas de energía vacías y 18 valores negativos (por hoja, vacías/negativas: 2023=9/7, 2024=7/3, 2025=6/4, 2026=5/4).
- **Qué haremos en plata:** Tratar negativos como error de captura (nulo) y definir regla de imputación o descarte.

### H9. Segmento de cliente sin dato

- **Archivo(s):** `enerandes_ventas_2023, enerandes_ventas_2024, enerandes_ventas_2025, enerandes_ventas_2026`
- **Evidencia:** 29 filas sin segmento (0.7 %), que no se pueden asignar a residencial/comercial/industrial.
- **Qué haremos en plata:** Clasificar como 'Sin segmento' o descartar según el análisis.

### H10. Formato ANCHO horario (Hour01...Hour24)

- **Archivo(s):** `xm_demanda, xm_generacion_recurso, xm_precio_bolsa`
- **Evidencia:** xm_demanda: 1,004 filas x 24 columnas de hora; xm_generacion_recurso: 350,361 filas x 24 columnas de hora; xm_precio_bolsa: 1,004 filas x 24 columnas de hora
- **Qué haremos en plata:** UNPIVOT a formato largo (fecha, hora, valor) en plata.

### H11. Catálogo de plantas con estructura distinta (endpoint lists)

- **Archivo(s):** `xm_listado_recursos`
- **Evidencia:** 2,493 recursos y 10 columnas; sin columna de fecha.
- **Qué haremos en plata:** Usarlo como dim_recurso (tipo, fuente, agente).

### H12. Cobertura desigual de observaciones por estación-día

- **Archivo(s):** `ideam_precipitacion_diaria`
- **Evidencia:** n_obs mínimo 1, mediana 144, máximo 16302; 579 filas con menos de la mitad de la mediana.
- **Qué haremos en plata:** Marcar días con cobertura baja (suma de lluvia subestimada).

### H13. Estaciones con cobertura parcial en el periodo

- **Archivo(s):** `ideam_precipitacion_diaria`
- **Evidencia:** 72 estaciones; días por estación: mín 35, mediana 494, máx 536.
- **Qué haremos en plata:** Filtrar estaciones con baja cobertura para el análisis.

### H14. Estaciones con cobertura parcial en el periodo

- **Archivo(s):** `ideam_temperatura_diaria`
- **Evidencia:** 44 estaciones; días por estación: mín 21, mediana 486, máx 527.
- **Qué haremos en plata:** Filtrar estaciones con baja cobertura para el análisis.

### H15. Trimestre móvil (SEAS) sin fecha: no cruza con datos diarios

- **Archivo(s):** `noaa_oni`
- **Evidencia:** 12 códigos de trimestre en 920 filas; ejemplo última fila: JAS 2026 (ANOM=2.16).
- **Qué haremos en plata:** Convertir SEAS+YR al mes central del trimestre (JAS 2026 -> 2026-08).

### H16. Una fila cubre varios días (vigencias de fin de semana y festivos)

- **Archivo(s):** `trm_diaria`
- **Evidencia:** 158 de 652 filas cubren más de un día.
- **Qué haremos en plata:** Expandir cada vigencia a días calendario (dim_fecha).

### H17. Filas duplicadas exactas

- **Archivo(s):** `xm_listado_recursos`
- **Evidencia:** xm_listado_recursos: 2 filas
- **Qué haremos en plata:** Deduplicar por la llave natural de cada tabla.

### H18. Columnas numéricas guardadas como texto

- **Archivo(s):** `enerandes_ventas_2023, enerandes_ventas_2024, enerandes_ventas_2025, enerandes_ventas_2026, ideam_precipitacion_diaria, ideam_temperatura_diaria, noaa_oni, trm_diaria, xm_aportes_energia, xm_demanda, xm_embalses, xm_precio_bolsa`
- **Evidencia:** 78 columnas numéricas en formato texto en 12 archivos (ej.: enerandes_ventas_2023.col_4)
- **Qué haremos en plata:** Convertir a DOUBLE/INTEGER en plata con validación (TRY_CAST).

### H19. Columnas con 1 % o más de nulos

- **Archivo(s):** `enerandes_ventas_2023, enerandes_ventas_2024, enerandes_ventas_2026`
- **Evidencia:** enerandes_ventas_2023.col_2: 16 nulos (1.4 %); enerandes_ventas_2026.col_5: 11 nulos (1.3 %); enerandes_ventas_2024.col_6: 12 nulos (1.1 %); enerandes_ventas_2026.col_4: 9 nulos (1.1 %)
- **Qué haremos en plata:** Definir regla por columna: imputar, descartar o marcar como dato faltante.
