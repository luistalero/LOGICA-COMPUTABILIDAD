# Informe de apoyo - Proyecto Integrador Final

## 1. Empresa y proceso analizado

La empresa seleccionada para contextualizar el proyecto es **LogiStock S.A.S.**, una organizacion dedicada a la administracion y control de inventarios empresariales. El proceso operativo analizado es el **control de inventario por centro logistico**, porque permite identificar donde se concentra la mayor cantidad de activos y el mayor valor contable.

## 2. Modulo I: gestion de nomina

El sistema genera un desprendible de pago para un empleado de la empresa. Se solicitan salario base, horas extras, deducciones y bonificaciones. Con estos datos se calcula el neto a pagar:

```text
neto = salario base + horas extras + bonificaciones - deducciones
```

El archivo `nomina.txt` se escribe y se lee usando la sentencia `with`, lo que garantiza el cierre correcto del recurso. El programa valida que los valores monetarios sean numericos y no negativos, y controla excepciones de entrada/salida durante la manipulacion del archivo.

## 3. Modulo II: analisis cuantitativo con NumPy

El inventario se modela con arreglos de NumPy a partir de la columna `Valor`. Las metricas calculadas son:

- **Suma:** determina el valor contable total administrado.
- **Promedio:** estima el valor medio por activo.
- **Mediana:** muestra el valor central y reduce el efecto de valores extremos.
- **Minimo y maximo:** delimitan el rango de valores registrados.
- **Desviacion estandar:** mide la dispersion de los valores frente al promedio.
- **Proyeccion del 5%:** simula un escenario de incremento del valor total para apoyar la planeacion.

Estas metricas ayudan a priorizar controles, auditorias y decisiones de reposicion en los centros donde se concentra el mayor valor.

## 4. Modulo III: visualizacion gerencial

El proyecto genera varias visualizaciones para fortalecer el apoyo visual:

1. `activos_por_centro.png`: grafico de barras para comparar cantidad de activos.
2. `valor_por_centro.png`: grafico de lineas para comparar valor contable acumulado.
3. `distribucion_valores.png`: histograma para observar la distribucion de valores.
4. `participacion_valor_centro.png`: grafico circular tipo dona para observar la participacion porcentual del valor por centro.
5. `valor_por_categoria.png`: grafico de barras horizontales para identificar las categorias con mayor peso contable.

Cada grafico incluye titulo, etiquetas de ejes con unidades y leyenda. Las imagenes se exportan en alta resolucion mediante `savefig()`.

## 5. Analisis critico

La lectura conjunta de los graficos permite identificar los centros con mayor concentracion de activos y de valor contable. Si un centro tiene muchos activos pero un valor menor, la decision puede enfocarse en control operativo. Si un centro tiene menos activos pero mayor valor, la decision debe priorizar aseguramiento, mantenimiento y seguimiento financiero.

La comparacion entre promedio y mediana es especialmente util: cuando existe una diferencia grande, significa que hay activos de valor muy alto que distorsionan el promedio. Por eso el informe recomienda revisar varias metricas y no basar la decision en un solo indicador.

## 6. Conclusiones

El proyecto cumple con la integracion solicitada: administra nomina con persistencia en archivo, analiza inventario con NumPy y transforma las metricas en graficos gerenciales. La interfaz `app.py` facilita la sustentacion porque permite filtrar datos, mostrar indicadores, presentar graficos dinamicos y navegar los modulos en una experiencia visual ordenada.
