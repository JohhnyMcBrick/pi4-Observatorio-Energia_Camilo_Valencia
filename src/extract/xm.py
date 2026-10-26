"""
Fuente 1 - API REST de XM (operador del mercado eléctrico colombiano).

  - Método POST con cuerpo JSON; no requiere usuario ni clave.
  - Máximo ~30 días por consulta -> se pide por VENTANAS.
  - Seis métricas (ver config.XM_METRICAS): precio de bolsa, demanda, embalses,
    generación por planta, aportes hídricos y catálogo de plantas.
  - El catálogo (ListadoRecursos) es distinto: va al endpoint 'lists', no recibe
    fechas y responde con otra estructura (ListEntities).

Documentación: https://github.com/EquipoAnaliticaXM/API_XM
"""
from datetime import date
from typing import List, Optional

import pandas as pd

from src import config
from src.common.cli import ejecutar_extractor
from src.common.descarga import descargar_por_ventanas, limpiar_cache
from src.common.http import http_json
from src.common.logger import log
from src.common.storage import guardar_bronce, ya_existe

# Clave que contiene las entidades según la granularidad de la respuesta
CLAVE_ENTIDADES = {"hourly": "HourlyEntities", "daily": "DailyEntities"}


def aplanar(respuesta: dict, periodo: str) -> List[dict]:
    """
    Convierte el JSON anidado de XM (hourly / daily) en filas planas,
    SIN cambiar los valores.

      hourly -> {"Date", "Id", "Hour01" ... "Hour24"}
      daily  -> {"Date", "Id", "Value"}
    """
    clave = CLAVE_ENTIDADES[periodo]
    filas = []
    for item in respuesta.get("Items", []):
        for entidad in item.get(clave, []):
            fila = {"Date": item.get("Date"), "Id": entidad.get("Id")}
            valores = entidad.get("Values")
            if isinstance(valores, dict):      # hourly: Hour01 ... Hour24
                fila.update(valores)
            if "Value" in entidad:             # daily
                fila["Value"] = entidad["Value"]
            filas.append(fila)
    return filas


def aplanar_lista(respuesta: dict) -> List[dict]:
    """
    Convierte la respuesta del endpoint 'lists' (estructura ListEntities) en filas.

    Cada entidad del catálogo es una fila: su 'Id' más los campos de 'Values'
    (nombre, tipo, fuente de la planta, agente, etc.). Si una entidad no trae
    'Values', se usan sus campos simples directamente.
    """
    filas = []
    for item in respuesta.get("Items", []):
        for entidad in item.get("ListEntities", []):
            fila = {}
            if "Id" in entidad:
                fila["Id"] = entidad["Id"]
            valores = entidad.get("Values")
            if isinstance(valores, dict):
                fila.update(valores)
            else:
                fila.update({k: v for k, v in entidad.items()
                             if k != "Id" and not isinstance(v, (dict, list))})
            filas.append(fila)
    return filas


def cuerpo_consulta(m: config.MetricaXM, inicio: Optional[date] = None, fin: Optional[date] = None) -> dict:
    """Arma el cuerpo JSON del pedido. El endpoint 'lists' NO lleva fechas."""
    cuerpo = {"MetricId": m.metric_id, "Entity": m.entidad}
    if m.periodo != "lists":
        cuerpo.update({"StartDate": str(inicio), "EndDate": str(fin), "Filter": []})
    return cuerpo


def _extraer_serie(m: config.MetricaXM, url: str, forzar: bool) -> pd.DataFrame:
    def pedir(a: date, b: date) -> List[dict]:
        return aplanar(http_json("POST", url, json=cuerpo_consulta(m, a, b)), m.periodo)

    filas = descargar_por_ventanas(m.nombre, config.FECHA_INICIO, config.FECHA_FIN,
                                   m.max_dias, pedir, forzar, etiqueta=m.metric_id)
    return pd.DataFrame(filas)


def _extraer_catalogo(m: config.MetricaXM, url: str) -> pd.DataFrame:
    respuesta = http_json("POST", url, json=cuerpo_consulta(m))
    filas = aplanar_lista(respuesta)
    log(f"   {m.metric_id} (catálogo): {len(filas):,} filas")
    return pd.DataFrame(filas)


def extraer_metrica(m: config.MetricaXM, forzar: bool = False) -> None:
    """Descarga una métrica de XM y la guarda en bronce."""
    if ya_existe(m.nombre, forzar):
        return
    url = config.XM_URL.format(periodo=m.periodo)
    df = _extraer_catalogo(m, url) if m.periodo == "lists" else _extraer_serie(m, url, forzar)
    guardar_bronce(df, m.nombre, fuente="XM", origen=f"{url} MetricId={m.metric_id} Entity={m.entidad}")
    limpiar_cache(m.nombre)


def extraer(forzar: bool = False) -> None:
    """Descarga las métricas definidas en config.XM_METRICAS."""
    log("XM - API REST del mercado eléctrico")
    for metrica in config.XM_METRICAS:
        extraer_metrica(metrica, forzar)


if __name__ == "__main__":
    ejecutar_extractor(extraer, "Extrae las métricas de XM a bronce")
