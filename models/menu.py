"""
menu.py
-------
Módulo que contiene la clase Menu para el manejo del menú de productos
de Happy Burger usando SQLite.
"""

from db.database import BaseDatos


class Menu:
    """
    Clase Menu
    ----------
    Administra los productos del menú utilizando la tabla Menu en SQLite.
    """

    def __init__(self, db_name="happy_burger.db"):
        """Inicializa la clase Menu con una instancia de BaseDatos."""
        self.db = BaseDatos(db_name)

    def agregar_producto(self, clave, nombre, precio):
        """
        Agregar producto.

        Inserta un nuevo producto en la tabla Menu.
        """
        with self.db.get_connection() as conn:
            conn.execute(
                "INSERT INTO Menu (clave, nombre, precio) VALUES (?, ?, ?)",
                (clave, nombre, precio),
            )
            conn.commit()

    def eliminar_producto(self, clave):
        """
        Eliminar producto.

        Elimina un producto por su clave.
        """
        with self.db.get_connection() as conn:
            conn.execute("DELETE FROM Menu WHERE clave = ?", (clave,))
            conn.commit()

    def actualizar_producto(self, clave, nombre=None, precio=None):
        """
        Actualizar producto.

        Actualiza nombre y/o precio del producto con la clave dada.
        """
        with self.db.get_connection() as conn:
            prod = conn.execute(
                "SELECT id, nombre, precio FROM Menu WHERE clave = ?", (clave,)
            ).fetchone()

            if not prod:
                return

            _, nombre_actual, precio_actual = prod

            nuevo_nombre = nombre if nombre is not None else nombre_actual
            nuevo_precio = precio if precio is not None else precio_actual

            conn.execute(
                """
                UPDATE Menu
                SET nombre = ?, precio = ?
                WHERE clave = ?
                """,
                (nuevo_nombre, nuevo_precio, clave),
            )
            conn.commit()

    def obtener_todos(self):
        """
        Obtiene todos los productos del menú.
        """
        with self.db.get_connection() as conn:
            return conn.execute("SELECT clave, nombre, precio FROM Menu").fetchall()
def obtener_por_clave(self, clave):
    """
    Obtiene un solo producto del menú por su clave.
    """
    with self.db.get_connection() as conn:
        return conn.execute(
            "SELECT clave, nombre, precio FROM Menu WHERE clave = ?",
            (clave,)
        ).fetchone()