"""
pedido_routes.py
----------------
Rutas Flask para manejar los pedidos en Happy Burger.
Incluye operaciones CRUD y visualización detallada con JOIN.
"""

from flask import Blueprint, request, jsonify
from models.pedido import Pedido

# Crear Blueprint
pedido_bp = Blueprint("pedido", __name__)

# Instancia del modelo
pedido_model = Pedido()


@pedido_bp.route("/pedidos", methods=["GET"])
def obtener_pedidos():
    """
    GET /pedidos
    Obtiene todos los pedidos (sin detalle).
    """
    pedidos = pedido_model.obtener_todos()
    return jsonify(pedidos), 200


@pedido_bp.route("/pedidos/detalle", methods=["GET"])
def obtener_pedidos_detalle():
    """
    GET /pedidos/detalle
    Obtiene todos los pedidos con JOIN de Clientes y Menu.
    """
    pedidos = pedido_model.obtener_todos_con_detalle()
    return jsonify(pedidos), 200


@pedido_bp.route("/pedidos/<int:numero_pedido>", methods=["GET"])
def obtener_pedido(numero_pedido):
    """
    GET /pedidos/<numero_pedido>
    Obtiene un pedido por su número (sin detalle).
    """
    pedido = pedido_model.obtener_por_numero(numero_pedido)
    if pedido:
        return jsonify(pedido), 200
    return jsonify({"error": "Pedido no encontrado"}), 404


@pedido_bp.route("/pedidos/<int:numero_pedido>/detalle", methods=["GET"])
def obtener_pedido_detalle(numero_pedido):
    """
    GET /pedidos/<numero_pedido>/detalle
    Obtiene un solo pedido con JOIN (cliente + producto).
    """
    pedido = pedido_model.obtener_por_numero_con_detalle(numero_pedido)
    if pedido:
        return jsonify(pedido), 200
    return jsonify({"error": "Pedido no encontrado"}), 404


@pedido_bp.route("/pedidos", methods=["POST"])
def crear_pedido():
    """
    POST /pedidos
    Crea un nuevo pedido.

    Espera JSON:
    {
        "cliente": "C01",
        "producto": "H01",
        "precio": 89.50
    }
    """
    data = request.json

    try:
        numero = pedido_model.crear_pedido(
            cliente=data["cliente"],
            producto=data["producto"],
            precio=float(data["precio"])
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "mensaje": "Pedido creado exitosamente",
        "numero_pedido": numero
    }), 201


@pedido_bp.route("/pedidos/<int:numero_pedido>", methods=["DELETE"])
def cancelar_pedido(numero_pedido):
    """
    DELETE /pedidos/<numero_pedido>
    Cancela (elimina) un pedido.
    """
    pedido_model.cancelar_pedido(numero_pedido)
    return jsonify({"mensaje": "Pedido cancelado correctamente"}), 200
