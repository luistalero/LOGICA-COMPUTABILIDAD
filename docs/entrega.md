# Guia de entrega y sustentacion

## Ejecucion de consola

1. Instalar dependencias:

```bash
pip install -r requirements.txt
```

2. Ejecutar:

```bash
python main.py
```

Durante la ejecucion se debe ingresar la informacion de nomina. Luego el programa analiza el inventario y genera los graficos.

## Ejecucion del frontend

Para abrir la interfaz de presentacion:

```bash
streamlit run app.py
```

La aplicacion muestra cuatro pestañas: nomina, inventario, graficos y checklist de entrega.

## Evidencias esperadas

- Captura y validacion de datos de nomina.
- Generacion y lectura de `nomina.txt` mediante `with`.
- Manejo de excepciones con `try-except`.
- Conversion de datos del inventario a arreglos NumPy.
- Calculos estadisticos y proyeccion porcentual.
- Generacion de al menos dos tipos de graficos con Matplotlib.
- Exportacion de imagenes mediante `savefig()`.
- Informe con interpretacion gerencial.

## Contenido del archivo comprimido

- `main.py`
- `app.py`
- `requirements.txt`
- `README.md`
- `nomina.txt`
- `data/`
- `graficos/`
- `docs/`

Si se usa la base real del equipo, debe ubicarse en `data/inventario.xlsx` antes de comprimir.
