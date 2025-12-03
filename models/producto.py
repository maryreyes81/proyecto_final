from db.database import BaseDatos

class Producto:
    def __init__(self, db_name='db.sqlite3'):
        self.db = BaseDatos(db_name)

    def obtener_todos(self):
        with self.db.get_connection() as conn:
            return conn.execute("SELECT * FROM Producto").fetchall()

    def obtener_por_id(self, producto_id):
        with self.db.get_connection() as conn:
            return conn.execute(
                "SELECT * FROM Producto WHERE id = ?",
                (producto_id,)
            ).fetchone()

    def crear(self, nombre, descripcion, precio, categoria, activo=1):
        with self.db.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO Producto (nombre, descripcion, precio, categoria, activo)
                VALUES (?, ?, ?, ?, ?)
                """,
                (nombre, descripcion, precio, categoria, activo)
            )
            conn.commit()

    def actualizar(self, producto_id, nombre, descripcion, precio, categoria, activo=1):
        with self.db.get_connection() as conn:
            conn.execute(
                """
                UPDATE Producto
                SET nombre = ?, descripcion = ?, precio = ?, categoria = ?, activo = ?
                WHERE id = ?
                """,
                (nombre, descripcion, precio, categoria, activo, producto_id)
            )
            conn.commit()

    def eliminar(self, producto_id):
        with self.db.get_connection() as conn:
            conn.execute(
                "DELETE FROM Producto WHERE id = ?",
                (producto_id,)
            )
            conn.commit()
    def obtener_por_categoria(self, categoria):
        with self.db.get_connection() as conn:
            return conn.execute(
                "SELECT * FROM Producto WHERE categoria = ?",
                (categoria,)
            ).fetchall()
            
    def buscar_por_nombre(self, nombre):
        with self.db.get_connection() as conn:
            return conn.execute(
                "SELECT * FROM Producto WHERE nombre LIKE ?",
                ('%' + nombre + '%',)
            ).fetchall()
            
    def obtener_productos_activos(self):
        with self.db.get_connection() as conn:
            return conn.execute(
                "SELECT * FROM Producto WHERE activo = 1"
            ).fetchall()
            