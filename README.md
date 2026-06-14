# Sitio web para control de gastos personales

Proyecto local desarrollado en Python 3 utilizando Flask. La aplicacion permite registrar, consultar y analizar gastos personales de forma sencilla.

## Funciones incluidas

- Pagina principal con resumen general de gastos.
- Registro de nuevos gastos mediante formulario.
- Listado de gastos guardados.
- Almacenamiento de datos en archivo CSV.
- Calculo del total gastado.
- Calculo del promedio por gasto.
- Conteo de registros guardados.
- Agrupacion de gastos por categoria usando Pandas.
- Uso de NumPy para calculos numericos.
- Generacion de grafico de gastos por categoria con Matplotlib.
- Separacion del proyecto en rutas, servicios, plantillas y archivos estaticos.

## Librerias utilizadas

- Flask
- Pandas
- NumPy
- Matplotlib

## Como abrirlo en Visual Studio Code

1. Abrir Visual Studio Code.
2. Ir a `File > Open Folder`.
3. Seleccionar la carpeta del proyecto.
4. Abrir una terminal integrada con `Terminal > New Terminal`.

## Como ejecutarlo

En la terminal de Visual Studio Code:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Luego abrir en el navegador:

```text
http://127.0.0.1:5000
```

## Estructura general

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
    │   └── gastos.csv
    ├── static/
    │   ├── css/
    │   │   └── styles.css
    │   └── img/
    └── templates/
        ├── base.html