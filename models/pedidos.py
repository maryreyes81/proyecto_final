# models/pedidos.py
"""
pedidos.py
----------
Modelo para el manejo de pedidos de Happy Burger usando SQLite.
"""

from db.database import BaseDatos


class Pedidos:
    """
    Clase Pedidos
    -------------
    Administra los pedidos utilizando la tabla Pedido en SQLite.
    """

    def __init__(self, db_name="happy_burger.db"):
        self.db = BaseDatos(db_name)

    def agregar_pedido(self, pedido_num, cliente_id, producto_id):
        """
        Inserta un nuevo pedido en la tabla Pedido.
        El precio NO se recibe desde el formulario, se toma del Menu.
        - pedido_num -> campo 'pedido' (número del pedido, UNIQUE)
        - precio -> se obtiene de Menu.precio donde Menu.id = producto_id
        """
        with self.db.get_connection() as conn:
            # Usamos INSERT ... SELECT para tomar el precio del producto
            conn.execute(
                """
                INSERT INTO Pedido (pedido, cliente_id, producto_id, precio)
                SELECT ?, ?, ?, precio
                FROM Menu
                WHERE id = ?
                """,
                (pedido_num, cliente_id, producto_id, producto_id),
            )
            conn.commit()

    def obtener_pedidos(self):
        """
        Obtiene todos los pedidos registrados.
        Devuelve lista de tuplas: (id, pedido, cliente_id, producto_id, precio)
        """
        with self.db.get_connection() as conn:
            return conn.execute(
                """
                SELECT id, pedido, cliente_id, producto_id, precio
                FROM Pedido
                ORDER BY id
                """
            ).fetchall()

    def eliminar_pedido(self, pedido_id):
        """
        Elimina un pedido por su ID.
        """
        with self.db.get_connection() as conn:
            conn.execute("DELETE FROM Pedido WHERE id = ?", (pedido_id,))
            conn.commit()

