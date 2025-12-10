"""
clientes_routes.py
------------------
Rutas Flask para manejar clientes en Happy Burger.
"""

from flask import Blueprint, request, jsonify, redirect, url_for
from models.clientes import Clientes

clientes_bp = Blueprint("clientes", __name__)
clientes_model = Clientes()


# --- API JSON ---

@clientes_bp.route("/clientes", methods=["GET"])
def obtener_clientes():
    clientes = clientes_model.obtener_todos()
    resultado = [
        {
            "id": c[0],
            "nombre": c[1],
            "direccion": c[2],
            "correo_electronico": c[3],
            "telefono": c[4],
        }
        for c in clientes
    ]
    return jsonify(resultado), 200


@clientes_bp.route("/clientes/<int:cliente_id>", methods=["GET"])
def obtener_cliente(cliente_id):
    cliente = clientes_model.obtener_por_id(cliente_id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    c = {
        "id": cliente[0],
        "nombre": cliente[1],
        "direccion": cliente[2],
        "correo_electronico": cliente[3],
        "telefono": cliente[4],
    }
    return jsonify(c), 200


@clientes_bp.route("/clientes", methods=["POST"])
def crear_cliente():
    """
    Crea un cliente desde JSON o formulario.
    """
    if request.is_json:
        data = request.get_json()
        nombre = data.get("nombre")
        direccion = data.get("direccion")
        correo = data.get("correo_electronico")
        telefono = data.get("telefono")
    else:
        # soporte para form-data
        nombre = request.form.get("nombre")
        direccion = request.form.get("direccion")
        correo = request.form.get("correo_electronico")
        telefono = request.form.get("telefono")

    clientes_model.agregar_cliente(nombre, direccion, correo, telefono)
    return jsonify({"mensaje": "Cliente creado exitosamente"}), 201


@clientes_bp.route("/clientes/<int:cliente_id>", methods=["PUT"])
def actualizar_cliente(cliente_id):
    data = request.get_json()
    clientes_model.actualizar_cliente(
        cliente_id,
        nombre=data.get("nombre"),
        direccion=data.get("direccion"),
        correo_electronico=data.get("correo_electronico"),
        telefono=data.get("telefono"),
    )
    return jsonify({"mensaje": "Cliente actualizado correctamente"}), 200


@clientes_bp.route("/clientes/<int:cliente_id>", methods=["DELETE"])
def eliminar_cliente(cliente_id):
    clientes_model.eliminar_cliente(cliente_id)
    return jsonify({"mensaje": "Cliente eliminado correctamente"}), 200


# --- RUTAS PARA FORMULARIOS DESDE index.html ---

@clientes_bp.route("/clientes/crear_form", methods=["POST"])
def crear_cliente_form():
    nombre = request.form.get("nombre")
    direccion = request.form.get("direccion")
    correo = request.form.get("correo_electronico")
    telefono = request.form.get("telefono")

    clientes_model.agregar_cliente(nombre, direccion, correo, telefono)
    return redirect(url_for("index"))


@clientes_bp.route("/clientes/actualizar_form", methods=["POST"])
def actualizar_cliente_form():
    cliente_id = request.form.get("id")
    if not cliente_id:
        return redirect(url_for("index"))

    clientes_model.actualizar_cliente(
        int(cliente_id),
        nombre=request.form.get("nombre") or None,
        direccion=request.form.get("direccion") or None,
        correo_electronico=request.form.get("correo_electronico") or None,
        telefono=request.form.get("telefono") or None,
    )
    return redirect(url_for("index"))


@clientes_bp.route("/clientes/eliminar_form", methods=["POST"])
def eliminar_cliente_form():
    cliente_id = request.form.get("id")
    if cliente_id:
        clientes_model.eliminar_cliente(int(cliente_id))
    return redirect(url_for("index"))
