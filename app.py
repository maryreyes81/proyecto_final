from flask import Flask
from routes.cliente_routes import cliente_routes
from routes.menu_routes import menu_routes
from routes.producto_routes import producto_routes
from routes.menu_producto_routes import menu_producto_routes
from routes.pedido_routes import pedido_routes
from routes.pedido_detalle_routes import pedido_detalle_routes

#API web con Flask

app = Flask(__name__)

app.register_blueprint(cliente_routes)
app.register_blueprint(menu_routes)
app.register_blueprint(producto_routes)
app.register_blueprint(menu_producto_routes)
app.register_blueprint(pedido_routes)
app.register_blueprint(pedido_detalle_routes)

if __name__ == '__main__':
    app.run(debug=True)
