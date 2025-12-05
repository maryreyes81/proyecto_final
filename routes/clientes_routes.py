"""
clientes_routes.py
------------------
Rutas Flask para manejar clientes en Happy Burger.
"""

from flask import Blueprint, request, jsonify
from models.clientes import Clientes

# Crear Blueprint
clientes_bp = Blueprint("clientes", __name__)

# Instancia del modelo
clientes_model = Clientes()


@clientes_bp.route("/clientes", methods=["GET"])
def obtener_clientes():
    """
    GET /clientes
    Obtiene todos los clientes registrados.
    """
    clientes = clientes_model.obtener_todos()
    return jsonify(clientes), 200


@clientes_bp.route("/clientes/<string:clave>", methods=["GET"])
def obtener_cliente(clave):
    """
    GET /clientes/<clave>
    Obtiene un cliente específico por su clave.
    """
    cliente = clientes_model.obtener_por_clave(clave)
    if cliente:
        return jsonify(cliente), 200
    return jsonify({"error": "Cliente no encontrado"}), 404


@clientes_bp.route("/clientes", methods=["POST"])
def crear_cliente():
    """
    POST /clientes
    Crea un nuevo cliente.
    Espera JSON:
    {
        "clave": "C01",
        "nombre": "Mary",
        "direccion": "Calle 123",
        "correo_electronico": "mary@example.com",
        "telefono": "555-123456"
    }
    """
    data = request.json

    clientes_model.agregar_cliente(
        data["clave"],
        data["nombre"],
        data["direccion"],
        data["correo_electronico"],
        data["telefono"],
    )

    return jsonify({"mensaje": "Cliente creado exitosamente"}), 201


@clientes_bp.route("/clientes/<string:clave>", methods=["PUT"])
def actualizar_cliente(clave):
    """
    PUT /clientes/<clave>
    Actualiza los datos de un cliente.
    """
    data = request.json

    clientes_model.actualizar_cliente(
        clave,
        data.get("nombre"),
        data.get("direccion"),
        data.get("correo_electronico"),
        data.get("telefono"),
    )

    return jsonify({"mensaje": "Cliente actualizado correctamente"}), 200


@clientes_bp.route("/clientes/<string:clave>", methods=["DELETE"])
def eliminar_cliente(clave):
    """
    DELETE /clientes/<clave>
    Elimina un cliente por su clave.
    """
    clientes_model.eliminar_cliente(clave)
    return jsonify({"mensaje": "Cliente eliminado correctamente"}), 200

