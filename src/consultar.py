"""
Ejecuta las consultas SQL de la carpeta consultas/ con DuckDB, directo sobre Parquet.

Uso:
    python -m src.consultar
"""
import os

import duckdb

from src import config
from src.common.logger import log


def main() -> None:
    os.chdir(config.RAIZ)                   # las rutas de los .sql son relativas a la raíz
    con = duckdb.connect()                  # base en memoria: no crea archivos
    for archivo in sorted((config.RAIZ / "consultas").glob("*.sql")):
        log(f"Consulta: {archivo.name}")
        print(con.sql(archivo.read_text(encoding="utf-8")).df().to_string(index=False))
        print()


if __name__ == "__main__":
    main()
