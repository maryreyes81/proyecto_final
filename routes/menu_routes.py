# routes/menu_routes.py

from flask import Blueprint, request, redirect, url_for, render_template
from models.menu import Menu

menu_bp = Blueprint("menu", __name__)
menu_model = Menu()


@menu_bp.route("/menu", methods=["GET"])
def listar_menu():
    items = menu_model.obtener_menu()
    return render_template("menu.html", menu_items=items)


@menu_bp.route("/menu/crear_form", methods=["POST"])
def crear_menu_form():
    nombre = request.form.get("nombre")
    precio = request.form.get("precio")

    try:
        precio = float(precio)
    except (TypeError, ValueError):
        precio = 0.0

    menu_model.agregar_producto(nombre, precio)
    return redirect(url_for("index"))


@menu_bp.route("/menu/eliminar/<int:item_id>", methods=["POST"])
def eliminar_menu_item(item_id):
    menu_model.eliminar_producto(item_id)
    return redirect(url_for("index"))


@menu_bp.route("/menu/editar/<int:item_id>", methods=["GET"])
def editar_menu_item(item_id):
    item = menu_model.obtener_por_id(item_id)
    if not item:
        return redirect(url_for("index"))
    return render_template("editar_menu.html", item=item)


@menu_bp.route("/menu/actualizar_form", methods=["POST"])
def actualizar_menu_form():
    item_id = request.form.get("id")
    nombre = request.form.get("nombre")
    precio = request.form.get("precio")

    try:
        item_id = int(item_id)
        precio = float(precio)
    except (TypeError, ValueError):
        return redirect(url_for("index"))

    menu_model.actualizar_producto(item_id, nombre, precio)
    return redirect(url_for("index"))

