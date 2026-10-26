"""
Descarga por ventanas de fechas con CACHE REANUDABLE.

Las fuentes lentas (IDEAM: ~90 ventanas por dataset; XM: ~30 por métrica) pueden
tardar mucho. Cada ventana descargada se guarda en data/bronze/_cache/<nombre>/;
si el proceso se interrumpe, al volver a correr solo se piden las ventanas que
faltan. Al terminar bien, el cache se borra (el resultado queda en el Parquet).
"""
import json
import shutil
from datetime import date
from pathlib import Path
from typing import Callable, List

from src import config
from src.common.fechas import ventanas
from src.common.logger import log


def dir_cache(nombre: str) -> Path:
    return config.DIR_BRONZE / "_cache" / nombre


def limpiar_cache(nombre: str) -> None:
    shutil.rmtree(dir_cache(nombre), ignore_errors=True)


def descargar_por_ventanas(
    nombre: str,
    inicio: date,
    fin: date,
    dias: int,
    pedir: Callable[[date, date], List[dict]],
    forzar: bool = False,
    etiqueta: str = "",
) -> List[dict]:
    """
    Recorre las ventanas de [inicio, fin] y junta las filas.

    pedir(a, b) debe devolver la lista de filas (dicts) de la ventana [a, b].
    """
    carpeta = dir_cache(nombre)
    if forzar:
        limpiar_cache(nombre)
    carpeta.mkdir(parents=True, exist_ok=True)

    filas: List[dict] = []
    for a, b in ventanas(inicio, fin, dias):
        archivo = carpeta / f"{a}_{b}.json"
        if archivo.exists():
            lote = json.loads(archivo.read_text(encoding="utf-8"))
            estado = "(cache)"
        else:
            lote = pedir(a, b)
            archivo.write_text(json.dumps(lote), encoding="utf-8")
            estado = ""
        filas.extend(lote)
        log(f"   {etiqueta or nombre} {a} a {b}: {len(lote):,} filas {estado}".rstrip())
    return filas
