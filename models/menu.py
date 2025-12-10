# models/menu.py
from db.database import BaseDatos


class Menu:
    def __init__(self, db_name="happy_burger.db"):
        self.db = BaseDatos(db_name)

    def obtener_menu(self):
        with self.db.get_connection() as conn:
            return conn.execute(
                "SELECT id, nombre, precio FROM Menu ORDER BY id"
            ).fetchall()

    def obtener_por_id(self, item_id):
        with self.db.get_connection() as conn:
            return conn.execute(
                "SELECT id, nombre, precio FROM Menu WHERE id = ?",
                (item_id,),
            ).fetchone()

    def agregar_producto(self, nombre, precio):
        with self.db.get_connection() as conn:
            conn.execute(
                "INSERT INTO Menu (nombre, precio) VALUES (?, ?)",
                (nombre, precio),
            )
            conn.commit()

    def actualizar_producto(self, item_id, nombre, precio):
        with self.db.get_connection() as conn:
            conn.execute(
                """
                UPDATE Menu
                SET nombre = ?, precio = ?
                WHERE id = ?
                """,
                (nombre, precio, item_id),
            )
            conn.commit()

    def eliminar_producto(self, item_id):
        with self.db.get_connection() as conn:
            conn.execute("DELETE FROM Menu WHERE id = ?", (item_id,))
            conn.commit()

