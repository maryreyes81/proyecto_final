# routes/clientes_routes.py

from flask import Blueprint, request, redirect, url_for, render_template
from models.clientes import Clientes

clientes_bp = Blueprint("clientes", __name__)
clientes_model = Clientes()


@clientes_bp.route("/clientes", methods=["GET"])
def listar_clientes():
    """
    Vista opcional para listar clientes aparte del index.
    """
    clientes = clientes_model.obtener_clientes()
    return render_template("clientes.html", clientes=clientes)


@clientes_bp.route("/clientes/crear_form", methods=["POST"])
def crear_cliente_form():
    """
    Crear cliente desde el formulario del index.
    """
    nombre = request.form.get("nombre")
    direccion = request.form.get("direccion")
    correo = request.form.get("correo_electronico")
    telefono = request.form.get("telefono")

    clientes_model.agregar_cliente(nombre, direccion, correo, telefono)
    return redirect(url_for("index"))


@clientes_bp.route("/clientes/eliminar/<int:cliente_id>", methods=["POST"])
def eliminar_cliente(cliente_id):
    """
    Eliminar cliente por ID desde el index.
    """
    clientes_model.eliminar_cliente(cliente_id)
    return redirect(url_for("index"))


@clientes_bp.route("/clientes/editar/<int:cliente_id>", methods=["GET"])
def editar_cliente(cliente_id):
    """
    Muestra un formulario para editar los datos de un cliente.
    """
    cliente = clientes_model.obtener_por_id(cliente_id)
    if not cliente:
        # Si no existe, regresamos al index
        return redirect(url_for("index"))

    # cliente = (id, nombre, direccion, correo, telefono)
    return render_template("editar_cliente.html", cliente=cliente)


@clientes_bp.route("/clientes/actualizar_form", methods=["POST"])
def actualizar_cliente_form():
    """
    Procesa el formulario de edición y actualiza los datos del cliente.
    """
    cliente_id = request.form.get("id")
    nombre = request.form.get("nombre")
    direccion = request.form.get("direccion")
    correo = request.form.get("correo_electronico")
    telefono = request.form.get("telefono")

    try:
        cliente_id = int(cliente_id)
    except (TypeError, ValueError):
        return redirect(url_for("index"))

    clientes_model.actualizar_cliente(
        cliente_id,
        nombre=nombre,
        direccion=direccion,
        correo_electronico=correo,
        telefono=telefono,
    )

    return redirect(url_for("index"))
