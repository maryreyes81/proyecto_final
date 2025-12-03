from db.database import BaseDatos

class Menu:
    def __init__(self, db_name='db.sqlite3'):
        self.db = BaseDatos(db_name)

    def obtener_todos(self):
        with self.db.get_connection() as conn:
            return conn.execute("SELECT * FROM Menu").fetchall()

    def obtener_por_id(self, menu_id):
        with self.db.get_connection() as conn:
            return conn.execute(
                "SELECT * FROM Menu WHERE id = ?",
                (menu_id,)
            ).fetchone()

    def crear(self, nombre, descripcion, activo=1):
        with self.db.get_connection() as conn:
            conn.execute(
                "INSERT INTO Menu (nombre, descripcion, activo) VALUES (?, ?, ?)",
                (nombre, descripcion, activo)
            )
            conn.commit()

    def actualizar(self, menu_id, nombre, descripcion, activo=1):
        with self.db.get_connection() as conn:
            conn.execute(
                "UPDATE Menu SET nombre = ?, descripcion = ?, activo = ? WHERE id = ?",
                (nombre, descripcion, activo, menu_id)
            )
            conn.commit()

    def eliminar(self, menu_id):
        with self.db.get_connection() as conn:
            conn.execute(
                "DELETE FROM Menu WHERE id = ?",
                (menu_id,)
            )
            conn.commit()
