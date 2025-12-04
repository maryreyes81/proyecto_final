from flask import Blueprint, request, jsonify
from models.producto import Producto

producto_routes = Blueprint('producto_routes', __name__)
producto_model = Producto()

@producto_routes.get('/productos')
def obtener_productos():
    return jsonify(producto_model.obtener_todos())

@producto_routes.get('/productos/<int:id>')
def obtener_producto(id):
    return jsonify(producto_model.obtener_por_id(id))

@producto_routes.post('/productos')
def crear_producto():
    data = request.json
    producto_model.crear(
        data['nombre'], data['descripcion'], data['precio'], data['categoria'], data.get('activo', 1)
    )
    return {"mensaje": "Producto creado"}

@producto_routes.put('/productos/<int:id>')
def actualizar_producto(id):
    data = request.json
    producto_model.actualizar(
        id, data['nombre'], data['descripcion'], data['precio'], data['categoria'], data.get('activo', 1)
    )
    return {"mensaje": "Producto actualizado"}

@producto_routes.delete('/productos/<int:id>')
def eliminar_producto(id):
    producto_model.eliminar(id)
    return {"mensaje": "Producto eliminado"}
