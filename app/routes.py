from flask import Blueprint, redirect, render_template, request, url_for

from app.services import (
    agregar_gasto,
    calcular_promedio_mensual,
    cargar_gastos,
    comparar_gastos_por_mes,
    crear_grafico_categorias,
    crear_grafico_comparacion_meses,
    obtener_resumen,
    obtener_mayor_categoria,
    eliminar_gasto,
    actualizar_gasto,
    obtener_presupuesto,
    guardar_presupuesto
    
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


@main.route("/resumen/mayor-categoria")
def mayor_categoria():
    gastos = cargar_gastos()
    resumen_data = obtener_resumen(gastos)
    grafico = crear_grafico_categorias(gastos)
    categorias = resumen_data["por_categoria"].to_dict("records")
    mayor_categoria_data = obtener_mayor_categoria(gastos)

    return render_template(
        "resumen.html",
        resumen=resumen_data,
        categorias=categorias,
        grafico=grafico,
        mayor_categoria=mayor_categoria_data,
    )


@main.route("/resumen/promedio-mensual")
def promedio_mensual():
    gastos = cargar_gastos()
    resumen_data = obtener_resumen(gastos)
    grafico = crear_grafico_categorias(gastos)
    categorias = resumen_data["por_categoria"].to_dict("records")
    promedio_mensual_data = calcular_promedio_mensual(gastos)

    return render_template(
        "resumen.html",
        resumen=resumen_data,
        categorias=categorias,
        grafico=grafico,
        promedio_mensual=promedio_mensual_data,
    )


@main.route("/resumen/comparar-meses")
def comparar_meses():
    gastos = cargar_gastos()
    resumen_data = obtener_resumen(gastos)
    grafico = crear_grafico_categorias(gastos)
    categorias = resumen_data["por_categoria"].to_dict("records")
    comparacion_meses_data = comparar_gastos_por_mes(gastos)
    grafico_comparacion_meses = crear_grafico_comparacion_meses(gastos)

    return render_template(
        "resumen.html",
        resumen=resumen_data,
        categorias=categorias,
        grafico=grafico,
        comparacion_meses=comparacion_meses_data,
        grafico_comparacion_meses=grafico_comparacion_meses,
    )

#######################################JEREMI

@main.route("/gastos/eliminar/<int:id>")
def eliminar_gasto_route(id):
    eliminar_gasto(id)
    return redirect(url_for("main.gastos"))


@main.route("/gastos/editar/<int:id>", methods=["GET", "POST"])
def editar_gasto(id):
    gastos = cargar_gastos()
    gasto = gastos[gastos["id"] == id].iloc[0]

    if request.method == "POST":
        actualizar_gasto(
            id,
            request.form["fecha"],
            request.form["categoria"],
            request.form["descripcion"],
            request.form["monto"],
        )
        return redirect(url_for("main.gastos"))

    return render_template("editar_gasto.html", gasto=gasto)


from datetime import datetime
@main.route("/gastos/filtrar")
def filtrar_gastos_route():
    gastos_df = cargar_gastos()
    
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")
    categoria = request.args.get("categoria")

    if fecha_inicio:
        fecha_inicio_date = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        gastos_df = gastos_df[gastos_df["fecha"] >= fecha_inicio_date]

    if fecha_fin:
        fecha_fin_date = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        gastos_df = gastos_df[gastos_df["fecha"] <= fecha_fin_date]

    if categoria:
        gastos_df = gastos_df[gastos_df["categoria"] == categoria]

    registros = gastos_df.sort_values("fecha", ascending=False).to_dict("records")
    
    return render_template(
        "gastos.html",
        gastos=registros,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        categoria=categoria
    )


#################################################### Aaron abajo
@main.route("/presupuesto")
def presupuesto_mensual():
    presupuesto_mes = obtener_presupuesto()
    return render_template("presupuesto.html", pm=presupuesto_mes)

@main.route("/actualizar_presupuesto", methods=["POST"])
def actualizar_presupuesto():

    nuevo_presupuesto = request.form["presupuesto"]

    guardar_presupuesto(nuevo_presupuesto)

    return "OK"
#################################################### Aaron arriba
