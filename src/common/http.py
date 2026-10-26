"""
Peticiones HTTP con reintentos y espera exponencial.

Solo se reintenta lo que tiene sentido reintentar: fallas de red, 5xx y 429.
Un 4xx (por ejemplo 400 por una consulta mal armada) falla de inmediato,
porque repetirlo no lo va a arreglar y solo hace perder tiempo.
"""
import time
from typing import Callable

import requests

from src import config
from src.common.logger import log


def _es_reintentable(error: requests.RequestException) -> bool:
    respuesta = getattr(error, "response", None)
    if isinstance(error, requests.HTTPError) and respuesta is not None:
        return respuesta.status_code >= 500 or respuesta.status_code == 429
    return True     # timeouts, conexión caída, JSON truncado, etc.


def con_reintentos(funcion: Callable, descripcion: str):
    """Ejecuta funcion(); si falla de forma reintentable espera 2, 4, 8... s y reintenta."""
    for intento in range(1, config.HTTP_REINTENTOS + 1):
        try:
            return funcion()
        except requests.RequestException as error:
            ultimo = intento == config.HTTP_REINTENTOS
            if ultimo or not _es_reintentable(error):
                raise RuntimeError(f"Fallo definitivo en {descripcion}: {error}") from error
            espera = 2 ** intento
            log(f"   ! intento {intento} falló ({type(error).__name__}); reintento en {espera} s")
            time.sleep(espera)


def http_json(metodo: str, url: str, **kwargs):
    """GET o POST que devuelve JSON (dict o list), con reintentos."""
    def llamar():
        r = requests.request(metodo, url, timeout=config.HTTP_TIMEOUT, **kwargs)
        r.raise_for_status()
        return r.json()
    return con_reintentos(llamar, f"{metodo} {url}")


def http_texto(url: str) -> str:
    """GET que devuelve texto plano, con reintentos."""
    def llamar():
        r = requests.get(url, timeout=config.HTTP_TIMEOUT)
        r.raise_for_status()
        return r.text
    return con_reintentos(llamar, f"GET {url}")
