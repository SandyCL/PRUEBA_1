from flask import Blueprint, redirect, render_template, request, url_for

from app.services import (
    agregar_gasto,
    cargar_gastos,
    crear_grafico_categorias,
    obtener_resumen,
)


main = Blueprint("main", __name__)


@main.route("/")
def index():
    gastos = cargar_gastos()
    resumen = obtener_resumen(gastos)
    ultimos_gastos = gastos.tail(5).to_dict("records")
    return render_template("index.html", resumen=resumen, ultimos_gastos=ultimos_gastos)


@main.route("/gastos")
def gastos():
    gastos_df = cargar_gastos()
    registros = gastos_df.sort_values("fecha", ascending=False).to_dict("records")
    return render_template("gastos.html", gastos=registros)


@main.route("/gastos/nuevo", methods=["GET", "POST"])
def nuevo_gasto():
    if request.method == "POST":
        agregar_gasto(
            fecha=request.form["fecha"],
            categoria=request.form["categoria"],
            descripcion=request.form["descripcion"],
            monto=request.form["monto"],
        )
        return redirect(url_for("main.gastos"))

    return render_template("nuevo_gasto.html")


@main.route("/resumen")
def resumen():
    gastos = cargar_gastos()
    resumen_data = obtener_resumen(gastos)
    grafico = crear_grafico_categorias(gastos)
    categorias = resumen_data["por_categoria"].to_dict("records")
    return render_template(
        "resumen.html",
        resumen=resumen_data,
        categorias=categorias,
        grafico=grafico,
    )




