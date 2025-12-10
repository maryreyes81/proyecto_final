# routes/pedidos_routes.py
"""
Rutas para el manejo de pedidos en Happy Burger.
"""

import os
from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    render_template,
    make_response,
)
from models.pedidos import Pedidos

pedidos_bp = Blueprint("pedidos", __name__)
pedidos_model = Pedidos()


@pedidos_bp.route("/pedidos", methods=["GET"])
def listar_pedidos():
    """
    Vista opcional para listar pedidos en una página aparte.
    (El index ya los muestra, pero esta ruta queda por si la necesitas.)
    """
    pedidos = pedidos_model.obtener_pedidos()
    totales_pedidos = pedidos_model.obtener_totales_pedidos()
    return render_template(
        "pedidos.html",
        pedidos=pedidos,
        totales_pedidos=totales_pedidos,
    )


@pedidos_bp.route("/pedidos/crear_form", methods=["POST"])
def crear_pedido_form():
    """
    Crea una línea de pedido desde el formulario del index.
    Cada envío agrega un producto al número de pedido indicado.
    """
    pedido = request.form.get("pedido")
    cliente_id = request.form.get("cliente_id")
    producto_id = request.form.get("producto_id")

    try:
        pedido_num = int(pedido)
        cliente_id_int = int(cliente_id)
        producto_id_int = int(producto_id)
    except (TypeError, ValueError):
        # Si algo falla en la conversión, regresamos al index
        return redirect(url_for("index"))

    pedidos_model.agregar_pedido(pedido_num, cliente_id_int, producto_id_int)
    return redirect(url_for("index"))


@pedidos_bp.route("/pedidos/eliminar/<int:pedido_id>", methods=["POST"])
def eliminar_pedido(pedido_id):
    """
    Elimina una línea de pedido por su ID (columna 'id').
    No borra todas las líneas del mismo número de pedido, solo esa fila.
    """
    pedidos_model.eliminar_pedido(pedido_id)
    return redirect(url_for("index"))


@pedidos_bp.route("/pedidos/editar/<int:linea_id>", methods=["GET"])
def editar_pedido_linea(linea_id):
    """
    Muestra el formulario para editar una línea de pedido.
    """
    linea = pedidos_model.obtener_por_id(linea_id)
    if not linea:
        return redirect(url_for("index"))

    # linea = (id, pedido, cliente_id, producto_id, precio)
    return render_template("editar_pedido.html", linea=linea)


@pedidos_bp.route("/pedidos/actualizar_form", methods=["POST"])
def actualizar_pedido_form():
    """
    Procesa el formulario de edición de una línea de pedido.
    El precio se recalcula automáticamente desde el menú.
    """
    linea_id = request.form.get("id")
    pedido = request.form.get("pedido")
    cliente_id = request.form.get("cliente_id")
    producto_id = request.form.get("producto_id")

    try:
        linea_id_int = int(linea_id)
        pedido_num = int(pedido)
        cliente_id_int = int(cliente_id)
        producto_id_int = int(producto_id)
    except (TypeError, ValueError):
        return redirect(url_for("index"))

    pedidos_model.actualizar_linea(
        linea_id_int, pedido_num, cliente_id_int, producto_id_int
    )

    return redirect(url_for("index"))


@pedidos_bp.route("/pedidos/ticket/<int:pedido_num>", methods=["GET"])
def ver_ticket(pedido_num):
    """
    Muestra un ticket HTML para el número de pedido dado.
    """
    lineas = pedidos_model.obtener_ticket(pedido_num)

    if not lineas:
        return redirect(url_for("index"))

    # Todas las líneas comparten el mismo cliente
    pedido = lineas[0][0]
    cliente_id = lineas[0][1]
    cliente_nombre = lineas[0][2]
    direccion = lineas[0][3]
    correo = lineas[0][4]
    telefono = lineas[0][5]

    total = sum(l[8] for l in lineas)

    return render_template(
        "ticket.html",
        pedido=pedido,
        cliente_id=cliente_id,
        cliente_nombre=cliente_nombre,
        direccion=direccion,
        correo=correo,
        telefono=telefono,
        lineas=lineas,
        total=total,
    )


@pedidos_bp.route("/pedidos/ticket_txt/<int:pedido_num>", methods=["GET"])
def ticket_txt(pedido_num):
    """
    Genera un ticket en texto plano (.txt) para el número de pedido dado,
    lo guarda en la carpeta 'tickets' y lo devuelve como descarga.
    """
    lineas = pedidos_model.obtener_ticket(pedido_num)

    if not lineas:
        return redirect(url_for("index"))

    pedido = lineas[0][0]
    cliente_id = lineas[0][1]
    cliente_nombre = lineas[0][2]
    direccion = lineas[0][3] or ""
    correo = lineas[0][4] or ""
    telefono = lineas[0][5] or ""

    total = sum(l[8] for l in lineas)

    lineas_txt = []
    lineas_txt.append("HAPPY BURGER")
    lineas_txt.append(f"Pedido #: {pedido}")
    lineas_txt.append("")
    lineas_txt.append(f"Cliente: {cliente_nombre} (ID {cliente_id})")
    lineas_txt.append(f"Dirección: {direccion}")
    lineas_txt.append(f"Correo: {correo}")
    lineas_txt.append(f"Teléfono: {telefono}")
    lineas_txt.append("")
    lineas_txt.append("Productos:")
    lineas_txt.append("------------------------------")

    for l in lineas:
        # l = (pedido, cliente_id, cliente_nombre, direccion, correo, telefono,
        #      producto_nombre, producto_id, precio)
        producto_nombre = l[6]
        precio = l[8]
        lineas_txt.append(f"- {producto_nombre}  ${precio:.2f}")

    lineas_txt.append("------------------------------")
    lineas_txt.append(f"TOTAL: ${total:.2f}")
    lineas_txt.append("")
    lineas_txt.append("¡Gracias por su compra!")

    contenido = "\n".join(lineas_txt)

    # ===== Guardar en carpeta tickets =====
    base_dir = os.path.dirname(os.path.dirname(__file__))
    tickets_dir = os.path.join(base_dir, "tickets")
    os.makedirs(tickets_dir, exist_ok=True)

    file_path = os.path.join(tickets_dir, f"ticket_{pedido}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(contenido)

    # ===== Devolver como descarga =====
    response = make_response(contenido)
    response.headers["Content-Type"] = "text/plain; charset=utf-8"
    response.headers["Content-Disposition"] = f"attachment; filename=ticket_{pedido}.txt"

    return response


