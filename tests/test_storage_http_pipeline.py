import pandas as pd
import pytest
import requests

from src import config, pipeline
from src.common import http
from src.common.storage import guardar_bronce, ruta_bronce, ya_existe
from src.muestras import generar_muestras


def test_guardar_bronce_agrega_las_tres_columnas_de_linaje_y_no_toca_los_valores(carpetas):
    guardar_bronce(pd.DataFrame({"x": ["007", "1.50"]}), "prueba", fuente="F", origen="http://o")
    df = pd.read_parquet(ruta_bronce("prueba"))
    assert df["x"].tolist() == ["007", "1.50"]
    assert df[["_fuente", "_origen"]].iloc[0].tolist() == ["F", "http://o"]
    assert df["_extraido_en"].iloc[0].endswith("+00:00")


def test_guardar_bronce_tolera_columnas_con_tipos_mezclados(carpetas):
    guardar_bronce(pd.DataFrame({"x": [1, "a", None]}), "mezcla", fuente="F", origen="o")
    x = pd.read_parquet(ruta_bronce("mezcla"))["x"]
    assert x.tolist()[:2] == ["1", "a"] and pd.isna(x.iloc[2])


def test_ya_existe_respeta_forzar(carpetas):
    assert not ya_existe("a", forzar=False)
    guardar_bronce(pd.DataFrame({"x": [1]}), "a", "F", "o")
    assert ya_existe("a", forzar=False)
    assert not ya_existe("a", forzar=True)


def test_http_reintenta_errores_de_servidor_y_luego_funciona(monkeypatch):
    monkeypatch.setattr(http.time, "sleep", lambda s: None)
    estados = iter([503, 503, 200])

    class R:
        def __init__(self, code): self.status_code = code
        def raise_for_status(self):
            if self.status_code >= 400:
                raise requests.HTTPError(response=self)
        def json(self): return {"ok": True}

    monkeypatch.setattr(http.requests, "request", lambda *a, **k: R(next(estados)))
    assert http.http_json("GET", "http://x") == {"ok": True}


def test_http_no_reintenta_un_400_porque_repetirlo_no_lo_arregla(monkeypatch):
    llamadas = []

    class R:
        status_code = 400
        def raise_for_status(self): raise requests.HTTPError(response=self)

    monkeypatch.setattr(http.requests, "request", lambda *a, **k: llamadas.append(1) or R())
    with pytest.raises(RuntimeError, match="Fallo definitivo"):
        http.http_json("GET", "http://x")
    assert len(llamadas) == 1


def test_pipeline_completo_con_red_simulada_genera_bronce_y_muestras(carpetas, rango_corto, red_falsa, excel_enerandes):
    codigo = pipeline.main([])
    assert codigo == 0
    esperados = {m.nombre for m in config.XM_METRICAS} | {d.nombre for d in config.IDEAM_DATASETS} | {
        "noaa_oni", "trm_diaria", "enerandes_ventas_2023", "enerandes_ventas_2025"}
    assert {p.stem for p in config.DIR_BRONZE.glob("*.parquet")} == esperados
    assert {p.stem for p in config.DIR_SAMPLE.glob("*.csv")} == esperados


def test_pipeline_omite_los_archivos_que_ya_existen(carpetas, rango_corto, red_falsa, excel_enerandes, monkeypatch):
    pipeline.main(["--sin-muestras"])
    marca = ruta_bronce("noaa_oni").stat().st_mtime_ns
    from src.extract import noaa
    monkeypatch.setattr(noaa, "http_texto", lambda u: pytest.fail("no debía descargar de nuevo"))
    assert pipeline.main(["--sin-muestras"]) == 0
    assert ruta_bronce("noaa_oni").stat().st_mtime_ns == marca


def test_pipeline_continua_si_una_fuente_falla_y_devuelve_codigo_de_error(carpetas, rango_corto, red_falsa, excel_enerandes, monkeypatch):
    from src.extract import noaa
    def caida(u): raise RuntimeError("NOAA caído")
    monkeypatch.setattr(noaa, "http_texto", caida)
    assert pipeline.main(["--sin-muestras"]) == 1
    assert ruta_bronce("trm_diaria").exists() and not ruta_bronce("noaa_oni").exists()


def test_muestra_tiene_maximo_200_filas(carpetas):
    guardar_bronce(pd.DataFrame({"x": range(500)}), "grande", "F", "o")
    generar_muestras()
    assert len(pd.read_csv(config.DIR_SAMPLE / "grande.csv")) == 200
