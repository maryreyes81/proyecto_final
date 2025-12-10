# routes/pedidos_routes.py

from flask import Blueprint, request, redirect, url_for, render_template,make_response
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

@pedidos_bp.route("/pedidos/ticket_txt/<int:pedido_num>", methods=["GET"])
def ticket_txt(pedido_num):
    """
    Genera un ticket en texto plano (.txt) para el número de pedido dado.
    """
    lineas = pedidos_model.obtener_ticket(pedido_num)

    # Si no hay líneas, regresamos al inicio
    if not lineas:
        return redirect(url_for("index"))

    # Tomamos datos del cliente desde la primera línea
    pedido = lineas[0][0]
    cliente_id = lineas[0][1]
    cliente_nombre = lineas[0][2]
    direccion = lineas[0][3] or ""
    correo = lineas[0][4] or ""
    telefono = lineas[0][5] or ""

    total = sum(l[8] for l in lineas)

    # Construimos el texto del ticket
    lineas_txt = []
    lineas_txt.append("HAPPY BURGER")
    lineas_txt.append("Pedido #: {}".format(pedido))
    lineas_txt.append("")
    lineas_txt.append("Cliente: {} (ID {})".format(cliente_nombre, cliente_id))
    lineas_txt.append("Dirección: {}".format(direccion))
    lineas_txt.append("Correo: {}".format(correo))
    lineas_txt.append("Teléfono: {}".format(telefono))
    lineas_txt.append("")
    lineas_txt.append("Productos:")
    lineas_txt.append("------------------------------")

    for l in lineas:
        # l = (pedido, cliente_id, cliente_nombre, direccion, correo, telefono,
        #      producto_nombre, producto_id, precio)
        producto_nombre = l[6]
        precio = l[8]
        lineas_txt.append("- {}  ${:.2f}".format(producto_nombre, precio))

    lineas_txt.append("------------------------------")
    lineas_txt.append("TOTAL: ${:.2f}".format(total))
    lineas_txt.append("")
    lineas_txt.append("¡Gracias por su compra!")

    contenido = "\n".join(lineas_txt)

    # Creamos respuesta como archivo .txt descargable
    response = make_response(contenido)
    response.headers["Content-Type"] = "text/plain; charset=utf-8"
    response.headers["Content-Disposition"] = f"attachment; filename=ticket_{pedido}.txt"

    return response

