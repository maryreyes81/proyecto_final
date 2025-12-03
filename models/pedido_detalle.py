from db.database import BaseDatos

class PedidoDetalle:
    """
    Clase PedidoDetalle
    -------------------
    Administra los registros de la tabla PedidoDetalle.
    """

    def __init__(self, db_name='db.sqlite3'):
        """Inicializa la conexión con la base de datos."""
        self.db = BaseDatos(db_name)

    def obtener_por_pedido(self, pedido_id):
        """
        Obtiene todos los detalles de un pedido, incluyendo el nombre del producto.
        """
        with self.db.get_connection() as conn:
            return conn.execute(
                """
                SELECT pd.*, p.nombre AS producto_nombre
                FROM PedidoDetalle AS pd
                JOIN Producto AS p ON pd.producto_id = p.id
                WHERE pd.pedido_id = ?
                """,
                (pedido_id,)
            ).fetchall()

    def crear(self, pedido_id, producto_id, cantidad, precio_unitario):
        """
        Crea un registro de detalle para un pedido.
        Calcula automáticamente el subtotal.
        """
        subtotal = cantidad * precio_unitario
        with self.db.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO PedidoDetalle
                (pedido_id, producto_id, cantidad, precio_unitario, subtotal)
                VALUES (?, ?, ?, ?, ?)
                """,
                (pedido_id, producto_id, cantidad, precio_unitario, subtotal)
            )
            conn.commit()

    def eliminar(self, detalle_id):
        """
        Elimina un detalle específico mediante su ID.
        """
        with self.db.get_connection() as conn:
            conn.execute(
                "DELETE FROM PedidoDetalle WHERE id = ?",
                (detalle_id,)
            )
            conn.commit()

    def actualizar_cantidad(self, detalle_id, cantidad):
        """
        Actualiza la cantidad y recalcula el subtotal.
        Maneja casos donde el detalle no existe.
        """
        with self.db.get_connection() as conn:
            fila = conn.execute(
                "SELECT precio_unitario FROM PedidoDetalle WHERE id = ?",
                (detalle_id,)
            ).fetchone()

            if fila is None:
                print("❌ Error: No existe un detalle con ese ID.")
                return False

            precio_unitario = fila[0]
            subtotal = cantidad * precio_unitario

            conn.execute(
                """
                UPDATE PedidoDetalle
                SET cantidad = ?, subtotal = ?
                WHERE id = ?
                """,
                (cantidad, subtotal, detalle_id)
            )
            conn.commit()
            return True

    def eliminar_por_pedido(self, pedido_id):
        """
        Elimina todos los detalles asociados a un pedido.
        """
        with self.db.get_connection() as conn:
            conn.execute(
                "DELETE FROM PedidoDetalle WHERE pedido_id = ?",
                (pedido_id,)
            )
            conn.commit()

    def obtener_total_por_pedido(self, pedido_id):
        """
        Calcula el total sumando subtotales de todos los detalles del pedido.
        """
        with self.db.get_connection() as conn:
            fila = conn.execute(
                """
                SELECT SUM(subtotal)
                FROM PedidoDetalle
                WHERE pedido_id = ?
                """,
                (pedido_id,)
            ).fetchone()

            return fila[0] if fila[0] else 0.0

            
            