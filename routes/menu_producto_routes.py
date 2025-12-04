from flask import Blueprint, request, jsonify
from models.menu_producto import MenuProducto

menu_producto_routes = Blueprint('menu_producto_routes', __name__)
mp_model = MenuProducto()

@menu_producto_routes.post('/menu-producto')
def crear_relacion():
    data = request.json
    mp_model.crear(data['menu_id'], data['producto_id'])
    return {"mensaje": "Producto agregado al menú"}

@menu_producto_routes.delete('/menu-producto')
def eliminar_relacion():
    data = request.json
    mp_model.eliminar(data['menu_id'], data['producto_id'])
    return {"mensaje": "Producto eliminado del menú"}

@menu_producto_routes.get('/menu/<int:menu_id>/productos')
def obtener_productos_menu(menu_id):
    return jsonify(mp_model.obtener_productos_de_menu(menu_id))
