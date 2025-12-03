from db.database import BaseDatos

#Tabla intermedia para la relación muchos a muchos entre Menú y Producto

class MenuProducto:
    def __init__(self, db_name='db.sqlite3'):
        self.db = BaseDatos(db_name)

    def obtener_todos(self):
        with self.db.get_connection() as conn:
            return conn.execute("SELECT * FROM MenuProducto").fetchall()

    def crear(self, menu_id, producto_id):
        with self.db.get_connection() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO MenuProducto (menu_id, producto_id)
                VALUES (?, ?)
                """,
                (menu_id, producto_id)
            )
            conn.commit()

    def eliminar(self, menu_id, producto_id):
        with self.db.get_connection() as conn:
            conn.execute(
                "DELETE FROM MenuProducto WHERE menu_id = ? AND producto_id = ?",
                (menu_id, producto_id)
            )
            conn.commit()

    def obtener_productos_de_menu(self, menu_id):
        with self.db.get_connection() as conn:
            return conn.execute(
                """
                SELECT pr.*
                FROM Producto AS pr
                JOIN MenuProducto AS mp ON pr.id = mp.producto_id
                WHERE mp.menu_id = ?
                """,
                (menu_id,)
            ).fetchall()
    def obtener_menus_de_producto(self, producto_id):
        with self.db.get_connection() as conn:
            return conn.execute(
                """
                SELECT m.*
                FROM Menu AS m
                JOIN MenuProducto AS mp ON m.id = mp.menu_id
                WHERE mp.producto_id = ?
                """,
                (producto_id,)
            ).fetchall()
            