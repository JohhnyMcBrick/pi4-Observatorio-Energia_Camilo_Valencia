"""
Fuente 3 - NOAA: índice ONI de El Niño (archivo de texto separado por espacios).

  Columnas: SEAS (trimestre móvil, ej. JAS), YR (año), TOTAL (temp. del mar), ANOM (anomalía)
  ANOM >= +0.5 -> El Niño     ANOM <= -0.5 -> La Niña
"""
import io

import pandas as pd

from src import config
from src.common.cli import ejecutar_extractor
from src.common.http import http_texto
from src.common.logger import log
from src.common.storage import guardar_bronce, ya_existe

NOMBRE = "noaa_oni"


def parsear(texto: str) -> pd.DataFrame:
    """Texto del archivo -> tabla. Todo como texto: en bronce no se convierten tipos."""
    return pd.read_csv(io.StringIO(texto), sep=r"\s+", dtype=str)


def extraer(forzar: bool = False) -> None:
    log("NOAA - índice ONI (El Niño)")
    if ya_existe(NOMBRE, forzar):
        return
    df = parsear(http_texto(config.NOAA_ONI_URL))
    guardar_bronce(df, NOMBRE, fuente="NOAA", origen=config.NOAA_ONI_URL)


if __name__ == "__main__":
    ejecutar_extractor(extraer, "Extrae el índice ONI de NOAA a bronce")
