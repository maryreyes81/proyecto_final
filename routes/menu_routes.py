# routes/menu_routes.py

from flask import Blueprint, request, redirect, url_for, render_template
from models.menu import Menu

menu_bp = Blueprint("menu", __name__)
menu_model = Menu()


@menu_bp.route("/menu", methods=["GET"])
def listar_menu():
    """
    Página para ver el menú en una vista aparte (opcional).
    """
    items = menu_model.obtener_menu()
    return render_template("menu.html", menu_items=items)


@menu_bp.route("/menu/crear_form", methods=["POST"])
def crear_producto_form():
    """
    Recibe el formulario del index.html para agregar un producto al menú.
    """
    nombre = request.form.get("nombre")
    precio = request.form.get("precio")

    try:
        precio = float(precio)
    except (TypeError, ValueError):
        precio = 0.0

    menu_model.agregar_producto(nombre, precio)
    # Después de crear, regresa al index
    return redirect(url_for("index"))


@menu_bp.route("/menu/eliminar/<int:producto_id>", methods=["POST"])
def eliminar_producto(producto_id):
    """
    Eliminar un producto del menú.
    """
    menu_model.eliminar_producto(producto_id)
    return redirect(url_for("index"))
