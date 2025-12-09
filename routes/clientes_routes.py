"""
clientes_routes.py
------------------
Rutas Flask para manejar clientes en Happy Burger.
"""

from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from models.clientes import Clientes

# Crear Blueprint (SOLO UNA VEZ)
clientes_bp = Blueprint("clientes", __name__)

# Instancia del modelo (SOLO UNA VEZ)
clientes_model = Clientes()

# ==========================
# RUTAS API JSON
# ==========================

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


# ==========================
# RUTAS FRONT-END HTML
# ==========================

@clientes_bp.route("/clientes/ui", methods=["GET"])
def clientes_ui():
    """
    Vista HTML que muestra la lista de clientes y formulario de creación.
    """
    clientes = clientes_model.obtener_todos()
    return render_template("clientes.html", clientes=clientes)


@clientes_bp.route("/clientes/ui/crear", methods=["POST"])
def clientes_ui_crear():
    """
    Procesa el formulario HTML para crear un cliente.
    """
    clave = request.form.get("clave")
    nombre = request.form.get("nombre")
    direccion = request.form.get("direccion")
    correo = request.form.get("correo_electronico")
    telefono = request.form.get("telefono")

    clientes_model.agregar_cliente(clave, nombre, direccion, correo, telefono)
    return redirect(url_for("clientes.clientes_ui"))


@clientes_bp.route("/clientes/ui/eliminar/<string:clave>", methods=["POST"])
def clientes_ui_eliminar(clave):
    """
    Elimina un cliente desde el front HTML.
    """
    clientes_model.eliminar_cliente(clave)
    return redirect(url_for("clientes.clientes_ui"))


@clientes_bp.route("/clientes/ui/editar/<string:clave>", methods=["GET", "POST"])
def clientes_ui_editar(clave):
    """
    Muestra y procesa el formulario de edición de un cliente.
    """
    if request.method == "POST":
        nombre = request.form.get("nombre")
        direccion = request.form.get("direccion")
        correo = request.form.get("correo_electronico")
        telefono = request.form.get("telefono")

        clientes_model.actualizar_cliente(
            clave,
            nombre=nombre,
            direccion=direccion,
            correo_electronico=correo,
            telefono=telefono,
        )
        return redirect(url_for("clientes.clientes_ui"))

    # GET → mostrar formulario con datos actuales
    cliente = clientes_model.obtener_por_clave(clave)
    if not cliente:
        return "Cliente no encontrado", 404

    # cliente = (clave, nombre, direccion, correo_electronico, telefono)
    return render_template("editar_cliente.html", cliente=cliente)
