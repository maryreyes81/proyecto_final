"""
app.py
------
Aplicación principal Flask para Happy Burger.

- Inicializa la base de datos SQLite.
- Registra los Blueprints de clientes, menú y pedidos.
- Expone una vista HTML para consultar un pedido por número.
"""

from flask import Flask, render_template
from db.database import BaseDatos
from models.pedido import Pedido
from routes.clientes_routes import clientes_bp
from routes.menu_routes import menu_bp
from routes.pedido_routes import pedido_bp


def create_app():
    """
    Crea y configura la aplicación Flask.
    """
    app = Flask(__name__)

    # Inicializar base de datos y crear tablas
    db = BaseDatos()
    db.crear_tablas()

    # Instancia del modelo Pedido (para la vista HTML)
    pedido_model = Pedido()

    # Registrar blueprints (rutas API tipo JSON)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(pedido_bp)

    @app.route("/")
    def index():
        """
        Página de inicio: muestra la página principal con formulario, etc.
        """
        return render_template("index.html")

    @app.route("/pedido/<int:numero_pedido>")
    def ver_pedido_html(numero_pedido):
        """
        Vista HTML para consultar un pedido por su número.

        Usa el método obtener_por_numero_con_detalle() del modelo Pedido
        para mostrar:
        - Número de pedido
        - Cliente (clave y nombre)
        - Producto (clave y nombre)
        - Precio de producto
        - Total del pedido
        """
        pedido = pedido_model.obtener_por_numero_con_detalle(numero_pedido)

        if not pedido:
            # Podrías usar un template de error si quieres
            return f"<h1>Pedido {numero_pedido} no encontrado</h1>", 404

        # pedido es una tupla:
        # (numero_pedido, cliente_clave, cliente_nombre,
        #  producto_clave, producto_nombre, precio_producto, total_pedido)
        datos = {
            "numero_pedido": pedido[0],
            "cliente_clave": pedido[1],
            "cliente_nombre": pedido[2],
            "producto_clave": pedido[3],
            "producto_nombre": pedido[4],
            "precio_producto": pedido[5],
            "total_pedido": pedido[6],
        }

        return render_template("pedido.html", pedido=datos)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
