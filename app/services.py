from pathlib import Path
from uuid import uuid4

######PARA FECHAS
from datetime import datetime 

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "gastos.csv"
CHART_FILE = BASE_DIR / "static" / "img" / "gastos_por_categoria.png"
PRESUPUESTO_FILE = BASE_DIR / "data" / "presupuesto.txt"

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
##################################################################


# def validar_campos(fecha, categoria, descripcion, monto):   
#     errores = []

#     if fecha.strip() == "" or fecha == False:
#         errores.append("Fecha no se puede dejar vacío")
    
#     else: ##if the format is incorrect
#         print ("Favor escribirlo como ")
    
#     categorias = categoria 
#     if categoria.strip() == "":
        


#     return errores
# errores = validar_campos
# print(f"{errores}")


# def mayor_gasto(gastos):
    
#     df = pd.read_csv(DATA_FILE)
    
   
# mayor_gasto()

# #     return categoria


def promedio_mensual(gastos):
    
    df = pd.read_csv(DATA_FILE)

    promedio = df

    return promedio

########################################### Aaron abajo
def establecer_presupuesto():
    while True:
        try:
            nuevo_presupuesto = float(input("Digite su nuevo presupuesto: "))
            break
        except: 
            print("Presupuesto invalido, por favor intentelo de nuevo\n")
    with open (PRESUPUESTO_FILE, 'w') as presupuesto:
        presupuesto.write(str(nuevo_presupuesto))


def obtener_presupuesto():
    gastos = cargar_gastos()
    total = float(gastos["monto"].sum()) if not gastos.empty else 0
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(columns=COLUMNAS).to_csv(DATA_FILE, index=False)
    if PRESUPUESTO_FILE.exists() and PRESUPUESTO_FILE.stat().st_size > 0:
        with open (PRESUPUESTO_FILE, 'r') as archivo:
            presupuesto = archivo.read()
        presupuesto_num = float(presupuesto)
        porcentaje_gastado = (total / presupuesto_num) * 100
        if total > presupuesto_num:
            numeros_rojos = True
        else:
            numeros_rojos = False
        return {
        "total": total,
        "presupuesto": presupuesto_num,
        "porcentaje": porcentaje_gastado,
        "rojo": numeros_rojos} 
    else:
        establecer_presupuesto()
        return obtener_presupuesto()

########################################### Aaron arriba
    
def guardar_presupuesto(valor):
    with open(PRESUPUESTO_FILE, "w") as archivo:
        archivo.write(str(valor))
