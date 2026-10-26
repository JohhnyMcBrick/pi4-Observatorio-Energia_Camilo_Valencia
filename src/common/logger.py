"""Mensajes en pantalla con la hora."""
from datetime import datetime


def log(mensaje: str) -> None:
    """Escribe un mensaje con la hora delante: [21:30:32] mensaje."""
    print(f"[{datetime.now():%H:%M:%S}] {mensaje}", flush=True)
