# Datos de entrada

El programa busca automaticamente:

1. `data/inventario.xlsx`, si el equipo tiene la base real.
2. `data/inventario_ejemplo.csv`, si no existe el archivo anterior.

La base debe contener al menos:

- `Centro`: centro logistico, sede o area.
- `Valor`: valor contable del activo en COP.

El archivo `data/resultados.json` se genera al ejecutar `main.py` o `app.py`.
