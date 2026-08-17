"""Proyecto Integrador Final - Programacion y Analisis de Datos en Python.

Empresa contextualizada: LogiStock S.A.S., una compania dedicada a la
administracion y control de inventarios empresariales.

El programa integra los tres modulos solicitados en el documento guia:
1. Gestion de nomina con archivos, with y excepciones.
2. Analisis cuantitativo del inventario con arreglos NumPy.
3. Visualizacion gerencial con Matplotlib y exportacion de graficos.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".matplotlib"))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA_DIR = ROOT / "data"
DATA_XLSX = DATA_DIR / "inventario.xlsx"
DATA_CSV = DATA_DIR / "inventario_ejemplo.csv"
NOMINA = ROOT / "nomina.txt"
GRAFICOS = ROOT / "graficos"
RESULTADOS = DATA_DIR / "resultados.json"


def pedir_float(mensaje: str, permitir_cero: bool = True) -> float:
    """Solicita un numero no negativo y controla entradas invalidas."""
    while True:
        try:
            entrada = input(mensaje).strip().replace("$", "").replace(",", "")
            valor = float(entrada)
            if valor < 0 or (not permitir_cero and valor == 0):
                raise ValueError("el valor debe ser mayor que cero.")
            return valor
        except ValueError as exc:
            print(f"Entrada invalida: {exc}")


def calcular_nomina(
    empleado: str,
    salario: float,
    horas_extras: float,
    deducciones: float,
    bonificaciones: float,
) -> tuple[float, str]:
    """Calcula el pago neto y devuelve el desprendible formateado."""
    neto = salario + horas_extras + bonificaciones - deducciones
    contenido = (
        "DESPRENDIBLE DE NOMINA\n"
        "=======================\n"
        f"Empresa: LogiStock S.A.S.\n"
        f"Empleado: {empleado or 'Empleado'}\n"
        f"Salario base: ${salario:,.2f} COP\n"
        f"Horas extras: ${horas_extras:,.2f} COP\n"
        f"Bonificaciones: ${bonificaciones:,.2f} COP\n"
        f"Deducciones: ${deducciones:,.2f} COP\n"
        "-----------------------\n"
        f"Neto a pagar: ${neto:,.2f} COP\n"
    )
    return neto, contenido


def guardar_y_leer_nomina(contenido: str, ruta: Path = NOMINA) -> str:
    """Persiste y lee el desprendible usando with, como exige la guia."""
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)

        with open(ruta, "r", encoding="utf-8") as archivo:
            return archivo.read()
    except (OSError, IOError, FileNotFoundError) as exc:
        raise RuntimeError(f"Error de entrada/salida al manipular {ruta.name}: {exc}") from exc


def generar_nomina() -> None:
    """Captura datos, calcula el neto y escribe/lee nomina.txt."""
    print("\n=== MODULO I: GESTION DE NOMINA ===")
    empleado = input("Nombre del empleado: ").strip() or "Empleado"
    salario = pedir_float("Salario base (COP): ", permitir_cero=False)
    horas_extras = pedir_float("Pago por horas extras (COP): ")
    deducciones = pedir_float("Deducciones (COP): ")
    bonificaciones = pedir_float("Bonificaciones (COP): ")

    _, contenido = calcular_nomina(empleado, salario, horas_extras, deducciones, bonificaciones)

    try:
        contenido_leido = guardar_y_leer_nomina(contenido)
        print("\nArchivo nomina.txt generado correctamente.\n")
        print(contenido_leido)
    except RuntimeError as exc:
        print(exc)


def cargar_inventario() -> pd.DataFrame | None:
    """Carga inventario real si existe; si no, usa una base ejemplo incluida."""
    try:
        if DATA_XLSX.exists():
            df = pd.read_excel(DATA_XLSX)
            fuente = DATA_XLSX.name
        elif DATA_CSV.exists():
            df = pd.read_csv(DATA_CSV)
            fuente = DATA_CSV.name
            print(f"No se encontro {DATA_XLSX.name}; se usara {DATA_CSV.name} para la demo.")
        else:
            print("No hay datos de inventario. Agrega data/inventario.xlsx o data/inventario_ejemplo.csv.")
            return None
    except (OSError, ValueError, ImportError) as exc:
        print(f"No fue posible leer la base de inventario: {exc}")
        return None

    df.columns = [str(c).strip() for c in df.columns]
    df.attrs["fuente"] = fuente
    return df


def preparar_inventario(df: pd.DataFrame) -> pd.DataFrame | None:
    """Normaliza columnas y valida que existan los datos necesarios."""
    columnas_requeridas = {"Centro", "Valor"}
    faltantes = columnas_requeridas.difference(df.columns)
    if faltantes:
        print(f"Error: faltan columnas requeridas: {', '.join(sorted(faltantes))}.")
        return None

    limpio = df.copy()
    limpio["Centro"] = limpio["Centro"].astype(str)
    limpio["Valor"] = pd.to_numeric(limpio["Valor"], errors="coerce").fillna(0)
    return limpio


def calcular_metricas(df: pd.DataFrame) -> dict:
    """Calcula metricas con np.array para apoyar decisiones de inventario."""
    valores = np.array(df["Valor"], dtype=float)
    centros = np.array(df["Centro"], dtype=str)

    total = float(np.sum(valores))
    promedio = float(np.mean(valores))
    mediana = float(np.median(valores))
    minimo = float(np.min(valores))
    maximo = float(np.max(valores))
    desviacion = float(np.std(valores))
    proyeccion_5 = float(total * 1.05)

    resumen = (
        df.groupby("Centro", as_index=False)
        .agg(Cantidad=("Valor", "count"), Valor_Total=("Valor", "sum"))
        .sort_values("Centro")
    )
    por_categoria = pd.DataFrame()
    if "Categoria" in df.columns:
        por_categoria = (
            df.groupby("Categoria", as_index=False)
            .agg(Cantidad=("Valor", "count"), Valor_Total=("Valor", "sum"))
            .sort_values("Valor_Total", ascending=False)
        )

    participacion = resumen.copy()
    participacion["Participacion_Valor"] = np.where(
        total > 0,
        participacion["Valor_Total"].to_numpy(dtype=float) / total * 100,
        0,
    )

    return {
        "fuente": df.attrs.get("fuente", "DataFrame"),
        "registros": int(valores.size),
        "centros": int(np.unique(centros).size),
        "total": total,
        "promedio": promedio,
        "mediana": mediana,
        "minimo": minimo,
        "maximo": maximo,
        "desviacion": desviacion,
        "proyeccion_5": proyeccion_5,
        "resumen": resumen,
        "por_categoria": por_categoria,
        "participacion": participacion,
    }


def exportar_resultados(metricas: dict) -> None:
    """Guarda un resumen JSON para que el frontend pueda mostrar indicadores."""
    DATA_DIR.mkdir(exist_ok=True)
    payload = {
        clave: valor
        for clave, valor in metricas.items()
        if clave not in {"resumen", "por_categoria", "participacion"}
    }
    payload["resumen"] = metricas["resumen"].to_dict(orient="records")
    payload["por_categoria"] = metricas["por_categoria"].to_dict(orient="records")
    payload["participacion"] = metricas["participacion"].to_dict(orient="records")

    with open(RESULTADOS, "w", encoding="utf-8") as archivo:
        json.dump(payload, archivo, ensure_ascii=False, indent=2)


def analizar_inventario() -> tuple[pd.DataFrame, dict] | tuple[None, None]:
    """Carga la base y realiza calculos estadisticos requeridos con NumPy."""
    print("=== MODULO II: ANALISIS CON NUMPY ===")
    df = cargar_inventario()
    if df is None:
        return None, None

    df = preparar_inventario(df)
    if df is None or df.empty:
        print("La base no contiene registros validos para analizar.")
        return None, None

    metricas = calcular_metricas(df)
    exportar_resultados(metricas)

    print(f"Fuente de datos: {metricas['fuente']}")
    print(f"Registros: {metricas['registros']:,}")
    print(f"Centros: {metricas['centros']:,}")
    print(f"Valor total: ${metricas['total']:,.0f} COP")
    print(f"Promedio: ${metricas['promedio']:,.0f} COP")
    print(f"Mediana: ${metricas['mediana']:,.0f} COP")
    print(f"Minimo: ${metricas['minimo']:,.0f} COP")
    print(f"Maximo: ${metricas['maximo']:,.0f} COP")
    print(f"Desviacion estandar: ${metricas['desviacion']:,.0f} COP")
    print(f"Proyeccion con incremento del 5%: ${metricas['proyeccion_5']:,.0f} COP")
    print("\nResumen por centro:")
    print(metricas["resumen"].to_string(index=False))
    if not metricas["por_categoria"].empty:
        print("\nResumen por categoria:")
        print(metricas["por_categoria"].to_string(index=False))

    return df, metricas


def generar_graficos(df: pd.DataFrame, metricas: dict) -> None:
    """Genera tres graficos y los exporta en alta resolucion."""
    print("\n=== MODULO III: VISUALIZACION ===")
    GRAFICOS.mkdir(exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid")

    resumen = metricas["resumen"]
    colores = ["#2563eb", "#16a34a", "#f97316", "#7c3aed", "#0f766e"]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.bar(resumen["Centro"], resumen["Cantidad"], color=colores[: len(resumen)], label="Activos")
    ax.set_title("Cantidad de activos registrados por centro")
    ax.set_xlabel("Centro logistico")
    ax.set_ylabel("Cantidad de activos (unidades)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(GRAFICOS / "activos_por_centro.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(
        resumen["Centro"],
        resumen["Valor_Total"],
        marker="o",
        linewidth=2.5,
        color="#dc2626",
        label="Valor total",
    )
    ax.set_title("Valor contable acumulado del inventario por centro")
    ax.set_xlabel("Centro logistico")
    ax.set_ylabel("Valor contable (COP)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(GRAFICOS / "valor_por_centro.png", dpi=200)
    plt.close(fig)

    valores_positivos = np.array(df.loc[df["Valor"] > 0, "Valor"], dtype=float)
    if valores_positivos.size:
        fig, ax = plt.subplots(figsize=(9, 5.5))
        ax.hist(np.log10(valores_positivos), bins=min(12, valores_positivos.size), color="#0891b2", label="Valores")
        ax.set_title("Distribucion de valores del inventario")
        ax.set_xlabel("log10(valor en COP)")
        ax.set_ylabel("Cantidad de registros (unidades)")
        ax.legend()
        fig.tight_layout()
        fig.savefig(GRAFICOS / "distribucion_valores.png", dpi=200)
        plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(
        resumen["Valor_Total"],
        labels=resumen["Centro"],
        autopct="%1.1f%%",
        startangle=90,
        colors=colores[: len(resumen)],
        wedgeprops={"width": 0.42, "edgecolor": "white"},
    )
    ax.set_title("Participacion del valor contable por centro")
    ax.legend(title="Centro logistico", loc="center left", bbox_to_anchor=(1, 0.5))
    fig.tight_layout()
    fig.savefig(GRAFICOS / "participacion_valor_centro.png", dpi=200)
    plt.close(fig)

    por_categoria = metricas.get("por_categoria")
    if por_categoria is not None and not por_categoria.empty:
        fig, ax = plt.subplots(figsize=(10, 5.8))
        ax.barh(
            por_categoria["Categoria"],
            por_categoria["Valor_Total"],
            color="#0f766e",
            label="Valor total",
        )
        ax.set_title("Valor contable acumulado por categoria")
        ax.set_xlabel("Valor contable (COP)")
        ax.set_ylabel("Categoria")
        ax.legend()
        ax.invert_yaxis()
        fig.tight_layout()
        fig.savefig(GRAFICOS / "valor_por_categoria.png", dpi=200)
        plt.close(fig)

    print("Graficos exportados en la carpeta graficos/.")


def main() -> None:
    generar_nomina()
    df, metricas = analizar_inventario()
    if df is not None and metricas is not None:
        generar_graficos(df, metricas)


if __name__ == "__main__":
    main()
