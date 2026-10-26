"""
Almacenamiento de la capa BRONCE.

  - ruta_bronce():    ruta data/bronze/<nombre>.parquet
  - ya_existe():      idempotencia (no volver a descargar lo que ya está)
  - guardar_bronce(): guarda en Parquet agregando columnas de LINAJE
"""
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pyarrow as pa

from src import config
from src.common.logger import log

COLUMNAS_LINAJE = ("_fuente", "_origen", "_extraido_en")


def ruta_bronce(nombre: str) -> Path:
    return config.DIR_BRONZE / f"{nombre}.parquet"


def ya_existe(nombre: str, forzar: bool) -> bool:
    """Si el archivo ya está y no se pide forzar, no se descarga de nuevo."""
    if ruta_bronce(nombre).exists() and not forzar:
        log(f"   = {nombre}.parquet ya existe; se omite (use --forzar para repetir)")
        return True
    return False


def _homogeneizar(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parquet exige un solo tipo por columna. Si una columna mezcla tipos
    (p. ej. números y textos), se pasa a texto SIN alterar los valores.
    """
    for columna in df.columns:
        if df[columna].dtype != object:
            continue
        try:
            pa.array(df[columna])
        except (pa.ArrowInvalid, pa.ArrowTypeError):
            df[columna] = df[columna].map(lambda v: v if v is None or pd.isna(v) else str(v))
    return df


def guardar_bronce(df: pd.DataFrame, nombre: str, fuente: str, origen: str) -> None:
    """Guarda TAL CUAL llegó + 3 columnas de linaje. En bronce no se limpia nada."""
    df = df.copy()
    df["_fuente"] = fuente
    df["_origen"] = origen
    df["_extraido_en"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    config.DIR_BRONZE.mkdir(parents=True, exist_ok=True)
    _homogeneizar(df).to_parquet(ruta_bronce(nombre), index=False)
    log(f"   + {nombre}.parquet guardado: {len(df):,} filas x {df.shape[1]} columnas")
