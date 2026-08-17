"""Frontend Streamlit para sustentar el Proyecto Integrador Final."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".matplotlib"))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from main import (
    GRAFICOS,
    NOMINA,
    calcular_metricas,
    calcular_nomina,
    cargar_inventario,
    exportar_resultados,
    generar_graficos,
    guardar_y_leer_nomina,
    preparar_inventario,
)


st.set_page_config(
    page_title="LogiStock | Proyecto Final",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --bg: #f4f7fb;
        --ink: #172033;
        --muted: #64748b;
        --line: #dbe4ef;
        --blue: #2563eb;
        --green: #0f9f6e;
        --amber: #d97706;
    }
    .stApp { background: var(--bg); color: var(--ink); }
    .block-container { padding-top: 1.7rem; padding-bottom: 2.5rem; }
    h1, h2, h3 { letter-spacing: 0; }
    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--line);
    }
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
    }
    div[data-testid="stMetricLabel"] p { color: var(--muted); font-size: 0.86rem; }
    .hero {
        border-bottom: 1px solid var(--line);
        padding: 0.3rem 0 1rem 0;
        margin-bottom: 1rem;
    }
    .hero p { color: var(--muted); max-width: 850px; }
    .status-ok {
        display: inline-block;
        padding: 0.25rem 0.55rem;
        border-radius: 999px;
        background: #dcfce7;
        color: #166534;
        font-size: 0.82rem;
        font-weight: 700;
    }
    .panel {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
    }
    .mini-title {
        color: var(--muted);
        font-size: 0.82rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
        text-transform: uppercase;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def obtener_datos() -> tuple[pd.DataFrame, dict]:
    df = cargar_inventario()
    if df is None:
        return pd.DataFrame(), {}
    df = preparar_inventario(df)
    if df is None or df.empty:
        return pd.DataFrame(), {}
    metricas = calcular_metricas(df)
    exportar_resultados(metricas)
    generar_graficos(df, metricas)
    return df, metricas


def moneda(valor: float) -> str:
    return f"${valor:,.0f} COP"


def grafico_nomina(salario: float, horas_extras: float, bonificaciones: float, deducciones: float) -> plt.Figure:
    neto = salario + horas_extras + bonificaciones - deducciones
    conceptos = ["Salario", "Extras", "Bonos", "Deducciones", "Neto"]
    valores = [salario, horas_extras, bonificaciones, -deducciones, neto]
    colores = ["#2563eb", "#0f9f6e", "#16a34a", "#dc2626", "#111827"]

    fig, ax = plt.subplots(figsize=(8.5, 4.7))
    ax.bar(conceptos, valores, color=colores)
    ax.axhline(0, color="#94a3b8", linewidth=1)
    ax.set_title("Composicion del desprendible de nomina")
    ax.set_xlabel("Concepto")
    ax.set_ylabel("Valor (COP)")
    fig.tight_layout()
    return fig


def grafico_participacion(resumen: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    colores = ["#2563eb", "#16a34a", "#f97316", "#7c3aed", "#0f766e"]
    ax.pie(
        resumen["Valor_Total"],
        labels=resumen["Centro"],
        autopct="%1.1f%%",
        startangle=90,
        colors=colores[: len(resumen)],
        wedgeprops={"width": 0.42, "edgecolor": "white"},
    )
    ax.set_title("Participacion del valor contable por centro")
    fig.tight_layout()
    return fig


def preparar_filtros(datos: pd.DataFrame) -> pd.DataFrame:
    if datos.empty:
        return datos

    st.sidebar.header("Filtros")
    centros = sorted(datos["Centro"].astype(str).unique())
    seleccion_centros = st.sidebar.multiselect("Centro logistico", centros, default=centros)

    filtrado = datos[datos["Centro"].astype(str).isin(seleccion_centros)]
    if "Categoria" in datos.columns:
        categorias = sorted(datos["Categoria"].astype(str).unique())
        seleccion_categorias = st.sidebar.multiselect("Categoria", categorias, default=categorias)
        filtrado = filtrado[filtrado["Categoria"].astype(str).isin(seleccion_categorias)]

    return filtrado


st.markdown(
    """
    <div class="hero">
      <span class="status-ok">Proyecto integrador listo para sustentar</span>
      <h1>LogiStock S.A.S. | Nomina, Inventario y Visualizacion Gerencial</h1>
      <p>
        Tablero construido para presentar los tres componentes exigidos: gestion de nomina con archivos,
        analisis cuantitativo con NumPy y graficos exportados en alta resolucion.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

df, metricas = obtener_datos()
df_filtrado = preparar_filtros(df)
metricas_filtradas = calcular_metricas(df_filtrado) if not df_filtrado.empty else {}

tab_nomina, tab_inventario, tab_graficos, tab_entrega = st.tabs(
    ["Nomina", "Tablero", "Graficos", "Entrega"]
)

with tab_nomina:
    st.subheader("Desprendible de pago")
    col_form, col_preview = st.columns([0.9, 1.1], gap="large")

    with col_form:
        empleado = st.text_input("Empleado", "Laura Gomez")
        salario = st.number_input("Salario base (COP)", min_value=1.0, value=2500000.0, step=100000.0)
        horas_extras = st.number_input("Horas extras (COP)", min_value=0.0, value=180000.0, step=20000.0)
        bonificaciones = st.number_input("Bonificaciones (COP)", min_value=0.0, value=250000.0, step=50000.0)
        deducciones = st.number_input("Deducciones (COP)", min_value=0.0, value=210000.0, step=50000.0)

        if st.button("Generar nomina", type="primary"):
            _, contenido = calcular_nomina(empleado, salario, horas_extras, deducciones, bonificaciones)
            leido = guardar_y_leer_nomina(contenido)
            st.session_state["nomina"] = leido
            st.success("nomina.txt fue generado y leido correctamente con with.")

    with col_preview:
        contenido = st.session_state.get("nomina")
        if contenido is None and NOMINA.exists():
            contenido = NOMINA.read_text(encoding="utf-8")
        st.code(contenido or "Genera la nomina para ver el desprendible.", language="text")
        st.pyplot(grafico_nomina(salario, horas_extras, bonificaciones, deducciones), width="stretch")

with tab_inventario:
    st.subheader("Tablero gerencial del inventario")
    if df_filtrado.empty or not metricas_filtradas:
        st.error("No hay datos validos para analizar.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Registros", f"{metricas_filtradas['registros']:,}")
        c2.metric("Centros", f"{metricas_filtradas['centros']:,}")
        c3.metric("Valor total", moneda(metricas_filtradas["total"]))
        c4.metric("Proyeccion +5%", moneda(metricas_filtradas["proyeccion_5"]))

        c5, c6, c7, c8 = st.columns(4)
        c5.metric("Promedio", moneda(metricas_filtradas["promedio"]))
        c6.metric("Mediana", moneda(metricas_filtradas["mediana"]))
        c7.metric("Minimo", moneda(metricas_filtradas["minimo"]))
        c8.metric("Desv. estandar", moneda(metricas_filtradas["desviacion"]))

        col_resumen, col_dona = st.columns([1.1, 0.9], gap="large")
        with col_resumen:
            st.markdown('<div class="mini-title">Resumen por centro</div>', unsafe_allow_html=True)
            st.dataframe(metricas_filtradas["resumen"], width="stretch", hide_index=True)
        with col_dona:
            st.pyplot(grafico_participacion(metricas_filtradas["resumen"]), width="stretch")

        barras = metricas_filtradas["resumen"].set_index("Centro")[["Cantidad", "Valor_Total"]]
        st.bar_chart(barras, width="stretch")

with tab_graficos:
    st.subheader("Apoyo visual gerencial")
    if not metricas_filtradas:
        st.warning("Ejecuta el analisis para generar los graficos.")
    else:
        por_categoria = metricas_filtradas.get("por_categoria", pd.DataFrame())
        if not por_categoria.empty:
            st.markdown('<div class="mini-title">Valor por categoria</div>', unsafe_allow_html=True)
            categoria_chart = por_categoria.set_index("Categoria")["Valor_Total"]
            st.bar_chart(categoria_chart, width="stretch")

        col_a, col_b = st.columns(2, gap="large")
        with col_a:
            st.image(str(GRAFICOS / "activos_por_centro.png"), caption="Cantidad de activos por centro")
        with col_b:
            st.image(str(GRAFICOS / "valor_por_centro.png"), caption="Valor contable por centro")
        col_c, col_d = st.columns(2, gap="large")
        with col_c:
            st.image(str(GRAFICOS / "distribucion_valores.png"), caption="Distribucion de valores del inventario")
        with col_d:
            st.image(str(GRAFICOS / "participacion_valor_centro.png"), caption="Participacion por centro")

        categoria_png = GRAFICOS / "valor_por_categoria.png"
        if categoria_png.exists():
            st.image(str(categoria_png), caption="Valor contable por categoria")

        st.info(
            "La comparacion por centro permite priorizar controles donde se concentra mayor valor. "
            "La diferencia entre promedio y mediana ayuda a identificar valores extremos que pueden "
            "distorsionar una decision si solo se revisa el promedio."
        )

with tab_entrega:
    st.subheader("Checklist de cumplimiento")
    st.checkbox("Codigo Python comentado y estructurado", value=True, disabled=True)
    st.checkbox("nomina.txt generado con escritura y lectura mediante with", value=True, disabled=True)
    st.checkbox("Validacion de errores numericos y valores negativos", value=True, disabled=True)
    st.checkbox("Analisis del proceso con np.array y funciones NumPy", value=True, disabled=True)
    st.checkbox("Minimo dos tipos de graficos con titulos, ejes y leyendas", value=True, disabled=True)
    st.checkbox("Imagenes exportadas con savefig()", value=True, disabled=True)
    st.checkbox("Informe de soporte con interpretacion gerencial", value=True, disabled=True)

    st.markdown(
        """
        Para entregar, comprime la carpeta del proyecto con `main.py`, `app.py`, `nomina.txt`,
        `data/`, `graficos/`, `docs/`, `README.md` y `requirements.txt`.
        """
    )
