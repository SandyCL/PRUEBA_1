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
MONTHLY_COMPARISON_CHART_FILE = BASE_DIR / "static" / "img" / "comparacion_gastos_mes.png"
PRESUPUESTO_CHART_FILE = BASE_DIR / "static" / "img" / "Analisis_de_presupuesto.png"
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

def validar_campos_completos(fecha, categoria, descripcion, monto):
    if fecha == "" or categoria == "" or descripcion == "" or monto == "":
        return False
    return True 

def verificar_monto_positivo(monto):
    try:
        if float(monto) < 0:
            return False 
        return True 
    except:
        return False

def buscar_por_descripcion(texto_buscado):
    gastos_df = cargar_gastos()
    lista_gastos = gastos_df.to_dict("records")
    resultados = []
    for gasto in lista_gastos:
        descripcion_gasto = gasto["descripcion"].lower()
        termino_buscado = texto_buscado.lower()
        if termino_buscado in descripcion_gasto:
            resultados.append(gasto)
    return resultados


def agregar_gasto(fecha, categoria, descripcion, monto):
    gastos = cargar_gastos()

    nuevo_id = int(gastos["id"].max()) + 1 if not gastos.empty else 1

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


############################################ JEREMI
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

    gastos['fecha']  = pd.to_datetime(gastos['fecha']) ##using pandas, convert 'fechas' to format datetime
    gastos['mes'] = gastos['fecha'].dt.to_period('M')##extract the month from 'fechas'

    promedio = gastos.groupby('mes')['monto'].mean()

    p_mensual = []

    guide = str("MES >>> CANTIDAD")
    p_mensual.append(guide)
     
    
    for mes, value in promedio.items(): 
        result = f"{mes.month} >>> ₵{value:.2f}"
        p_mensual.append(result)
    

    return p_mensual


def comparar_gastos_por_mes(gastos):
    
    if gastos.empty: 
        return None

    lista = []

    gastos['fecha']  = pd.to_datetime(gastos['fecha']) 
    gastos['mes'] = gastos['fecha'].dt.to_period('M') 

    gastoXmes = gastos.groupby('mes')['monto'].sum().sort_values(ascending=False) ##sum of all month  + sortes from small to big

    title = str('MES >>> CANTIDAD')
    lista.append(title)

    for mes, monto in gastoXmes.items():
        result= f"{mes.month} >>> ₵{monto:.2f}"
        lista.append(result)
    
    return lista

def datos_gastosXmes(gastos):
    gastos['fecha']  = pd.to_datetime(gastos['fecha']) 
    gastos['mes'] = gastos['fecha'].dt.to_period('M') 

    gastoXmes = gastos.groupby('mes')['monto'].sum() #

    return gastoXmes

def crear_grafico_comparacion_meses(gastos):
    gastoXmes = datos_gastosXmes(gastos)

    if gastoXmes is None:
        return 
    
    mes = gastoXmes.index.astype(str)
    monto = gastoXmes.values

    plt.figure(figsize=(8, 4.5))
    plt.barh(mes,monto,color=("#004a98", "#1A1919", "#f2e860"))
    plt.title('COMPARACIÓN DE GASTOS POR MES')
    plt.xlabel("MONTO")
    plt.ylabel("MES")
    plt.tight_layout()
    plt.savefig(MONTHLY_COMPARISON_CHART_FILE)
    plt.close()


    # Espacio reservado para crear el grafico de comparacion de gastos por mes.
    # Cuando implementes la logica con Matplotlib, guarda la imagen en
    # MONTHLY_COMPARISON_CHART_FILE y retorna "img/comparacion_gastos_mes.png".
    return "img/comparacion_gastos_mes.png"

########################################### AARON
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
            restante = 0 
            Deficit = total - presupuesto_num
        else:
            numeros_rojos = False
            Deficit = 0
            restante = presupuesto_num - total
        datos_numéricos = [total,restante]
        datos_literales = ["Gastos totales","Presupuesto Restante"]
        piechart_dictionary = {"Numeros":datos_numéricos,"Títulos":datos_literales}
        DFdictionary = pd.DataFrame(piechart_dictionary)
        plt.pie(x = DFdictionary.Numeros, labels=DFdictionary.Títulos, colors = ["#2F7D6D","#E37971"], autopct='%1.1f%%')
        plt.title('Análisis de presupuesto')
        plt.savefig(PRESUPUESTO_CHART_FILE, bbox_inches='tight', dpi=100)
        plt.close()
        return {
        "total": total,
        "presupuesto": presupuesto_num,
        "porcentaje": porcentaje_gastado,
        "rojo": numeros_rojos,
        "deficit": Deficit} 
    else:
        establecer_presupuesto()
        return obtener_presupuesto()

def guardar_presupuesto(valor):
    with open(PRESUPUESTO_FILE, "w") as archivo:
        archivo.write(str(valor))
