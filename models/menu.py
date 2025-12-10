# models/menu.py
"""
menu.py
-------
Módulo que contiene la clase Menu para el manejo
de los productos del menú de Happy Burger usando SQLite.
"""

from db.database import BaseDatos


class Menu:
    """
    Clase Menu
    ----------
    Administra los productos usando la tabla Menu en SQLite.
    """

    def __init__(self, db_name="happy_burger.db"):
        """
        Inicializa la clase Menu con una instancia de BaseDatos.
        """
        self.db = BaseDatos(db_name)

    # CREATE
    def agregar_producto(self, nombre, precio):
        """
        Agrega un producto al menú.
        """
        with self.db.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO Menu (nombre, precio)
                VALUES (?, ?)
                """,
                (nombre, precio),
            )
            conn.commit()

    # READ - todos
    def obtener_menu(self):
        """
        Obtener todos los productos del menú.
        Devuelve lista de tuplas (id, nombre, precio).
        """
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT id, nombre, precio
                FROM Menu
                ORDER BY id
                """
            )
            return cursor.fetchall()

    # READ - por id
    def obtener_producto_por_id(self, producto_id):
        """
        Obtener un producto por su id.
        """
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT id, nombre, precio
                FROM Menu
                WHERE id = ?
                """,
                (producto_id,),
            )
            return cursor.fetchone()

    # UPDATE
    def actualizar_producto(self, producto_id, nombre, precio):
        """
        Actualizar un producto del menú.
        """
        with self.db.get_connection() as conn:
            conn.execute(
                """
                UPDATE Menu
                SET nombre = ?, precio = ?
                WHERE id = ?
                """,
                (nombre, precio, producto_id),
            )
            conn.commit()

    # DELETE
    def eliminar_producto(self, producto_id):
        """
        Eliminar un producto del menú.
        """
        with self.db.get_connection() as conn:
            conn.execute(
                """
                DELETE FROM Menu
                WHERE id = ?
                """,
                (producto_id,),
            )
            conn.commit()

