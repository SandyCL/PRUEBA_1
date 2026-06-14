# Sitio web para control de gastos personales

Proyecto local en Python 3 con Flask para registrar gastos personales, revisar resumenes y controlar cobros fijos mensuales.

## Funciones incluidas

- Registro de gastos con fecha validada en formato `AAAA-MM-DD`.
- Listado de gastos ordenados por fecha.
- Resumen de gastos con Pandas y NumPy.
- Grafico de gastos por categoria con Matplotlib.
- Cobros fijos mensuales, como suscripciones o servicios.
- Calculo de proximas fechas de cobro segun el dia configurado.
- Total mensual estimado de cobros fijos activos.

## Como abrirlo en Visual Studio Code

1. Abrir Visual Studio Code.
2. Ir a `File > Open Folder`.
3. Seleccionar la carpeta del proyecto.
4. Abrir una terminal integrada.

## Como ejecutarlo

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py

```text
control_gastos_flask/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── app/
    ├── __init__.py
    ├── routes.py
    ├── services.py
    ├── data/
    │   ├── gastos.csv
    │   └── cobros_fijos.csv
    ├── static/
    │   └── css/
    │       └── styles.css
    └── templates/
        ├── base.html
        ├── index.html
        ├── gastos.html
        ├── nuevo_gasto.html
        ├── cobros_fijos.html
        └── resumen.
```