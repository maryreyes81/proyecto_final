from flask import Blueprint, request, jsonify
from models.menu import Menu

menu_routes = Blueprint('menu_routes', __name__)
menu_model = Menu()

@menu_routes.get('/menus')
def obtener_menus():
    return jsonify(menu_model.obtener_todos())

@menu_routes.get('/menus/<int:id>')
def obtener_menu(id):
    return jsonify(menu_model.obtener_por_id(id))

@menu_routes.post('/menus')
def crear_menu():
    data = request.json
    menu_model.crear(data['nombre'], data['descripcion'], data.get('activo', 1))
    return {"mensaje": "Menú creado"}

@menu_routes.put('/menus/<int:id>')
def actualizar_menu(id):
    data = request.json
    menu_model.actualizar(id, data['nombre'], data['descripcion'], data.get('activo', 1))
    return {"mensaje": "Menú actualizado"}

@menu_routes.delete('/menus/<int:id>')
def eliminar_menu(id):
    menu_model.eliminar(id)
    return {"mensaje": "Menú eliminado"}
