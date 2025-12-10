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

    def agregar_pedido(self, pedido_num, cliente_id, producto_id, precio):
        """
        Inserta un nuevo pedido en la tabla Pedido.
        pedido_num => campo 'pedido' (número de pedido, UNIQUE).
        """
        with self.db.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO Pedido (pedido, cliente_id, producto_id, precio)
                VALUES (?, ?, ?, ?)
                """,
                (pedido_num, cliente_id, producto_id, precio),
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
