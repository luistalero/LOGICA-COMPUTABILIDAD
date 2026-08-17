# Informe de apoyo — Proyecto Integrador Final

## 1. Empresa y proceso analizado

Para el módulo cuantitativo se utiliza la base de inventario suministrada para la actividad. La base contiene **28.140 registros** y 9 variables. El análisis se centra en la distribución de activos y su valor contable por centro.

## 2. Resultados principales

- Registros analizados: **28.140**.
- Centros identificados: **2** (1001 y 1002).
- Valor contable total: **$165.719.988.779 COP**.
- Valor promedio por registro: **$5.889.125 COP**.
- Mediana: **$417.141 COP**.
- Mínimo: **$0 COP**.
- Máximo: **$45.289.466.320 COP**.
- Proyección del valor total con un incremento del 5%: **$174.005.988.218 COP**.

> **Nota sobre la desviación estándar:** el valor debe tomarse de la ejecución final de `main.py`, ya que depende de los datos efectivamente cargados y de la configuración utilizada por NumPy. Se evita fijar aquí una cifra que pueda diferir de la ejecución reproducible.

## 3. Lectura gerencial

El centro 1001 concentra **19.497 activos (69,3%)** y **$126.429.794.502 COP (76,3%)** del valor contable. El centro 1002 concentra **8.643 activos (30,7%)** y **$39.290.194.277 COP (23,7%)**.

La diferencia entre la media y la mediana es muy grande debido a registros de valor excepcionalmente alto. Por esta razón se presentan ambas medidas y un histograma en escala logarítmica: utilizar únicamente el promedio podría producir una percepción equivocada del valor típico de un activo.

## 4. Utilidad de los cálculos

- **Suma:** determina el valor contable total administrado.
- **Promedio y mediana:** permiten comparar el valor típico y detectar el efecto de valores extremos.
- **Mínimo y máximo:** identifican el rango de valores registrados.
- **Desviación estándar:** cuantifica la dispersión de los valores respecto de la media.
- **Incremento del 5%:** permite simular un escenario sencillo de crecimiento del valor del inventario para apoyar la planeación.

## 5. Visualizaciones

1. `activos_por_centro.png`: compara la cantidad de activos por centro mediante un gráfico de barras.
2. `valor_por_centro.png`: compara el valor contable acumulado por centro mediante un gráfico de barras.
3. `distribucion_valores.png`: muestra la distribución de los valores positivos en escala `log10`, reduciendo el efecto visual de los valores extremos.

## 6. Conclusión

El análisis muestra que el inventario está concentrado principalmente en el centro 1001 tanto por cantidad de activos como por valor contable. La fuerte diferencia entre media y mediana evidencia que existen valores extremos, por lo que la toma de decisiones no debería basarse únicamente en el promedio. NumPy permite realizar los cálculos de forma reproducible y Matplotlib facilita convertirlos en información visual para apoyar la interpretación del inventario.
