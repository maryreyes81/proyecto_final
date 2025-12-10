# routes/pedidos_routes.py

from flask import Blueprint, request, redirect, url_for, render_template
from models.pedidos import Pedidos

pedidos_bp = Blueprint("pedidos", __name__)
pedidos_model = Pedidos()


@pedidos_bp.route("/pedidos", methods=["GET"])
def listar_pedidos():
    """
    Página opcional para ver los pedidos en una vista aparte.
    """
    pedidos = pedidos_model.obtener_pedidos()
    return render_template("pedidos.html", pedidos=pedidos)


@pedidos_bp.route("/pedidos/crear_form", methods=["POST"])
def crear_pedido_form():
    """
    Recibe el formulario del index.html para crear un pedido.
    No se recibe precio desde el formulario.
    """
    pedido_num = request.form.get("pedido", "").strip()
    cliente_id = request.form.get("cliente_id", "").strip()
    producto_id = request.form.get("producto_id", "").strip()

    # Convertir a enteros con validaciones sencillas
    try:
        pedido_num = int(pedido_num)
        cliente_id = int(cliente_id)
        producto_id = int(producto_id)
    except ValueError:
        # Si algo viene mal, simplemente regresamos al index por ahora
        return redirect(url_for("index"))

    pedidos_model.agregar_pedido(pedido_num, cliente_id, producto_id)

    # Volver al index
    return redirect(url_for("index"))


@pedidos_bp.route("/pedidos/eliminar/<int:pedido_id>", methods=["POST"])
def eliminar_pedido(pedido_id):
    """
    Eliminar un pedido por su ID.
    """
    pedidos_model.eliminar_pedido(pedido_id)
    return redirect(url_for("index"))
