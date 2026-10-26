"""
Punto de entrada único del pipeline de extracción (capa BRONCE).

Uso:
    python -m src.pipeline                    # descarga lo que falte
    python -m src.pipeline --forzar           # vuelve a descargar todo
    python -m src.pipeline --solo xm trm      # solo algunas fuentes
    python -m src.pipeline --perfilar         # además genera docs/perfilamiento.md

Si una fuente falla, las demás continúan; al final se informa cuáles fallaron
y el programa termina con código de error (útil para GitHub Actions).
"""
import argparse
import sys
import time
from typing import Dict, List, Optional

import pandas as pd

from src import config
from src.common.logger import log
from src.extract import enerandes, ideam, noaa, trm, xm
from src.muestras import generar_muestras

# Orden de ejecución: de la fuente más pesada a la más liviana
EXTRACTORES = {
    "xm": xm,
    "ideam": ideam,
    "noaa": noaa,
    "enerandes": enerandes,
    "trm": trm,
}


def ejecutar(fuentes: List[str], forzar: bool) -> Dict[str, Optional[str]]:
    """Corre los extractores pedidos. Devuelve {fuente: None si salió bien, o el error}."""
    resultados: Dict[str, Optional[str]] = {}
    for fuente in fuentes:
        try:
            EXTRACTORES[fuente].extraer(forzar)
            resultados[fuente] = None
        except Exception as error:      # una fuente caída no debe tumbar a las demás
            log(f"   X {fuente} falló: {error}")
            resultados[fuente] = str(error)
    return resultados


def resumen() -> None:
    """Tabla con los archivos de la capa bronce."""
    log("Resumen de la capa bronce:")
    print(f"   {'archivo':<34}{'filas':>10}{'columnas':>10}{'KB':>8}")
    for archivo in sorted(config.DIR_BRONZE.glob("*.parquet")):
        df = pd.read_parquet(archivo)
        print(f"   {archivo.name:<34}{len(df):>10,}{df.shape[1]:>10}{archivo.stat().st_size // 1024:>8}")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Pipeline de extracción (capa bronce)")
    parser.add_argument("--forzar", action="store_true", help="volver a descargar todo")
    parser.add_argument("--solo", nargs="+", choices=list(EXTRACTORES), metavar="FUENTE",
                        help=f"solo estas fuentes ({', '.join(EXTRACTORES)})")
    parser.add_argument("--sin-muestras", action="store_true", help="no generar data/sample/")
    parser.add_argument("--perfilar", action="store_true", help="generar docs/perfilamiento.md")
    args = parser.parse_args(argv)

    fuentes = args.solo or list(EXTRACTORES)
    inicio = time.time()
    log(f"Pipeline bronce | XM {config.FECHA_INICIO} a {config.FECHA_FIN} | "
        f"IDEAM desde {config.IDEAM_FECHA_INICIO} | forzar={args.forzar}")

    resultados = ejecutar(fuentes, args.forzar)
    resumen()
    if not args.sin_muestras:
        generar_muestras()
    if args.perfilar:
        from src.perfilar import generar_perfilamiento
        generar_perfilamiento()

    fallidas = {f: e for f, e in resultados.items() if e}
    log(f"Listo en {time.time() - inicio:.0f} s | fuentes OK: {len(resultados) - len(fallidas)}/{len(resultados)}")
    for fuente, error in fallidas.items():
        log(f"   FALLÓ {fuente}: {error}")
    return 1 if fallidas else 0


if __name__ == "__main__":
    sys.exit(main())
