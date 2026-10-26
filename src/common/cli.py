"""Punto de entrada común para ejecutar un extractor suelto: python -m src.extract.<fuente>"""
import argparse
from typing import Callable


def ejecutar_extractor(extraer: Callable[[bool], None], descripcion: str = "") -> None:
    parser = argparse.ArgumentParser(description=descripcion)
    parser.add_argument("--forzar", action="store_true", help="volver a descargar aunque ya exista")
    extraer(parser.parse_args().forzar)
