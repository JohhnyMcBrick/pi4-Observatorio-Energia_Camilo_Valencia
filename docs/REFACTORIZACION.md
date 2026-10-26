# Qué se refactorizó respecto al código base de la clase (19 de octubre)

El código de la clase funcionaba, pero tenía tres límites: una sola ruta de datos con valores fijos, un
`utils.py` que mezclaba responsabilidades y un pipeline que se detenía en el primer error. Esta versión
mantiene la idea (bronce = dato tal cual + linaje, idempotencia, SoQL en el servidor) y la ordena.

| Antes (clase) | Ahora | Por qué |
|---|---|---|
| `utils.py` único (log, HTTP, fechas, Parquet) | Paquete `src/common/`: `logger`, `http`, `fechas`, `storage`, `descarga`, `cli` | Una responsabilidad por módulo; cada pieza se prueba sola |
| `XM_METRICAS` como lista de tuplas | `MetricaXM` (dataclass inmutable) con `max_dias` propio | Agregar una métrica es una línea y no hay que recordar el orden de la tupla |
| XM solo `hourly`/`daily` | + `Gene` por `Recurso`, `AporEner` y **`ListadoRecursos`** en el endpoint `lists` (sin fechas, estructura `ListEntities`) | Requisito EA1: 6 métricas |
| `aplanar` asumía siempre `Id` y `Values` | `aplanar` y `aplanar_lista` tolerantes (`.get`, `Value`/`Values`) | Las respuestas de XM no son idénticas entre métricas |
| IDEAM: un dataset, código fijo | `DatasetIdeam` (dataclass) + `extraer_dataset()` genérico: precipitación **y temperatura** | El mismo SoQL (filtro + agregación en el servidor) sirve para ambos; solo cambian las agregaciones |
| IDEAM registraba `len(lote)` de la última página | El log cuenta las filas de **toda** la ventana | Bug del código base: con paginación el conteo era engañoso |
| Reintentaba cualquier error, incluido un 400 | Solo reintenta red, 5xx y 429; un 4xx falla de una vez | Repetir una consulta mal armada no la arregla y hace perder minutos |
| Si el IDEAM se caía a la mitad, se perdía todo | **Cache por ventana** reanudable en `data/bronze/_cache/` | El IDEAM tarda 30–90 min; no se repite lo ya descargado |
| Pipeline se detenía en la primera falla | Cada fuente en `try/except`; resumen final y código de salida 1 | Una API caída no tumba las otras 4 fuentes; sirve para GitHub Actions |
| `sys.argv` a mano | `argparse`: `--forzar`, `--solo`, `--perfilar`, `--sin-muestras` | Opciones documentadas con `--help` |
| Sin muestras ni perfilamiento | `src/muestras.py` (200 filas en CSV) y `src/perfilar.py` (tablas + hallazgos) | Requisitos EA1 |
| Sin pruebas | 36 pruebas con `pytest`, sin internet | Requisito EA1 y red de seguridad para EA2 |
| Parquet fallaba con columnas de tipos mezclados | `_homogeneizar()` pasa a texto sin alterar valores | Un valor numérico suelto entre textos no debe tumbar la escritura |
| 4 fuentes | + **TRM** (fuente propia, `src/extract/trm.py`) | Requisito EA1 |

## Reglas que se conservaron a propósito
1. **Bronce no limpia nada**: Excel como texto con títulos y fila TOTAL incluidos; NOAA como texto.
2. **Linaje** en cada archivo: `_fuente`, `_origen`, `_extraido_en`.
3. **Idempotencia**: si el Parquet existe, se omite (salvo `--forzar`).
4. **Configuración central** en `src/config.py`: fechas, URLs y métricas no se riegan por el código.
