"""Proyecto Integrador Final - Programación y Análisis de Datos en Python.

Integra:
1. Gestión de nómina con archivos y excepciones.
2. Análisis cuantitativo de inventario con NumPy.
3. Visualización de resultados con Matplotlib.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "inventario.xlsx"
NOMINA = ROOT / "nomina.txt"
GRAFICOS = ROOT / "graficos"


def pedir_float(mensaje, permitir_cero=True):
    """Solicita un número no negativo y controla entradas inválidas."""
    while True:
        try:
            entrada = input(mensaje).strip().replace("$", "").replace(",", "")
            valor = float(entrada)
            if valor < 0 or (not permitir_cero and valor == 0):
                raise ValueError("El valor debe ser mayor o igual a cero.")
            return valor
        except ValueError as exc:
            print(f"Entrada inválida: {exc}")


def generar_nomina():
    """Captura datos, calcula el neto y escribe/lee nomina.txt con with."""
    print("\n=== MÓDULO I: GESTIÓN DE NÓMINA ===")
    empleado = input("Nombre del empleado: ").strip() or "Empleado"
    salario = pedir_float("Salario base (COP): ")
    horas_extras = pedir_float("Pago por horas extras (COP): ")
    deducciones = pedir_float("Deducciones (COP): ")
    bonificaciones = pedir_float("Bonificaciones (COP): ")
    neto = salario + horas_extras + bonificaciones - deducciones

    contenido = (
        "DESPRENDIBLE DE NÓMINA\n"
        "=======================\n"
        f"Empleado: {empleado}\n"
        f"Salario base: ${salario:,.2f} COP\n"
        f"Horas extras: ${horas_extras:,.2f} COP\n"
        f"Bonificaciones: ${bonificaciones:,.2f} COP\n"
        f"Deducciones: ${deducciones:,.2f} COP\n"
        "-----------------------\n"
        f"Neto a pagar: ${neto:,.2f} COP\n"
    )

    try:
        with open(NOMINA, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)
        print("\nArchivo nomina.txt generado correctamente.")

        with open(NOMINA, "r", encoding="utf-8") as archivo:
            contenido_leido = archivo.read()
        print("\n" + contenido_leido)
    except OSError as exc:
        print(f"Error de entrada/salida al manipular nomina.txt: {exc}")


def analizar_inventario():
    """Carga la base y realiza los cálculos estadísticos requeridos con NumPy."""
    print("=== MÓDULO II: ANÁLISIS CON NUMPY ===")

    if not DATA.exists():
        print(f"No se encontró la base de datos: {DATA}")
        print("Coloca el archivo suministrado por el equipo en data/inventario.xlsx.")
        return None

    try:
        df = pd.read_excel(DATA)
    except (OSError, ValueError, ImportError) as exc:
        print(f"No fue posible leer la base de inventario: {exc}")
        return None

    df.columns = [str(c).strip() for c in df.columns]
    if "Valor" not in df.columns:
        print("Error: la base debe contener una columna llamada 'Valor'.")
        return None

    valores = pd.to_numeric(df["Valor"], errors="coerce").fillna(0).to_numpy(dtype=float)
    if valores.size == 0:
        print("La base no contiene registros para analizar.")
        return None

    total = np.sum(valores)
    promedio = np.mean(valores)
    mediana = np.median(valores)
    minimo = np.min(valores)
    maximo = np.max(valores)
    desviacion = np.std(valores)
    incremento_5 = total * 1.05

    print(f"Registros: {len(valores):,}")
    print(f"Valor total: ${total:,.0f} COP")
    print(f"Promedio: ${promedio:,.0f} COP")
    print(f"Mediana: ${mediana:,.0f} COP")
    print(f"Mínimo: ${minimo:,.0f} COP")
    print(f"Máximo: ${maximo:,.0f} COP")
    print(f"Desviación estándar: ${desviacion:,.0f} COP")
    print(f"Proyección con incremento del 5%: ${incremento_5:,.0f} COP")

    if "Centro" in df.columns:
        por_centro = df.assign(Valor=valores).groupby("Centro")["Valor"].agg(["count", "sum"]).sort_index()
        print("\nResumen por centro:")
        print(por_centro.to_string())

    df = df.copy()
    df["Valor"] = valores
    return df


def generar_graficos(df):
    """Genera dos tipos de gráficos y los exporta con savefig()."""
    print("\n=== MÓDULO III: VISUALIZACIÓN ===")
    GRAFICOS.mkdir(exist_ok=True)

    if "Centro" not in df.columns:
        print("No se puede graficar por centro: falta la columna 'Centro'.")
        return

    conteo = df.groupby("Centro").size().sort_index()
    valor_centro = df.groupby("Centro")["Valor"].sum().sort_index()

    # Gráfico 1: barras para comparar cantidades.
    ax = conteo.plot(kind="bar", figsize=(9, 5.5), title="Cantidad de activos registrados por centro")
    ax.set_xlabel("Centro")
    ax.set_ylabel("Cantidad de activos (unidades)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(GRAFICOS / "activos_por_centro.png", dpi=180)
    plt.close()

    # Gráfico 2: barras para comparar valor contable.
    ax = valor_centro.plot(kind="bar", figsize=(9, 5.5), title="Valor contable acumulado del inventario por centro")
    ax.set_xlabel("Centro")
    ax.set_ylabel("Valor contable (COP)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(GRAFICOS / "valor_por_centro.png", dpi=180)
    plt.close()

    # Gráfico 3: histograma para observar la distribución de valores positivos.
    valores_positivos = df.loc[df["Valor"] > 0, "Valor"].to_numpy(dtype=float)
    if valores_positivos.size:
        plt.figure(figsize=(9, 5.5))
        plt.hist(np.log10(valores_positivos), bins=35)
        plt.title("Distribución de valores del inventario (escala log10)")
        plt.xlabel("log10(valor en COP)")
        plt.ylabel("Cantidad de registros (unidades)")
        plt.tight_layout()
        plt.savefig(GRAFICOS / "distribucion_valores.png", dpi=180)
        plt.close()

    print("Gráficos exportados en la carpeta graficos/.")


def main():
    generar_nomina()
    df = analizar_inventario()
    if df is not None:
        generar_graficos(df)


if __name__ == "__main__":
    main()
