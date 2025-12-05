"""
menu_routes.py
---------------
Rutas Flask para manejar el menú de productos de Happy Burger.
"""

from flask import Blueprint, request, jsonify
from models.menu import Menu

# Crear Blueprint
menu_bp = Blueprint("menu", __name__)

# Instancia del modelo
menu_model = Menu()


@menu_bp.route("/menu", methods=["GET"])
def obtener_menu():
    """
    GET /menu
    Obtiene todos los productos del menú.
    """
    productos = menu_model.obtener_todos()
    return jsonify(productos), 200


@menu_bp.route("/menu/<string:clave>", methods=["GET"])
def obtener_producto(clave):
    """
    GET /menu/<clave>
    Obtiene un producto del menú por su clave.
    """
    producto = menu_model.obtener_por_clave(clave)
    if producto:
        return jsonify(producto), 200
    return jsonify({"error": "Producto no encontrado"}), 404


@menu_bp.route("/menu", methods=["POST"])
def crear_producto():
    """
    POST /menu
    Crea un nuevo producto del menú.

    Espera JSON:
    {
        "clave": "H01",
        "nombre": "Hamburguesa Clásica",
        "precio": 89.50
    }
    """
    data = request.json

    menu_model.agregar_producto(
        data["clave"],
        data["nombre"],
        data["precio"]
    )

    return jsonify({"mensaje": "Producto agregado al menú"}), 201


@menu_bp.route("/menu/<string:clave>", methods=["PUT"])
def actualizar_producto(clave):
    """
    PUT /menu/<clave>
    Actualiza un producto del menú.
    """
    data = request.json

    menu_model.actualizar_producto(
        clave,
        data.get("nombre"),
        data.get("precio")
    )

    return jsonify({"mensaje": "Producto actualizado correctamente"}), 200


@menu_bp.route("/menu/<string:clave>", methods=["DELETE"])
def eliminar_producto(clave):
    """
    DELETE /menu/<clave>
    Elimina un producto del menú por su clave.
    """
    menu_model.eliminar_producto(clave)
    return jsonify({"mensaje": "Producto eliminado del menú"}), 200
