"""Utilidades de fechas."""
from datetime import date, timedelta
from typing import Iterator, Tuple


def ventanas(inicio: date, fin: date, dias: int) -> Iterator[Tuple[date, date]]:
    """
    Parte el rango [inicio, fin] (ambos inclusive) en bloques de 'dias' días.

    Los bloques no se solapan, no dejan huecos y el último se recorta en 'fin'.
    Con inicio > fin no entrega nada.
    """
    if dias < 1:
        raise ValueError("'dias' debe ser >= 1")
    a = inicio
    while a <= fin:
        b = min(a + timedelta(days=dias - 1), fin)
        yield a, b
        a = b + timedelta(days=1)
