from pathlib import Path
from uuid import uuid4

######PARA FECHAS
from datetime import datetime 

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "gastos.csv"
CHART_FILE = BASE_DIR / "static" / "img" / "gastos_por_categoria.png"

COLUMNAS = ["id", "fecha", "categoria", "descripcion", "monto"]


def cargar_gastos():
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(columns=COLUMNAS).to_csv(DATA_FILE, index=False)

    gastos = pd.read_csv(DATA_FILE)

    if gastos.empty:
        return pd.DataFrame(columns=COLUMNAS)

    gastos["fecha"] = pd.to_datetime(gastos["fecha"]).dt.date
    gastos["monto"] = pd.to_numeric(gastos["monto"], errors="coerce").fillna(0)
    return gastos


def agregar_gasto(fecha, categoria, descripcion, monto):
    gastos = cargar_gastos()

    nuevo_id = len(gastos) +1

    nuevo = pd.DataFrame(
        [
            {
                "id": nuevo_id, ### agarrar ultimo indice 
                "fecha": fecha,
                "categoria": categoria.strip().title(),
                "descripcion": descripcion.strip(),
                "monto": float(monto),
            }
        ]
    )

    gastos = pd.concat([gastos, nuevo], ignore_index=True)
    gastos.to_csv(DATA_FILE, index=False)


def obtener_resumen(gastos):
    total = float(gastos["monto"].sum()) if not gastos.empty else 0
    promedio = float(np.mean(gastos["monto"])) if not gastos.empty else 0
    cantidad = int(len(gastos))

    if gastos.empty:
        por_categoria = pd.DataFrame(columns=["categoria", "monto"])
    else:
        por_categoria = (
            gastos.groupby("categoria", as_index=False)["monto"]
            .sum()
            .sort_values("monto", ascending=False)
        )

    return {
        "total": total,
        "promedio": promedio,
        "cantidad": cantidad,
        "por_categoria": por_categoria,
    }


def crear_grafico_categorias(gastos):
    CHART_FILE.parent.mkdir(parents=True, exist_ok=True)

    if gastos.empty:
        if CHART_FILE.exists():
            CHART_FILE.unlink()
        return None

    por_categoria = gastos.groupby("categoria")["monto"].sum().sort_values()

    plt.figure(figsize=(8, 4.5))
    plt.barh(por_categoria.index, por_categoria.values, color="#2f7d6d")
    plt.xlabel("Monto")
    plt.ylabel("Categoria")
    plt.title("Gastos por categoria")
    plt.tight_layout()
    plt.savefig(CHART_FILE)
    plt.close()

    return "img/gastos_por_categoria.png"


############################################Jeremi
def eliminar_gasto(id):
    gastos = cargar_gastos()
    gastos = gastos[gastos["id"] != id]
    gastos.to_csv(DATA_FILE, index=False)


def actualizar_gasto(id, fecha, categoria, descripcion, monto):
    gastos = cargar_gastos()

    gastos.loc[gastos["id"] == id, "fecha"] = fecha
    gastos.loc[gastos["id"] == id, "categoria"] = categoria.strip().title()
    gastos.loc[gastos["id"] == id, "descripcion"] = descripcion.strip()
    gastos.loc[gastos["id"] == id, "monto"] = float(monto)

    gastos.to_csv(DATA_FILE, index=False)


def filtrar_gastos(gastos, fecha_inicio=None, fecha_fin=None, categoria=None):

    if fecha_inicio:
        gastos = gastos[gastos["fecha"] >= fecha_inicio]

    if fecha_fin:
        gastos = gastos[gastos["fecha"] <= fecha_fin]

    if categoria:
        gastos = gastos[gastos["categoria"] == categoria]

    return gastos
################################################################## SANDY

def validar_campos(fecha, categoria, descripcion, monto):
    errores = []

    try:
        datetime.strptime(fecha, '%y-%m-%d')
    except (ValueError, TypeError):
        errores.append("Introducir la fecha en formato AAAA-MM-DD.")
    
    if categoria.strip() == "":
        errores.append("Favor especificar la categoría.")
    
    if descripcion.strip() == "":
        errores.append("Debe de añadir una descripción.")
    
    try: 
        monto = float(monto)
        if monto <= 0:
            errores.append("Monto inválido, debe ser mayor a 0.")
    
    except (ValueError, TypeError):
        errores.append("El monto debe ser en números válidos.")
    
    return errores


def obtener_mayor_categoria(gastos):
    if gastos.empty: 
        return None
    
    resultado = []
    
    by_categoria = gastos.groupby('categoria')['monto'].sum()
    top3 = by_categoria.nlargest(3)
    
    print("TOP 3 CATEGORÍAS DE GASTOS")

    for categoria, monto in top3.items():
        resultado.append(f"{categoria}: ₵{monto:.2f}")

    
    return resultado

    
def calcular_promedio_mensual(gastos):
    gastos = cargar_gastos()

    if gastos.empty: 
        return None

    gastos  = gastos.groupby['fecha']('%m').mean()
    
    return gastos 
    
##def cargar_gastos():
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(columns=COLUMNAS).to_csv(DATA_FILE, index=False)

    gastos = pd.read_csv(DATA_FILE)

    if gastos.empty:
        return pd.DataFrame(columns=COLUMNAS)

    gastos["fecha"] = pd.to_datetime(gastos["fecha"]).dt.date
    gastos["monto"] = pd.to_numeric(gastos["monto"], errors="coerce").fillna(0)
    return gastos


# def calcular_promedio_mensual(gastos):
#     if gastos.empty:
#         return None

#     gastos["fecha"] = pd.to_datetime(gastos["fecha"])
#     gastos["mes"] = gastos["fecha"].dt.to_period("M")

#     promedio_por_mes = gastos.groupby("mes", as_index=False)["monto"].mean()

#     return promedio_por_mes.to_dict("records")