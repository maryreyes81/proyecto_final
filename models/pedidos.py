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
        """
        Inicializa la clase Pedidos con una instancia de BaseDatos.
        """
        self.db = BaseDatos(db_name)

    def agregar_pedido(self, pedido_num, cliente_id, producto_id):
        """
        Inserta un nuevo registro en la tabla Pedido.

        IMPORTANTE:
        - El precio NO se recibe desde el formulario.
        - El precio se toma automáticamente de la tabla Menu,
          usando el producto_id.

        Cada llamada a este método inserta una "línea" del pedido:
        un número de pedido + un producto.
        De esta forma se pueden tener varios productos con el mismo
        número de pedido.
        """
        with self.db.get_connection() as conn:
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
        Obtiene todas las líneas de pedidos registradas.

        Devuelve lista de tuplas:
        (id, pedido, cliente_id, producto_id, precio)
        """
        with self.db.get_connection() as conn:
            return conn.execute(
                """
                SELECT id, pedido, cliente_id, producto_id, precio
                FROM Pedido
                ORDER BY pedido, id
                """
            ).fetchall()

    def obtener_totales_pedidos(self):
        """
        Devuelve un resumen por número de pedido:
        (pedido, cliente_id, num_items, total)

        - pedido: número de pedido (puede tener varias líneas)
        - cliente_id: ID del cliente asociado a ese pedido
        - num_items: cuántos productos hay en ese pedido
        - total: suma de los precios de todas las líneas de ese pedido
        """
        with self.db.get_connection() as conn:
            return conn.execute(
                """
                SELECT 
                    pedido, 
                    cliente_id, 
                    COUNT(*) AS num_items,
                    SUM(precio) AS total
                FROM Pedido
                GROUP BY pedido, cliente_id
                ORDER BY pedido
                """
            ).fetchall()

    def obtener_por_id(self, linea_id):
        """
        Obtiene una línea de pedido por su ID (columna id).
        Devuelve tupla: (id, pedido, cliente_id, producto_id, precio)
        """
        with self.db.get_connection() as conn:
            return conn.execute(
                """
                SELECT id, pedido, cliente_id, producto_id, precio
                FROM Pedido
                WHERE id = ?
                """,
                (linea_id,),
            ).fetchone()

    def actualizar_linea(self, linea_id, pedido_num, cliente_id, producto_id):
        """
        Actualiza una línea de pedido. El precio se recalcula
        tomando el precio del producto en el menú.
        """
        with self.db.get_connection() as conn:
            conn.execute(
                """
                UPDATE Pedido
                SET pedido      = ?,
                    cliente_id  = ?,
                    producto_id = ?,
                    precio      = (SELECT precio FROM Menu WHERE id = ?)
                WHERE id = ?
                """,
                (pedido_num, cliente_id, producto_id, producto_id, linea_id),
            )
            conn.commit()

    def eliminar_pedido(self, pedido_id):
        """
        Elimina una línea de pedido por su ID (columna 'id').
        No borra todas las líneas con el mismo número de pedido,
        solo la fila específica.
        """
        with self.db.get_connection() as conn:
            conn.execute("DELETE FROM Pedido WHERE id = ?", (pedido_id,))
            conn.commit()
