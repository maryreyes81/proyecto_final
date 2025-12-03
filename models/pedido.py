from db.database import BaseDatos

class Pedido:
    def __init__(self, db_name='db.sqlite3'):
        self.db = BaseDatos(db_name)

    def obtener_todos(self):
        with self.db.get_connection() as conn:
            return conn.execute("SELECT * FROM Pedidos").fetchall()

    def obtener_por_id(self, pedido_id):
        with self.db.get_connection() as conn:
            return conn.execute(
                "SELECT * FROM Pedidos WHERE id = ?",
                (pedido_id,)
            ).fetchone()

    def crear(self, cliente_id, fecha, estado='pendiente', description=None, total=0):
        with self.db.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO Pedidos (cliente_id, fecha, estado, description, total)
                VALUES (?, ?, ?, ?, ?)
                """,
                (cliente_id, fecha, estado, description, total)
            )
            conn.commit()

    def actualizar_total(self, pedido_id, total):
        with self.db.get_connection() as conn:
            conn.execute(
                "UPDATE Pedidos SET total = ? WHERE id = ?",
                (total, pedido_id)
            )
            conn.commit()

    def actualizar_estado(self, pedido_id, estado):
        with self.db.get_connection() as conn:
            conn.execute(
                "UPDATE Pedidos SET estado = ? WHERE id = ?",
                (estado, pedido_id)
            )
            conn.commit()

    def eliminar(self, pedido_id):
        with self.db.get_connection() as conn:
            conn.execute(
                "DELETE FROM Pedidos WHERE id = ?",
                (pedido_id,)
            )
            conn.commit()

