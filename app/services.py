from pathlib import Path
from uuid import uuid4

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
    nuevo = pd.DataFrame(
        [
            {
                "id": str(uuid4()),
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

##Logica Pandas, CSV, calculos, graficos, etc