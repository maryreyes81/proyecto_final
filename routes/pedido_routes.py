"""
pedido_routes.py
----------------
Rutas Flask para manejar pedidos.
"""

from flask import Blueprint, request, jsonify
from models.pedido import Pedido

pedido_bp = Blueprint("pedido", __name__)
pedido_model = Pedido()


@pedido_bp.route("/pedidos", methods=["GET"])
def obtener_pedidos():
    pedidos = pedido_model.obtener_todos()
    resultado = [
        {
            "id": p[0],
            "pedido": p[1],
            "cliente_id": p[2],
            "producto_id": p[3],
            "precio": p[4],
        }
        for p in pedidos
    ]
    return jsonify(resultado), 200


@pedido_bp.route("/pedidos/detalle", methods=["GET"])
def obtener_pedidos_con_detalle():
    filas = pedido_model.obtener_todos_con_detalle()
    resultado = [
        {
            "numero_pedido": f[0],
            "cliente_nombre": f[1],
            "producto_nombre": f[2],
            "total_pedido": f[3],
        }
        for f in filas
    ]
    return jsonify(resultado), 200


@pedido_bp.route("/pedidos", methods=["POST"])
def crear_pedido():
    data = request.get_json()
    cliente_id = int(data.get("cliente_id"))
    producto_id = int(data.get("producto_id"))
    precio = data.get("precio")  # opcional

    if precio is not None:
        precio = float(precio)

    num_pedido = pedido_model.crear(cliente_id, producto_id, precio)
    return jsonify({"mensaje": "Pedido creado", "pedido": num_pedido}), 201

