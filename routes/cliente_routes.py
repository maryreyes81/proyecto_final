from flask import Blueprint, request, jsonify
from models.cliente import Cliente

cliente_routes = Blueprint('cliente_routes', __name__)
cliente_model = Cliente()

@cliente_routes.get('/clientes')
def obtener_clientes():
    return jsonify(cliente_model.obtener_todos())

@cliente_routes.get('/clientes/<int:id>')
def obtener_cliente(id):
    resultado = cliente_model.obtener_por_id(id)
    return jsonify(resultado) if resultado else ({"error": "Cliente no encontrado"}, 404)

@cliente_routes.post('/clientes')
def crear_cliente():
    data = request.json
    cliente_model.crear(
        data['nombre'], data['correo'], data['telefono'], data['direccion']
    )
    return {"mensaje": "Cliente creado con éxito"}

@cliente_routes.put('/clientes/<int:id>')
def actualizar_cliente(id):
    data = request.json
    cliente_model.actualizar(
        id, data['nombre'], data['correo'], data['telefono'], data['direccion']
    )
    return {"mensaje": "Cliente actualizado"}

@cliente_routes.delete('/clientes/<int:id>')
def eliminar_cliente(id):
    cliente_model.eliminar(id)
    return {"mensaje": "Cliente eliminado"}

@cliente_routes.get('/clientes/<int:id>/pedidos')
def obtener_pedidos_cliente(id):
    return jsonify(cliente_model.obtener_pedidos(id))
