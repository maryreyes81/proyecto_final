# app.py
"""
Aplicación principal de Happy Burger
------------------------------------
Arranca Flask, crea las tablas si no existen y registra
las rutas (blueprints) de Clientes, Menú y Pedidos.
"""

from flask import Flask, render_template

from db.database import BaseDatos
from models.clientes import Clientes
from models.menu import Menu
from models.pedidos import Pedidos  # 👈 modelo Pedidos

from routes.clientes_routes import clientes_bp
from routes.menu_routes import menu_bp
from routes.pedidos_routes import pedidos_bp  # 👈 blueprint Pedidos


# Crear instancia de Flask
app = Flask(__name__)

# Crear tablas en la base de datos (si no existen)
db = BaseDatos()
db.crear_tablas()

# Instancias de los modelos
clientes_model = Clientes()
menu_model = Menu()
pedidos_model = Pedidos()  # 👈 usamos el modelo de pedidos


@app.route("/")
def index():
    """
    Página principal de Happy Burger.
    Muestra:
      - Lista de clientes
      - Lista de productos del menú
      - Lista de líneas de pedido
      - Resumen de totales por pedido
    """
    clientes = clientes_model.obtener_clientes()
    menu_items = menu_model.obtener_menu()
    pedidos = pedidos_model.obtener_pedidos()
    totales_pedidos = pedidos_model.obtener_totales_pedidos()  # 👈 AQUÍ CALCULAMOS TOTALES

    return render_template(
        "index.html",
        clientes=clientes,
        menu_items=menu_items,
        pedidos=pedidos,
        totales_pedidos=totales_pedidos,  # 👈 LOS MANDAMOS AL TEMPLATE
    )


@app.route("/health")
def health():
    return {"status": "ok"}


# Registrar blueprints de las rutas
app.register_blueprint(clientes_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(pedidos_bp)


if __name__ == "__main__":
    app.run(debug=True)

