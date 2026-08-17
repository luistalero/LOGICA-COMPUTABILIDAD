# Proyecto Integrador Final - LogiStock S.A.S.

Solucion en Python para la actividad final de **Programacion y Analisis de Datos en Python**.
Integra nomina, analisis cuantitativo de inventario con NumPy y visualizacion gerencial con Matplotlib.

## Cumplimiento del documento

- **Modulo I:** genera `nomina.txt`, lo escribe y lo lee con `with`, valida entradas numericas y controla errores de archivo.
- **Modulo II:** analiza el proceso de inventario con `np.array`, suma, promedio, mediana, minimo, maximo, desviacion estandar y proyeccion del 5%.
- **Modulo III:** exporta graficos en `graficos/` con titulos, ejes, unidades y leyendas.
- **Soporte:** incluye informe, guia de entrega y una interfaz Streamlit para sustentacion.

## Como iniciar el proyecto

1. Instalar Python 3.10 o superior.
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar la version de consola:

```bash
python main.py
```

4. Ejecutar el frontend elegante para presentar:

```bash
streamlit run app.py
```

Streamlit abrira una URL local, normalmente `http://localhost:8501`.

## Datos

El programa busca primero `data/inventario.xlsx`. Si ese archivo no existe, usa
`data/inventario_ejemplo.csv`, incluido para que el proyecto sea reproducible.

Para entregar con la base real del equipo, coloca el archivo como:

```text
data/inventario.xlsx
```

La base debe tener al menos estas columnas:

- `Centro`: centro logistico o area responsable.
- `Valor`: valor contable del activo en COP.

## Archivos generados

- `nomina.txt`: desprendible de nomina.
- `graficos/activos_por_centro.png`: grafico de barras.
- `graficos/valor_por_centro.png`: grafico de lineas.
- `graficos/distribucion_valores.png`: histograma.
- `graficos/participacion_valor_centro.png`: grafico de participacion porcentual.
- `graficos/valor_por_categoria.png`: grafico por categoria, cuando la base contiene esa columna.
- `data/resultados.json`: indicadores usados por el frontend.

## Entrega sugerida

Comprimir la carpeta del proyecto con:

- `main.py`
- `app.py`
- `requirements.txt`
- `README.md`
- `nomina.txt`
- `data/`
- `graficos/`
- `docs/`
