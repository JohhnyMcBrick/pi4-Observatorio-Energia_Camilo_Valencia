import pandas as pd

from src import config, consultar, perfilar, pipeline


def test_perfil_calcula_filas_nulos_y_duplicados():
    df = pd.DataFrame({"a": ["1", "1", None], "b": ["x", "x", "y"]})
    p = perfilar.perfil("archivo_x", df)
    assert p["filas"] == 3 and p["duplicadas"] == 1
    assert {c["columna"]: c["nulos"] for c in p["columnas"]}["a"] == 1


def test_perfilamiento_genera_tablas_y_al_menos_cinco_hallazgos(carpetas, rango_corto, red_falsa, excel_enerandes):
    pipeline.main(["--sin-muestras"])
    texto = perfilar.generar_perfilamiento()
    assert (config.DIR_DOCS / "perfilamiento.md").exists()
    assert "| Columna | Tipo | Nulos | % nulos |" in texto
    for archivo in config.DIR_BRONZE.glob("*.parquet"):
        assert f"`{archivo.stem}.parquet`" in texto
    assert texto.count("### H") >= 5


def test_hallazgos_de_enerandes_detectan_los_problemas_sembrados(carpetas, excel_enerandes):
    from src.extract import enerandes
    enerandes.extraer()
    dfs = {p.stem: pd.read_parquet(p) for p in config.DIR_BRONZE.glob("*.parquet")}
    titulos = " ".join(h.titulo for h in perfilar.hallazgos_enerandes(dfs))
    assert "TOTAL" in titulos and "duplicados" in titulos.lower() and "encabezados" in titulos


def test_las_consultas_sql_corren_sobre_el_bronce(carpetas, rango_corto, red_falsa, excel_enerandes, monkeypatch, capsys):
    pipeline.main(["--sin-muestras"])
    monkeypatch.setattr(config, "RAIZ", config.RAIZ)            # las rutas SQL son relativas a la raíz real
    import os, shutil
    raiz_tmp = carpetas / "proyecto"
    shutil.copytree(config.RAIZ / "consultas", raiz_tmp / "consultas")
    shutil.copytree(config.DIR_BRONZE, raiz_tmp / "data" / "bronze")
    monkeypatch.setattr(config, "RAIZ", raiz_tmp)
    cwd = os.getcwd()
    try:
        consultar.main()
    finally:
        os.chdir(cwd)
    salida = capsys.readouterr().out
    for n in ("01_precio_vs_embalses", "03_aportes_vs_embalses", "05_clima_mensual", "06_precio_vs_trm"):
        assert n in salida
    assert "2026-01" in salida and "El Niño" in salida
