"""
Perfilamiento de la capa BRONCE -> docs/perfilamiento.md

Para cada archivo Parquet de data/bronze/ genera una tabla con: filas, columnas,
tipos de datos, % de nulos por columna, filas duplicadas y rango de fechas.
Además detecta hallazgos de calidad con evidencia numérica.

Uso:
    python -m src.perfilar

El archivo se REGENERA completo cada vez. Las notas manuales del equipo van en
docs/notas_perfilamiento.md (si existe, se anexan al final).
"""
import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Dict, List, Optional

import pandas as pd

from src import config
from src.common.logger import log
from src.common.storage import COLUMNAS_LINAJE


# ---------------------------------------------------------------------------
# Modelo
# ---------------------------------------------------------------------------
@dataclass
class Hallazgo:
    archivo: str        # archivo(s) de bronce afectado(s)
    titulo: str
    evidencia: str      # número(s) concretos que lo respaldan
    accion: str         # qué se hará en la capa plata


# ---------------------------------------------------------------------------
# Utilidades de perfilamiento por archivo
# ---------------------------------------------------------------------------
def columnas_datos(df: pd.DataFrame) -> List[str]:
    return [c for c in df.columns if c not in COLUMNAS_LINAJE]


def pct(parte: float, total: float) -> str:
    return f"{(100 * parte / total if total else 0):.1f} %"


def tipo_legible(serie: pd.Series) -> str:
    t = str(serie.dtype)
    if t == "object" or t.startswith("string"):
        return "texto"
    if t.startswith("int") or t.startswith("Int"):
        return "entero"
    if t.startswith("float"):
        return "decimal"
    if t.startswith("datetime"):
        return "fecha"
    return t


def _fechas(serie: pd.Series) -> pd.Series:
    return pd.to_datetime(serie, errors="coerce", utc=True).dropna()


def rango_fechas(nombre: str, df: pd.DataFrame) -> str:
    """Rango de fechas del archivo según su columna de fecha conocida."""
    if nombre.startswith("enerandes_"):
        return "n/a: fechas como texto en formatos mixtos (se normalizan en plata)"
    if nombre.startswith("xm_") and "Date" in df:
        f = _fechas(df["Date"])
    elif nombre.startswith("ideam_") and "fecha" in df:
        f = _fechas(df["fecha"])
    elif nombre.startswith("trm_") and config.TRM_CAMPO_FECHA in df:
        f = _fechas(df[config.TRM_CAMPO_FECHA])
    elif nombre.startswith("noaa_") and "YR" in df:
        anios = pd.to_numeric(df["YR"], errors="coerce").dropna()
        return f"{int(anios.min())} a {int(anios.max())} (años)" if len(anios) else "sin datos"
    else:
        return "n/a (sin columna de fecha)"
    return f"{f.min():%Y-%m-%d} a {f.max():%Y-%m-%d}" if len(f) else "sin fechas válidas"


def perfil(nombre: str, df: pd.DataFrame) -> dict:
    datos = columnas_datos(df)
    filas = len(df)
    columnas = []
    for c in df.columns:
        vacios = 0
        if tipo_legible(df[c]) == "texto":
            vacios = int(df[c].dropna().astype(str).str.strip().eq("").sum())
        columnas.append({
            "columna": c,
            "tipo": tipo_legible(df[c]),
            "nulos": int(df[c].isna().sum()),
            "vacios": vacios,
        })
    return {
        "nombre": nombre,
        "filas": filas,
        "columnas_n": df.shape[1],
        "duplicadas": int(df.duplicated(subset=datos).sum()) if datos else 0,
        "rango": rango_fechas(nombre, df),
        "columnas": columnas,
    }


def tabla_md(p: dict) -> str:
    filas = p["filas"]
    L = [f"### `{p['nombre']}.parquet`", "",
         "| Métrica | Valor |", "|---|---|",
         f"| Filas | {filas:,} |",
         f"| Columnas | {p['columnas_n']} |",
         f"| Filas duplicadas (exactas, sin columnas de linaje) | {p['duplicadas']:,} ({pct(p['duplicadas'], filas)}) |",
         f"| Rango de fechas | {p['rango']} |", "",
         "| Columna | Tipo | Nulos | % nulos | Vacíos ('') |", "|---|---|---:|---:|---:|"]
    for c in p["columnas"]:
        L.append(f"| `{c['columna']}` | {c['tipo']} | {c['nulos']:,} | {pct(c['nulos'], filas)} | {c['vacios']:,} |")
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------------------
# Hallazgos generales (aplican a cualquier archivo)
# ---------------------------------------------------------------------------
def _es_numerica_en_texto(serie: pd.Series) -> bool:
    s = serie.dropna()
    if tipo_legible(serie) != "texto" or s.empty:
        return False
    return pd.to_numeric(s, errors="coerce").notna().mean() >= 0.95


def hallazgos_generales(dfs: Dict[str, pd.DataFrame]) -> List[Hallazgo]:
    out = []
    # Duplicados exactos (los de EnerAndes se detallan aparte)
    dup = {n: int(d.duplicated(subset=columnas_datos(d)).sum()) for n, d in dfs.items()
           if not n.startswith("enerandes_")}
    dup = {n: k for n, k in dup.items() if k > 0}
    if dup:
        out.append(Hallazgo(", ".join(dup), "Filas duplicadas exactas",
                            "; ".join(f"{n}: {k:,} filas" for n, k in dup.items()),
                            "Deduplicar por la llave natural de cada tabla."))
    # Numéricos guardados como texto
    num_texto = {n: [c for c in columnas_datos(d) if _es_numerica_en_texto(d[c])] for n, d in dfs.items()}
    num_texto = {n: cs for n, cs in num_texto.items() if cs}
    if num_texto:
        total = sum(len(cs) for cs in num_texto.values())
        out.append(Hallazgo(", ".join(num_texto), "Columnas numéricas guardadas como texto",
                            f"{total} columnas numéricas en formato texto en {len(num_texto)} archivos "
                            f"(ej.: {next(iter(num_texto))}.{num_texto[next(iter(num_texto))][0]})",
                            "Convertir a DOUBLE/INTEGER en plata con validación (TRY_CAST)."))
    # Columnas con nulos relevantes
    nulos = []
    for n, d in dfs.items():
        for c in columnas_datos(d):
            k = int(d[c].isna().sum())
            if k and k / len(d) >= 0.01:
                nulos.append((k / len(d), n, c, k))
    if nulos:
        nulos.sort(reverse=True)
        top = nulos[:4]
        out.append(Hallazgo(", ".join(sorted({t[1] for t in top})), "Columnas con 1 % o más de nulos",
                            "; ".join(f"{n}.{c}: {k:,} nulos ({100 * p:.1f} %)" for p, n, c, k in top),
                            "Definir regla por columna: imputar, descartar o marcar como dato faltante."))
    return out


# ---------------------------------------------------------------------------
# EnerAndes
# ---------------------------------------------------------------------------
def _sin_tildes(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def hoja(df: pd.DataFrame) -> dict:
    """Separa título / encabezado / datos / fila TOTAL de una hoja cruda de EnerAndes."""
    cols = columnas_datos(df)
    i = int(df.index[df[cols[1]].notna()][0])        # primera fila con 2+ celdas = encabezado
    encabezado = [str(x) for x in df.loc[i, cols] if pd.notna(x)]
    datos = df.loc[i + 1:, cols]
    es_total = datos[cols[0]].astype(str).str.strip().str.upper().eq("TOTAL")
    return {"titulo_filas": i, "encabezado": encabezado, "total": int(es_total.sum()),
            "datos": datos[~es_total].reset_index(drop=True), "cols": cols}


def _patron_fecha(valor) -> str:
    return re.sub(r"[A-Za-z]+", "a", re.sub(r"\d", "9", str(valor).strip()))


def hallazgos_enerandes(dfs: Dict[str, pd.DataFrame]) -> List[Hallazgo]:
    hojas = {n: hoja(d) for n, d in sorted(dfs.items()) if n.startswith("enerandes_")}
    if not hojas:
        return []
    arch = ", ".join(hojas)
    out = []

    # 1. Encabezados distintos y filas de título
    enc = {n: tuple(h["encabezado"][:7]) for n, h in hojas.items()}
    con_titulo = {n: h["titulo_filas"] for n, h in hojas.items() if h["titulo_filas"] > 0}
    out.append(Hallazgo(arch, "Cada hoja anual tiene encabezados distintos y algunas traen título encima",
                        f"{len(set(enc.values()))} encabezados distintos en {len(hojas)} hojas; "
                        f"{len(con_titulo)} hojas con filas de título previas ({', '.join(f'{n[-4:]}: {k} filas' for n, k in con_titulo.items())}); "
                        f"la hoja 2024 tiene además columna UNIDAD (8 columnas vs 7).",
                        "Mapear cada hoja a un esquema común y saltar las filas de título."))

    # 2. Fila TOTAL
    out.append(Hallazgo(arch, "Fila 'TOTAL' mezclada con los datos",
                        f"{sum(h['total'] for h in hojas.values())} filas TOTAL (una por hoja) que sumarían doble.",
                        "Excluir filas TOTAL antes de agregar."))

    # 3. Formatos de fecha
    pats = {}
    for n, h in hojas.items():
        pats[n] = h["datos"][h["cols"][0]].map(_patron_fecha).value_counts().to_dict()
    nombres = {"9999-99": "AAAA-MM", "99/9999": "MM/AAAA", "a-99": "mmm-AA", "99/99/9999": "DD/MM/AAAA"}
    todos = {}
    for d in pats.values():
        for p, k in d.items():
            todos[p] = todos.get(p, 0) + k
    out.append(Hallazgo(arch, "Fechas en formatos mixtos",
                        f"{len(todos)} formatos: " + "; ".join(f"{nombres.get(p, p)}: {k:,} filas" for p, k in sorted(todos.items(), key=lambda x: -x[1]))
                        + ". En la hoja 2024 conviven 3 formatos: "
                        + ", ".join(f"{nombres.get(p, p)}={k}" for p, k in pats.get("enerandes_ventas_2024", {}).items()) + ".",
                        "Parser por formato hacia fecha de primer día de mes (DATE)."))

    # 4. Duplicados
    dups = {n: int(h["datos"].duplicated().sum()) for n, h in hojas.items()}
    total_filas = sum(len(h["datos"]) for h in hojas.values())
    out.append(Hallazgo(arch, "Registros duplicados exactos",
                        f"{sum(dups.values())} duplicados sobre {total_filas:,} filas de datos "
                        f"({pct(sum(dups.values()), total_filas)}); por hoja: " + ", ".join(f"{n[-4:]}={k}" for n, k in dups.items()),
                        "Deduplicar por (mes, municipio, segmento, tipo de compra)."))

    # 5. Municipios mal escritos
    var_raw, var_norm, med = 0, 0, set()
    for h in hojas.values():
        m = h["datos"][h["cols"][1]].dropna()
        var_raw += m.nunique()
        var_norm += m.map(lambda s: _sin_tildes(s).strip().lower()).nunique()
        med |= {s for s in m.unique() if _sin_tildes(s).strip().lower().startswith("medell")}
    todos_mun = set().union(*[set(h["datos"][h["cols"][1]].dropna().unique()) for h in hojas.values()])
    out.append(Hallazgo(arch, "Municipios mal escritos (tildes, mayúsculas, espacios, abreviaturas)",
                        f"{len(todos_mun)} escrituras distintas para ~{len(set(_sin_tildes(s).strip().lower() for s in todos_mun))} "
                        f"nombres tras quitar tildes/mayúsculas/espacios; Medellín aparece de {len(med)} formas: "
                        + ", ".join(f"'{s}'" for s in sorted(med)) + ". Siguen quedando variantes como 'Rio Negro'/'Rionegro', 'Sta Fe de Antioquia'.",
                        "Normalizar contra el catálogo DIVIPOLA con tabla de equivalencias."))

    # 6. Unidades mezcladas
    h24 = hojas.get("enerandes_ventas_2024")
    if h24 and "UNIDAD" in h24["encabezado"]:
        u = h24["datos"][h24["cols"][5]].value_counts().to_dict()
        mwh = pd.to_numeric(h24["datos"].loc[h24["datos"][h24["cols"][5]] == "MWh", h24["cols"][4]], errors="coerce")
        kwh = pd.to_numeric(h24["datos"].loc[h24["datos"][h24["cols"][5]] == "kWh", h24["cols"][4]], errors="coerce")
        out.append(Hallazgo("enerandes_ventas_2024", "Unidades mezcladas (kWh y MWh) en la misma columna",
                            f"{u.get('kWh', 0)} filas en kWh y {u.get('MWh', 0)} en MWh ({pct(u.get('MWh', 0), sum(u.values()))}); "
                            f"mediana kWh = {kwh.median():,.0f} vs mediana MWh = {mwh.median():,.1f}: sumarlas sin convertir subestima el consumo ~1000 veces.",
                            "Convertir todo a kWh (MWh × 1000) usando la columna UNIDAD."))

    # 7. Tipo de compra
    tipos = {}
    for h in hojas.values():
        for k, v in h["datos"][h["cols"][3]].value_counts().items():
            tipos[k] = tipos.get(k, 0) + int(v)
    out.append(Hallazgo(arch, "Tipo de compra con escrituras inconsistentes",
                        f"{len(tipos)} valores para 2 categorías reales: " + ", ".join(f"'{k}'={v:,}" for k, v in sorted(tipos.items(), key=lambda x: -x[1])),
                        "Mapear a {Contrato, Bolsa}."))

    # 8. Nulos y negativos en la energía
    nul = {n: int(h["datos"][h["cols"][4]].isna().sum()) for n, h in hojas.items()}
    neg = {}
    for n, h in hojas.items():
        e = pd.to_numeric(h["datos"][h["cols"][4]], errors="coerce")
        neg[n] = int((e < 0).sum())
    out.append(Hallazgo(arch, "Celdas vacías y valores negativos imposibles en energía",
                        f"{sum(nul.values())} celdas de energía vacías y {sum(neg.values())} valores negativos "
                        f"(por hoja, vacías/negativas: " + ", ".join(f"{n[-4:]}={nul[n]}/{neg[n]}" for n in hojas) + ").",
                        "Tratar negativos como error de captura (nulo) y definir regla de imputación o descarte."))

    # 9. Segmento vacío
    seg = sum(int(h["datos"][h["cols"][2]].isna().sum()) for h in hojas.values())
    out.append(Hallazgo(arch, "Segmento de cliente sin dato",
                        f"{seg} filas sin segmento ({pct(seg, total_filas)}), que no se pueden asignar a residencial/comercial/industrial.",
                        "Clasificar como 'Sin segmento' o descartar según el análisis."))
    return out


# ---------------------------------------------------------------------------
# XM, IDEAM, NOAA, TRM
# ---------------------------------------------------------------------------
def hallazgos_xm(dfs: Dict[str, pd.DataFrame]) -> List[Hallazgo]:
    out = []
    for n, d in dfs.items():
        if not n.startswith("xm_") or "Date" not in d:
            continue
        f = _fechas(d["Date"])
        if f.empty:
            continue
        esperados = (f.max() - f.min()).days + 1
        presentes = f.dt.normalize().nunique()
        if presentes < esperados:
            out.append(Hallazgo(n, "Días faltantes en la serie de XM",
                                f"{presentes} días con datos de {esperados} esperados entre {f.min():%Y-%m-%d} y {f.max():%Y-%m-%d} "
                                f"({esperados - presentes} días sin datos).",
                                "Revisar ventanas fallidas o completar con re-extracción."))
        if "Hour25" in d and d["Hour25"].notna().any():
            out.append(Hallazgo(n, "Columna Hour25 con datos (día de 25 horas)",
                                f"{int(d['Hour25'].notna().sum())} filas con Hour25.", "Tratar Hour25 al pasar a formato largo."))
    hor = [n for n, d in dfs.items() if n.startswith("xm_") and "Hour01" in d]
    if hor:
        out.append(Hallazgo(", ".join(hor), "Formato ANCHO horario (Hour01...Hour24)",
                            "; ".join(f"{n}: {len(dfs[n]):,} filas x {len([c for c in dfs[n].columns if c.startswith('Hour')])} columnas de hora" for n in hor),
                            "UNPIVOT a formato largo (fecha, hora, valor) en plata."))
    if "xm_listado_recursos" in dfs:
        d = dfs["xm_listado_recursos"]
        out.append(Hallazgo("xm_listado_recursos", "Catálogo de plantas con estructura distinta (endpoint lists)",
                            f"{len(d):,} recursos y {len(columnas_datos(d))} columnas; sin columna de fecha.",
                            "Usarlo como dim_recurso (tipo, fuente, agente)."))
    return out


def hallazgos_ideam(dfs: Dict[str, pd.DataFrame]) -> List[Hallazgo]:
    out = []
    p = dfs.get("ideam_precipitacion_diaria")
    if p is not None and "precipitacion_mm" in p:
        v = pd.to_numeric(p["precipitacion_mm"], errors="coerce")
        if (v < 0).sum():
            out.append(Hallazgo("ideam_precipitacion_diaria", "Precipitación negativa (centinelas)",
                                f"{int((v < 0).sum()):,} filas con precipitación < 0.", "Tratar como dato faltante."))
        out.append(Hallazgo("ideam_precipitacion_diaria", "Cobertura desigual de observaciones por estación-día",
                            f"n_obs mínimo {pd.to_numeric(p['n_obs']).min():.0f}, mediana {pd.to_numeric(p['n_obs']).median():.0f}, "
                            f"máximo {pd.to_numeric(p['n_obs']).max():.0f}; {int((pd.to_numeric(p['n_obs']) < pd.to_numeric(p['n_obs']).median() / 2).sum()):,} "
                            f"filas con menos de la mitad de la mediana.",
                            "Marcar días con cobertura baja (suma de lluvia subestimada)."))
    t = dfs.get("ideam_temperatura_diaria")
    if t is not None and {"temp_min_c", "temp_max_c", "temp_media_c"} <= set(t.columns):
        mn, mx, me = (pd.to_numeric(t[c], errors="coerce") for c in ("temp_min_c", "temp_max_c", "temp_media_c"))
        inv = int((mn > mx).sum())
        fuera = int(((me < -5) | (me > 45)).sum())
        if inv or fuera:
            out.append(Hallazgo("ideam_temperatura_diaria", "Temperaturas inconsistentes o fuera de rango físico",
                                f"{inv:,} filas con mínima > máxima; {fuera:,} filas con media fuera de [-5, 45] °C.",
                                "Validar rangos y descartar/marcar valores imposibles."))
    for n in ("ideam_precipitacion_diaria", "ideam_temperatura_diaria"):
        d = dfs.get(n)
        if d is not None and "codigoestacion" in d:
            out.append(Hallazgo(n, "Estaciones con cobertura parcial en el periodo",
                                f"{d['codigoestacion'].nunique():,} estaciones; días por estación: mín {d.groupby('codigoestacion').size().min()}, "
                                f"mediana {d.groupby('codigoestacion').size().median():.0f}, máx {d.groupby('codigoestacion').size().max()}.",
                                "Filtrar estaciones con baja cobertura para el análisis."))
    return out


def hallazgos_noaa(dfs: Dict[str, pd.DataFrame]) -> List[Hallazgo]:
    d = dfs.get("noaa_oni")
    if d is None or "SEAS" not in d:
        return []
    return [Hallazgo("noaa_oni", "Trimestre móvil (SEAS) sin fecha: no cruza con datos diarios",
                     f"{d['SEAS'].nunique()} códigos de trimestre en {len(d):,} filas; ejemplo última fila: {d['SEAS'].iloc[-1]} {d['YR'].iloc[-1]} (ANOM={d['ANOM'].iloc[-1]}).",
                     "Convertir SEAS+YR al mes central del trimestre (JAS 2026 -> 2026-08)."),
            ]


def hallazgos_trm(dfs: Dict[str, pd.DataFrame]) -> List[Hallazgo]:
    d = dfs.get("trm_diaria")
    c = config.TRM_CAMPO_FECHA
    if d is None or c not in d or "vigenciahasta" not in d:
        return []
    desde, hasta = _fechas(d[c]), _fechas(d["vigenciahasta"])
    dias = ((hasta - desde.reset_index(drop=True)).dt.days + 1) if len(desde) == len(hasta) else pd.Series(dtype=float)
    multi = int((dias > 1).sum()) if len(dias) else 0
    return [Hallazgo("trm_diaria", "Una fila cubre varios días (vigencias de fin de semana y festivos)",
                     f"{multi:,} de {len(d):,} filas cubren más de un día.",
                     "Expandir cada vigencia a días calendario (dim_fecha).")]


# ---------------------------------------------------------------------------
# Generación del documento
# ---------------------------------------------------------------------------
def recopilar_hallazgos(dfs: Dict[str, pd.DataFrame]) -> List[Hallazgo]:
    return (hallazgos_enerandes(dfs) + hallazgos_xm(dfs) + hallazgos_ideam(dfs)
            + hallazgos_noaa(dfs) + hallazgos_trm(dfs) + hallazgos_generales(dfs))


def archivos_esperados() -> List[str]:
    """Nombres de bronce que el pipeline completo debe producir (las hojas de EnerAndes varían)."""
    return ([m.nombre for m in config.XM_METRICAS] + [d.nombre for d in config.IDEAM_DATASETS]
            + ["noaa_oni", "trm_diaria"])


def construir_documento(dfs: Dict[str, pd.DataFrame]) -> str:
    perfiles = [perfil(n, d) for n, d in dfs.items()]
    hallazgos = recopilar_hallazgos(dfs)
    ahora = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    L = ["# Perfilamiento de la capa bronce", "",
         f"> Generado automáticamente con `python -m src.perfilar` el {ahora}. "
         "No editar a mano: se regenera completo (las notas del equipo van en `docs/notas_perfilamiento.md`).", "",
         ]
    faltan = [n for n in archivos_esperados() if n not in dfs]
    if faltan:
        L += ["> ⚠️ **Perfilamiento parcial:** faltan en `data/bronze/` " + ", ".join(f"`{n}`" for n in faltan)
              + ". Ejecute `python -m src.pipeline --perfilar` con internet para completarlo.", ""]
    L += ["## Resumen", "",
         "| Archivo | Filas | Columnas | Duplicadas | Rango de fechas |", "|---|---:|---:|---:|---|"]
    for p in perfiles:
        L.append(f"| `{p['nombre']}` | {p['filas']:,} | {p['columnas_n']} | {p['duplicadas']:,} | {p['rango']} |")
    L += ["", "## Tablas por archivo", ""]
    L += [tabla_md(p) for p in perfiles]
    L += [f"## Hallazgos de calidad ({len(hallazgos)})", ""]
    for i, h in enumerate(hallazgos, 1):
        L += [f"### H{i}. {h.titulo}", "",
              f"- **Archivo(s):** `{h.archivo}`", f"- **Evidencia:** {h.evidencia}",
              f"- **Qué haremos en plata:** {h.accion}", ""]
    notas = config.DIR_DOCS / "notas_perfilamiento.md"
    if notas.exists():
        L += ["## Notas del equipo", "", notas.read_text(encoding="utf-8")]
    return "\n".join(L)


def generar_perfilamiento(salida=None) -> str:
    archivos = sorted(config.DIR_BRONZE.glob("*.parquet"))
    if not archivos:
        raise FileNotFoundError("No hay archivos en data/bronze/. Ejecute primero: python -m src.pipeline")
    dfs = {a.stem: pd.read_parquet(a) for a in archivos}
    salida = salida or (config.DIR_DOCS / "perfilamiento.md")
    config.DIR_DOCS.mkdir(parents=True, exist_ok=True)
    texto = construir_documento(dfs)
    salida.write_text(texto, encoding="utf-8")
    log(f"Perfilamiento: {len(dfs)} archivos, {len(recopilar_hallazgos(dfs))} hallazgos -> {salida}")
    return texto


if __name__ == "__main__":
    generar_perfilamiento()
