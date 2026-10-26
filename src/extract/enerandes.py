"""
Fuente 4 - Archivo interno de EnerAndes (Excel con una hoja por año).

Cada hoja tiene encabezados DISTINTOS y algunas traen un título encima.
Regla de bronce: NO se modifica nada. Cada hoja se guarda tal cual, como texto,
incluidas las filas de título y la fila TOTAL. Limpiar es trabajo de la capa plata.
"""
import pandas as pd

from src import config
from src.common.cli import ejecutar_extractor
from src.common.logger import log
from src.common.storage import guardar_bronce, ya_existe


def nombre_bronce(nombre_hoja: str) -> str:
    """'Ventas 2024' -> 'enerandes_ventas_2024'"""
    return "enerandes_" + nombre_hoja.strip().lower().replace(" ", "_")


def extraer(forzar: bool = False) -> None:
    """Lee todas las hojas del Excel de EnerAndes y guarda cada una en bronce."""
    log("EnerAndes - Excel interno")
    archivo = config.ENERANDES_EXCEL
    if not archivo.exists():
        raise FileNotFoundError(f"No se encontró {archivo}. Cópielo en data/insumos/.")

    # sheet_name=None: todas las hojas; header=None: sin encabezado; dtype=str: sin convertir
    hojas = pd.read_excel(archivo, sheet_name=None, header=None, dtype=str)
    for nombre_hoja, df in hojas.items():
        nombre = nombre_bronce(nombre_hoja)
        if ya_existe(nombre, forzar):
            continue
        df.columns = [f"col_{i}" for i in range(df.shape[1])]   # Parquet exige nombres de texto
        guardar_bronce(df, nombre, fuente="EnerAndes", origen=f"{archivo.name}#{nombre_hoja}")


if __name__ == "__main__":
    ejecutar_extractor(extraer, "Extrae el Excel de EnerAndes a bronce")
