"""
Genera data/sample/: las primeras N filas (200) de cada archivo de bronce, en CSV.
Los datos completos de bronce NO se suben a GitHub; la muestra sí.

Uso:
    python -m src.muestras
"""
from pathlib import Path
from typing import List

import pandas as pd

from src import config
from src.common.logger import log


def generar_muestras(filas: int = None) -> List[Path]:
    filas = filas or config.MUESTRA_FILAS
    config.DIR_SAMPLE.mkdir(parents=True, exist_ok=True)
    creados = []
    for archivo in sorted(config.DIR_BRONZE.glob("*.parquet")):
        destino = config.DIR_SAMPLE / f"{archivo.stem}.csv"
        pd.read_parquet(archivo).head(filas).to_csv(destino, index=False, encoding="utf-8")
        creados.append(destino)
    log(f"Muestras: {len(creados)} archivos CSV de {filas} filas en {config.DIR_SAMPLE}")
    return creados


if __name__ == "__main__":
    generar_muestras()
