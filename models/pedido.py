"""
pedido.py
---------
Modelo para el manejo de pedidos de Happy Burger.
"""

from db.database import BaseDatos


class Pedido:
    """
    Clase Pedido
    ------------
    Administra los pedidos usando la tabla Pedido.
    """

    def __init__(self, db_name="happy_burger.db"):
        self.db = BaseDatos(db_name)

    def _siguiente_numero_pedido(self):
        """
        Obtiene el siguiente número de pedido (pedido INTEGER).
        """
        with self.db.get_connection() as conn:
            row = conn.execute(
                "SELECT COALESCE(MAX(pedido), 0) + 1 FROM Pedido"
            ).fetchone()
            return row[0]

    def crear(self, cliente_id, producto_id, precio=None):
        """
        Crea un nuevo pedido.
        Si precio es None, se toma de la tabla Menu.
        """
        with self.db.get_connection() as conn:
            if precio is None:
                fila = conn.execute(
                    "SELECT precio FROM Menu WHERE id = ?",
                    (producto_id,),
                ).fetchone()
                if not fila:
                    raise ValueError("Producto no encontrado para obtener precio.")
                precio = fila[0]

            num_pedido = self._siguiente_numero_pedido()

            conn.execute(
                """
                INSERT INTO Pedido (pedido, cliente_id, producto_id, precio)
                VALUES (?, ?, ?, ?)
                """,
                (num_pedido, cliente_id, producto_id, precio),
            )
            conn.commit()
            return num_pedido

    def obtener_todos(self):
        """
        Devuelve todos los pedidos sin JOIN.
        """
        with self.db.get_connection() as conn:
            return conn.execute(
                """
                SELECT id, pedido, cliente_id, producto_id, precio
                FROM Pedido
                ORDER BY id
                """
            ).fetchall()

    def obtener_todos_con_detalle(self):
        """
        Devuelve todos los pedidos con JOIN a Clientes y Menu.
        """
        with self.db.get_connection() as conn:
            return conn.execute(
                """
                SELECT
                    p.pedido            AS numero_pedido,
                    c.nombre            AS cliente_nombre,
                    m.nombre            AS producto_nombre,
                    p.precio            AS total_pedido
                FROM Pedido AS p
                JOIN Clientes AS c ON p.cliente_id = c.id
                JOIN Menu     AS m ON p.producto_id = m.id
                ORDER BY p.pedido
                """
            ).fetchall()

    def obtener_por_numero_con_detalle(self, numero_pedido):
        """
        Devuelve un pedido por su campo 'pedido' con JOIN a Clientes y Menu.
        """
        with self.db.get_connection() as conn:
            return conn.execute(
                """
                SELECT
                    p.pedido            AS numero_pedido,
                    c.nombre            AS cliente_nombre,
                    m.nombre            AS producto_nombre,
                    p.precio            AS total_pedido
                FROM Pedido AS p
                JOIN Clientes AS c ON p.cliente_id = c.id
                JOIN Menu     AS m ON p.producto_id = m.id
                WHERE p.pedido = ?
                """,
                (numero_pedido,),
            ).fetchone()

    def eliminar_por_numero(self, numero_pedido):
        """
        Elimina un pedido por su número de pedido (campo pedido).
        """
        with self.db.get_connection() as conn:
            conn.execute(
                "DELETE FROM Pedido WHERE pedido = ?",
                (numero_pedido,),
            )
            conn.commit()
