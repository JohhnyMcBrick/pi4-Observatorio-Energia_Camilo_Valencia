from datetime import date

import pandas as pd

from src import config
from src.extract import enerandes, ideam, noaa, trm
from tests.conftest import TEXTO_ONI


def _dataset(nombre):
    return next(d for d in config.IDEAM_DATASETS if d.nombre == nombre)


def test_ideam_filtra_y_agrega_en_el_servidor_la_precipitacion():
    p = ideam.consulta_soql(_dataset("ideam_precipitacion_diaria"), date(2026, 1, 1), date(2026, 1, 7), 0)
    assert "sum(valorobservado)" in p["$select"]
    assert "ANTIOQUIA" in p["$where"] and "2026-01-01T00:00:00" in p["$where"]
    assert p["$group"] and p["$limit"] == config.IDEAM_PAGINA and p["$offset"] == 0


def test_ideam_temperatura_pide_media_minima_y_maxima_por_dia_y_estacion():
    p = ideam.consulta_soql(_dataset("ideam_temperatura_diaria"), date(2026, 1, 1), date(2026, 1, 7), 0)
    for expr in ("avg(valorobservado)", "min(valorobservado)", "max(valorobservado)"):
        assert expr in p["$select"]
    assert "codigoestacion" in p["$group"] and "fecha" in p["$group"]


def test_ideam_config_cubre_un_anio_desde_2025_y_usa_el_dataset_de_temperatura():
    assert config.IDEAM_FECHA_INICIO == date(2025, 1, 1)
    assert (config.FECHA_FIN - config.IDEAM_FECHA_INICIO).days >= 365
    assert any(d.url.endswith("sbwg-7ju4.json") for d in config.IDEAM_DATASETS)


def test_ideam_pagina_hasta_recibir_menos_filas_que_el_limite(monkeypatch):
    monkeypatch.setattr(config, "IDEAM_PAGINA", 2)
    paginas = {0: [{"a": 1}, {"a": 2}], 2: [{"a": 3}]}
    monkeypatch.setattr(ideam, "http_json", lambda m, u, **kw: paginas[kw["params"]["$offset"]])
    filas = ideam.pedir_ventana(_dataset("ideam_precipitacion_diaria"), date(2026, 1, 1), date(2026, 1, 7))
    assert [f["a"] for f in filas] == [1, 2, 3]


def test_ideam_extrae_los_dos_datasets(carpetas, rango_corto, red_falsa):
    ideam.extraer()
    lluvia = pd.read_parquet(config.DIR_BRONZE / "ideam_precipitacion_diaria.parquet")
    temp = pd.read_parquet(config.DIR_BRONZE / "ideam_temperatura_diaria.parquet")
    assert len(lluvia) == 45 * 2 and "precipitacion_mm" in lluvia
    assert {"temp_media_c", "temp_min_c", "temp_max_c"} <= set(temp.columns)


def test_ideam_reanuda_desde_el_cache_si_se_interrumpe(carpetas, rango_corto, monkeypatch):
    from tests.conftest import falso_socrata
    llamadas = []

    def inestable(m, u, **kw):
        llamadas.append(kw["params"]["$where"])
        if len(llamadas) == 3:
            raise RuntimeError("se cayó el servidor")
        return falso_socrata(m, u, **kw)

    monkeypatch.setattr(ideam, "http_json", inestable)
    ds = _dataset("ideam_precipitacion_diaria")
    try:
        ideam.extraer_dataset(ds)
    except RuntimeError:
        pass
    assert not (config.DIR_BRONZE / f"{ds.nombre}.parquet").exists()
    monkeypatch.setattr(ideam, "http_json", falso_socrata)
    antes = len(llamadas)
    ideam.extraer_dataset(ds)
    assert (config.DIR_BRONZE / f"{ds.nombre}.parquet").exists()
    assert len(llamadas) == antes                               # las 2 primeras ventanas salieron del cache


def test_trm_filtra_en_el_servidor_con_margen_previo():
    p = trm.consulta_soql(0)
    assert p["$where"].startswith(f"{config.TRM_CAMPO_FECHA} BETWEEN '2023-12-25T00:00:00'")
    assert p["$order"] == config.TRM_CAMPO_FECHA


def test_trm_extrae_y_guarda_con_linaje(carpetas, rango_corto, red_falsa):
    trm.extraer()
    df = pd.read_parquet(config.DIR_BRONZE / "trm_diaria.parquet")
    assert len(df) == 2 and df["_origen"].iloc[0] == config.TRM_URL


def test_noaa_parsea_el_texto_como_texto_sin_convertir_tipos():
    df = noaa.parsear(TEXTO_ONI)
    assert list(df.columns) == ["SEAS", "YR", "TOTAL", "ANOM"]
    assert df["ANOM"].tolist() == ["-0.5", "2.16"]


def test_enerandes_guarda_cada_hoja_tal_cual_incluidas_filas_de_titulo_y_total(carpetas, excel_enerandes):
    enerandes.extraer()
    h25 = pd.read_parquet(config.DIR_BRONZE / "enerandes_ventas_2025.parquet")
    assert h25["col_0"].iloc[0] == "Reporte 2025"               # el título NO se quita en bronce
    assert (h25["col_0"] == "TOTAL").sum() == 1                  # la fila TOTAL tampoco
    h23 = pd.read_parquet(config.DIR_BRONZE / "enerandes_ventas_2023.parquet")
    assert len(h23) == 4 and h23["_fuente"].iloc[0] == "EnerAndes"


def test_enerandes_sin_el_excel_da_un_error_claro(carpetas, monkeypatch):
    import pytest
    monkeypatch.setattr(config, "ENERANDES_EXCEL", carpetas / "no_existe.xlsx")
    with pytest.raises(FileNotFoundError, match="data/insumos"):
        enerandes.extraer()
