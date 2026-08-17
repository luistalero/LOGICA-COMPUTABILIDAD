# Informe de apoyo — Proyecto Integrador Final

## Empresa y proceso analizado
Para el módulo cuantitativo se utiliza la base de inventario suministrada por el equipo. La base contiene **28.140 registros** y 9 variables. El análisis se centra en la distribución de activos y su valor contable por centro.

## Resultados principales
- Registros analizados: **28.140**.
- Centros identificados: **2** (1001 y 1002).
- Valor contable total: **$165.719.988.779 COP**.
- Valor promedio por registro: **$5.889.125 COP**.
- Mediana: **$417.141 COP**.
- Desviación estándar: **$279.527.034 COP**.
- Mínimo: **$0 COP**.
- Máximo: **$45.289.466.320 COP**.
- Proyección del valor total con un incremento del 5%: **$174.005.988.218 COP**.

## Lectura gerencial
El centro 1001 concentra **19.497 activos (69,3%)** y **$126.429.794.502 COP (76,3%)** del valor contable. El centro 1002 concentra **8.643 activos (30,7%)** y **$39.290.194.277 COP (23,7%)**.

La diferencia entre media ($5.889.125) y mediana ($417.141) es muy grande debido a registros de valor excepcionalmente alto. Por eso se incluyen ambas medidas y un histograma en escala logarítmica: usar solamente el promedio podría dar una percepción equivocada del valor típico de un activo.

## Utilidad de los cálculos
- **Suma:** determina el valor contable total administrado.
- **Promedio y mediana:** permiten comparar el valor típico y detectar sesgos producidos por valores extremos.
- **Mínimo y máximo:** identifican el rango de valores registrados.
- **Desviación estándar:** cuantifica la dispersión de los valores.
- **Incremento del 5%:** permite simular un escenario sencillo de crecimiento del valor del inventario para apoyar la planeación.

## Gráficos
1. `activos_por_centro.png`: compara la cantidad de activos por centro.
2. `valor_por_centro.png`: compara el valor contable acumulado por centro.
3. `distribucion_valores.png`: muestra la distribución de los valores positivos en escala log10 para reducir el efecto visual de los valores extremos.
