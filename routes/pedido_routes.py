from flask import Blueprint, request, jsonify
from models.pedido import Pedido

pedido_routes = Blueprint('pedido_routes', __name__)
pedido_model = Pedido()

@pedido_routes.get('/pedidos')
def obtener_pedidos():
    return jsonify(pedido_model.obtener_todos())

@pedido_routes.get('/pedidos/<int:id>')
def obtener_pedido(id):
    return jsonify(pedido_model.obtener_por_id(id))

@pedido_routes.post('/pedidos')
def crear_pedido():
    data = request.json
    pedido_model.crear(
        data['cliente_id'], data['fecha'], data.get('estado', 'pendiente'),
        data.get('description'), data.get('total', 0)
    )
    return {"mensaje": "Pedido creado"}

@pedido_routes.put('/pedidos/<int:id>/estado')
def actualizar_estado(id):
    data = request.json
    pedido_model.actualizar_estado(id, data['estado'])
    return {"mensaje": "Estado actualizado"}

@pedido_routes.put('/pedidos/<int:id>/total')
def actualizar_total(id):
    data = request.json
    pedido_model.actualizar_total(id, data['total'])
    return {"mensaje": "Total actualizado"}

@pedido_routes.delete('/pedidos/<int:id>')
def eliminar_pedido(id):
    pedido_model.eliminar(id)
    return {"mensaje": "Pedido eliminado"}
