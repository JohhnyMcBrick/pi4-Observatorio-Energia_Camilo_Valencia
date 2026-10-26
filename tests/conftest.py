"""
Fixtures de las pruebas. NINGUNA prueba usa internet: las respuestas de XM, IDEAM,
NOAA y TRM se simulan, y los archivos se escriben en carpetas temporales.
"""
from datetime import date, timedelta

import pandas as pd
import pytest

from src import config

TEXTO_ONI = """SEAS  YR  TOTAL  ANOM
 DJF 2025  26.0  -0.5
 JAS 2026  28.9   2.16
"""


@pytest.fixture
def carpetas(tmp_path, monkeypatch):
    """Redirige bronce, muestras, docs e insumos a una carpeta temporal."""
    monkeypatch.setattr(config, "DIR_BRONZE", tmp_path / "bronze")
    monkeypatch.setattr(config, "DIR_SAMPLE", tmp_path / "sample")
    monkeypatch.setattr(config, "DIR_DOCS", tmp_path / "docs")
    monkeypatch.setattr(config, "DIR_INSUMOS", tmp_path / "insumos")
    return tmp_path


@pytest.fixture
def rango_corto(monkeypatch):
    """Rango pequeño (45 días) para que las pruebas sean rápidas."""
    monkeypatch.setattr(config, "FECHA_INICIO", date(2026, 1, 1))
    monkeypatch.setattr(config, "FECHA_FIN", date(2026, 2, 14))
    monkeypatch.setattr(config, "IDEAM_FECHA_INICIO", date(2026, 1, 1))


@pytest.fixture
def excel_enerandes(carpetas, monkeypatch):
    """Excel mínimo con dos hojas de estilos distintos (una con título encima)."""
    ruta = carpetas / "insumos" / "ventas_mini.xlsx"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    h1 = pd.DataFrame([["Fecha", "Municipio", "Segmento", "Tipo_Compra", "Energia_kWh", "Valor_COP", "Clientes"],
                       ["2023-01", "Medellin", "Comercial", "Bolsa", "100", "90", "2"],
                       ["2023-01", "Medellin", "Comercial", "Bolsa", "100", "90", "2"],
                       ["TOTAL"] + [None] * 6])
    h2 = pd.DataFrame([["Reporte 2025"] + [None] * 6, [None] * 7,
                       ["mes", "municipio", "segmento", "tipo compra", "consumo (kWh)", "facturado", "usuarios"],
                       ["01/2025", "Bello", "Industrial", "Contrato", "50", "45", "1"],
                       ["TOTAL"] + [None] * 6])
    with pd.ExcelWriter(ruta) as w:
        h1.to_excel(w, sheet_name="Ventas 2023", header=False, index=False)
        h2.to_excel(w, sheet_name="Ventas 2025", header=False, index=False)
    monkeypatch.setattr(config, "ENERANDES_EXCEL", ruta)
    return ruta


def _dias(a, b):
    d = a
    while d <= b:
        yield d
        d += timedelta(days=1)


def falso_xm(metodo, url, **kwargs):
    """Imita a la API de XM: hourly, daily y lists."""
    cuerpo = kwargs["json"]
    if url.endswith("/lists"):
        assert "StartDate" not in cuerpo, "el endpoint lists no recibe fechas"
        return {"Items": [{"ListEntities": [
            {"Id": "ABC1", "Values": {"Name": "PLANTA A", "Type": "HIDRAULICA"}},
            {"Id": "XYZ2", "Values": {"Name": "PLANTA B", "Type": "TERMICA"}}]}]}
    a = date.fromisoformat(cuerpo["StartDate"])
    b = date.fromisoformat(cuerpo["EndDate"])
    assert (b - a).days + 1 <= 30, "XM no acepta más de 30 días"
    items = []
    for d in _dias(a, b):
        if url.endswith("/hourly"):
            ids = ["PLANTA1", "PLANTA2"] if cuerpo["Entity"] == "Recurso" else ["Sistema"]
            ents = [{"Id": i, "Values": {f"Hour{h:02d}": str(100 + h) for h in range(1, 25)}} for i in ids]
            items.append({"Date": str(d), "HourlyEntities": ents})
        else:
            items.append({"Date": str(d), "DailyEntities": [{"Id": "Sistema", "Value": "0.55"}]})
    return {"Items": items}


def falso_socrata(metodo, url, **kwargs):
    """Imita a datos.gov.co (IDEAM y TRM)."""
    p = kwargs["params"]
    if "32sa-8pi3" in url:
        assert "$select" not in p
        return [{"valor": "4000.5", "unidad": "COP", "vigenciadesde": "2026-01-02T00:00:00.000",
                 "vigenciahasta": "2026-01-04T00:00:00.000"},
                {"valor": "4010.0", "unidad": "COP", "vigenciadesde": "2026-01-05T00:00:00.000",
                 "vigenciahasta": "2026-01-05T00:00:00.000"}]
    assert "$group" in p and "$where" in p, "la agregación y el filtro deben ir en el servidor"
    if p["$offset"]:
        return []
    ini = date.fromisoformat(p["$where"].split("BETWEEN '")[1][:10])
    fin = date.fromisoformat(p["$where"].split("AND '")[1][:10])
    es_temp = "avg(" in p["$select"]
    filas = []
    for d in _dias(ini, fin):
        for est in ("1001", "1002"):
            fila = {"codigoestacion": est, "nombreestacion": f"EST {est}", "municipio": "BELLO",
                    "fecha": f"{d}T00:00:00.000", "n_obs": "144"}
            if es_temp:
                fila.update({"temp_media_c": "22.5", "temp_min_c": "17.0", "temp_max_c": "29.1"})
            else:
                fila.update({"precipitacion_mm": "3.2"})
            filas.append(fila)
    return filas


@pytest.fixture
def red_falsa(monkeypatch):
    """Reemplaza TODAS las llamadas de red de los extractores por respuestas simuladas."""
    from src.extract import ideam, noaa, trm, xm
    monkeypatch.setattr(xm, "http_json", falso_xm)
    monkeypatch.setattr(ideam, "http_json", falso_socrata)
    monkeypatch.setattr(trm, "http_json", falso_socrata)
    monkeypatch.setattr(noaa, "http_texto", lambda url: TEXTO_ONI)
