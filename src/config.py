"""
Configuración central del pipeline (capa BRONCE).

Todo lo que puede cambiar (fechas, URLs, rutas, métricas, datasets) vive AQUÍ.
Si hay que cambiar una fecha, una URL o agregar una métrica, se hace en este
archivo y en ningún otro.
"""
from dataclasses import dataclass
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# Rango de fechas (EA1: mínimo 2 años de XM desde 2024-01-01)
# ---------------------------------------------------------------------------
FECHA_INICIO = date(2024, 1, 1)
FECHA_FIN = date(2026, 9, 30)

# ---------------------------------------------------------------------------
# Rutas (relativas a la raíz del proyecto)
# ---------------------------------------------------------------------------
RAIZ = Path(__file__).resolve().parent.parent
DIR_INSUMOS = RAIZ / "data" / "insumos"
DIR_BRONZE = RAIZ / "data" / "bronze"
DIR_SAMPLE = RAIZ / "data" / "sample"
DIR_DOCS = RAIZ / "docs"

# ---------------------------------------------------------------------------
# Comportamiento HTTP
# ---------------------------------------------------------------------------
HTTP_TIMEOUT = 120       # segundos de espera por respuesta
HTTP_REINTENTOS = 4      # intentos ante fallas de red o del servidor (5xx / 429)
MUESTRA_FILAS = 200      # filas de cada archivo de bronce que van a data/sample/


# ---------------------------------------------------------------------------
# Fuente 1: API REST de XM
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class MetricaXM:
    """Una métrica de XM a descargar."""
    metric_id: str          # MetricId de la API
    entidad: str            # Sistema | Recurso
    periodo: str            # hourly | daily | lists
    nombre: str             # nombre del archivo en bronce (sin .parquet)
    max_dias: int = 30      # la API no acepta rangos más largos (se ignora en 'lists')


XM_URL = "https://servapibi.xm.com.co/{periodo}"

XM_METRICAS = (
    MetricaXM("PrecBolsNaci", "Sistema", "hourly", "xm_precio_bolsa"),
    MetricaXM("DemaReal", "Sistema", "hourly", "xm_demanda"),
    MetricaXM("PorcVoluUtilDiar", "Sistema", "daily", "xm_embalses"),
    # --- ampliación EA1 ---
    MetricaXM("Gene", "Recurso", "hourly", "xm_generacion_recurso"),   # generación por planta
    MetricaXM("AporEner", "Sistema", "daily", "xm_aportes_energia"),   # aportes hídricos
    # Catálogo de plantas: endpoint 'lists', sin fechas, respuesta con ListEntities
    MetricaXM("ListadoRecursos", "Sistema", "lists", "xm_listado_recursos"),
)


# ---------------------------------------------------------------------------
# Fuente 2: IDEAM en datos.gov.co (API Socrata, filtrado y agregación con SoQL)
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class DatasetIdeam:
    """Un dataset del IDEAM que se agrega por día y estación EN EL SERVIDOR."""
    nombre: str             # nombre del archivo en bronce
    url: str                # endpoint .json del dataset
    agregados: str          # expresiones SoQL de agregación ($select)
    descripcion: str


IDEAM_DEPARTAMENTO = "ANTIOQUIA"
IDEAM_CAMPOS_ESTACION = "codigoestacion, nombreestacion, municipio, zonahidrografica, latitud, longitud"
IDEAM_DIAS_VENTANA = 7          # pedir de a una semana evita timeouts del servidor
IDEAM_PAGINA = 50000            # filas máximas por pedido ($limit)
# EA1: mínimo 1 año desde el 1 de enero de 2025.
# El IDEAM es la fuente MÁS LENTA (5 a 30 s por semana y por dataset).
IDEAM_FECHA_INICIO = date(2025, 1, 1)

IDEAM_DATASETS = (
    DatasetIdeam(
        nombre="ideam_precipitacion_diaria",
        url="https://www.datos.gov.co/resource/s54a-sgyg.json",
        agregados="sum(valorobservado) AS precipitacion_mm, count(*) AS n_obs",
        descripcion="Precipitación diaria por estación (suma de las observaciones)",
    ),
    DatasetIdeam(
        nombre="ideam_temperatura_diaria",
        url="https://www.datos.gov.co/resource/sbwg-7ju4.json",
        agregados=("avg(valorobservado) AS temp_media_c, min(valorobservado) AS temp_min_c, "
                   "max(valorobservado) AS temp_max_c, count(*) AS n_obs"),
        descripcion="Temperatura del aire diaria por estación (media, mínima y máxima)",
    ),
)


# ---------------------------------------------------------------------------
# Fuente 3: NOAA, índice ONI (archivo de texto)
# ---------------------------------------------------------------------------
NOAA_ONI_URL = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"


# ---------------------------------------------------------------------------
# Fuente 4: archivo interno de EnerAndes (Excel)
# ---------------------------------------------------------------------------
ENERANDES_EXCEL = DIR_INSUMOS / "ventas_enerandes_2023_2026.xlsx"


# ---------------------------------------------------------------------------
# Fuente 5 (PROPIA): TRM, Banco de la República vía datos.gov.co
# ---------------------------------------------------------------------------
TRM_URL = "https://www.datos.gov.co/resource/32sa-8pi3.json"
TRM_CAMPO_FECHA = "vigenciadesde"   # columna por la que se filtra y ordena
TRM_PAGINA = 50000
TRM_MARGEN_DIAS = 7                 # días previos al inicio: la vigencia de una TRM empieza antes
