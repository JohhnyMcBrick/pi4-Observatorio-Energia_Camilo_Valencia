"""
Fuente 5 (PROPIA) - TRM: Tasa Representativa del Mercado (Banco de la República,
publicada en datos.gov.co, dataset 32sa-8pi3).

¿Para qué? Pregunta propia del equipo: "¿El precio del dólar presiona el precio de
bolsa y el costo de compra de EnerAndes cuando entra generación térmica?".
Las térmicas dependen de combustibles y equipos cotizados en dólares; en un
Niño fuerte el dólar y el embalse bajo pueden empujar el precio en la misma dirección.

Se filtra y ordena en el servidor (SoQL) y se pagina. Como la TRM trae una fila por
periodo de vigencia, el volumen es pequeño y no necesita ventanas.
"""
from datetime import timedelta
from typing import List

import pandas as pd

from src import config
from src.common.cli import ejecutar_extractor
from src.common.http import http_json
from src.common.logger import log
from src.common.storage import guardar_bronce, ya_existe

NOMBRE = "trm_diaria"


def consulta_soql(offset: int) -> dict:
    """Filtra desde unos días antes de FECHA_INICIO (la vigencia empieza antes) hasta FECHA_FIN."""
    campo = config.TRM_CAMPO_FECHA
    desde = config.FECHA_INICIO - timedelta(days=config.TRM_MARGEN_DIAS)
    return {
        "$where": f"{campo} BETWEEN '{desde}T00:00:00' AND '{config.FECHA_FIN}T23:59:59'",
        "$order": campo,
        "$limit": config.TRM_PAGINA,
        "$offset": offset,
    }


def extraer(forzar: bool = False) -> None:
    log("TRM - Banco de la República (fuente propia)")
    if ya_existe(NOMBRE, forzar):
        return
    filas: List[dict] = []
    offset = 0
    while True:
        lote = http_json("GET", config.TRM_URL, params=consulta_soql(offset))
        filas.extend(lote)
        if len(lote) < config.TRM_PAGINA:
            break
        offset += config.TRM_PAGINA
    log(f"   TRM {config.FECHA_INICIO} a {config.FECHA_FIN}: {len(filas):,} filas")
    guardar_bronce(pd.DataFrame(filas), NOMBRE, fuente="Banco de la República (datos.gov.co)",
                   origen=config.TRM_URL)


if __name__ == "__main__":
    ejecutar_extractor(extraer, "Extrae la TRM a bronce")
