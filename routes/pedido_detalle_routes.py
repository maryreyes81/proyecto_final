from flask import Blueprint, request, jsonify
from models.pedido_detalle import PedidoDetalle

pedido_detalle_routes = Blueprint('pedido_detalle_routes', __name__)
detalle_model = PedidoDetalle()

@pedido_detalle_routes.get('/pedido/<int:pedido_id>/detalles')
def obtener_detalles(pedido_id):
    return jsonify(detalle_model.obtener_por_pedido(pedido_id))

@pedido_detalle_routes.post('/pedido-detalle')
def crear_detalle():
    data = request.json
    detalle_model.crear(
        data['pedido_id'], data['producto_id'], data['cantidad'], data['precio_unitario']
    )
    return {"mensaje": "Detalle agregado"}

@pedido_detalle_routes.put('/pedido-detalle/<int:id>')
def actualizar_detalle(id):
    data = request.json
    detalle_model.actualizar_cantidad(id, data['cantidad'])
    return {"mensaje": "Cantidad actualizada"}

@pedido_detalle_routes.delete('/pedido-detalle/<int:id>')
def eliminar_detalle(id):
    detalle_model.eliminar(id)
    return {"mensaje": "Detalle eliminado"}

@pedido_detalle_routes.delete('/pedido/<int:pedido_id>/detalles')
def eliminar_detalles_pedido(pedido_id):
    detalle_model.eliminar_por_pedido(pedido_id)
    return {"mensaje": "Detalles eliminados del pedido"}
