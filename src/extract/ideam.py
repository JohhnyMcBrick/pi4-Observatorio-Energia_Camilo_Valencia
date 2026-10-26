"""
Fuente 2 - IDEAM en datos.gov.co (plataforma Socrata, lenguaje SoQL).

  - Los datasets tienen MILLONES de observaciones (una cada pocos minutos desde 2005).
  - Por eso FILTRAMOS ($where) y AGREGAMOS ($select + $group) EN EL SERVIDOR:
    viaja un resumen diario por estación, nunca millones de filas.
  - Se pide por ventanas de 7 días y se pagina con $limit / $offset.
  - Dos datasets con el mismo código: precipitación (suma) y temperatura (media/mín/máx).

Documentación SoQL: https://dev.socrata.com/docs/queries/
"""
from datetime import date
from typing import List

import pandas as pd

from src import config
from src.common.cli import ejecutar_extractor
from src.common.descarga import descargar_por_ventanas, limpiar_cache
from src.common.http import http_json
from src.common.logger import log
from src.common.storage import guardar_bronce, ya_existe


def consulta_soql(dataset: config.DatasetIdeam, inicio: date, fin: date, offset: int) -> dict:
    """Parámetros SoQL: filtrar departamento y fechas, y agregar por día y estación."""
    campos = config.IDEAM_CAMPOS_ESTACION
    return {
        "$select": f"{campos}, date_trunc_ymd(fechaobservacion) AS fecha, {dataset.agregados}",
        "$where": (f"departamento = '{config.IDEAM_DEPARTAMENTO}' AND "
                   f"fechaobservacion BETWEEN '{inicio}T00:00:00' AND '{fin}T23:59:59'"),
        "$group": f"{campos}, fecha",
        "$order": "fecha, codigoestacion",
        "$limit": config.IDEAM_PAGINA,
        "$offset": offset,
    }


def pedir_ventana(dataset: config.DatasetIdeam, inicio: date, fin: date) -> List[dict]:
    """Todas las filas de una ventana, recorriendo las páginas necesarias."""
    filas: List[dict] = []
    offset = 0
    while True:
        lote = http_json("GET", dataset.url, params=consulta_soql(dataset, inicio, fin, offset))
        filas.extend(lote)
        if len(lote) < config.IDEAM_PAGINA:     # menos filas que el límite: era la última página
            return filas
        offset += config.IDEAM_PAGINA


def extraer_dataset(dataset: config.DatasetIdeam, forzar: bool = False) -> None:
    """Descarga un dataset del IDEAM, ventana por ventana, y lo guarda en bronce."""
    log(f"IDEAM - {dataset.descripcion}")
    if ya_existe(dataset.nombre, forzar):
        return
    filas = descargar_por_ventanas(
        dataset.nombre, config.IDEAM_FECHA_INICIO, config.FECHA_FIN, config.IDEAM_DIAS_VENTANA,
        lambda a, b: pedir_ventana(dataset, a, b), forzar, etiqueta="semana")
    guardar_bronce(pd.DataFrame(filas), dataset.nombre, fuente="IDEAM", origen=dataset.url)
    limpiar_cache(dataset.nombre)


def extraer(forzar: bool = False) -> None:
    for dataset in config.IDEAM_DATASETS:
        extraer_dataset(dataset, forzar)


if __name__ == "__main__":
    ejecutar_extractor(extraer, "Extrae precipitación y temperatura del IDEAM a bronce")
