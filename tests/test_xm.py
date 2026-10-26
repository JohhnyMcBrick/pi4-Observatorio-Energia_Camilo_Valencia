from datetime import date

import pandas as pd

from src import config
from src.extract import xm

HORARIA = {"Items": [{"Date": "2026-01-01", "HourlyEntities": [
    {"Id": "Sistema", "Values": {"Hour01": "300.5", "Hour02": "310.0"}}]}]}
DIARIA = {"Items": [{"Date": "2026-01-01", "DailyEntities": [{"Id": "Sistema", "Value": "0.61"}]},
                    {"Date": "2026-01-02", "DailyEntities": [{"Id": "Sistema", "Value": "0.62"}]}]}
LISTA = {"Items": [{"ListEntities": [
    {"Id": "ABC1", "Values": {"Name": "PLANTA A", "Type": "HIDRAULICA"}},
    {"Id": "XYZ2", "Values": {"Name": "PLANTA B", "Type": "TERMICA"}}]}]}


def test_aplanar_horario_convierte_json_anidado_en_filas_sin_cambiar_valores():
    assert xm.aplanar(HORARIA, "hourly") == [
        {"Date": "2026-01-01", "Id": "Sistema", "Hour01": "300.5", "Hour02": "310.0"}]


def test_aplanar_diario():
    filas = xm.aplanar(DIARIA, "daily")
    assert [f["Value"] for f in filas] == ["0.61", "0.62"]
    assert filas[0] == {"Date": "2026-01-01", "Id": "Sistema", "Value": "0.61"}


def test_aplanar_respuesta_vacia_no_falla():
    assert xm.aplanar({}, "hourly") == []
    assert xm.aplanar_lista({}) == []


def test_aplanar_lista_resuelve_la_estructura_ListEntities():
    filas = xm.aplanar_lista(LISTA)
    assert len(filas) == 2
    assert filas[0] == {"Id": "ABC1", "Name": "PLANTA A", "Type": "HIDRAULICA"}


def test_cuerpo_de_lists_no_lleva_fechas_y_el_de_series_si():
    catalogo = next(m for m in config.XM_METRICAS if m.metric_id == "ListadoRecursos")
    assert xm.cuerpo_consulta(catalogo) == {"MetricId": "ListadoRecursos", "Entity": "Sistema"}
    gene = next(m for m in config.XM_METRICAS if m.metric_id == "Gene")
    cuerpo = xm.cuerpo_consulta(gene, date(2026, 1, 1), date(2026, 1, 30))
    assert cuerpo["Entity"] == "Recurso" and cuerpo["StartDate"] == "2026-01-01" and cuerpo["Filter"] == []


def test_config_tiene_las_seis_metricas_del_reto_y_el_rango_de_dos_anios():
    ids = {m.metric_id for m in config.XM_METRICAS}
    assert ids == {"PrecBolsNaci", "DemaReal", "PorcVoluUtilDiar", "Gene", "AporEner", "ListadoRecursos"}
    assert config.FECHA_INICIO == date(2024, 1, 1) and config.FECHA_FIN >= date(2026, 9, 30)
    assert next(m for m in config.XM_METRICAS if m.metric_id == "ListadoRecursos").periodo == "lists"


def test_extraer_guarda_las_seis_metricas_en_bronce(carpetas, rango_corto, red_falsa):
    xm.extraer()
    nombres = {p.stem for p in config.DIR_BRONZE.glob("*.parquet")}
    assert nombres == {m.nombre for m in config.XM_METRICAS}
    gene = pd.read_parquet(config.DIR_BRONZE / "xm_generacion_recurso.parquet")
    assert len(gene) == 45 * 2                                  # 45 días x 2 plantas
    assert {"_fuente", "_origen", "_extraido_en"} <= set(gene.columns)
    catalogo = pd.read_parquet(config.DIR_BRONZE / "xm_listado_recursos.parquet")
    assert list(catalogo["Id"]) == ["ABC1", "XYZ2"]
